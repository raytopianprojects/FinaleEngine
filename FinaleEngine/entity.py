from panda3d.core import NodePath, Vec3, VirtualFileSystem
from panda3d import bullet
from window import window
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject

VFS = VirtualFileSystem()


class Entity(NodePath, DirectObject):
    def __init__(self, name, mesh_name=None, has_bones=False, collider=False,
                 collider_shapes=bullet.BulletBoxShape(Vec3(1, 1, 1)), mass=None,
                 physics_world=window.physics_world):
        super().__init__(name)
        self.name = name

        # reparent Entity to the scene graph automatically so users don't have to
        self.reparent_to(window.render)

        # Add the entity to the window entity list, so we can do things such as collision
        window.entity_list[(self.node,)] = self

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

        # Create the entity's mesh
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

    @property
    def scale(self):
        return self.get_scale()

    @scale.setter
    def scale(self, scale):
        self.set_scale(scale)

    @property
    def x_scale(self):
        return self.get_sx()

    @x_scale.setter
    def x_scale(self, scale):
        self.set_sx(scale)

    @property
    def y_scale(self):
        return self.get_sy()

    @y_scale.setter
    def y_scale(self, scale):
        self.set_sy(scale)

    @property
    def z_scale(self):
        return self.get_sz()

    @z_scale.setter
    def z_scale(self, scale):
        self.set_sz(scale)

    @property
    def rotation(self):
        return self.get_hpr()

    @rotation.setter
    def rotation(self, rotation):
        self.set_hpr(rotation)

    @property
    def heading(self):
        return self.get_h()

    @heading.setter
    def heading(self, degrees):
        self.set_h(degrees)

    @property
    def pitch(self):
        return self.get_p()

    @pitch.setter
    def pitch(self, degrees):
        self.set_p(degrees)

    @property
    def roll(self):
        return self.get_r()

    @roll.setter
    def roll(self, degrees):
        self.set_r(degrees)

    @property
    def quat(self):
        return self.get_quat()

    @quat.setter
    def quat(self, quaternion):
        self.set_quat(quaternion)

    @property
    def texture(self):
        if self.mesh:
            if self.mesh.has_texture():
                return self.mesh.get_texture()
        else:
            return None

    @texture.setter
    def texture(self, texture):
        if self.mesh:
            self.mesh.set_texture(texture)

    @property
    def shader(self):
        return self.get_shader()

    @shader.setter
    def shader(self, shader):
        self.set_shader(shader)

    @property
    def material(self):
        if self.has_material():
            return self.get_material()

    @material.setter
    def material(self, material):
        if material is None:
            self.clear_material()
        else:
            self.set_material(material)

    @property
    def bin_draw_order(self):
        return self.get_bin_draw_order()

    @property
    def bin_name(self):
        return self.get_bin_name()

    @property
    def color(self):
        return self.get_color()

    @property
    def depth_offset(self):
        return self.get_depth_offset()

    @property
    def depth_write(self):
        return self.get_depth_write()

    @property
    def depth_test(self):
        return self.get_depth_test()

    @property
    def instance_count(self):
        return self.get_instance_count()

    @instance_count.setter
    def instance_count(self, instance_count):
        self.set_instance_count(instance_count)

    @property
    def matrix(self):
        return self.get_mat()

    @matrix.setter
    def matrix(self, matrix):
        self.set_mat(matrix)

    @property
    def max_search_depth(self):
        return self.get_max_search_depth()

    @max_search_depth.setter
    def max_search_depth(self, max_search_depth):
        self.set_max_search_depth(max_search_depth)

    @property
    def node_name(self):
        return self.get_name()

    @node_name.setter
    def node_name(self, node_name):
        self.set_name(node_name)

    @property
    def alpha(self):
        return self.get_sa()

    @alpha.setter
    def alpha(self, alpha):
        self.set_sa(alpha)

    @property
    def red(self):
        return self.get_sr()

    @red.setter
    def red(self, red):
        self.set_sr(red)

    @property
    def blue(self):
        return self.get_sb()

    @blue.setter
    def blue(self, blue):
        self.set_sb(blue)

    @property
    def green(self):
        return self.get_sg()

    @green.setter
    def green(self, green):
        self.set_sg(green)

    @property
    def shear(self):
        return self.get_shear()

    @shear.setter
    def shear(self, shear):
        self.set_shear(shear)

    @property
    def two_sided(self):
        return self.get_two_sided()

    @two_sided.setter
    def two_sided(self, is_two_sided):
        self.set_two_sided(is_two_sided)

    @property
    def transparency(self):
        return self.get_transparency()

    @transparency.setter
    def transparency(self, transparency):
        self.set_transparency(transparency)

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
        if type(self.mesh) == Actor:
            self.mesh.delete()

        self.remove_node()

        self.ignore_all()
        self.remove_all_tasks()


if __name__ == "__main__":
    entity = Entity("A", mesh_name="teapot", collider=True, mass=10)
    print(entity.node() == entity.collider.get_parent(0))
    window.gravity = Vec3((0, 0, -9.81))
    window.accept("p", lambda: window.render.ls())
    window.run()
