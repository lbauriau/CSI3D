from decimateur_utils import *

def decimating_conquest(vertices, faces):
    patchId = 0
    patchs = []
    patchsBeRemoved = []
    

    fifoGate = []

    output = []
    
    firstGate = getFirstGate(vertices, faces)
    gateVertices = firstGate.vertices
    gateVertices[0].tag = Tag.Plus
    gateVertices[1].tag = Tag.Minus

    fifoGate.append(firstGate)
    while fifoGate != []:
        entryGate = fifoGate[0]
        
        frontFace = entryGate.frontFace
        frontVertex = entryGate.getFrontVertex()
        
        if (frontFace.flag == Flag.Conquered) or (frontFace.flag == Flag.ToBeRemoved):
            # Nothing to do, patch we enter has already been or cannot be conquered
            # We discard the current gate
            fifoGate.pop(0)
        elif (frontVertex.flag == Flag.Free) and (frontVertex.getValence() <= 6):
            # The corresponding patch will be decimated and retriangulated
            patch = Patch(patchId, entryGate)
            patchs.append(patch)
            patchsBeRemoved.append(patch)

            # The front vertex is flagged ToBeRemoved
            frontVertex.flag = Flag.ToBeRemoved
            incidentFaces = frontVertex.attachedFaces
            valence = len(incidentFaces)

            # Its neighboring vertices are flagged Conquered
            neighboringVertices = patch.boundingVertices
            for neighborVertex in neighboringVertices:
                neighborVertex.flag = Flag.Conquered
                
            
            # And its incident faces are flagged ToBeRemoved
            for face in incidentFaces:
                face.flag = Flag.ToBeRemoved

            # Tag bounding vertices of the patch
            gateVertices = entryGate.vertices
            for nv in neighboringVertices:
                if nv not in gateVertices:
                    match valence:
                        case 3:
                            if ((gateVertices[0].tag == Tag.Plus) and (gateVertices[1].tag == Tag.Plus)):
                                nv.tag = Tag.Minus
                            else:
                                nv.tag = Tag.Plus
                        case 4:
                            pass
                        case 5:
                            pass
                        case 6:
                            pass
                        case _:
                            pass 

            # The symbol v corresponding to the valence of the removed vertex is output, 
            output.append(valence)

            # And the v-1 output gates are generated and pushed to the fifo queue
            outputGates = patch.getOutputGates()
            fifoGate += outputGates
            fifoGate.pop(0)

        elif ((frontVertex.flag == Flag.Free) and (frontVertex.getValence() > 6)) or (frontVertex.flag == Flag.Conquered):
            # The front face must be a null patch; we declare it conquered,
            frontFace.flag = Flag.Conquered

            # A code null patch is generated 
            output.append(0)

            # And the two other output gates of the triangle are pushed onto the fifo queue
            patch = Patch(patchId, entryGate)
            patchs.append(patch)
            outputGates = patch.getOutputGates()
            fifoGate += outputGates

            #  We discard the current gate, and proceed to the next gate available on the fifo queue
            fifoGate.pop(0)

    return patchsBeRemoved, output




