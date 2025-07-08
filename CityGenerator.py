import bpy
import random
import os
#Add your texture here
image_path = r"C:\Users\Vivek\Downloads\building.jpeg"

def delete_all_meshes():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def create_ground(rows, cols, spacing):
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=((rows * spacing) / 2 - spacing / 2,
                  (cols * spacing) / 2 - spacing / 2,
                  0)
    )
    ground = bpy.context.object
    ground.scale = (rows * spacing / 2, cols * spacing / 2, 1)
    ground.name = "Ground"

    # Oyou can add here ground gray colour (optional)
    mat = bpy.data.materials.new(name="GroundMaterial")
    mat.diffuse_color = (0.1, 0.1, 0.1, 1)
    ground.data.materials.append(mat)

def create_building_material_with_texture():
    if not os.path.exists(image_path):
        print("Image not found:", image_path)
        return None

    img = bpy.data.images.load(image_path)
    mat = bpy.data.materials.new(name="BuildingTextureMat")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in nodes:
        nodes.remove(node)
    # Nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    tex_image = nodes.new('ShaderNodeTexImage')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')

    # Texture setup
    tex_image.image = img
    tex_image.projection = 'BOX'
    tex_image.interpolation = 'Linear'

    # controls how large texture appears on buildings
    mapping.inputs['Scale'].default_value = (3.0, 2.0, 3.0)

    # Node links
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
    links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return mat

def generate_city(rows=25, cols=25, spacing=2, min_height=0.5, max_height=10):
    delete_all_meshes()
    create_ground(rows, cols, spacing)

    building_material = create_building_material_with_texture()

    for i in range(rows):
        for j in range(cols):
            x = i * spacing
            y = j * spacing
            height = random.uniform(min_height, max_height)
            width = random.uniform(1.2, 2.0)
            depth = random.uniform(1.2, 2.0)

            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
            cube = bpy.context.object
            cube.scale = (width / 2, depth / 2, height / 2)
            cube.location.z = height / 2
            cube.name = f"Building_{i}_{j}"

            if building_material:
                if cube.data.materials:
                    cube.data.materials[0] = building_material
                else:
                    cube.data.materials.append(building_material)

generate_city()