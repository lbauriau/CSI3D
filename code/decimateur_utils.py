from enum import Enum

class Flag(Enum):
    Free = 1
    Conquered = 2
    ToBeRemoved = 3

class Tag(Enum):
    Plus = 1
    Minus = 2

class Face:

    def __init__(self, flag, vertices):
        self.flag = flag
        self.vertices = vertices

class Vertex:

    def __init__(self, attachedFaces, flag, tag, x, y, z):
        self.flag = flag
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.attachedFaces = attachedFaces

class Patch:

    def __init__(self, id, boundingVertices):
        self.id = id
        self.boundingVertices = boundingVertices
        
class Gate:

    def __init__(self, id, frontFace, vertices):
        self.id = id
        self.frontFace = frontFace
        self.vertices = vertices

    





        
    

