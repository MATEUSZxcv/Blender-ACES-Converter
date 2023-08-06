bl_info = {
    "name" : "ACES conversion",
    "description" : "Addon converts to ACES",
    "author" : "Mateusz Kuc",
    "version" : (1, 0, 0),
    "blender" : (3, 2, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy
import os
from bpy.types import Operator
from bpy.types import Panel

class TLA_OT_operator(Operator):
    """ click """
    bl_idname = "demo.operator"
    bl_label = "I'm a Skeleton Operator"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):

        self.report({'INFO'},
            f"execute()")

        #getting blendfile directory
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        print(directory)

        tmp_path = os.path.join( directory , "tmp.txt")

        #creating file
        f=open(tmp_path,'a')
        f.close()
        #openig file
        f=open(tmp_path,'r+')

        try:
            mode = int(f.readline())
        except:
            mode = 0
            
        if mode == 0:
            f.write("1\n")
            for m in bpy.data.images:
                f.write(m.colorspace_settings.name+"\n")
            f.close()
            
        else:
            color = f.read().splitlines()
                
            i = 0
            for m in bpy.data.images:
                if i == len(color):
                    break
                if color[i] == "sRGB":
                    m.colorspace_settings.name = 'role_matte_paint'
                elif color[i] == "Non-Color":
                    m.colorspace_settings.name = 'role_data'
                elif color[i] == "Linear":
                    m.colorspace_settings.name = 'Utility - Linear - sRGB'
                i = i+1
                
            f.close()
            #deleting file
            f=open(tmp_path,'w')
            f.close()
            os.remove(tmp_path)

        return {'FINISHED'}

class TLA_PT_sidebar(Panel):
    """Display test button"""
    bl_label = "Aces Conversion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        col = self.layout.column(align=True)
        prop = col.operator(TLA_OT_operator.bl_idname, text="Convert")

 
classes = [
    TLA_OT_operator,
    TLA_PT_sidebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()