from window import window
from direct.actor.Actor import Actor


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