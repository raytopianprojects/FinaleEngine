from entity import Entity
from window import window
from panda3d.core import LODNode, NodePath, FadeLODNode, Fog, AmbientLight, GeoMipTerrain, HeightfieldTesselator
import enums

_array = [0, 1, 1, 1, 1,
          1, 1, 1, 1, 1,
          1, 1, 1, 1, 1,
          1, 1, 0, 1, 1,
          1, 1, 1, 1, 1,
          1, 0, 1, 1, 1,
          1, 1, 1, 1, 0,
          0, 0, 0, 1, 1,
          1, 0, 1, 1, 1,
          1, 1, 1, 1, 0,
          0, 0, 0, 1, 1,
          1, 0, 1, 1, 1,
          1, 1, 1, 1, 0,
          0, 0, 0, 1, 1,
          1, 0, 1, 1, 1,
          1, 0, 1, 1, 1,
          ]

models = {1: window.loader.load_model("teapot"),
          2: window.loader.load_model("teapot"),
          3: window.loader.load_model("teapot")}


class Chunk(Entity):
    def __init__(self, name, grid_3d, model_map, spacing=5, grid_size=5):
        super().__init__(name)

        self.grid_3d = grid_3d
        self.model_map = model_map

        z_pos = 0
        for x in range(grid_size):
            y_pos = 0
            for y in range(grid_size):
                x_pos = 0
                for z in range(grid_size):
                    cube_value = grid_3d[(x * grid_size + y) * 3 + z]

                    if cube_value == 0:
                        continue

                    lod = FadeLODNode("block")
                    lod_node = NodePath(lod)
                    lod_node.reparent_to(self)
                    lod.add_switch(300, 0)

                    # model = Entity("block")
                    # model.reparent_to(lod_node)
                    self.model_map[cube_value].instance_to(lod_node)
                    lod_node.set_pos((x_pos * spacing, y_pos * spacing, z_pos * spacing))

                    # lod_node.flatten_strong()

                    x_pos += 1
                y_pos += 1
            z_pos += 1

    def destroy_block(self, block_index):
        self.get_child(block_index).remove_node()

    def add_block(self, block_index, block_type):
        from utilities import load_model

        model = load_model(self.model_map[block_type])
        model.reparent_to(self)
        self.flatten_strong()


class ChunkChunk(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.chunks = []

    def create_chunks(self, amount):

        for z in range(amount):
            for y in range(amount):
                for x in range(amount):
                    chunk = Chunk("chunk", _array, models)
                    chunk.set_pos((x * 25, y * 25, z * 25))
                    self.chunks.append(chunk)
                    chunk.reparent_to(self)

        for chunk in self.chunks:
            chunk.flatten_strong()


class Terrain(Entity):
    def __init__(self, name, height_map, texture = None, height = 1, terrain_type=enums.TerrainTypes.GeoMipMap):
        super().__init__(name)

        if terrain_type == enums.TerrainTypes.GeoMipMap:
            self._terrain = GeoMipTerrain(name)
            self._terrain.set_heightfield(height_map)
            self._terrain.getRoot().reparent_to(self)
            self._terrain.getRoot().set_sz(height)

            if texture:
                self._terrain.getRoot().set_texture(texture)

            self._terrain.set_block_size(8)
            self._terrain.set_near(40)
            self._terrain.set_far(100)
            self._terrain.set_focal_point(window.camera)

            self._terrain.generate()

            self.add_task(self.update_terrain)

        elif terrain_type == enums.TerrainTypes.Heightfield:
            ...

        elif terrain_type == enums.TerrainTypes.Shader:
            ...

    def update_terrain(self, task):
        self._terrain.update()
        return task.cont