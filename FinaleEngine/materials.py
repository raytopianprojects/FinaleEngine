from direct.filter.FilterManager import FilterManager
from panda3d.core import Texture, Shader, NodePath, Material
from FinaleEngine.window import window


class PostProcess:
    """A class that manages post process effects. It simplifies setting up, manging, and chaining them."""

    def __init__(self, window_win=None, window_cam=None):

        if window_cam is None:
            window_cam = window.cam
        if window_win is None:
            window_win = window.win

        self.filter_manager = FilterManager(window_win, window_cam)
        self.effects = []

    def add_effect(self, vertex_shader, fragment_shader, multiply=1, divide=1, alignment=1,
                   order=None, depth_texture=None, color_texture=None, aux_texture0=None,
                   aux_texture1=None, fb_props=None, **kwargs):
        if len(self.effects) > 1:
            quad = self.filter_manager.render_quad_into(mul=multiply, div=divide, align=alignment,
                                                        depthtex=depth_texture, colortex=color_texture,
                                                        auxtex0=aux_texture0, auxtex1=aux_texture1, fbprops=fb_props)
            shader = Shader.make(Shader.SL_GLSL, vertex=vertex_shader, fragment=fragment_shader)
            quad.set_shader(shader)
            quad.set_shader_inputs(**kwargs)
        else:
            quad = self.filter_manager.render_scene_into(depthtex=depth_texture, colortex=color_texture,
                                                         fbprops=fb_props)
            shader = Shader.make(Shader.SL_GLSL, vertex=vertex_shader, fragment=fragment_shader)
            quad.set_shader(shader)
            quad.set_shader_inputs(**kwargs)

        # Only input the texture if the user created one
        for name, texture in {"depth_texture": depth_texture, "color_texture": color_texture,
                              "aux_texture0": aux_texture0, "aux_texture1": aux_texture1}.items():
            if texture:
                quad.set_shader_inputs(**{name: texture})

        # The order post process effects are rendered are very important so let the person using it to place the effect
        # where they want it to be
        if order:
            self.effects.insert(order, quad)
        else:
            self.effects.append(quad)

    def remove_effect(self, index):
        """Removes the effect based on the index the user has given."""
        self.effects.remove(index)


class Look:
    def __init__(self):
        self.material = None
        self.attributes = {}
        self.shader = None
        self.shader_inputs = None

    def apply(self, node: NodePath):
        node.set_shader(self.shader)
        node.set_shader_inputs(self.shader_inputs)

        for attribute, priority in self.attributes.items():
            node.set_attrib(self.attributes, priority)


if __name__ == "__main__":
    post_process = PostProcess()

    post_process.add_effect(vertex_shader="""#version 150
// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

// Output to fragment shader
out vec2 texcoord;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  texcoord = p3d_MultiTexCoord0;
}""", fragment_shader="""#version 150

uniform sampler2D color_texture;

// Input from vertex shader
in vec2 texcoord;

// Output to the screen
out vec4 p3d_FragColor;

void main() {
  vec4 color = texture(color_texture, texcoord);
  color.r = sin(color.r);
  p3d_FragColor = color.rrga;
}
""", color_texture=Texture(), divide=5)

    window.loader.load_model("environment").reparent_to(window.render)
    window.accept("p", lambda: print(post_process.effects))
    window.run()
