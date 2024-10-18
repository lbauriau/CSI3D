from enum import Enum

class Flag(Enum):
    Free = 1
    Conquered = 2
    ToBeRemoved = 3

class Tag(Enum):
    Plus = 1
    Minus = 2

class Face:

    def __init__(self, id, flag, vertices):
        self.id = id
        self.flag = flag
        self.vertices = vertices

class Vertex:

    def __init__(self, id, flag, tag, x, y, z):
        self.id = id
        self.flag = flag
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z

class Patch:

    def __init__(self, id, boundingVertices):
        self.id = id
        self.boundingVertices = boundingVertices
        
class Gate:

    def __init__(self, id, frontFace, vertex):
        self.id = id
        self.frontFace = frontFace
        self.vertex = vertex



        
    

