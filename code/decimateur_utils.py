import random
from enum import Enum
import numpy as np
import obja

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
        """
        Renvoie la normale de la face
        """
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
        """
        Renvoie la valence du vertex
        """
        # Renvoie la valence d'un vertex
        # cette dernière correspond au nombre de faces liées à ce vertex
        connected_vertices = np.array([f.vertices for f in self.attached_faces]).flatten()
        connected_vertices = [v.id for v in connected_vertices]
        #print(f"GET VALENCE index {self.id} {np.unique(connected_vertices)} = {len(np.unique(connected_vertices)) - 1}")
        return len(np.unique(connected_vertices)) - 1

    def isOnTheBoundary(self):
        """
         Le vertex est-il sur un bord ?
        """
        # Un vertex est sur le bord si sa valence n'est pas égale au nombre de faces liées à ce vertex
        return self.getValence() != len(self.attached_faces)

class Patch:

    def __init__(self, id, entry_gate, is_null_patch, bounding_vertices = None):

        self.id = id
        self.is_null_patch = is_null_patch
        self.entry_gate = entry_gate
        self.center_vertex = entry_gate.getFrontVertex()

        if bounding_vertices is not None:
            self.bounding_vertices = bounding_vertices
        else:
            self.bounding_vertices = []
            if is_null_patch:
                self.bounding_vertices = [ entry_gate.vertices[0], entry_gate.vertices[1], entry_gate.getFrontVertex() ]
            else:
                def findNextFace(list_faces, vertex):
                    """
                    Renvoie la prochaine face du patch dans le sens anti_horraire

                    :param [in] list_faces: liste des faces que nous voulons sonder.
                    :param [in] vertex: le bounding vertex dont on veut connaître la face "à sa droite"
                    :return: La face demandée si elle existe et None sinon
                    """
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
                            error_string += f"\n face {f.id}: {[v.id for v in f.vertices]} in faces general list"
                        raise Exception(error_string)
                # print(f"Gate: verts = {[v.id for v in self.entry_gate.vertices]}")
                # print(f"bounding verts = {[v.id for v in self.bounding_vertices]}")
                # print("")

    def getValence(self):
        """
        Renvoie la valence du patch qui n'est autre que la valence du vertex central
        """
        #La valence d'un patch est en réalité la valence du vertex central, et
        #cette dernière correspond au nombre de faces liées à ce vertex.
        return self.center_vertex.getValence() if not self.is_null_patch else 0

    #Retourne une liste ordonnée des outputs gates
    def getOutputGates(self):
        """
        Renvoie l'ensemble des gates orientées vers l'extérieur du patch (hormis la gate d'entrée)
        dans le sens anti-horraires en commançant par la gate " à droite" de la gate d'entrée.
        """
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

    def setTags(self):
        i = 0
        gate_vertices = self.entry_gate.vertices
        for nv in self.bounding_vertices:
            if nv not in gate_vertices:
                if (nv.tag is None):
                    match self.getValence():
                        case 3:
                            if ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus)):
                                nv.tag = Tag.Minus
                            else:
                                nv.tag = Tag.Plus
                        case 4:
                            if ((gate_vertices[0].tag == Tag.Minus) and (gate_vertices[1].tag == Tag.Plus) or ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus))) :
                                if i%2:
                                    nv.tag = Tag.Minus
                                else:
                                    nv.tag = Tag.Plus
                            else: 
                                if i%2:
                                    nv.tag = Tag.Plus
                                else:
                                    nv.tag = Tag.Minus
                        case 5:
                            if ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus)) :
                                if i%2:
                                    nv.tag = Tag.Minus
                                else:
                                    nv.tag = Tag.Plus
                            else: 
                                if i%2:
                                    nv.tag = Tag.Plus
                                else:
                                    nv.tag = Tag.Minus
                        case 6:
                            if ((gate_vertices[0].tag == Tag.Minus) and (gate_vertices[1].tag == Tag.Plus) or ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus))) :
                                if i%2:
                                    nv.tag = Tag.Minus
                                else:
                                    nv.tag = Tag.Plus
                            else: 
                                if i%2:
                                    nv.tag = Tag.Plus
                                else:
                                    nv.tag = Tag.Minus
                        case _:
                            pass 
                i +=1

    def getNormal(self):
        """
        Renvoie la normale du patch
        """
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
        norm_N = np.linalg.norm(N)
        N = N/norm_N
        return N

    def getBaricentre(self):
        """
        Renvoie le baricentre du patch
        """
        n = len(self.bounding_vertices)
        b = np.array([0,0,0])
        for i in range (0,n):
            vert = self.bounding_vertices[i]
            b = b + np.array([vert.x,vert.y,vert.z])
        b = b/n
        return b

    def getFrenet(self):
        """
        Renvoie la base de frenet du patch
        """
        N = self.getNormal()
        b = self.getBaricentre()
        t1 = getFirstTangent(self,N)
        t2 = getSecondTangent(N,t1)
        return [b,t1,t2,N]

    def getFrenetCoordinates(self, vertex):
        """
        Renvoie les coordonées de frenet dans ce patch d'un vertex

        :param [in] vertex: le vertex dont on veut connaître les coordonnées de frenet
        :return: les coordonnées dans le repère de frenet du patch du vertex
        """
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
    """
    Renvoie la première tangente du repère de frenet du patch connaissant sa normale

    :param [in] patch: patch dont nous voulons connaitre la 1ere tangente
    :param [in] N: Normale du patch
    :return: la premiere tangente au sens de frenet
    """
    vecteur_gate = patch.entry_gate
    v1 = vecteur_gate.vertices[0]
    v2 = vecteur_gate.vertices[1]
    p1 = np.array([v1.x,v1.y,v1.z])
    p2 = np.array([v2.x,v2.y,v2.z])
    gate = p2-p1
    t1 = gate - np.dot(gate, N) * N 
    t1 = t1 / np.linalg.norm(t1)
    return t1

def getSecondTangent(N,t1):
    """
    Renvoie la seconde tangente du repère de frenet du patch connaissant sa normale et sa 1ere tangente

    :param [in] N:  normale du patch
    :param [in] t1: 1ere tangente du patch
    :return: 2nd tangente du patch
    """
    t2 = np.cross(N,t1)
    return t2

class Gate:

    def __init__(self, front_face, vertices):
        self.front_face = front_face
        self.vertices = vertices

    def getFrontVertex(self):
        """
        Renvoie le vertex de la front_face n'étant pas dans les vertices de la gate.
        """
        front_vertex = None
        for v in self.front_face.vertices:
            if v not in self.vertices:
                front_vertex = v
        return front_vertex

def printVertsAndFaces(vertices,faces):
    """
    Fonction d'affichage à des fins de débug

    :param [in] vertices: ensemble des vertices de la mesh.
    :param [in] faces: ensemble des faces de la mesh
    """
    for j in range (len(vertices)):
        vert = vertices[j]
        print(f"Vertex {j}: id:{vert.id} flag:{vert.flag} tag:{vert.tag} pos:{vert.x},{vert.y},{vert.z} attached_faces_id:{[i.id for i in vert.attached_faces]}")

    for j in range (len(faces)):
        face = faces[j]
        print(f"Face {j}: id:{face.id} flag:{face.flag} verts_id:{[v.id for v in face.vertices]}")

def getFirstGate(faces):
    """
    Renvoie une gate au hasard grâce au module random.randint
    :param [in] faces: ensemble des faces de la mesh
    :return: Une gate tirée au hasard
    """
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
    """
    Renvoie le prochain id disponible afin d'en assurer l'unicité
    :param faces_or_verts: ensemble des faces OU des vertices
    :return: un id jamais utilisé
    """
    element_idx = [f.id for f in faces_or_verts]
    return max(element_idx) + 1
"""
def getFaceWithVertices(vert1,vert2):
    n = len(vert1.attached_faces)
    for i in range(n):
        if (vert1.attached_faces[i] in vert2.attached_faces):
            if (vert1.attached_face[1].flag == Flag.Free):
                return vert1.attached_faces[i]
    return 0
"""
def getAdjacentFace(face, vert1, vert2):
    """
    Renvoie la face adjacente à face par l'edge [vert1, vert2]
    :param [in] face: face dont on veut connaitre la face adjacente
    :param [in] vert1 et vert2: vertex constituant l'edge d'adjacence

    :return: la face adjacente si elle existe, None sinon.
    """
    for f in vert1.attached_faces:
        if f in vert2.attached_faces and f.id != face.id:
            return f
    return None

def getThirdVertex(face, vert1, vert2):
    """
    Renvoie le 3e vertex d'une face.
    :param face:  face de travail
    :param vert1 et vert2: vertices connus

    :return: le 3e vertices de la face
    """
    for i in range(3):
        aux_vert = face.vertices[i]
        if (aux_vert!= vert1 and aux_vert!= vert2):
            return aux_vert

def isSameFace(face1, face2):
    is_same = True
    for v in face1.vertices:
        is_same &= v.id in [vert.id for vert in face2.vertices]
    return is_same

def resetFlagTagParam(faces, vertices):
        """
        Remet à zeros les Flag et Tag de l'ensemble des vertex et des faces.
        """
        for face in faces:
            face.flag = Flag.Free
        for vertex in vertices:
            vertex.flag = Flag.Free
            vertex.tag = None

def checkAlreadyEdged(v1,v2,faces):
    """
    Vérifie si deux vertices sont déjà liés par une face
    """
    contained_in_faces = [f for f in faces if v1 in f.vertices and v2 in f.vertices]
    # s=""
    # for f in contained_in_faces:
    #     s += f"{[v.id for v in f.vertices]}\n"
    # if len(contained_in_faces) > 0:
    #     raise Exception(f"    v1:{v1.id} v2:{v2.id} contained faces: {s}")
    return len(contained_in_faces) > 0

def canBeDecimated(entry_gate, faces, breaking_manifold):
    """
    checks the manifold condition for the decimation of a patch
    """
    breaking_manifold = False

    front_face = entry_gate.front_face
    front_vertex = entry_gate.getFrontVertex()
    valence = front_vertex.getValence()

    is_valid = True

    if not front_vertex.isOnTheBoundary():
        try:
            patch = Patch(0,entry_gate, False)
        except:
            print(f"    Error: Patch creation failed")
            breaking_manifold = True
            return False

        patch_bounding_vertices = patch.bounding_vertices[:]

        [vertex1,vertex2] = entry_gate.vertices[:]

        match valence :
            case 3 :
                new_face = Face(getNextElementIndex(faces), Flag.Conquered,patch_bounding_vertices)

                matching_faces = [f for f in faces if isSameFace(f, new_face)]

                is_valid = len(matching_faces) == 0
            case 4 :
                vertex4 = patch_bounding_vertices.pop()
                vertex3 = patch_bounding_vertices.pop()
                match vertex2.tag:
                    case Tag.Minus:
                        is_valid = not checkAlreadyEdged(vertex1, vertex3,faces)

                    case Tag.Plus:
                        is_valid = not checkAlreadyEdged(vertex2, vertex4,faces)
                    case _ :
                        raise Exception(f"    Error : Tag incorecte tag vert2 {vertex2.tag} ---------------------------------")
            case 5 :
                vertex5 = patch_bounding_vertices.pop()
                vertex4 = patch_bounding_vertices.pop()
                vertex3 = patch_bounding_vertices.pop()
                match vertex1.tag, vertex2.tag:
                    case _,Tag.Minus:
                        is_valid = not checkAlreadyEdged(vertex1, vertex3,faces)
                        is_valid &= not checkAlreadyEdged(vertex3, vertex5,faces)

                    case Tag.Minus,Tag.Plus:
                        is_valid = not checkAlreadyEdged(vertex2, vertex5,faces)
                        is_valid &= not checkAlreadyEdged(vertex3, vertex5,faces)

                    case Tag.Plus,Tag.Plus:
                        is_valid = not checkAlreadyEdged(vertex1, vertex4,faces)
                        is_valid &= not checkAlreadyEdged(vertex2, vertex4,faces)

                    case _ :
                        raise Exception(f"    Error : Tag incorecte tag vert1 {vertex1.tag} vert2 {vertex2.tag} ---------------------------------")
            case 6 :
                vertex6 = patch_bounding_vertices.pop()
                vertex5 = patch_bounding_vertices.pop()
                vertex4 = patch_bounding_vertices.pop()
                vertex3 = patch_bounding_vertices.pop()
                match vertex2.tag:
                    case Tag.Minus:
                        is_valid = not checkAlreadyEdged(vertex1, vertex3,faces)
                        is_valid &= not checkAlreadyEdged(vertex3, vertex5,faces)
                        is_valid &= not checkAlreadyEdged(vertex5, vertex1,faces)

                    case Tag.Plus:
                        is_valid = not checkAlreadyEdged(vertex2, vertex4,faces)
                        is_valid &= not checkAlreadyEdged(vertex4, vertex6,faces)
                        is_valid &= not checkAlreadyEdged(vertex2, vertex6,faces)

                    case _ :
                        raise Exception(f"    Error : Tag incorecte tag vert2 {vertex2.tag} ---------------------------------")
            case _ :
                raise Exception(f"    Error : valence: {valence}")
                return False
    return is_valid

def createOutputModel(operations, outputFile, isObj = False, random_color = False):
    """
    Écrit dans le fichier de sortie les instructions obja

    :param [in] operations: liste des operations effectuées durant la compression/decompression.
    :param [in/out] outputFile: Fichier dans lequel sont écritent les instructions obja
    :param [in] isObj: booléen permettant de créer un fichier .obj afin de l'afficher dans Blender
    """

    #  Write the result in output file
    output_model = obja.Output(outputFile, random_color)
    for (ty, index, value) in operations:
        match isObj, ty:
            case _, "vertex":
                output_model.add_vertex(index, value)
            case _,"face":
                output_model.add_face(index, value)
            case False, "delete_face":
                output_model.delete_face(index)

    return output_model

def addMeshToOperations(operations, vertices, faces):
    # Iterate through the vertex
    for (_, vertex) in enumerate(vertices):
        #print(f"Adding vertex {vertex.id} to obja: {vertex.x} {vertex.y} {vertex.z}")
        operations.append(('vertex', vertex.id, np.array([vertex.x,vertex.y,vertex.z], np.double)))

    # Iterate through the faces
    for (_, face) in enumerate(faces):
        #print(f"Adding face {face.id} to obja: vertices {[v.id for v in face.vertices]}")
        operations.append(('face', face.id, obja.Face(face.vertices[0].id,
                                                      face.vertices[1].id,
                                                      face.vertices[2].id,True)))
