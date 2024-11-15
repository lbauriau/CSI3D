# coding: iso-8859-1 -*-

from decimateur_utils import *
import func_init

def cleaningConquest(vertices, faces):
    bn = []
    FrenCoord = []
    
    firstGate = getFirstGate(faces)
    fifo = [firstGate]
    
    #Tant qu'il y en a on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        print("")
        print("________ New patch ________")
        print(f"current gate vertices: {[v.id for v in current_gate.vertices]} front face id:{current_gate.frontFace.id}")
        
        #On crée une instance de l'objet patch à l'aide de la gate traitée
        current_patch = Patch(0,current_gate)
        
        print(f"current patch center vertex:{current_patch.center_vertex.id} valence: {current_patch.getValence()}")
        
        #On récupère les portes de sorties liées à ce patch
        outputGates = current_patch.getOutputGates()
        print(f"-> GetOutputGates: {outputGates}")
        
        #On vérifie si le patch a déjà été conquis et si oui on retire la gate de la fifo
        if(current_gate.frontFace.flag == Flag.Conquered) or (current_gate.frontFace.flag == Flag.ToBeRemoved):
            print(f"Patch has already been conquered")

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() <= 3):
            #On traite le patch
            current_gate.center_vertex.flag = Flag.ToBeRemoved #Pas très utile car on traite le patch ici
            bn.append(current_patch.getValence())
            FrenCoord.append(current_patch.getFrenetCoordinates())

            for v in current_patch.boundingVertices:
                v.flag = Flag.Conquered

            #On marque les faces des output gates comme étant conquered et on
            #ajoute à la fifo les output gates correctes
            for gate in outputGates:
                gate.frontFace.flag = Flag.Conquered
            for gate in outputGates:
                fifo += Patch(0,gate, True).getOutputGates()

            #Suppression des éléments du patch
            for face in current_patch.center_vertex.attachedFaces:
                #On enlève toutes les références aux faces que l'on enlève
                for v in current_patch.boundingVertices:
                    if face in v.attachedFaces:
                        v.attachedFaces.remove(face)
                #On enlève la face de la liste des faces
                faces.remove(face)
                #On enlève le center vertex de la liste des vertices
                vertices.remove(current_patch.center_vertex)
            #On ajoute la nouvelle face à la liste des faces
            newFace = Face(0,Flag.Conquered,current_patch.boundingVertices)
            faces.append(newFace)

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() > 3) or current_patch.center_vertex.flag == Tag.Conquered:
            current_gate.frontFace.flag == Flag.Conquered
            fifo += Patch(0,current_gate, True).getOutputGates()
            bn.append(0)
            
        #On enlève la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")

        return bn, firstGate
        
#(v,f) = func_init.initialize('../TestModels/3ValenceShape.obj')
(v,f) = func_init.initialize('../TestModels/TestCleaningSimple.obj')
printVertsAndFaces(v,f)
cleaningConquest(v,f)