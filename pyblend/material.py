import bpy
import numpy as np
from numpy.random import rand


def reset_mat(mat):
    """Reset material to default"""
    mats = bpy.data.materials
    name = mat.name
    mats.remove(mat)
    mat = mats.new(name)
    mat.use_nodes = True
    return mat


def create_mat(name: str, nodes: bpy.types.NodeGroup = None) -> bpy.types.Material:
    """
    Create material with name and nodes
    """
    mats = bpy.data.materials
    mat = mats.new(name)
    mat.use_nodes = True
    if nodes is not None:
        mat.node_tree.nodes.clear()
        mat.node_tree.nodes.new("ShaderNodeGroup").node_tree = nodes
    return mat


def create_texture_node(nodes: bpy.types.NodeGroup, path: str = None, img: bpy.types.Image = None) -> bpy.types.Node:
    """
    Create a texture node and load image from path or img
    """
    tex_node = nodes.new("ShaderNodeTexImage")
    if img is not None:
        tex_node.image = img
    elif path is not None:
        tex_node.image = bpy.data.images.load(filepath=path)
    return tex_node


def load_mat_library(lib_root):
    """
    Load material library from .blend file
    """
    assert lib_root.endswith(".blend"), "Only support .blend file"
    with bpy.data.libraries.load(lib_root, link=True) as (data_from, data_to):
        data_to.materials = data_from.materials


def set_voronoi_texture(mat_or_obj):
    if isinstance(mat_or_obj, bpy.types.Material):
        mat = mat_or_obj
    elif isinstance(mat_or_obj, bpy.types.Object):
        mat = mat_or_obj.active_material
    elif mat_or_obj is None:
        mat = None
    else:
        raise TypeError(f"mat_or_obj must be Material or Object, got {type(mat_or_obj)}")
    if mat is None:
        mat = bpy.data.materials.new(name="Material")
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    tex_node = nodes.new("ShaderNodeTexVoronoi")

    links = mat.node_tree.links
    links.new(tex_node.outputs[1], nodes["Principled BSDF"].inputs[0])
    return mat


def random_transparent_mat(nodes, color=None):
    prin_node = nodes["Principled BSDF"]

    # The mapping was taken by running:
    # for i, e in enumerate(prin_node.inputs):
    #     print(f"{i}: {type(e)}: {e}")
    key2idx = {
        "Base Color": 0,
        "Metallic": 1,
        "Roughness": 2,
        "IOR": 3,
        "Alpha": 4 ,
        "Normal": 5,
        "Weight": 6,
        "Subsurface Weight": 7,
        "Subsurface Radius": 8,
        "Subsurface Scale": 9,
        "Subsurface IOR": 10,
        "Subsurface Anisotropy": 11,
        "Specular IOR Level": 12,
        "Specular Tint": 13,
        "Anisotropic": 14,
        "Anisotropic Rotation": 15,
        "Tangent": 16,
        "Transmission Weight": 17,
        "Coat Weight": 18,
        "Coat Roughness": 19,
        "Coat IOR": 20,
        "Coat Tint": 21,
        "Coat Normal": 22,
        "Sheen Weight": 23,
        "Sheen Roughness": 24,
        "Sheen Tint": 25,
        "Emission Color": 26,
        "Emission Strength": 27
    }

    if color is None:
        prin_node.inputs[key2idx["Base Color"]].default_value = np.random.uniform(0.3, 0.9, 4)
    else:
        prin_node.inputs[key2idx["Base Color"]].default_value = color
    
    prin_node.inputs[key2idx["Alpha"]].default_value = 0
    # prin_node.inputs[key2idx["Normal"]].default_value = 0  # Of type vector instead of float
    prin_node.inputs[key2idx["Weight"]].default_value = 0
    prin_node.inputs[key2idx["Subsurface Weight"]].default_value = 0
    # prin_node.inputs[key2idx["Subsurface Radius"]].default_value = 0  # Of type vector instead of float
    prin_node.inputs[key2idx["Subsurface Scale"]].default_value = 0
    prin_node.inputs[key2idx["Subsurface IOR"]].default_value = 0
    prin_node.inputs[key2idx["Subsurface Anisotropy"]].default_value = 0
    prin_node.inputs[key2idx["Specular IOR Level"]].default_value = 0

    prin_node.inputs[key2idx["Anisotropic"]].default_value = 1.45
    prin_node.inputs[key2idx["Roughness"]].default_value = 0
    prin_node.inputs[key2idx["Transmission Weight"]].default_value = 0.9 + rand() * 0.1



def random_metallic_mat(nodes, color=None):
    prin_node = nodes["Principled BSDF"]

    # The mapping was taken by running:
    # for i, e in enumerate(prin_node.inputs):
    #     print(f"{i}: {type(e)}: {e}")
    key2idx = {
        "Base Color": 0,
        "Metallic": 1,
        "Roughness": 2,
        "IOR": 3,
        "Alpha": 4 ,
        "Normal": 5,
        "Weight": 6,
        "Subsurface Weight": 7,
        "Subsurface Radius": 8,
        "Subsurface Scale": 9,
        "Subsurface IOR": 10,
        "Subsurface Anisotropy": 11,
        "Specular IOR Level": 12,
        "Specular Tint": 13,
        "Anisotropic": 14,
        "Anisotropic Rotation": 15,
        "Tangent": 16,
        "Transmission Weight": 17,
        "Coat Weight": 18,
        "Coat Roughness": 19,
        "Coat IOR": 20,
        "Coat Tint": 21,
        "Coat Normal": 22,
        "Sheen Weight": 23,
        "Sheen Roughness": 24,
        "Sheen Tint": 25,
        "Emission Color": 26,
        "Emission Strength": 27
    }

    if color is None:
        prin_node.inputs[key2idx["Base Color"]].default_value = np.random.uniform(0.3, 0.9, 4)
    else:
        prin_node.inputs[key2idx["Base Color"]].default_value = color
    
    prin_node.inputs[key2idx["Weight"]].default_value = rand() / 5
    prin_node.inputs[key2idx["Subsurface Weight"]].default_value = rand() / 5
    # prin_node.inputs[key2idx["Subsurface Radius"]].default_value = rand() / 5  # Of type vector instead of float
    prin_node.inputs[key2idx["Subsurface Scale"]].default_value = rand() / 5
    prin_node.inputs[key2idx["Subsurface IOR"]].default_value = rand() / 5
    prin_node.inputs[key2idx["Subsurface Anisotropy"]].default_value = rand() / 5
    prin_node.inputs[key2idx["Specular IOR Level"]].default_value = rand() / 5
    # prin_node.inputs[key2idx["Specular Tint"]].default_value = rand() / 5  # Of type color instead of float
    prin_node.inputs[key2idx["Anisotropic"]].default_value = rand() / 5
    prin_node.inputs[key2idx["Anisotropic Rotation"]].default_value = rand() / 5


def random_mat(mat, color=None):
    if mat is None:
        mat = bpy.data.materials.new(name="Material")
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    prob = rand()
    if prob <= 0.5:
        random_transparent_mat(nodes, color)
    elif 0.5 < prob <= 1.0:
        random_metallic_mat(nodes, color)
    return mat
