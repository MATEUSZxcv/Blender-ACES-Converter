bl_info = {
    "name" : "ACES Converter",
    "description" : "Script changing all images' colorspaces to their ACES counterparts.",
    "author" : "Mateusz Kuc",
    "version" : (1, 0, 0),
    "blender" : (3, 2, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "Tool"
}

import bpy
import os
from bpy.types import Operator
from bpy.types import Panel

def SaveColorSpaces(self, context):

    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    tmp_path = os.path.join( directory , "ACES-Converter_tmp.txt")

    f=open(tmp_path,'w')
        
    for m in bpy.data.images:
        f.write(m.colorspace_settings.name+"\n")
    f.close()
        
def LoadColorSpaces(self, context):
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    tmp_path = os.path.join( directory , "ACES-Converter_tmp.txt")
    
    f=open(tmp_path, 'r')
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
    os.remove(tmp_path)

class Save_operator(Operator):
    """ Save colorspaces """
    bl_idname = "save.operator"
    bl_label = "Save"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        SaveColorSpaces(self, context)
        self.report({'INFO'}, f"Colorspaces saved")
        return {'FINISHED'}
    
class Load_operator(Operator):
    """ Load colorspaces in ACES """
    bl_idname = "load.operator"
    bl_label = "Load"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        LoadColorSpaces(self, context)
        self.report({'INFO'}, f"Colorspaces loaded in ACES")
        return {'FINISHED'}


class sidebar(Panel):
    bl_label = "ACES Converter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        col = self.layout.column(align=True)
        prop = col.operator(Save_operator.bl_idname, text="Save")
        prop2 = col.operator(Load_operator.bl_idname, text="Load")

 
classes = [
    Save_operator,
    Load_operator,
    sidebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()