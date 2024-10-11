# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
bl_info = {
    "name": "Weave Mapper",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy
from bpy.props import StringProperty, FloatProperty, PointerProperty, EnumProperty

class WeaveMapperProperties(bpy.types.PropertyGroup):
    controller_object: StringProperty(name="Controller Object")
    paste_data_path: StringProperty(name="Paste Data Path")
    min_slider: FloatProperty(name="Min")
    max_slider: FloatProperty(name="Max")
    min_trans: FloatProperty(name="Min")
    max_trans: FloatProperty(name="Max")
    range_mode: EnumProperty(
        name="Range Mode",
        items=[
            ("LINEAR", "Linear", "Linear interpolation"),
            ("CLAMP", "Clamp", "Clamp values to range"),
            ("WRAP", "Wrap", "Wrap values within range"),
            ("PINGPONG", "PingPong", "Pingpong effect"),
        ]
    )
    custom_property_path: StringProperty(name="Custom Property Path")
    easing_type: EnumProperty(
        name="Easing Type",
        items=[
            ("LINEAR", "Linear", "Linear interpolation"),
            ("EASE", "Ease", "Ease interpolation"),
            ("EASEIN", "Ease In", "Ease-in interpolation"),
            ("EASEOUT", "Ease Out", "Ease-out interpolation"),
            ("EASEINOUT", "Ease In Out", "Ease-in-out interpolation"),
            ("SINEIN", "Sine In", "Sine in interpolation"),
            ("SINEOUT", "Sine Out", "Sine out interpolation"),
            ("SINEINOUT", "Sine In Out", "Sine in-out interpolation"),
            ("CUBICIN", "Cubic In", "Cubic in interpolation"),
            ("CUBICOUT", "Cubic Out", "Cubic out interpolation"),
            ("CUBICINOUT", "Cubic In Out", "Cubic in-out interpolation"),
            ("QUINTIN", "Quint In", "Quint in interpolation"),
            ("QUINTOUT", "Quint Out", "Quint out interpolation"),
            ("QUINTINOUT", "Quint In Out", "Quint in-out interpolation"),
            ("CIRCIN", "Circ In", "Circ in interpolation"),
            ("CIRCOUT", "Circ Out", "Circ out interpolation"),
            ("CIRCINOUT", "Circ In Out", "Circ in-out interpolation"),
            ("ELASTICIN", "Elastic In", "Elastic in interpolation"),
            ("ELASTICOUT", "Elastic Out", "Elastic out interpolation"),
            ("ELASTICINOUT", "Elastic In Out", "Elastic in-out interpolation"),
            ("QUADIN", "Quad In", "Quad in interpolation"),
            ("QUADOUT", "Quad Out", "Quad out interpolation"),
            ("QUADINOUT", "Quad In Out", "Quad in-out interpolation"),
            ("QUARTIN", "Quart In", "Quart in interpolation"),
            ("QUARTOUT", "Quart Out", "Quart out interpolation"),
            ("QUARTINOUT", "Quart In Out", "Quart in-out interpolation"),
            ("EXPOIN", "Expo In", "Expo in interpolation"),
            ("EXPOOUT", "Expo Out", "Expo out interpolation"),
            ("EXPOINOUT", "Expo In Out", "Expo in-out interpolation"),
            ("BACKIN", "Back In", "Back in interpolation"),
            ("BACKOUT", "Back Out", "Back out interpolation"),
            ("BACKINOUT", "Back In Out", "Back in-out interpolation"),
            ("BOUNCEIN", "Bounce In", "Bounce in interpolation"),
            ("BOUNCEOUT", "Bounce Out", "Bounce out interpolation"),
            ("BOUNCEINOUT", "Bounce In Out", "Bounce in-out interpolation"),
        ]
    )

class OBJECT_PT_WeaveMapper(bpy.types.Panel):
    bl_label = "Weave Mapper"
    bl_idname = "OBJECT_PT_weavemapper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Weave Mapper"

    def draw(self, context):
        layout = self.layout
        wm_props = context.scene.weave_mapper_props

        layout.label(text="Controller")
        layout.prop_search(wm_props, "controller_object", context.scene, "objects")
        layout.prop(wm_props, "paste_data_path")

        layout.label(text="Range")
        layout.prop(wm_props, "min_slider")
        layout.prop(wm_props, "max_slider")

        layout.label(text="Transitional Data")
        layout.prop(wm_props, "min_trans")
        layout.prop(wm_props, "max_trans")

        layout.label(text="Mode")
        layout.prop(wm_props, "range_mode")

        layout.label(text="Easing Type")
        layout.prop(wm_props, "easing_type")

        # Add to Location
        layout.label(text="Add to Location")
        row = layout.row(align=True)
        row.operator("object.add_driver", text="X").axis = 'location_x'
        row.operator("object.add_driver", text="Y").axis = 'location_y'
        row.operator("object.add_driver", text="Z").axis = 'location_z'
        row.operator("object.add_driver", text="All").axis = 'location_all'

        # Add to Rotation
        layout.label(text="Add to Rotation")
        row = layout.row(align=True)
        row.operator("object.add_driver", text="X").axis = 'rotation_x'
        row.operator("object.add_driver", text="Y").axis = 'rotation_y'
        row.operator("object.add_driver", text="Z").axis = 'rotation_z'
        row.operator("object.add_driver", text="All").axis = 'rotation_all'

        # Add to Scale
        layout.label(text="Add to Scale")
        row = layout.row(align=True)
        row.operator("object.add_driver", text="X").axis = 'scale_x'
        row.operator("object.add_driver", text="Y").axis = 'scale_y'
        row.operator("object.add_driver", text="Z").axis = 'scale_z'
        row.operator("object.add_driver", text="All").axis = 'scale_all'

def get_easing_expression(easing_type, min_slider, max_slider, min_trans, max_trans):
    if easing_type == "LINEAR":
        return f"(var - {min_slider}) / ({max_slider} - {min_slider}) * ({max_trans} - {min_trans}) + {min_trans}"
    elif easing_type == "EASEIN":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider}))**3 + {min_trans}"
    elif easing_type == "EASEOUT":
        return f"({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**3)) + {min_trans}"
    elif easing_type == "EASEINOUT":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**3 + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))/2)**3) + {min_trans}"
    elif easing_type == "SINEIN":
        return f"({max_trans} - {min_trans}) * (1 - cos((var - {min_slider}) / ({max_slider} - {min_slider}) * pi / 2)) + {min_trans}"
    elif easing_type == "SINEOUT":
        return f"({max_trans} - {min_trans}) * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * pi / 2) + {min_trans}"
    elif easing_type == "SINEINOUT":
        return f"({max_trans} - {min_trans}) * (1 - cos((var - {min_slider}) / ({max_slider} - {min_slider}) * pi)) / 2 + {min_trans}"
    elif easing_type == "CUBICIN":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider}))**3 + {min_trans}"
    elif easing_type == "CUBICOUT":
        return f"({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**3)) + {min_trans}"
    elif easing_type == "CUBICINOUT":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**3 + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))/2)**3) + {min_trans}"
    elif easing_type == "QUINTIN":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider}))**5 + {min_trans}"
    elif easing_type == "QUINTOUT":
        return f"({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**5)) + {min_trans}"
    elif easing_type == "QUINTINOUT":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**5 + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))/2)**5) + {min_trans}"
    elif easing_type == "CIRCIN":
        return f"({max_trans} - {min_trans}) * (1 - sqrt(1 - ((var - {min_slider}) / ({max_slider} - {min_slider}))**2)) + {min_trans}"
    elif easing_type == "CIRCOUT":
        return f"({max_trans} - {min_trans}) * sqrt(1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**2)) + {min_trans}"
    elif easing_type == "CIRCINOUT":
        return f"({max_trans} - {min_trans}) * (1 - sqrt(1 - ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**2)) + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * sqrt(1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))/2)**2) + {min_trans}"
    elif easing_type == "ELASTICIN":
        return f"({max_trans} - {min_trans}) * (2 ** (10 * ((var - {min_slider}) / ({max_slider} - {min_slider}) - 1))) * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * (pi * 10 / 3)) + {min_trans}"
    elif easing_type == "ELASTICOUT":
        return f"({max_trans} - {min_trans}) * (2 ** (-10 * (var - {min_slider}) / ({max_slider} - {min_slider}))) * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * (pi * 10 / 3)) + {min_trans}"
    elif easing_type == "ELASTICINOUT":
        return f"({max_trans} - {min_trans}) * (2 ** (10 * ((var - {min_slider}) / ({max_slider} - {min_slider})/2 - 1))) * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * (pi * 10 / 6)) + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (2 ** (-10 * (var - {min_slider}) / ({max_slider} - {min_slider})/2)) * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * (pi * 10 / 6)) + {min_trans}"
    elif easing_type == "QUADIN":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider}))**2 + {min_trans}"
    elif easing_type == "QUADOUT":
        return f"({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**2)) + {min_trans}"
    elif easing_type == "QUADINOUT":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**2 + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))/2)**2) + {min_trans}"
    elif easing_type == "QUARTIN":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider}))**4 + {min_trans}"
    elif easing_type == "QUARTOUT":
        return f"({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**4)) + {min_trans}"
    elif easing_type == "QUARTINOUT":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**4 + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))/2)**4) + {min_trans}"
    elif easing_type == "EXPOIN":
        return f"({max_trans} - {min_trans}) * (2 ** (10 * ((var - {min_slider}) / ({max_slider} - {min_slider}) - 1))) + {min_trans}"
    elif easing_type == "EXPOOUT":
        return f"({max_trans} - {min_trans}) * (1 - 2 ** (-10 * (var - {min_slider}) / ({max_slider} - {min_slider}))) + {min_trans}"
    elif easing_type == "EXPOINOUT":
        return f"({max_trans} - {min_trans}) * (2 ** (10 * ((var - {min_slider}) / ({max_slider} - {min_slider})/2 - 1))) + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - 2 ** (-10 * (var - {min_slider}) / ({max_slider} - {min_slider})/2)) + {min_trans}"
    elif easing_type == "BACKIN":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider}))**3 - ((var - {min_slider}) / ({max_slider} - {min_slider}) * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * pi)) + {min_trans}"
    elif easing_type == "BACKOUT":
        return f"({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider}))**3) + sin((var - {min_slider}) / ({max_slider} - {min_slider}) * pi)) + {min_trans}"
    elif easing_type == "BACKINOUT":
        return f"({max_trans} - {min_trans}) * ((var - {min_slider}) / ({max_slider} - {min_slider})/2)**3 - ((var - {min_slider}) / ({max_slider} - {min_slider})/2 * sin((var - {min_slider}) / ({max_slider} - {min_slider}) * pi/2)) + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (1 - ((1 - (var - {min_slider}) / ({max_slider} - {min_slider})/2)**3) + sin((var - {min_slider}) / ({max_slider} - {min_slider}) * pi/2)) + {min_trans}"
    elif easing_type == "BOUNCEIN":
        return f"({max_trans} - {min_trans}) * (1 - abs(sin(6 * (1 - (var - {min_slider}) / ({max_slider} - {min_slider})) * pi) * (1 - (1 - (var - {min_slider}) / ({max_slider} - {min_slider})))) + {min_trans}"
    elif easing_type == "BOUNCEOUT":
        return f"({max_trans} - {min_trans}) * (abs(sin(6 * (var - {min_slider}) / ({max_slider} - {min_slider}) * pi) * (1 - (var - {min_slider}) / ({max_slider} - {min_slider}))) + {min_trans}"
    elif easing_type == "BOUNCEINOUT":
        return f"({max_trans} - {min_trans}) * (1 - abs(sin(6 * (1 - (var - {min_slider}) / ({max_slider} - {min_slider})/2) * pi) * (1 - (1 - (var - {min_slider}) / ({max_slider} - {min_slider})/2))) + {min_trans} if (var - {min_slider}) / ({max_slider} - {min_slider}) < 0.5 else ({max_trans} - {min_trans}) * (abs(sin(6 * (var - {min_slider}) / ({max_slider} - {min_slider})/2 * pi) * (1 - (var - {min_slider}) / ({max_slider} - {min_slider})/2))) + {min_trans}"
    else:
        return f"(var - {min_slider}) / ({max_slider} - {min_slider}) * ({max_trans} - {min_trans}) + {min_trans}"


def add_driver(self, context, axis):
    wm_props = context.scene.weave_mapper_props
    obj = context.object

    if obj.animation_data is None:
        obj.animation_data_create()

    def add_single_driver(property_name, index):
        # Check if driver already exists
        fcurve = obj.animation_data.drivers.find(f"{property_name}.{index}")
        if fcurve:
            driver = fcurve.driver
        else:
            try:
                driver = obj.driver_add(property_name, index).driver
            except (TypeError, ValueError, AttributeError) as e:
                self.report({'ERROR'}, f"Failed to add driver: {e}")
                return {'CANCELLED'}

        var = driver.variables.new()
        var.name = "var"
        var.type = 'SINGLE_PROP'
        target = var.targets[0]
        target.id_type = 'OBJECT'
        target.id = bpy.data.objects[wm_props.controller_object]
        target.data_path = wm_props.paste_data_path

                # Update expression based on range mode
        if wm_props.range_mode == "LINEAR":
            driver.expression = get_easing_expression(wm_props.easing_type, wm_props.min_slider, wm_props.max_slider, wm_props.min_trans, wm_props.max_trans)
        elif wm_props.range_mode == "CLAMP":
            driver.expression = f"max(min((var - {wm_props.min_slider}) / ({wm_props.max_slider} - {wm_props.min_slider}) * ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans}, {wm_props.max_trans}), {wm_props.min_trans})"
        elif wm_props.range_mode == "WRAP":
            driver.expression = f"radians(({wm_props.min_trans} + (var - {wm_props.min_slider}) / ({wm_props.max_slider} - {wm_props.min_slider}) * ({wm_props.max_trans} - {wm_props.min_trans})) % ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans})"
        elif wm_props.range_mode == "PINGPONG":
            driver.expression = f"(var <= ({wm_props.max_slider} / 2)) * ((var - {wm_props.min_slider}) / ({wm_props.max_slider}/2 - {wm_props.min_slider}) * ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans}) + (var > ({wm_props.max_slider} / 2)) * (({wm_props.max_slider} - var) / ({wm_props.max_slider} - {wm_props.max_slider}/2) * ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans})"

    if axis == 'location_all':
        for i in range(3):
            add_single_driver("location", i)
    elif axis == 'rotation_all':
        for i in range(3):
            add_single_driver("rotation_euler", i)
    elif axis == 'scale_all':
        for i in range(3):
            add_single_driver("scale", i)
    else:
        if axis.startswith('location'):
            index = {'location_x': 0, 'location_y': 1, 'location_z': 2}[axis]
            add_single_driver("location", index)
        elif axis.startswith('rotation'):
            index = {'rotation_x': 0, 'rotation_y': 1, 'rotation_z': 2}[axis]
            add_single_driver("rotation_euler", index)
        elif axis.startswith('scale'):
            index = {'scale_x': 0, 'scale_y': 1, 'scale_z': 2}[axis]
            add_single_driver("scale", index)

    return {'FINISHED'}

def add_custom_driver(self, context):
    wm_props = context.scene.weave_mapper_props
    obj = context.object

    if obj.animation_data is None:
        obj.animation_data_create()

    # Check if driver already exists
    fcurve = obj.animation_data.drivers.find(wm_props.custom_property_path)
    if fcurve:
        driver = fcurve.driver
    else:
        try:
            driver = obj.driver_add(wm_props.custom_property_path).driver
        except (TypeError, ValueError, AttributeError) as e:
            self.report({'ERROR'}, f"Failed to add driver: {e}")
            return {'CANCELLED'}

    var = driver.variables.new()
    var.name = "var"
    var.type = 'SINGLE_PROP'
    target = var.targets[0]
    target.id_type = 'OBJECT'
    target.id = bpy.data.objects[wm_props.controller_object]
    target.data_path = wm_props.paste_data_path

    # Update expression based on range mode
    if wm_props.range_mode == "LINEAR":
        driver.expression = get_easing_expression(wm_props.easing_type, wm_props.min_slider, wm_props.max_slider, wm_props.min_trans, wm_props.max_trans)
    elif wm_props.range_mode == "CLAMP":
        driver.expression = f"max(min((var - {wm_props.min_slider}) / ({wm_props.max_slider} - {wm_props.min_slider}) * ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans}, {wm_props.max_trans}), {wm_props.min_trans})"
    elif wm_props.range_mode == "WRAP":
        driver.expression = f"radians(({wm_props.min_trans} + (var - {wm_props.min_slider}) / ({wm_props.max_slider} - {wm_props.min_slider}) * ({wm_props.max_trans} - {wm_props.min_trans})) % ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans})"
    elif wm_props.range_mode == "PINGPONG":
        driver.expression = f"(var <= ({wm_props.max_slider} / 2)) * ((var - {wm_props.min_slider}) / ({wm_props.max_slider}/2 - {wm_props.min_slider}) * ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans}) + (var > ({wm_props.max_slider} / 2)) * (({wm_props.max_slider} - var) / ({wm_props.max_slider} - {wm_props.max_slider}/2) * ({wm_props.max_trans} - {wm_props.min_trans}) + {wm_props.min_trans})"

    return {'FINISHED'}

class OBJECT_OT_AddDriver(bpy.types.Operator):
    bl_idname = "object.add_driver"
    bl_label = "Add Driver"
    bl_options = {'REGISTER', 'UNDO'}
    axis: StringProperty()

    def execute(self, context):
        return add_driver(self, context, self.axis)

class OBJECT_OT_AddCustomDriver(bpy.types.Operator):
    bl_idname = "object.add_custom_driver"
    bl_label = "Add Custom Driver"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return add_custom_driver(self, context)

def register():
    bpy.utils.register_class(WeaveMapperProperties)
    bpy.types.Scene.weave_mapper_props = PointerProperty(type=WeaveMapperProperties)
    bpy.utils.register_class(OBJECT_PT_WeaveMapper)
    bpy.utils.register_class(OBJECT_OT_AddDriver)
    bpy.utils.register_class(OBJECT_OT_AddCustomDriver)

def unregister():
    bpy.utils.unregister_class(WeaveMapperProperties)
    del bpy.types.Scene.weave_mapper_props
    bpy.utils.unregister_class(OBJECT_PT_WeaveMapper)
    bpy.utils.unregister_class(OBJECT_OT_AddDriver)
    bpy.utils.unregister_class(OBJECT_OT_AddCustomDriver)

if __name__ == "__main__":
    register()
