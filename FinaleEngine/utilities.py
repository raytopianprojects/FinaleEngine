from window import window
from direct.actor.Actor import Actor
from panda3d.core import VirtualFileSystem, NodePath
import ast

# The virtual file system simplifies handling file paths
VFS = VirtualFileSystem.get_global_ptr()

# Data is a global dictionary that you can use to store any data you want. When calling save_game data
# is saved automatically
data = {}


def destroy(entity):
    entity.on_destroy()

    if entity in window.entity_list:
        window.entity_list.remove(entity)

    entity.remove_node()


def load_model(model):
    return window.loader.load_model(model)


def load_sfx(sound):
    return window.loader.load_sfx(sound)


def load_animation(animation):
    return Actor(animation)


def save(filename, save_data):
    VFS.write_file(filename, bytes(str(save_data)), auto_wrap=True)


def load(filename):
    return ast.literal_eval(str(VFS.openReadFile(filename, auto_unwrap=True)))
