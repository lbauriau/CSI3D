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
                if vertex in f.vertices and self.center_vertex in f.vertices:
                    return f
            return None

        self.boundingVertices += self.entry_gate.vertices

        faceslist = self.center_vertex.attachedFaces
        faceslist.remove(self.entry_gate.frontFace)
        current_vertex = self.entry_gate.vertices[1]

        while faceslist:
            print( "___________ Nouveau tour de boucle ______________")
            print("")
            print(f"Current vertex id:{current_vertex.id}")
            face = findnextface(faceslist, current_vertex)
            print(f"faceslist:{[f.id for f in faceslist]}")
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
                    
    def getValence(self):
        #La valence d'un patch est en réalité la valence du vertex central, et
        #cette dernière correspond au nombre de faces liées à ce vertex
        return len(self.center_vertex.attachedFaces)

    #Retourne une liste ordonnée des output gates
    def getOutputGates(self):
        output_gates = []
        
        #On traite chaque vertex les uns à la suite des autres. Chaque vertex est potentiellement attaché à 2 
        #output gates. On garde donc en mémoire les deux derniers points traités pour éviter les redondances.
        #On procède de manière circulaire en partant du coté "droit" de la gate d'entrée et en finissant du 
        #coté "gauche" de cette dernière.
        previous_vertex = self.entry_gate.vertices[0]
        current_vertex = self.entry_gate.vertices[1]
        print(f"gate verts index:{previous_vertex.id}, {current_vertex.id}")
        print(f"patch bounding verts idx:{[v.id for v in self.boundingVertices]}")
        
        for i in range(len(self.boundingVertices)):
            print("")
            print(f"Current vertex id:{current_vertex.id}")
            #On cherche maintenant à trouver à quel vertex parmis la liste des bounding vertex
            #le current vertex est attaché (ormis le previous_vertex car ce couple à déjà été traité)

            #Pour cela, on trouve la face connectée au current_vertex qui contient le center_vertex mais pas
            #le previous vertex. En effet, cette face donne accès au next_vertex
            print(f"prev vert id: {previous_vertex.id}")
            print(f"self.center_vertex id: {self.center_vertex.id}")
            next_interior_face = [f for f in current_vertex.attachedFaces if
                              self.center_vertex in f.vertices and
                              previous_vertex not in f.vertices]
            print(f"current_vertex attachedFaces ids:{[f.id for f in current_vertex.attachedFaces]}")
            for f in current_vertex.attachedFaces:
                print(f"   face {f.id} attached verts: {[v.id for v in f.vertices]}")
            print(f"[f for f in current_vertex.attachedFaces if self.center_vertex in f.vertices and previous_vertex not in f.vertices]:{[f.id for f in current_vertex.attachedFaces if
                              self.center_vertex in f.vertices]}")
            print(f"[f for f in current_vertex.attachedFaces if self.center_vertex in f.vertices and previous_vertex not in f.vertices]:{[f.id for f in current_vertex.attachedFaces if
                              previous_vertex not in f.vertices]}")
            print(f"next_interior_face ids:{[f.id for f in next_interior_face]}")
            
            #Si on ne trouve pas de face répondant aux contriantes on ne trouvera pas d'output gate pour le
            #current vertex
            if(len(next_interior_face) != 0):
                next_interior_face = next_interior_face[0]
            
                next_vertex = [v for v in next_interior_face.vertices if v != current_vertex and v != self.center_vertex][0]
            
                #On récupère maintenant la face exterieure au patch liant current_vertex avec next_vertex.
                #Elle dois contenir ces deux derniers vertex mais pas le center_vertex
                next_outside_face = [f for f in current_vertex.attachedFaces if
                                next_vertex in f.vertices and
                                self.center_vertex not in f.vertices]
            
                #Si on ne trouve pas de face répondant aux contriantes on ne trouvera pas d'output gate pour le
                #current vertex (c'est possible qu'il n'existe pas de faces en dehors du patch)
                if(len(next_outside_face) != 0):
                    next_outside_face = next_outside_face[0]
            
                    #On vérifie que la gate n'est pas déjà dans la liste output_gates. Pour cela, on vérifie que
                    #la next_outside_face n'est pas déjà renseignée par une des gates de la liste output_gates
                    if len([g for g in output_gates if g.frontFace == next_outside_face]) == 0:
                        #On ajoute la nouvelle gate aux output_gates
                        output_gates.append(Gate(next_outside_face, [current_vertex, next_vertex]))

                
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
    random_face = faces[0]
    
    #On récupère le premier vertex de la face
    first_vertex = random_face.vertices[1]
    
    #On récupère le deuxième vertex de la face
    second_vertex = random_face.vertices[2]
    
    return Gate(random_face, [first_vertex, second_vertex])


    





        
    

