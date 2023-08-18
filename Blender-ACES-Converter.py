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

    if os.path.isfile(tmp_path):
        self.report({'WARNING'}, f"File with colorspaces already exists and was overwritten.")

    try:
        f=open(tmp_path,'w')
    except PermissionError:
        self.report({'ERROR'}, f"No permission - Can't save file with colorspaces! (Is blendfile saved in accessible location?)")
        return

    for m in bpy.data.images:
        f.write(m.colorspace_settings.name+"\n")
    f.close()

    self.report({'INFO'}, f"Colorspaces saved to %s" %(tmp_path))
        
def LoadColorSpaces(self, context):
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    tmp_path = os.path.join( directory , "ACES-Converter_tmp.txt")

    try:
        f=open(tmp_path, 'r')
    except FileNotFoundError:
        self.report({'ERROR'}, f"File with colorspaces doesn't exist!")
        return
    
    color = f.read().splitlines()
        
    i = 0
    try:
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
    except TypeError:
        self.report({'ERROR'}, f"Can't find colorspaces - wrong ACES config!")
        f.close()
        return

    f.close()
    os.remove(tmp_path)
    self.report({'INFO'}, f"Colorspaces loaded in ACES")

class ACESCONV_OT_save(Operator):
    """ Save colorspaces """
    bl_idname = "object.save"
    bl_label = "Save"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        SaveColorSpaces(self, context)
        return {'FINISHED'}
    
class ACESCONV_OT_load(Operator):
    """ Load colorspaces in ACES """
    bl_idname = "object.load"
    bl_label = "Load"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        LoadColorSpaces(self, context)
        return {'FINISHED'}


class ACESCONV_PT_siebar(Panel):
    bl_label = "ACES Converter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator(ACESCONV_OT_save.bl_idname, text="Save", icon="IMPORT")
        col.operator(ACESCONV_OT_load.bl_idname, text="Load", icon="EXPORT")
        #TODO: save-load other way

classes = [
    ACESCONV_OT_save,
    ACESCONV_OT_load,
    ACESCONV_PT_siebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()