import random
from enum import Enum
import numpy as np

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
        
    
    def getNormal(self):
        listVertex = self.vertices
        v1 = listVertex[0]
        v2 = listVertex[1]
        v3 = listVertex[2]
        p1 = np.array([v1.x,v1.y,v1.z])
        p2 = np.array([v2.x,v2.y,v2.z])
        p3 = np.array([v3.x,v3.y,v3.z])
        V12 = p2 - p1
        V13 = p3 - p1
        return np.cross(V12,V13)

class Vertex:

    def __init__(self, id, attachedFaces, flag, tag, x, y, z):
        self.id = id
        self.flag = flag
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.attachedFaces = attachedFaces

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.id == other.id

    def getValence(self):
        #Renvoie la valence d'un vertex
        #cette dernière correspond au nombre de faces liées à ce vertex
        connected_vertices = np.array([f.vertices for f in self.attachedFaces]).flatten()
        connected_vertices = [v.id for v in connected_vertices]
        #print(f"GET VALENCE index {self.id} {np.unique(connected_vertices)} = {len(np.unique(connected_vertices)) - 1}")
        return len(np.unique(connected_vertices)) - 1

class Patch:

    def __init__(self, id, entry_gate, isNullPatch):

        self.id = id
        self.isNullPatch = isNullPatch
        self.entry_gate = entry_gate
        self.center_vertex = entry_gate.getFrontVertex()
        self.boundingVertices = []

        if isNullPatch:
            self.boundingVertices = [ entry_gate.vertices[0], entry_gate.vertices[1], entry_gate.getFrontVertex() ]
        else:
            def findnextface(listfaces, vertex):
                for f in listfaces:
                    if vertex in f.vertices and self.center_vertex in f.vertices:
                        return f
                return None

            self.boundingVertices += self.entry_gate.vertices

            faceslist = self.center_vertex.attachedFaces[:]
            faceslist.remove(self.entry_gate.frontFace)
            current_vertex = self.entry_gate.vertices[1]

            # print("")
            # print( "Triage des bounding vertex...")
            while faceslist:
                # print(f"faceslist{[f.id for f in faceslist]}")
                face = findnextface(faceslist, current_vertex)

                if face is not None:
                    for v in face.vertices:
                        if v not in self.boundingVertices and v!= self.center_vertex:
                            self.boundingVertices.append(v)

                    current_vertex = self.boundingVertices[-1]
                    faceslist.remove(face)
                else:
                    print("ERROR --------------------------------------------------------------")
                    break
            # print(f"Gate: verts = {[v.id for v in self.entry_gate.vertices]}")
            # print(f"bounding verts = {[v.id for v in self.boundingVertices]}")
            # print("")
                    
    def getValence(self):
        #La valence d'un patch est en réalité la valence du vertex central, et
        #cette dernière correspond au nombre de faces liées à ce vertex
        return self.center_vertex.getValence()

    #Retourne une liste ordonnée des output gates
    def getOutputGates(self):
        output_gates = []
        
        if self.isNullPatch:
            gate = self.entry_gate
            frontVertex = gate.getFrontVertex()
            first_outside_face = [f for f in frontVertex.attachedFaces if
                                (gate.vertices[0] in f.vertices and
                                gate.vertices[1] not in f.vertices and
                                frontVertex in f.vertices)
                                ]
            if(len(first_outside_face) != 0):
                first_outside_face = first_outside_face[0]
                output_gates.append(Gate(first_outside_face, [ gate.vertices[0], frontVertex ]))

            second_outside_face = [f for f in frontVertex.attachedFaces if
                        (gate.vertices[1] in f.vertices and
                        gate.vertices[0] not in f.vertices and
                        frontVertex in f.vertices)
                        ]
            if(len(second_outside_face) != 0):
                second_outside_face = second_outside_face[0]
                output_gates.append(Gate(second_outside_face, [ gate.vertices[1], frontVertex ]))
        else:
            #On commence par le vertex de "droite" de l'entry gate
            current_vertex = self.entry_gate.vertices[1]
        
            #-1 pour éviter l'entryGate
            for i in range(len(self.boundingVertices) - 1):
            
                next_vertex_index = (self.boundingVertices.index(current_vertex) + 1)%len(self.boundingVertices)

                next_vertex = self.boundingVertices[next_vertex_index]
            
                #On récupère maintenant la face exterieure au patch liant current_vertex avec next_vertex.
                #Elle dois contenir ces deux derniers vertex mais pas le center_vertex
                next_outside_face = [f for f in current_vertex.attachedFaces if
                                next_vertex in f.vertices and
                                self.center_vertex not in f.vertices]
            
                #Si on ne trouve pas de face répondant aux contriantes on ne trouvera pas d'output gate pour le
                #current vertex (c'est possible qu'il n'existe pas de faces en dehors du patch)
                if(len(next_outside_face) != 0):
                    next_outside_face = next_outside_face[0]
                    #On ajoute la nouvelle gate aux output_gates
                    output_gates.append(Gate(next_outside_face, [current_vertex, next_vertex]))
                current_vertex = next_vertex
                
        return output_gates
    
    def getNormal(self):
        n = len(self.boundingVertices)
        N = [0,0,0]
        for i in range (0,n-1):
            v1 = self.boundingVertices[i%n]
            v2 = self.boundingVertices[(i+1)%n]
            v3 = self.boundingVertices[(i+2)%n]
            p1 = np.array([v1.x,v1.y,v1.z])
            p2 = np.array([v2.x,v2.y,v2.z])
            p3 = np.array([v3.x,v3.y,v3.z])
            V12 = p2 - p1
            V13 = p3 - p1
            Ni = np.cross(V12,V13)
            N = N + Ni
        N = N/n
        return N
    
    def getBaricentre(self):
        n = len(self.boundingVertices)
        b = np.array([0,0,0])
        for i in range (0,n-1):
            vert = self.boundingVertices[i]
            b = b + np.array([vert.x,vert.y,vert.z])
        b = b/n
        return b
    
    def getFrenet(self):
        N = self.getNormal()
        b = self.getBaricentre()
        t1 = getFirstTangent(self,N)
        t2 = getSecondTangent(N,t1)
        return [b,t1,t2,N]
    
    def getFrenetCoordinates(self, vertex):
        # Frenet Frame
        [b,t1,t2,N] = self.getFrenet()

        vertexCoordinates = np.array([vertex.x, vertex.y, vertex.z])
        b = np.array(b)  
        t1 = np.array(t1)
        t2 = np.array(t2)  
        N = np.array(N)    

        offset = vertexCoordinates - b
        alpha = np.dot(offset, t1)
        beta = np.dot(offset, t2)
        gamma = np.dot(offset, N)

        return [alpha, beta, gamma]
    
def getFirstTangent(patch,N):
    vecteurGate = patch.entry_gate
    v1 = vecteurGate.vertices[0]
    v2 = vecteurGate.vertices[1]
    p1 = np.array([v1.x,v1.y,v1.z])
    p2 = np.array([v2.x,v2.y,v2.z])
    gate = p2-p1
    t1 = np.cross(N,gate)
    return t1
    
def getSecondTangent(N,t1):
    t2 = np.cross(N,t1)
    return t2

class Gate:

    def __init__(self, frontFace, vertices):
        self.frontFace = frontFace
        self.vertices = vertices

    def getFrontVertex(self):
        frontVertex = None
        for v in self.frontFace.vertices:
            if v not in self.vertices:
                frontVertex = v
        return frontVertex

def printVertsAndFaces(vertices,faces):
    for j in range (len(vertices)):
        vert = vertices[j]
        print(f"Vertex {j}: id:{vert.id} flag:{vert.flag} tag:{vert.tag} pos:{vert.x},{vert.y},{vert.z} attachedFaces_id:{[i.id for i in vert.attachedFaces]}")

    for j in range (len(faces)):
        face = faces[j]
        print(f"Face {j}: id:{face.id} flag:{face.flag} verts_id:{[v.id for v in face.vertices]}")

def getFirstGate(faces):
    #On choisie la "première" face stockée dans la liste de faces,
    #mais on pourrait aussi tirer une face au hasard, ce qui
    ##serait un peu plus couteux
    random_face = faces[random.randint(0, len(faces)-1)]
    
    #On récupère le premier vertex de la face
    first_vertex = random_face.vertices[1]
    
    #On récupère le deuxième vertex de la face
    second_vertex = random_face.vertices[2]
    
    return Gate(random_face, [first_vertex, second_vertex])

def getNextElementIndex(faces_or_verts):
    element_idx = [f.id for f in faces_or_verts]
    return max(element_idx) + 1