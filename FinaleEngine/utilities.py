from window import window
from direct.actor.Actor import Actor
from panda3d.core import VirtualFileSystem, NodePath, PerlinNoise2, PNMImage, StackedPerlinNoise2, Texture, CardMaker
import ast
from entities import Terrain
from random import randint

# The virtual file system simplifies handling file paths
VFS = VirtualFileSystem.get_global_ptr()

# Data is a global dictionary that you can use to store any data you want. When calling save_game data
# is saved automatically
data = {}


def destroy(entity):
    entity.on_destroy()

    if entity in window.entity_list:
        del window.entity_list[entity.node]

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


def get_entity(node):
    return window.entity_list[node]


def generate_terrain(texture=None, noise_amount=3, seed=0, image_size=64):
    # Create the texture we'll load the noise into, we need to add + 1 to the size as terrain needs a heightmap to be
    # a power of 2 + 1
    image = PNMImage(image_size + 1, image_size + 1, 1, 16)

    # Create the noise and apply several layers of noise to it
    noise = StackedPerlinNoise2()
    for q in range(noise_amount):
        added_noise = PerlinNoise2()
        added_noise.set_scale(randint(1, 5))
        noise.add_level(added_noise)

    noise.add_level(PerlinNoise2())

    # Transfer the noise into the PNMImage so we can use it as the heightmap
    # (Panda3D's terrain can't use noise directly)
    for x in range(image_size):
        for y in range(image_size):
            image.set_gray(x, y, (noise(x, y) + 1) * .5)
            print((noise(x, y) + 1) * .5)

    image.box_filter(2)

    # We want to see the height map used if the user hasn't passed in their own texture
    if texture is None:
        texture = Texture()
        texture.load(image)

    return Terrain("generate_terrain", image, height=100, texture=texture)


def plane():
    card = CardMaker("plane")
    return window.render.attach_new_node(card.generate())


water = plane()
water.set_p(-90)
water.set_scale(20, 20, 20)
water.set_z(20)

a = generate_terrain()
a.set_scale(100, 100, 8)
p = load_model("panda")
p.reparent_to(window.render)
p.set_z(150)
window.run()
