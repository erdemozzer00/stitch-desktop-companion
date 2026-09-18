"""Enable the reviewed official MCP add-on for this Blender process only."""

from pathlib import Path
import json
import sys

import addon_utils
import bpy

ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / ".local/phase-02/mcp-trial"
COPY = TRIAL / "stitch-trial.blend"
assert Path(bpy.data.filepath).resolve() == COPY.resolve(), "Open the trial copy only"
assert not bpy.context.preferences.filepaths.use_scripts_auto_execute
assert bpy.app.online_access

sys.path.insert(0, str(ROOT / ".local/runtime/blender-mcp-official/addon"))
# The add-on reads its preferences during register; create that in-memory entry.
# No save_userpref call is made, and BLENDER_USER_RESOURCES is isolated.
addon_utils.enable("blender_mcp_addon", default_set=True, persistent=False)
import blender_mcp_addon

# Do not use the upstream default autostart address or save preferences.
if bpy.app.timers.is_registered(blender_mcp_addon._autostart_timer):
    bpy.app.timers.unregister(blender_mcp_addon._autostart_timer)
prefs = bpy.context.preferences.addons["blender_mcp_addon"].preferences
prefs.use_autostart = False
prefs.host = "127.0.0.1"
prefs.port = 9877
assert bpy.ops.blmcp.server_start() == {"FINISHED"}

TRIAL.joinpath("bootstrap.json").write_text(json.dumps({
    "blender": bpy.app.version_string,
    "file": bpy.data.filepath,
    "address": "127.0.0.1:9877",
    "saved_preferences": False,
    "file_autoexec": bpy.context.preferences.filepaths.use_scripts_auto_execute,
}, indent=2) + "\n", encoding="utf-8")

# Automatically stop this temporary listener if a trial is abandoned.
def stop_trial_listener():
    bpy.ops.blmcp.server_stop()
    return None

bpy.app.timers.register(stop_trial_listener, first_interval=1800)
