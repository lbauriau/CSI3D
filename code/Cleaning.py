# coding: iso-8859-1 -*-

import decimateur_utils
import func_init

def cleaningConquest(vertices, faces):
    
    firstGate = decimateur_utils.getFirstGate(faces)
    
    fifo = [firstGate]
    
    #Tant qu'il y en a on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        print("________ New patch ________")
        print(f"current gate vertices: {[v.id for v in current_gate.vertices]} front face id:{current_gate.frontFace.id}")
        
        #On cr�e une instance de l'objet patch � l'aide de la gate trait�e
        current_patch = decimateur_utils.Patch(0,current_gate)
        
        print(f"current patch center vertex:{current_patch.center_vertex.id} valence: {current_patch.getValence()}")
        
        #On r�cup�re les portes de sorties li�es � ce patch
        outputGates = current_patch.getOutputGates()
        print(f"-> GetOutputGates: {outputGates}")
        
        #On ajoute les portes de sorties � la fifo
        fifo += outputGates
        
        #On d�cime le patch seulement si il est de valence 3
        if(current_patch.getValence() < 6):
            print(f"patch en traitement")
            
        #On enl�ve la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")
        
#(v,f) = func_init.initialize('../TestModels/3ValenceShape.obj')
(v,f) = func_init.initialize('../TestModels/TestCleaningSimple.obj')
decimateur_utils.printVertsAndFaces(v,f)
cleaningConquest(v,f)