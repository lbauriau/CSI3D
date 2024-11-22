from decimateur_utils import *

def decimating_conquest(vertices, faces):
    print("________ Decimation ________")
    patch_id = 0
    patchs = []
    patchs_be_removed = []
    

    fifo_gate = []

    output = []
    frenet_coordinates = []
    
    first_gate = getFirstGate(faces)
    gate_vertices = first_gate.vertices
    gate_vertices[0].tag = Tag.Plus
    gate_vertices[1].tag = Tag.Minus

    fifo_gate.append(first_gate)
    while fifo_gate != []:
        entry_gate = fifo_gate[0]
        print(f"    current gate = {[v.id for v in entry_gate.vertices]}, front face = {entry_gate.front_face.id}, front vertex = {entry_gate.getFrontVertex().id}")
        
        front_face = entry_gate.front_face
        front_vertex = entry_gate.getFrontVertex()

        if (front_face.flag == Flag.Conquered) or (front_face.flag == Flag.ToBeRemoved):
            print(f"    x Patch already computed flag:({front_face.flag})")
            # Nothing to do, patch we enter has already been or cannot be conquered
            # We discard the current gate
            fifo_gate.pop(0)
        elif (front_vertex.flag == Flag.Free) and (front_vertex.getValence() <= 6) and not front_vertex.isOnTheBoundary():
            print(f"    V Patch to decim found (front_vertex valence = {front_vertex.getValence()}, len(front_vertex.attached_faces) = {len(front_vertex.attached_faces)})")
            # The corresponding patch will be decimated and retriangulated
            patch = Patch(patch_id, entry_gate, False, faces)
            patchs.append(patch)
            patchs_be_removed.append(patch)

            # The front vertex is flagged ToBeRemoved
            front_vertex.flag = Flag.ToBeRemoved
            incident_faces = front_vertex.attached_faces
            valence = front_vertex.getValence()

            # Its neighboring vertices are flagged Conquered
            neighboring_vertices = patch.bounding_vertices
            for neighbor_vertex in neighboring_vertices:
                neighbor_vertex.flag = Flag.Conquered
                
            
            # And its incident faces are flagged ToBeRemoved
            for face in incident_faces:
                face.flag = Flag.ToBeRemoved

            # Tag bounding vertices of the patch
            gate_vertices = entry_gate.vertices
            i = 0
            for nv in neighboring_vertices:
                if nv not in gate_vertices:
                    if (nv.tag == None):
                        match valence:
                            case 3:
                                if ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus)):
                                    nv.tag = Tag.Minus
                                else:
                                    nv.tag = Tag.Plus
                            case 4:
                                if ((gate_vertices[0].tag == Tag.Minus) and (gate_vertices[1].tag == Tag.Plus) or ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus))) :
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
                                if ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus)) :
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
                                if ((gate_vertices[0].tag == Tag.Minus) and (gate_vertices[1].tag == Tag.Plus) or ((gate_vertices[0].tag == Tag.Plus) and (gate_vertices[1].tag == Tag.Plus))) :
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
            frenet = patch.getFrenetCoordinates(front_vertex)
            frenet_coordinates.append(frenet)
            
            # And the v-1 output gates are generated and pushed to the fifo queue
            output_gates = patch.getOutputGates()
            fifo_gate += output_gates
            fifo_gate.pop(0)

        elif ((front_vertex.flag == Flag.Free) and (front_vertex.getValence() > 6)) or (front_vertex.flag == Flag.Conquered) or front_vertex.isOnTheBoundary():
            # The front face must be a null patch; we declare it conquered,
            front_face.flag = Flag.Conquered

            if ((entry_gate.vertices[0].tag == Tag.Plus) and (entry_gate.vertices[1].tag == Tag.Plus)):
                front_vertex.tag = Tag.Minus
            else:
                front_vertex.tag = Tag.Plus

            print(f"    O Null patch found (front_vertex valence = {front_vertex.getValence()}, len(front_vertex.attached_faces) = {len(front_vertex.attached_faces)})")

            # A code null patch is generated. Not mandatory see 4.2 section
            # output.append(0)

            # And the two other output gates of the triangle are pushed onto the fifo queue
            patch = Patch(patch_id, entry_gate, True)
            patchs.append(patch)
            output_gates = patch.getOutputGates()
            fifo_gate += output_gates

            #  We discard the current gate, and proceed to the next gate available on the fifo queue
            fifo_gate.pop(0)

        if len(fifo_gate) > 0:
            print("")


    print("________ Fin Decimation ________")
    print("")
    return patchs_be_removed, output, first_gate




