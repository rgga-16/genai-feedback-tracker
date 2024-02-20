import openai
import bpy 

# Do this to link your python env to blender
#https://stackoverflow.com/questions/70639689/how-to-use-the-anaconda-environment-on-blender
#Also need to install BlenderKit

# Define a property group to hold your custom properties
class MyAddonProperties(bpy.types.PropertyGroup):
    my_string: bpy.props.StringProperty(
        name="My String",
        description="Enter a string",
        default="",
        maxlen=1024,
    )

class OBJECT_OT_MyButtonAction(bpy.types.Operator):
    bl_idname = "object.my_button_action"
    bl_label = "Do something"
    
    def execute(self,context):
        my_props = context.scene.my_addon_props
        if hasattr(bpy.data.window_managers["WinMan"], "blenderkit_models"):
            bpy.data.window_managers["WinMan"].blenderkit_models.search_keywords = my_props.my_string
            bpy.data.window_managers["WinMan"].blenderkit_search()
        else:
            self.report({'WARNING'}, "BlenderKit is not available or not enabled.")

        print("The string is: ", my_props.my_string)
        return {'FINISHED'}
        

class MyAddonPanel(bpy.types.Panel):
    bl_label = "My Addon Panel"
    bl_idname = "OBJECT_PT_myaddon_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type='UI'
    bl_category = "My Category"
    
    def draw(self,context):
        layout = self.layout
        obj = context.active_object
        
        #Access the custom properties from the scene
        my_props = context.scene.my_addon_props
        
        row = layout.row()
        row.label(text="Hello, world!")
        
        row = layout.row()
        row.prop(my_props, "my_string", text="")
        
        row = layout.row()
        row.operator("object.my_button_action", text = "Press Me")
        
        row = layout.row()
        if obj:
            row.label(text="Active object: " + obj.name)
        else:
            row.label(text="No active object")

class OBJECT_OT_update_panel(bpy.types.Operator):
    """Operator to force update the panel"""
    bl_idname = "object.update_panel"
    bl_label = "Update Panel"
    
    def modal(self,context,event):
        if event.type == 'MOUSECLICK':
            context.area.tag_redraw()
        else:
            print('not working')
        return {'PASS_THROUGH'}
    
    def invoke(self,context,event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
def register():
    bpy.utils.register_class(MyAddonProperties)
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=MyAddonProperties)
    bpy.utils.register_class(OBJECT_OT_MyButtonAction)
    bpy.utils.register_class(MyAddonPanel)
    bpy.utils.register_class(OBJECT_OT_update_panel)

def unregister():
    bpy.utils.unregister_class(MyAddonPanel)
    del bpy.types.Scene.my_addon_props
    bpy.utils.unregister_class(MyAddonProperties)
    bpy.utils.unregister_class(OBJECT_OT_MyButtonAction)
    bpy.utils.unregister_class(OBJECT_OT_update_panel)
    
if __name__ == "__main__":
    register()



    
    