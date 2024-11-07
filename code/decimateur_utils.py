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

    def __init__(self, id, attachedFaces, flag, tag, x, y, z):
        self.id = id
        self.flag = flag
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.attachedFaces = attachedFaces

class Patch:

    def __init__(self, id, entry_gate):

        self.id = id
        self.entry_gate = entry_gate
        self.center_vertex = entry_gate.getFrontVertex()
        self.boundingVertices = []

        def findnextface(listfaces, vertex):
            for f in listfaces:
                print(f"verts:{[v.id for v in f.vertices]}")
                if vertex in f.vertices and self.center_vertex in f.vertices:
                    return f
            return None

        self.boundingVertices += self.entry_gate.vertices

        faceslist = self.center_vertex.attachedFaces[:]
        faceslist.remove(self.entry_gate.frontFace)
        current_vertex = self.entry_gate.vertices[1]

        print("")
        print( "Triage des bounding vertex...")
        while faceslist:
            print( "___________ Nouveau tour de boucle ______________")
            print("")
            print(f"Current vertex id:{current_vertex.id}")
            print(f"faceslist:{[f.id for f in faceslist]}")
            face = findnextface(faceslist, current_vertex)
            print(f"current_faces:{face.id}")
            if face is not None:
                for v in face.vertices:
                    if v not in self.boundingVertices and v!= self.center_vertex:
                        print (f"v.id :{v.id}")
                        print (f"self.center_vertex.id :{self.center_vertex.id}")
                        self.boundingVertices.append(v)

                current_vertex = self.boundingVertices[-1]
                print (f"new current_vertex.id :{current_vertex.id}")
                print("")
                faceslist.remove(face)
        print(f"bounding verts = {[v.id for v in self.boundingVertices]}")
        print("")
                    
    def getValence(self):
        #La valence d'un patch est en réalité la valence du vertex central, et
        #cette dernière correspond au nombre de faces liées à ce vertex
        return len(self.center_vertex.attachedFaces)

    #Retourne une liste ordonnée des output gates
    def getOutputGates(self):
        output_gates = []
        
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
                output_gates.append(Gate(next_outside_face, [next_vertex, current_vertex]))
            current_vertex = next_vertex
                
        return output_gates
        
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
    random_face = faces[5]
    
    #On récupère le premier vertex de la face
    first_vertex = random_face.vertices[1]
    
    #On récupère le deuxième vertex de la face
    second_vertex = random_face.vertices[2]
    
    return Gate(random_face, [first_vertex, second_vertex])


    





        
    

