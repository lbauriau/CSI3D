from enum import Enum

class Flag(Enum):
    Free = 1
    Conquered = 2
    ToBeRemoved = 3

class Tag(Enum):
    Plus = 1
    Minus = 2

class Face:

    def __init__(self, flag, keyVertices):
        self.flag = flag
        self.keyVertices = keyVertices

class Vertex:

    def __init__(self, keyAttachedFaces, flag, tag, x, y, z):
        self.flag = flag
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.keyAttachedFaces = keyAttachedFaces

class Patch:

    def __init__(self, id, keyBoundingVertices):
        self.id = id
        self.keyBoundingVertices = keyBoundingVertices
        
class Gate:

    def __init__(self, frontFace, keyVertices):
        self.frontFace = frontFace
        self.keyVertices = keyVertices

    def getFrontVertex(self):
        frontVertex = None
        for v in self.frontFace.keyVertices:
            if v not in self.keyVertices:
                frontVertex = v
        return frontVertex
        


    





        
    

