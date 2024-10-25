import decimateur_utils

def cleaningConquest(vertices, faces):
    
    firstGate = decimateur_utils.getFirstGate(faces)
    
    fifo = [firstGate]
    
    #Tant qu'il y en a on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        current_patch = decimateur_utils.Patch(0,current_gate)
        outputGates = current_patch.getOutputGates()
        fifo += outputGates
        
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")