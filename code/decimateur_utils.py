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
        list_vertex = self.vertices
        v1 = list_vertex[0]
        v2 = list_vertex[1]
        v3 = list_vertex[2]
        p1 = np.array([v1.x,v1.y,v1.z])
        p2 = np.array([v2.x,v2.y,v2.z])
        p3 = np.array([v3.x,v3.y,v3.z])
        V12 = p2 - p1
        V13 = p3 - p1
        return np.cross(V12,V13)

class Vertex:

    def __init__(self, id, attached_faces, flag, tag, x, y, z):
        self.id = id
        self.flag = flag
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.attached_faces = attached_faces

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.id == other.id

    def getValence(self):
        # Renvoie la valence d'un vertex
        # cette dernière correspond au nombre de faces liées à ce vertex
        connected_vertices = np.array([f.vertices for f in self.attached_faces]).flatten()
        connected_vertices = [v.id for v in connected_vertices]
        #print(f"GET VALENCE index {self.id} {np.unique(connected_vertices)} = {len(np.unique(connected_vertices)) - 1}")
        return len(np.unique(connected_vertices)) - 1

    def isOnTheBoundary(self):
        # Un vertex est sur le bord si sa valence n'est pas égale au nombre de faces liées à ce vertex
        return self.getValence() != len(self.attached_faces)

class Patch:

    def __init__(self, id, entry_gate, is_null_patch, faces = None):

        self.id = id
        self.is_null_patch = is_null_patch
        self.entry_gate = entry_gate
        self.center_vertex = entry_gate.getFrontVertex()
        self.bounding_vertices = []

        if is_null_patch:
            self.bounding_vertices = [ entry_gate.vertices[0], entry_gate.vertices[1], entry_gate.getFrontVertex() ]
        else:
            def findNextFace(list_faces, vertex):
                for f in list_faces:
                    if vertex in f.vertices and self.center_vertex in f.vertices:
                        return f
                return None

            # Les premiers vertex de bounding_vertices sont ceux de la gate
            self.bounding_vertices += self.entry_gate.vertices

            # Récupération des faces constituant le patch
            faces_list = self.center_vertex.attached_faces[:]

            # Les vertices de la front_face de la gate étant déjà dans bounding vertex cette face est déjà traitée
            faces_list.remove(self.entry_gate.front_face)
            current_vertex = self.entry_gate.vertices[1]

            # print("")
            # print( "Triage des bounding vertex...")
            while faces_list:
                # print(f"faces_list{[f.id for f in faces_list]}")
                # Récuperation de la face non traitée suivante
                face = findNextFace(faces_list, current_vertex)

                if face is not None:
                    for v in face.vertices:
                        if v not in self.bounding_vertices and v!= self.center_vertex:
                            self.bounding_vertices.append(v)

                    current_vertex = self.bounding_vertices[-1]
                    faces_list.remove(face)
                else:
                    error_string = f"ERROR bounding vertex: looking for vertex {current_vertex.id} in:"
                    for f in faces_list:
                        error_string += f"\n face {f.id}: {[v.id for v in f.vertices]} "
                    error_string += f"\n in patch with center vertex {self.center_vertex.id} which has this faces connected:"
                    for f in self.center_vertex.attached_faces:
                        error_string += f"\n face {f.id}: {[v.id for v in f.vertices]} {"" if f in faces else "not"} in faces general list"
                    raise Exception(error_string)
                    break
            # print(f"Gate: verts = {[v.id for v in self.entry_gate.vertices]}")
            # print(f"bounding verts = {[v.id for v in self.bounding_vertices]}")
            # print("")

    def getValence(self):
        #La valence d'un patch est en réalité la valence du vertex central, et
        #cette dernière correspond au nombre de faces liées à ce vertex.
        return self.center_vertex.getValence()

    #Retourne une liste ordonnée des outputs gates
    def getOutputGates(self):
        output_gates = []

        if self.is_null_patch:
            gate = self.entry_gate
            front_vertex = gate.getFrontVertex()
            first_outside_face = [f for f in front_vertex.attached_faces if
                                (gate.vertices[0] in f.vertices and
                                gate.vertices[1] not in f.vertices and
                                front_vertex in f.vertices)
                                ]
            if(len(first_outside_face) != 0):
                first_outside_face = first_outside_face[0]
                output_gates.append(Gate(first_outside_face, [ gate.vertices[0], front_vertex ]))

            second_outside_face = [f for f in front_vertex.attached_faces if
                        (gate.vertices[1] in f.vertices and
                        gate.vertices[0] not in f.vertices and
                        front_vertex in f.vertices)
                        ]
            if(len(second_outside_face) != 0):
                second_outside_face = second_outside_face[0]
                output_gates.append(Gate(second_outside_face, [ front_vertex, gate.vertices[1] ]))
        else:
            #On commence par le vertex de "droite" de l'entry gate
            current_vertex = self.entry_gate.vertices[1]

            #-1 pour éviter l'entry_gate
            for i in range(len(self.bounding_vertices) - 1):

                next_vertex_index = (self.bounding_vertices.index(current_vertex) + 1)%len(self.bounding_vertices)

                next_vertex = self.bounding_vertices[next_vertex_index]

                #On récupère maintenant la face extérieure au patch liant current_vertex avec next_vertex.
                #Elle doit contenir ces deux derniers vertex, mais pas le center_vertex
                next_outside_face = [f for f in current_vertex.attached_faces if
                                next_vertex in f.vertices and
                                self.center_vertex not in f.vertices]

                #Si on ne trouve pas de face répondant aux contraintes, on ne trouvera pas d'output gate pour le
                #current vertex (c'est possible qu'il n'existe pas de faces en dehors du patch)
                if(len(next_outside_face) != 0):
                    next_outside_face = next_outside_face[0]
                    #On ajoute la nouvelle gate aux output_gates
                    output_gates.append(Gate(next_outside_face, [next_vertex, current_vertex]))
                current_vertex = next_vertex

        return output_gates

    def getNormal(self):
        n = len(self.bounding_vertices)
        N = [0,0,0]
        for i in range (0,n-1):
            v1 = self.bounding_vertices[i%n]
            v2 = self.bounding_vertices[(i+1)%n]
            v3 = self.bounding_vertices[(i+2)%n]
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
        n = len(self.bounding_vertices)
        b = np.array([0,0,0])
        for i in range (0,n-1):
            vert = self.bounding_vertices[i]
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

        vertex_coordinates = np.array([vertex.x, vertex.y, vertex.z])
        b = np.array(b)
        t1 = np.array(t1)
        t2 = np.array(t2)
        N = np.array(N)

        offset = vertex_coordinates - b
        alpha = np.dot(offset, t1)
        beta = np.dot(offset, t2)
        gamma = np.dot(offset, N)

        return [alpha, beta, gamma]

def getFirstTangent(patch,N):
    vecteur_gate = patch.entry_gate
    v1 = vecteur_gate.vertices[0]
    v2 = vecteur_gate.vertices[1]
    p1 = np.array([v1.x,v1.y,v1.z])
    p2 = np.array([v2.x,v2.y,v2.z])
    gate = p2-p1
    t1 = np.cross(N,gate)
    return t1

def getSecondTangent(N,t1):
    t2 = np.cross(N,t1)
    return t2

class Gate:

    def __init__(self, front_face, vertices):
        self.front_face = front_face
        self.vertices = vertices

    def getFrontVertex(self):
        front_vertex = None
        for v in self.front_face.vertices:
            if v not in self.vertices:
                front_vertex = v
        return front_vertex

def printVertsAndFaces(vertices,faces):
    for j in range (len(vertices)):
        vert = vertices[j]
        print(f"Vertex {j}: id:{vert.id} flag:{vert.flag} tag:{vert.tag} pos:{vert.x},{vert.y},{vert.z} attached_faces_id:{[i.id for i in vert.attached_faces]}")

    for j in range (len(faces)):
        face = faces[j]
        print(f"Face {j}: id:{face.id} flag:{face.flag} verts_id:{[v.id for v in face.vertices]}")

def getFirstGate(faces):
    #On choisit la "première" face stockée dans la liste de faces,
    #mais on pourrait aussi tirer une face au hasard, ce qui
    ##serait un peu plus couteux.
    random_face = faces[random.randint(0, len(faces)-1)]
    
    #On récupère le premier vertex de la face
    first_vertex = random_face.vertices[0]
    
    #On récupère le deuxième vertex de la face
    second_vertex = random_face.vertices[1]
    
    return Gate(random_face, [first_vertex, second_vertex])

def getNextElementIndex(faces_or_verts):
    element_idx = [f.id for f in faces_or_verts]
    return max(element_idx) + 1

def getFaceWithVertices(vert1,vert2):
    n = len(vert1.attached_faces)
    for i in range(n):
        if (vert1.attached_faces[i] in vert2.attached_faces):
            if (vert1.attached_face[1].flag == Flag.Free):
                return vert1.attached_faces[i]
    return 0

def getAdjacentFace(face, vert1, vert2):
    for f in vert1.attached_faces:
        if f in vert2.attached_faces and f.id != face.id:
            return f
    return None

def getThirdVertex(face, vert1, vert2):
    for i in range(3):
        aux_vert = face.vertices[i]
        if (aux_vert!= vert1 and aux_vert!= vert2):
            return aux_vert
