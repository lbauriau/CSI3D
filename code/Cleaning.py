# coding: iso-8859-1 -*-

from decimateur_utils import *
import func_init

def cleaningConquest(vertices, faces):
    print("")
    print("________ Cleaning ________")
    bn = []
    fren_coord = []
    removed_vertex_indices = []

    first_gate = getFirstGate(faces)
    fifo = [first_gate]

    print(f"first gate: {[v.id for v in first_gate.vertices]}")
    
    i = 0
    #Tant qu'il y en a, on traite les gates de la fifo
    while len(fifo) > 0:
        # print(f"valence {bn}")
        current_gate = fifo[0]
        front_face = current_gate.front_face
        front_vertex = current_gate.getFrontVertex()
        valence = front_vertex.getValence()
        print("")
        print("    ________ New patch ________")
        print(f"    current gate vertices: {[v.id for v in current_gate.vertices]} front vert id:{current_gate.getFrontVertex().id} front face id:{current_gate.front_face.id}")

        #On vérifie si le patch a déjà été conquis et si oui, on retire la gate de la fifo.
        if(front_face.flag == Flag.Conquered) or (front_face.flag == Flag.ToBeRemoved) or (front_face not in faces):
            print(f"    Patch has already been conquered")

        elif(front_vertex.flag == Flag.Free) and (valence <= 3) and not front_vertex.isOnTheBoundary():
            breaking_manifold = False
            if canBeDecimated(current_gate, faces, breaking_manifold):
                #On crée une instance de l'objet patch à l'aide de la gate traitee
                current_patch = Patch(0,current_gate, False)
                print(f"    current patch center vertex:{current_patch.center_vertex.id} valence: {current_patch.getValence()}")
                print(f"    Patch is going to be simplified")

                #On traite le patch
                current_patch.center_vertex.flag = Flag.ToBeRemoved #Pas très utile, car on traite le patch ici
                bn.append(current_patch.getValence())
                fren_coord.append(current_patch.getFrenetCoordinates(front_vertex))

                #On récupère les portes de sorties liées à ce patch
                output_gates = current_patch.getOutputGates()
                for eg in output_gates:
                    print(f"    -> Patch exit gate: {[v.id for v in eg.vertices]} f v = {eg.getFrontVertex().id}")

                for v in current_patch.bounding_vertices:
                    v.flag = Flag.Conquered

                #On marque les faces des outputs gates comme étant conquered et on
                #ajoute à la fifo les outputs gates correctes
                for gate in output_gates:
                    gate.front_face.flag = Flag.Conquered
                    gates = Patch(0,gate, True).getOutputGates()
                    print(f"   ____________ Conquered face: {gate.front_face.id} {[v.id for v in gate.front_face.vertices]}")

                    for g in gates:
                        print(f"   ____________ Side face: {g.front_face.id} {[v.id for v in g.front_face.vertices]}")
                        g.getFrontVertex().flag = Flag.Conquered
                    fifo += gates
                    print(f"        -> outputgate added to fifo: {[g for g in gates]}")

                #Suppression des éléments du patch
                while front_vertex.attached_faces:
                    face = front_vertex.attached_faces.pop(0)
                    #On enlève toutes les références aux faces que l'on enlève
                    for v in face.vertices:
                        if face in v.attached_faces:
                            v.attached_faces.remove(face)
                    #On enlève la face de la liste des faces
                    faces.remove(face)

                #On enlève le center vertex de la liste des vertices
                removed_vertex_indices.append(front_vertex.id)
                vertices.remove(front_vertex)
                print(f"    -> Removed vertex: {front_vertex.id}")
                #On ajoute la nouvelle face à la liste des faces
                if(len(current_patch.bounding_vertices) != 3):
                    raise Exception(f"{[v.id for v in current_patch.bounding_vertices]}")
                new_face = Face(getNextElementIndex(faces),Flag.Conquered,current_patch.bounding_vertices)
                for v in current_patch.bounding_vertices:
                    v.attached_faces.append(new_face)
                faces.append(new_face)

                if i == 0:
                    first_gate_third_index = current_patch.bounding_vertices[2].id
            else:
                if breaking_manifold:
                    bn.append(-1)
                    print(f"breaking manifold in cleaning")
                    first_gate_idx = [first_gate.vertices[0].id, first_gate.vertices[1].id, first_gate_third_index]
                    return bn, first_gate_idx, fren_coord, removed_vertex_indices
                print(f"    Valid patch could not be decimated without violating manifold properties")
                current_patch = computeNullPatch(fifo, front_face,current_gate,bn)
                if i == 0:
                    first_gate_third_index = current_patch.bounding_vertices[2].id

        elif((front_vertex.flag == Flag.Free) and (valence > 3)) or front_vertex.flag == Flag.Conquered or front_vertex.isOnTheBoundary() or not canBeDecimated(current_gate, faces):
             current_patch = computeNullPatch(fifo, front_face,current_gate,bn)
             if i == 0:
                first_gate_third_index = current_patch.bounding_vertices[2].id
        else:
            raise Exception("cleaning")
        #On enlève la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        i += 1
        print(f"len(fifo) = {len(fifo)}")

    first_gate_idx = [first_gate.vertices[0].id, first_gate.vertices[1].id, first_gate_third_index]
    return bn, first_gate_idx, fren_coord, removed_vertex_indices
        
def computeNullPatch(fifo, front_face, current_gate,bn):
    for v in current_gate.vertices:
        v.flag = Flag.Conquered
    print(f"    -> null patch found")
    front_face.flag = Flag.Conquered
    current_patch = Patch(0,current_gate, True)
    fifo += current_patch.getOutputGates()
    bn.append(0)

    return current_patch
#(v,f) = func_init.initialize('../TestModels/3ValenceShape.obj')
#(v,f) = func_init.initialize('../TestModels/TestCleaningSimple.obj')
#printVertsAndFaces(v,f)
#cleaningConquest(v,f)