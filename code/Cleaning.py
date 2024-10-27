import decimateur_utils

def cleaningConquest(vertices, faces):
    
    firstGate = decimateur_utils.getFirstGate(faces)
    
    fifo = [firstGate]
    
    #Tant qu'il y en a on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        
        #On cr�e une instance de l'objet patch � l'aide de la gate trait�e
        current_patch = decimateur_utils.Patch(0,current_gate)
        
        #On r�cup�re les portes de sorties li�es � ce patch
        outputGates = current_patch.getOutputGates()
        
        #On ajoute les portes de sorties � la fifo
        fifo += outputGates
        
        #On d�cime le patch seulement si il est de valence 3
        if(current_patch.getValence() == 3):
            print("Toto")
            
        #On enl�ve la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")
        
