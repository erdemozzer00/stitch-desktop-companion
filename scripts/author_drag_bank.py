"""Bounded 9x5 articulated response bank for the carried-toy preview, not runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from author_companion_motion import Character
from author_carry_preview import pose, apply
from prepare_stage import preservation_digests
from verify_companion_motion import action_data


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['poses','bank'], default='poses')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=ROOT/'.local/phase-04/directional-v1'
    out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'.local/phase-03/appearance-final/idle/idle.blend'
    source_hash=sha(source)
    bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
    scene=bpy.context.scene
    rig,mesh=bpy.data.objects['Stitch_Armature'],bpy.data.objects['Stitch_Mesh']
    scene.frame_set(1)
    baseline=preservation_digests(mesh,rig)
    original=action_data(bpy.data.actions['Stitch_Anim'])
    camera=[list(row) for row in scene.camera.matrix_world]
    character=Character()
    neutral=pose(rig)
    height=mesh.dimensions.z
    scene.render.resolution_x=scene.render.resolution_y=240
    scene.render.resolution_percentage=100
    scene.render.image_settings.color_mode='RGBA'
    scene.render.film_transparent=True
    scene.render.use_persistent_data=True
    scene.cycles.samples=6

    # A front torso vertex from the evaluated, subdivided mesh. No arbitrary-grip claim.
    anchor_index=28938
    def anchor():
        bpy.context.view_layer.update()
        obj=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
        data=obj.to_mesh()
        try:
            point=mesh.matrix_world@data.vertices[anchor_index].co
            p=world_to_camera_view(scene,scene.camera,point)
            return [p.x*240,(1-p.y)*240]
        finally:
            obj.to_mesh_clear()

    neutral_anchor=anchor()
    report={'size':240,'samples':6,'source_sha256':source_hash,'anchor_vertex':anchor_index,
            'neutral_anchor':neutral_anchor,'x_values':[i/4 for i in range(-4,5)],
            'y_values':[i/2 for i in range(-2,3)],'frames':{},
            'limits':'Finite draft bank with no live skeleton. X is relative ear/body follow-through, Y is vertical articulation. Runtime integration unproven.'}
    action=bpy.data.actions.new('CarriedToy_Bank_v1')
    rig.animation_data.action=action
    for yi,y in enumerate(report['y_values']):
        for xi,x in enumerate(report['x_values']):
            frame=yi*9+xi+1
            scene.frame_set(frame)
            apply(rig,neutral)
            # Full-body screen-space swing is separate; these changes prevent a rigid-sticker effect.
            character.rotate('Head',(0,1,0),x*1.8)
            character.rotate('Head',(1,0,0),y*1.4)
            for side,sign in [('L',1),('R',-1)]:
                character.rotate('Ear_A.'+side,(0,1,0),x*7-sign*y*2)
                character.rotate('Ear_B.'+side,(0,1,0),x*9-sign*y*3)
                character.rotate('Arm.'+side,(0,1,0),x*2+sign*y*1.2)
                character.rotate('ForeArm.'+side,(1,0,0),y*3)
                control=rig.pose.bones['CTRL_leg.'+side]
                delta=Vector((x*.007*height, y*.003*height, -y*.009*height))
                control.location += control.bone.matrix_local.to_quaternion().inverted()@delta
            for bone in rig.pose.bones:
                for prop in ('location','rotation_quaternion','scale'):
                    bone.keyframe_insert(data_path=prop,frame=frame,group=bone.name)
            name=f'bank_{xi}_{yi}.png'
            report['frames'][name]={'x':x,'y':y,'frame':frame,'anchor':anchor()}
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for key in curve.keyframe_points:
                        key.interpolation='LINEAR'
    scene.frame_start,scene.frame_end=1,45
    scene.frame_set(23)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'drag-bank.blend'),compress=True)
    for name,record in report['frames'].items():
        xi,yi=map(int,name.removesuffix('.png').split('_')[1:])
        if args.mode=='poses' and not (xi in (0,4,8) and yi in (0,2,4)):
            continue
        scene.frame_set(record['frame'])
        scene.render.filepath=str(out/name)
        bpy.ops.render.render(write_still=True)
        record['sha256']=sha(out/name)
    assert preservation_digests(mesh,rig)==baseline
    assert action_data(bpy.data.actions['Stitch_Anim'])==original
    assert [list(row) for row in scene.camera.matrix_world]==camera
    assert sha(source)==source_hash
    report['preservation']='PASS: accepted source file, original action, mesh/rig fields and camera'
    (out/(args.mode+'-manifest.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('DRAG_BANK_DONE',args.mode,flush=True)


if __name__=='__main__':
    main()
