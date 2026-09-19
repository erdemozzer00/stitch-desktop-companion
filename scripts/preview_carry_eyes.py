"""Compare accepted carry response with its requested geometric eye closure."""
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw
from preview_directional_drag import ROOT, FONT, SMALL, trace, projected, cursor, clamp

SOURCE = ROOT / '.local/phase-04/directional-v1'
OUT = ROOT / '.local/phase-04/directional-eyes-v1'


def main():
    bank = json.loads((SOURCE/'bank-manifest.json').read_text())
    eyes = json.loads((OUT/'eyes-manifest.json').read_text())
    records = trace()
    assert records == json.loads((SOURCE/'pointer-trace.json').read_text())
    images = {}
    for label, folder, manifest in [('open', SOURCE, bank), ('closed', OUT, eyes)]:
        for name, record in manifest['frames'].items():
            path = folder/name
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
            with Image.open(path) as image:
                image = image.convert('RGBA')
            assert image.size == (240, 240)
            bounds = image.getchannel('A').getbbox()
            assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<240 and bounds[3]<240
            images[label, name] = image
    transitions = []
    for record in records:
        t = record['t']
        amount = clamp(t/.25, 0, 1) if t<6.9 else 1-clamp((t-6.9)/.33, 0, 1)
        amount = amount*amount*(3-2*amount)
        level = round(amount*6)
        if level == 6:
            name = record['file']
        elif level == 0:
            name = record['file']
        else:
            # This replay blinks at neutral. Do not claim arbitrary moving entries.
            assert record['file'] == 'bank_4_2.png', (t, record['file'])
            name = f'blink_{level}.png'
        transitions.append({'t': t, 'level': level, 'file': name})
    for theme, bg, ink in [('light','#eef0f2','#233140'), ('dark','#19202b','#eef0f4')]:
        boards = []
        for record, eye in zip(records, transitions):
            board = Image.new('RGB', (1040,510), bg)
            draw = ImageDraw.Draw(board)
            for column, label in [(0,'ONAYLANAN TAŞIMA'), (1,'TAŞIRKEN GÖZLER KAPALI')]:
                draw.text((column*520+15,10),label,fill=ink,font=FONT)
                name = record['file']
                image = images['open',name] if column==0 or eye['level']==0 else images['closed',eye['file']]
                anchor = bank['frames'][name]['anchor']
                layer = projected(image, anchor, record['pointer'], record['angle'])
                bounds = layer.getchannel('A').getbbox()
                assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<520 and bounds[3]<450
                board.paste(layer,(column*520,35),layer)
                cursor(draw,(column*520+record['pointer'][0],35+record['pointer'][1]),record['held'])
            draw.line((520,0,520,475),fill='#647180')
            draw.text((16,466),record['phase'],fill=ink,font=FONT)
            draw.text((16,490),'Aynı taşıma tepkisi • tutarken kapanır, bıraktıktan sonra açılır • özel önizleme',fill=ink,font=SMALL)
            boards.append(board)
        durations=[(round((i+1)*100/24)-round(i*100/24))*10 for i in range(len(boards))]
        durations[-1]=900
        boards[0].save(OUT/f'carry-eyes-{theme}.gif',save_all=True,append_images=boards[1:],duration=durations,loop=0,optimize=False)
        sheet=Image.new('RGB',(1040,510*3),bg)
        for row, index in enumerate((3,45,169)):
            sheet.paste(boards[index],(0,row*510))
        sheet.save(OUT/f'eye-motion-sheet-{theme}.png')
    # Compact per-eye transition contact sheet at native review size.
    sheet=Image.new('RGB',(240*7,270),'#eef0f2')
    draw=ImageDraw.Draw(sheet)
    for i in range(7):
        image=images['closed',f'blink_{i}.png']
        sheet.paste(image,(240*i,25),image)
        draw.text((240*i+10,4),f'{i}/6',font=SMALL,fill='#233140')
    sheet.save(OUT/'eye-transition.png')
    report={'status':'PRIVATE_PREVIEW_CHECKS_PASS_NOT_NATIVE_ACCEPTANCE',
            'accepted_pointer_trace_exactly_preserved':True,
            'accepted_directional_action_preserved':eyes['preservation'],
            'closed_bank_frames':45, 'neutral_transition_frames':7,
            'actual_new_render_files':len(eyes['frames']), 'size':240,'samples':6,
            'closure_seconds':.25,'reopen_start_after_release_seconds':.25,'reopen_seconds':.33,
            'preview_raw_pixels_mib':52*240*240*4/2**20,
            'projected_replacement_bank_400_mib':52*400*400*4/2**20,
            'asset_strategy':'Closed bank replaces planned open carry bank; no 45x7 eye-state product. Arbitrary moving blink entry is not solved by neutral transition frames.',
            'limits':'Native capture/release, wave entry, arbitrary grips and process memory remain unproven. No installed-app update.'}
    (OUT/'eye-timeline.json').write_text(json.dumps(transitions,indent=2),encoding='utf-8')
    (ROOT/'context/evidence/phase-04-carry-eyes-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='eye_timeline'},indent=2))


if __name__ == '__main__':
    main()
