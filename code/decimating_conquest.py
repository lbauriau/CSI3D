from pickle import TRUE
from decimateur_utils import *
from retriangulation import *

def decimating_conquest(vertices, faces):
    print("________ Decimation ________")
    patch_id = 0
    

    fifo_gate = []

    output = []
    frenet_coordinates = []

    removed_vertex_indices = []
    
    first_gate = getFirstGate(faces)
    gate_vertices = first_gate.vertices
    gate_vertices[0].tag = Tag.Plus
    gate_vertices[1].tag = Tag.Minus

    fifo_gate.append(first_gate)
    i = 0
    while fifo_gate != []:
        entry_gate = fifo_gate[0]
        print(f"    current gate = {[v.id for v in entry_gate.vertices]}, front face = {entry_gate.front_face.id}, front vertex = {entry_gate.getFrontVertex().id}")
        
        front_face = entry_gate.front_face
        front_vertex = entry_gate.getFrontVertex()
        valence = front_vertex.getValence()

        if (front_face.flag == Flag.Conquered) or (front_face.flag == Flag.ToBeRemoved):
            print(f"    x Patch already computed flag:({front_face.flag})")
            # Nothing to do, patch we enter has already been or cannot be conquered
            # We discard the current gate
            fifo_gate.pop(0)
        elif (front_vertex.flag == Flag.Free) and (valence <= 6) and not front_vertex.isOnTheBoundary() and canBeDecimated(entry_gate, faces):
            print(f"    V Patch to decim found (front_vertex valence = {valence}, len(front_vertex.attached_faces) = {len(front_vertex.attached_faces)})")
            # The corresponding patch will be decimated and retriangulated
            patch = Patch(patch_id, entry_gate, False)

            # The front vertex is flagged ToBeRemoved
            front_vertex.flag = Flag.ToBeRemoved
            removed_vertex_indices.append(front_vertex.id)
            incident_faces = front_vertex.attached_faces
            valence = valence

            # Its neighboring vertices are flagged Conquered
            neighboring_vertices = patch.bounding_vertices
            for neighbor_vertex in neighboring_vertices:
                neighbor_vertex.flag = Flag.Conquered
                
            
            # And its incident faces are flagged ToBeRemoved
            for face in incident_faces:
                face.flag = Flag.ToBeRemoved

            # Tag bounding vertices of the patch
            patch.setTags()

            # The symbol v corresponding to the valence of the removed vertex is output, 
            output.append(valence)

            # Approximating Frenet coordinates
            frenet = patch.getFrenetCoordinates(front_vertex)
            frenet_coordinates.append(frenet)
            
            # And the v-1 output gates are generated and pushed to the fifo queue
            output_gates = patch.getOutputGates()

            removedVertex(patch, vertices, faces)

            fifo_gate += output_gates
            fifo_gate.pop(0)

            if i == 0:
                face = next(f for f in faces if entry_gate.vertices[0] in f.vertices
                                            and entry_gate.vertices[1] in f.vertices
                                            and f.vertices[0] in patch.bounding_vertices
                                            and f.vertices[1] in patch.bounding_vertices
                                            and f.vertices[2] in patch.bounding_vertices)
                first_gate_third_index = next(v.id for v in face.vertices if v.id != entry_gate.vertices[0].id
                                                                          and v.id != entry_gate.vertices[1].id)

        elif ((front_vertex.flag == Flag.Free) and (valence > 6)) or (front_vertex.flag == Flag.Conquered) or front_vertex.isOnTheBoundary() or not canBeDecimated(entry_gate, faces):
            # The front face must be a null patch; we declare it conquered,
            front_face.flag = Flag.Conquered

            if ((entry_gate.vertices[0].tag == Tag.Plus) and (entry_gate.vertices[1].tag == Tag.Plus)):
                front_vertex.tag = Tag.Minus
            else:
                front_vertex.tag = Tag.Plus

            print(f"    O Null patch found (front_vertex valence = {valence}, len(front_vertex.attached_faces) = {len(front_vertex.attached_faces)})")

            # A code null patch is generated. Not mandatory see 4.2 section
            output.append(0)

            # And the two other output gates of the triangle are pushed onto the fifo queue
            patch = Patch(patch_id, entry_gate, True)
            output_gates = patch.getOutputGates()
            fifo_gate += output_gates

            #  We discard the current gate, and proceed to the next gate available on the fifo queue
            fifo_gate.pop(0)

            if i == 0:
                first_gate_third_index = patch.bounding_vertices[2].id

        if len(fifo_gate) > 0:
            print("")
        i += 1


    print("________ Fin Decimation ________")
    print("")
    first_gate_idx = [first_gate.vertices[0].id, first_gate.vertices[1].id, first_gate_third_index]
    return output, first_gate_idx, frenet_coordinates, removed_vertex_indices

    





