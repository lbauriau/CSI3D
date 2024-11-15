# coding: iso-8859-1 -*-

from decimateur_utils import *
import func_init

def cleaningConquest(vertices, faces):
    
    firstGate = getFirstGate(faces)
    
    fifo = [firstGate]

    bn = []
    
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
            current_gate.center_vertex.flag = Flag.ToBeRemoved
            bn.append(current_patch.getValence())
            for v in current_patch.boundingVertices:
                v.flag = Flag.Conquered

            for face in current_patch.center_vertex.attachedFaces:
                face.flag = Flag.ToBeRemoved

            #On marque les faces des output gates comme étant conquered et on
            #ajoute à la fifo les output gates correctes
            for gate in outputGates:
                gate.frontFace.flag = Flag.Conquered
            for gate in outputGates:
                fifo += Patch(0,gate, True).getOutputGates()

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() > 3) or current_patch.center_vertex.flag == Tag.Conquered:
            current_gate.frontFace.flag == Flag.Conquered
            fifo += Patch(0,gate, True).getOutputGates()
            bn.append(0)
            
        #On enlève la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")

        return bn
        
#(v,f) = func_init.initialize('../TestModels/3ValenceShape.obj')
(v,f) = func_init.initialize('../TestModels/TestCleaningSimple.obj')
printVertsAndFaces(v,f)
cleaningConquest(v,f)