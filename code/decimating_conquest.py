from decimateur_utils import *

def decimating_conquest(vertices, faces):
    patchId = 0
    patchs = []
    patchsBeRemoved = []
    

    fifoGate = []

    output = []
    frenetCoordinates = []
    
    firstGate = getFirstGate(faces)
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
        elif (frontVertex.flag == Flag.Free) and (frontVertex.getValence() <= 6) and frontVertex.getValence() == len(frontVertex.attachedFaces):
            # The corresponding patch will be decimated and retriangulated
            patch = Patch(patchId, entryGate, False)
            patchs.append(patch)
            patchsBeRemoved.append(patch)

            # The front vertex is flagged ToBeRemoved
            frontVertex.flag = Flag.ToBeRemoved
            incidentFaces = frontVertex.attachedFaces
            valence = len(incidentFaces)
            print(f"front vertex = {frontVertex.id}")
            print(f"valence = {valence}")

            # Its neighboring vertices are flagged Conquered
            neighboringVertices = patch.boundingVertices
            for neighborVertex in neighboringVertices:
                neighborVertex.flag = Flag.Conquered
                
            
            # And its incident faces are flagged ToBeRemoved
            for face in incidentFaces:
                face.flag = Flag.ToBeRemoved

            # Tag bounding vertices of the patch
            gateVertices = entryGate.vertices
            i = 0
            for nv in neighboringVertices:
                if nv not in gateVertices:
                    if (nv.tag == None):
                        match valence:
                            case 3:
                                if ((gateVertices[0].tag == Tag.Plus) and (gateVertices[1].tag == Tag.Plus)):
                                    nv.tag = Tag.Minus
                                else:
                                    nv.tag = Tag.Plus
                            case 4:
                                if ((gateVertices[0].tag == Tag.Minus) and (gateVertices[1].tag == Tag.Plus) or ((gateVertices[0].tag == Tag.Plus) and (gateVertices[1].tag == Tag.Plus))) :
                                    if i%2:
                                        nv.tag = Tag.Minus
                                    else:
                                        nv.tag = Tag.Plus
                                else: 
                                    if i%2:
                                        nv.tag = Tag.Plus
                                    else:
                                        nv.tag = Tag.Minus
                            case 5:
                                if ((gateVertices[0].tag == Tag.Plus) and (gateVertices[1].tag == Tag.Plus)) :
                                    if i%2:
                                        nv.tag = Tag.Minus
                                    else:
                                        nv.tag = Tag.Plus
                                else: 
                                    if i%2:
                                        nv.tag = Tag.Plus
                                    else:
                                        nv.tag = Tag.Minus
                            case 6:
                                if ((gateVertices[0].tag == Tag.Minus) and (gateVertices[1].tag == Tag.Plus) or ((gateVertices[0].tag == Tag.Plus) and (gateVertices[1].tag == Tag.Plus))) :
                                    if i%2:
                                        nv.tag = Tag.Minus
                                    else:
                                        nv.tag = Tag.Plus
                                else: 
                                    if i%2:
                                        nv.tag = Tag.Plus
                                    else:
                                        nv.tag = Tag.Minus
                            case _:
                                pass 
                    i +=1

            # The symbol v corresponding to the valence of the removed vertex is output, 
            output.append(valence)

            # Approximating Frenet coordinates
            frenet = patch.getFrenetCoordinates(frontVertex)
            frenetCoordinates.append(frenet)
            
            # And the v-1 output gates are generated and pushed to the fifo queue
            outputGates = patch.getOutputGates()
            fifoGate += outputGates
            fifoGate.pop(0)

        elif ((frontVertex.flag == Flag.Free) and (frontVertex.getValence() > 6)) or (frontVertex.flag == Flag.Conquered) or frontVertex.getValence() != len(frontVertex.attachedFaces):
            # The front face must be a null patch; we declare it conquered,
            frontFace.flag = Flag.Conquered

            print("Null patch found")

            # A code null patch is generated. Not mandatory see 4.2 section
            # output.append(0)

            # And the two other output gates of the triangle are pushed onto the fifo queue
            patch = Patch(patchId, entryGate, True)
            patchs.append(patch)
            outputGates = patch.getOutputGates()
            fifoGate += outputGates

            #  We discard the current gate, and proceed to the next gate available on the fifo queue
            fifoGate.pop(0)



    return patchsBeRemoved, output, firstGate




