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

    def __init__(self, id, entry_gate):
        self.id = id
        self.entry_gate = entry_gate
        self.center_vertex = entry_gate.getFrontVertex()
        self.boundingVertices = []
        
        #On rempli la liste boundingVertices � l'aide du center_vertex
        for f in self.center_vertex.attachedFaces:
            for v in f.vertices:
                if v != self.center_vertex and v not in self.boundingVertices:
                    self.boundingVertices.append(v)

    #Retourne une liste ordonn�e des output gates
    def getOutputGates(self):
        output_gates = []
        
        #On traite chaque vertex les uns � la suite des autres. Chaque vertex est potentiellement attach� � 2 
        #output gates. On garde donc en m�moire les deux derniers points trait�s pour �viter les redondances.
        #On proc�de de mani�re circulaire en partant du cot� "droit" de la gate d'entr�e et en finissant du 
        #cot� "gauche" de cette derni�re.
        previous_vertex = self.entry_gate.vertices[0]
        current_vertex = self.entry_gate.vertices[1]
        
        for i in range(len(self.boundingVertices)):
            #On cherche maintenant � trouver � quel vertex parmis la liste des bounding vertex
            #le current vertex est attach� (ormis le previous_vertex car ce couple � d�j� �t� trait�)

            #Pour cela, on trouve la face connect�e au current_vertex qui contient le center_vertex mais pas
            #le previous vertex. En effet, cette face donne acc�s au next_vertex
            next_interior_face = [f for f in current_vertex.attachedFaces if
                              self.center_vertex in f.vertices and
                              previous_vertex not in f.vertices][0]
            
            next_vertex = [v for v in next_interior_face.vertices if v != current_vertex and v != self.center_vertex][0]
            
            #On r�cup�re maintenant la face exterieure au patch liant current_vertex avec next_vertex.
            #Elle dois contenir ces deux derniers vertex mais pas le center_vertex
            next_outside_face = [f for f in current_vertex.attachedFaces if
                            next_vertex in f.vertices and
                            self.center_vertex not in f.vertices][0]
            
            #On v�rifie que la gate n'est pas d�j� dans la liste output_gates. Pour cela, on v�rifie que
            #la next_outside_face n'est pas d�j� renseign�e par une des gates de la liste output_gates
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

def getFirstGate(faces):
    #On choisie la "premi�re" face stock�e dans la liste de faces,
    #mais on pourrait aussi tirer une face au hasard, ce qui
    ##serait un peu plus couteux
    random_face = faces[0]
    
    #On r�cup�re le premier vertex de la face
    first_vertex = random_face.vertices[0]
    
    #On r�cup�re le deuxi�me vertex de la face
    second_vertex = random_face.vertices[1]
    
    return Gate(random_face, [first_vertex, second_vertex])


    





        
    

