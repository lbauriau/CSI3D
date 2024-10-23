from enum import Enum
import random

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

def get_first_gate(vertices, faces):
    random_face = faces(random.randrange(0,len(faces)))
    
    #On récupère le premier vertex de la face
    first_vertex = vertices[random_face.keyVertices[0]]
    
    #On récupère le deuxième vertex de la face
    second_vertex = vertices[random_face.keyVertices[1]]
    
    return Gate(random_face, [first_vertex, second_vertex])


    





        
    

