from ursina import *
from ursina.shaders import lit_with_shadows_shader
from perlin_noise import PerlinNoise
import random, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Ground(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__()
        self.parent = scene
        self.model = 'cube' #wireframe_cube
        self.texture = 'grass'
        self.position = position
        self.color = color.white
        self.highlight_color = color.gray

riverPath = []
def BuildRiver(position = (0,0,0)):
    matrix = []

    for x in range(mapSize[0]):
        row = []
        for y in range(mapSize[1]):
            row.append(random.randint(0,1))
        matrix.append(row)
    
    grid = Grid(matrix=matrix)
    start = grid.node(0,0)
    end = grid.node(10,10)

    finder = AStarFinder()
    path, rus = finder.find_path(start, end, grid)
    print(path)

fullMap = []
mapSize = (16 * 4, 16 * 4)
def BuildGround(position = (0,0,0)):
    noise = PerlinNoise(octaves = random.uniform(0.1,2), seed = random.randint(0, sys.maxsize))
    freq = 16
    amp = 5
    for x in range(mapSize[0]):
        for z in range(mapSize[1]):
            y = noise([x / freq, z / freq]) * amp
            ground = Ground(position = (x + position[0],y + position[1],z + + position[2]))
            fullMap.append(ground)

# buildings
class Building(Button):
    def __init__(self, position = (0,0,0)):
        super().__init__()
        self.parent = scene
        self.model = 'cube'
        self.texture = 'white_cube'
        self.position = position
        self.color = color.white
        self.highlight_color = self.color

def BuildBuilding(position = (0,0,0)):
    # always be on top of the ground
    X = random.randint(0, mapSize[0])
    Z = random.randint(0, mapSize[1])
    for item in fullMap:
        if item.position.x == X and item.position.z == Z:
            newPosition = item.position
            newPosition.y += 1

    building = Building(position=newPosition)
    
app = Ursina()
camera = EditorCamera()
BuildGround()
# BuildBuilding()
BuildRiver()
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,1))
Sky()
app.run()
