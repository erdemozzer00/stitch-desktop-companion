"""Bounded stdio MCP probe; saves private responses under .local/ only.

Usage with the isolated MCP Python: script.py label [tool [arguments-json-file]]
Without a tool, initialize and enumerate tools. This is a diagnostic client,
not evidence that the Codex app has loaded this server natively.
"""

import base64
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".local/phase-02/mcp-trial"


def main():
    label = sys.argv[1]
    if not label.replace("-", "").replace("_", "").isalnum():
        raise ValueError("Use a simple output label")
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, BLENDER_MCP_HOST="127.0.0.1", BLENDER_MCP_PORT="9877")
    lines = queue.Queue()
    started = time.perf_counter()
    with OUT.joinpath(label + "-server.log").open("w", encoding="utf-8") as errors:
        proc = subprocess.Popen(
            [sys.executable, "-m", "blmcp", "--transport", "stdio"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors,
            text=True, encoding="utf-8", env=env,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )

        def read_output():
            for line in proc.stdout:
                lines.put(line)
            lines.put(None)

        threading.Thread(target=read_output, daemon=True).start()

        def send(message):
            proc.stdin.write(json.dumps(message) + "\n")
            proc.stdin.flush()

        def request(number, method, params):
            send({"jsonrpc": "2.0", "id": number, "method": method, "params": params})
            deadline = time.monotonic() + 90
            while True:
                line = lines.get(timeout=max(0.01, deadline - time.monotonic()))
                if line is None:
                    raise RuntimeError("MCP server ended; see private server log")
                message = json.loads(line)
                if message.get("id") == number:
                    if "error" in message:
                        raise RuntimeError(message["error"])
                    return message["result"]
                if time.monotonic() >= deadline:
                    raise TimeoutError(method)

        try:
            initialization = request(1, "initialize", {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "stitch-local-probe", "version": "1.0"},
            })
            send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            if len(sys.argv) > 2:
                arguments = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8-sig")) if len(sys.argv) > 3 else {}
                result = request(2, "tools/call", {"name": sys.argv[2], "arguments": arguments})
            else:
                result = request(2, "tools/list", {})
            structured = result.get("structuredContent", {})
            inner = structured.get("result", {})
            operation_failed = (result.get("isError", False)
                                or structured.get("status") == "error"
                                or (isinstance(inner, dict) and inner.get("status") == "error"))
            for index, block in enumerate(result.get("content", [])):
                if block.get("type") == "image":
                    path = OUT / f"{label}-{index}.png"
                    path.write_bytes(base64.b64decode(block.pop("data"), validate=True))
                    block["saved_local_image"] = str(path)
            record = {"initialization": initialization, "elapsed_seconds": round(time.perf_counter() - started, 3), "result": result}
            destination = OUT / (label + ".json")
            destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"record": str(destination), "elapsed_seconds": record["elapsed_seconds"], "operation_failed": operation_failed, "tool_count": len(result.get("tools", []))}))
            if operation_failed:
                raise RuntimeError("MCP tool reported an error; see response file")
        finally:
            proc.stdin.close()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait(timeout=5)


if __name__ == "__main__":
    main()
