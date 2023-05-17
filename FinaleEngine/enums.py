from enum import Enum
from panda3d.core import ShaderAttrib, AntialiasAttrib, TransparencyAttrib, FogAttrib, ColorAttrib, LightAttrib, \
    AuxBitplaneAttrib, RenderAttrib, MaterialAttrib, CullFaceAttrib, DepthOffsetAttrib, DepthTestAttrib, \
    DepthWriteAttrib, LightRampAttrib, RenderModeAttrib, RescaleNormalAttrib, ShadeModelAttrib, StencilAttrib, \
    TexGenAttrib, TexMatrixAttrib, TextureAttrib, ClipPlaneAttrib, ColorBlendAttrib, ColorScaleAttrib, \
    ColorWriteAttrib, CullBinAttrib, ScissorAttrib, LogicOpAttrib, AlphaTestAttrib, AudioVolumeAttrib, \
    RenderAttribRegistry, AttribNodeRegistry


class TerrainTypes(Enum):
    Heightfield = 1
    GeoMipMap = 2
    Shader = 3


class Attributes(Enum):
    Shader = ShaderAttrib
    Antialiasing = AntialiasAttrib
    Transparency = TransparencyAttrib
    Fog = FogAttrib
    Color = ColorAttrib
    Light = LightAttrib
    AuxBitplane = AuxBitplaneAttrib
    Render = RenderAttrib
    Material = MaterialAttrib
