import bpy


def add_view_items_from_collection(self, context):
    items = []
    collection = bpy.data.collections.get('ACON_col_cameras')

    if collection:
        for item in collection.objects:
            items.append((item.name, item.name, ""))

    return items


def goToCustomCamera(self, context):
    makeSureCameraExists()
    viewCamera = context.scene.camera
    targetCamera = bpy.data.objects[context.scene.ACON_prop.view]
    viewCamera.location[0] = targetCamera.location[0]
    viewCamera.location[1] = targetCamera.location[1]
    viewCamera.location[2] = targetCamera.location[2]
    viewCamera.rotation_mode = targetCamera.rotation_mode
    viewCamera.rotation_euler[0] = targetCamera.rotation_euler[0]
    viewCamera.rotation_euler[1] = targetCamera.rotation_euler[1]
    viewCamera.rotation_euler[2] = targetCamera.rotation_euler[2]
    viewCamera.scale[0] = targetCamera.scale[0]
    viewCamera.scale[1] = targetCamera.scale[1]
    viewCamera.scale[2] = targetCamera.scale[2]
    turnOnCameraView()


def makeSureCameraExists():
    # early out if scene camera exists
    if bpy.context.scene.camera: return

    # get camera to set to context
    camera_object = bpy.data.objects.get("View_Camera")

    # create camera if View_Camera does not exist
    if not camera_object or not camera_object.type == "CAMERA":
        camera_data = bpy.data.cameras.new("View_Camera")
        camera_object = bpy.data.objects.new("View_Camera", camera_data)
        camera_object.location[0] = 7.35889
        camera_object.location[1] = -6.92579
        camera_object.location[2] = 4.9583
        camera_object.rotation_mode = "XYZ"
        camera_object.rotation_euler[0] = 1.109319
        camera_object.rotation_euler[1] = 0
        camera_object.rotation_euler[2] = 0.814928
        bpy.context.scene.collection.objects.link(camera_object)

    # set context camera
    bpy.context.scene.camera = camera_object


# turn on camera view (set viewport to the current selected camera's view)
def turnOnCameraView(center_camera=True):
    makeSureCameraExists()
    # turn on camera view in the selected context(view pane)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                area.spaces[0].lock_camera = True
                if center_camera:
                    override = {}
                    override['area'] = area
                    bpy.ops.view3d.view_center_camera(override)
                break


def turnOffCameraView():
    # turn onff camera view in the selected context(view pane)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'PERSP'
            break


def switchToRendredView():
    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    for area in bpy.context.screen.areas: 
        if area.type == 'VIEW_3D':
            for space in area.spaces: 
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'