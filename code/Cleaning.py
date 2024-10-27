import decimateur_utils

def cleaningConquest(vertices, faces):
    
    firstGate = decimateur_utils.getFirstGate(faces)
    
    fifo = [firstGate]
    
    #Tant qu'il y en a on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        
        #On crée une instance de l'objet patch à l'aide de la gate traitée
        current_patch = decimateur_utils.Patch(0,current_gate)
        
        #On récupère les portes de sorties liées à ce patch
        outputGates = current_patch.getOutputGates()
        
        #On ajoute les portes de sorties à la fifo
        fifo += outputGates
        
        #On décime le patch seulement si il est de valence 3
        if(current_patch.getValence() == 3):
            print("Toto")
            
        #On enlève la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")
        
