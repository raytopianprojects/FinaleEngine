from panda3d.core import NodePath, Vec3, VirtualFileSystem
from panda3d import bullet
from window import window
from direct.actor.Actor import Actor

VFS = VirtualFileSystem()


class Entity(NodePath):
    def __init__(self, name, mesh_name=None, has_bones=False, collider=False,
                 collider_shapes=bullet.BulletBoxShape(Vec3(1, 1, 1)), mass=None,
                 physics_world=window.physics_world):
        super().__init__(name)
        self.name = name

        # reparent Entity to the scene graph automatically so users don't have to
        self.reparent_to(window.render)

        # Add the entity to the window entity list, so we can do things such as collision
        window.entity_list.append(self)

        # We only want to add a collider to an entity if the user wants one, otherwise we're wasting processing power
        if collider:
            self.collider = bullet.BulletRigidBodyNode()

            # If the user set a mass value we need to tell bullet this so the collider becomes dynamic instead
            # of rigid
            if mass:
                self.collider.set_mass(mass)

            # Check if the user passed in a list of colliders otherwise just add one the one
            if hasattr(collider_shapes, "__iter__"):
                for shape in collider_shapes:
                    self.collider.add_shape(shape)
            else:
                self.collider.add_shape(collider_shapes)

            # Add the collider to physics world so the bullet engine will update and manage the entity
            physics_world.attach_rigid_body(self.collider)

            # attach the collider to the Entity
            self.collider_node = self.attach_new_node(self.collider)

        if mesh_name:
            if has_bones:
                self.mesh: Actor = Actor(mesh_name)
                self._blend_animations = False

            else:
                self.mesh: NodePath = window.loader.load_model(mesh_name)

            if collider:
                self.mesh.reparent_to(self.collider_node)
            else:
                self.mesh.reparent_to(self)

    @property
    def location(self):
        return self.get_pos()

    @location.setter
    def location(self, value):
        self.set_pos(value)

    @property
    def x(self):
        return self.get_x()

    @x.setter
    def x(self, value):
        self.set_x(value)

    @property
    def y(self):
        return self.get_y()

    @y.setter
    def y(self, value):
        self.set_y(value)

    @property
    def z(self):
        return self.get_z()

    @z.setter
    def z(self, value):
        self.set_z(value)

    def play_animation(self, animation_name, start_frame=None, end_frame=None):
        if end_frame is None:
            end_frame = self.mesh.get_num_frames(animation_name)

        if start_frame is None:
            start_frame = 0

        self.mesh.play(animation_name, start_frame, end_frame)

    def loop_animation(self, animation_name, start_frame=None, end_frame=None, restart=1):
        if end_frame is None:
            end_frame = self.mesh.get_num_frames(animation_name)

        if start_frame is None:
            start_frame = 0

        self.mesh.loop(animation_name, start_frame, end_frame, restart)

    def stop_animation(self):
        self.mesh.stop()

    def pose_animation(self, animation_name, frame_number):
        self.mesh.pose(animation_name, frame_number)

    def current_frame(self, animation_name):
        return self.mesh.get_current_frame(animation_name)

    @property
    def play_rate(self):
        return self.mesh.get_play_rate()

    @play_rate.setter
    def play_rate(self, value):
        self.mesh.set_play_rate(value)

    def on_destroy(self):
        pass


if __name__ == "__main__":
    entity = Entity("A", mesh_name="teapot", collider=True, mass=10)
    print(entity.node() == entity.collider.get_parent(0))
    window.gravity = Vec3((0, 0, -9.81))
    window.accept("p", lambda: window.render.ls())
    window.run()
