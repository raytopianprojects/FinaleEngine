from direct.showbase.ShowBase import ShowBase
from panda3d import bullet
from panda3d.core import ClockObject, load_prc_file_data
from direct.showbase import Audio3DManager

clock = ClockObject.get_global_clock()

load_prc_file_data("", """show-frame-rate-meter #t""")


class Window(ShowBase):
    def __init__(self, window_type = None):
        if window_type:
            super().__init__(windowType=window_type)
        else:
            super().__init__()

        self.entity_list = []
        self.audio3d = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.camera)
        self.physics_world = bullet.BulletWorld()
        self.add_task(self.update_physics)
        self.accept("`", lambda: self.render.ls() or print(len(self.render.get_children())))

    def update_physics(self, task):
        dt = clock.get_dt()
        self.physics_world.doPhysics(dt)
        return task.cont

    @property
    def gravity(self):
        return self.physics_world.gravity

    @gravity.setter
    def gravity(self, value):
        self.physics_world.set_gravity(value)

    def switch_camera(self):
        ...


window: Window = Window()
