# coding: iso-8859-1 -*-

from decimateur_utils import *
import func_init

def cleaningConquest(vertices, faces):
    print("")
    print("________ Cleaning ________")
    bn = []
    FrenCoord = []
    
    firstGate = getFirstGate(faces)
    fifo = [firstGate]

    print(f"first gate: {[v.id for v in firstGate.vertices]}")
    
    #Tant qu'il y en a on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        print("")
        print("    ________ New patch ________")
        print(f"    current gate vertices: {[v.id for v in current_gate.vertices]} front face id:{current_gate.frontFace.id}")
        
        #On cr�e une instance de l'objet patch � l'aide de la gate trait�e
        current_patch = Patch(0,current_gate, False)
        
        print(f"    current patch center vertex:{current_patch.center_vertex.id} valence: {current_patch.getValence()}")
        
        #On v�rifie si le patch a d�j� �t� conquis et si oui on retire la gate de la fifo
        if(current_gate.frontFace.flag == Flag.Conquered) or (current_gate.frontFace.flag == Flag.ToBeRemoved):
            print(f"    Patch has already been conquered")

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() <= 3):
            print(f"    Patch is going to be simplified")

            #On traite le patch
            current_gate.center_vertex.flag = Flag.ToBeRemoved #Pas tr�s utile car on traite le patch ici
            bn.append(current_patch.getValence())
            FrenCoord.append(current_patch.getFrenetCoordinates())

            #On r�cup�re les portes de sorties li�es � ce patch
            outputGates = current_patch.getOutputGates()
            print(f"    -> Patch exit gate: {outputGates}")

            for v in current_patch.boundingVertices:
                v.flag = Flag.Conquered

            #On marque les faces des output gates comme �tant conquered et on
            #ajoute � la fifo les output gates correctes
            for gate in outputGates:
                gate.frontFace.flag = Flag.Conquered
            for gate in outputGates:
                gates = Patch(0,gate, True).getOutputGates()
                fifo += gates
                print(f"        -> outputgate added to fifo: {[g for g in gates]}")

            #Suppression des �l�ments du patch
            for face in current_patch.center_vertex.attachedFaces:
                #On enl�ve toutes les r�f�rences aux faces que l'on enl�ve
                for v in current_patch.boundingVertices:
                    if face in v.attachedFaces:
                        v.attachedFaces.remove(face)
                #On enl�ve la face de la liste des faces
                faces.remove(face)
                #On enl�ve le center vertex de la liste des vertices
                vertices.remove(current_patch.center_vertex)
                print(f"    -> Removed vertex: {current_patch.center_vertex.id}")
            #On ajoute la nouvelle face � la liste des faces
            newFace = Face(0,Flag.Conquered,current_patch.boundingVertices)
            faces.append(newFace)

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() > 3) or current_patch.center_vertex.flag == Tag.Conquered:
            print(f"    -> null patch found")
            current_gate.frontFace.flag == Flag.Conquered
            fifo += Patch(0,current_gate, True).getOutputGates()
            bn.append(0)
            
        #On enl�ve la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")

        return bn, firstGate
        
#(v,f) = func_init.initialize('../TestModels/3ValenceShape.obj')
#(v,f) = func_init.initialize('../TestModels/TestCleaningSimple.obj')
#printVertsAndFaces(v,f)
#cleaningConquest(v,f)