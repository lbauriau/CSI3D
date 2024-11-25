from decimateur_utils import *


def retriangulation_conquest(vertices, faces, list_patch_be_removed):
    print("________ Retriangulation ________")
    while (list_patch_be_removed !=[]):
        patch_removed = list_patch_be_removed.pop(0)
        removedVertex(patch_removed,vertices,faces)
        if len(list_patch_be_removed) > 0:
            print("")
    print("________ Fin Retriangulation ________")
    print("")
    return 1



def removedVertex(patch_to_remove,vertices, faces):

    print(f"    Computing patch with center vertex {patch_to_remove.center_vertex.id} (valence {patch_to_remove.getValence()}).")# Available faces: {[f.id for f in faces]}").

    patch_bounding_vertices = patch_to_remove.bounding_vertices[:]
    
    # On récupère le vertex à enlever ainsi que ces faces attachées
    vertex_to_remove = patch_to_remove.center_vertex
    attached_faces_to_remove = vertex_to_remove.attached_faces

    print(f"    faces to remove {[f.id for f in attached_faces_to_remove]}")

    
    # On récupère la valence du vertex centrale pour pouvoir retrianguler
    valence = patch_to_remove.getValence()
    
    # On récupère la face d'entrée pour faire correctement le flag
    entryGate = patch_to_remove.entry_gate
    [vertex1,vertex2] = entryGate.vertices
    flag1 = vertex1.flag
    flag2 = vertex2.flag

    match valence :
        case 3 :
            print(f"        case {valence}")
            new_face = Face(getNextElementIndex(faces), Flag.Conquered,patch_bounding_vertices)
            print(f"        New faces {[v.id for v in new_face.vertices]}")
            faces.append(new_face)
            for vertex in patch_bounding_vertices:
                vertex.attached_faces.append(new_face)
        case 4 :
            print(f"        case {valence}")
            vertex4 = patch_bounding_vertices.pop()
            vertex3 = patch_bounding_vertices.pop()
            match vertex2.tag:
                case Tag.Minus:     
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex3])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex1,vertex3,vertex4])
                    vertex1.attached_faces += [new_face1, new_face2]
                    vertex2.attached_faces.append(new_face1)
                    vertex3.attached_faces += [new_face1, new_face2]
                    vertex4.attached_faces.append(new_face2)
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]}")
                    faces += [new_face1,new_face2]
                case Tag.Plus:          
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex4])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex4])
                    vertex1.attached_faces.append(new_face1)
                    vertex2.attached_faces += [new_face1, new_face2]
                    vertex3.attached_faces.append(new_face2)
                    vertex4.attached_faces += [new_face1, new_face2]
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]}")
                    faces += [new_face1,new_face2]
                case _ :
                    print(f"    Error : Tag incorecte tag vert2 {vertex2.tag} ---------------------------------")
        case 5 :
            print(f"        case {valence}")
            vertex5 = patch_bounding_vertices.pop()
            vertex4 = patch_bounding_vertices.pop()
            vertex3 = patch_bounding_vertices.pop()
            match vertex1.tag, vertex2.tag:
                case _,Tag.Minus:
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex3])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex1,vertex3,vertex5])
                    new_face3 = Face(next_face_id + 2, Flag.Conquered,[vertex3,vertex4,vertex5])
                    vertex1.attached_faces += [new_face1, new_face2]
                    vertex2.attached_faces.append(new_face1)
                    vertex3.attached_faces += [new_face1, new_face2, new_face3]
                    vertex4.attached_faces.append(new_face3)
                    vertex5.attached_faces += [new_face2, new_face3]
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]} f3: {[v.id for v in new_face3.vertices]}")
                    faces += [new_face1,new_face2, new_face3]
                case Tag.Minus,Tag.Plus:
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex5])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex5])
                    new_face3 = Face(next_face_id + 2, Flag.Conquered,[vertex3,vertex4,vertex5])
                    vertex1.attached_faces.append(new_face1) 
                    vertex2.attached_faces += [new_face1, new_face2]
                    vertex3.attached_faces += [new_face2, new_face3]
                    vertex4.attached_faces.append(new_face3)
                    vertex5.attached_faces += [new_face1, new_face2, new_face3]
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]} f3: {[v.id for v in new_face3.vertices]}")
                    faces += [new_face1,new_face2, new_face3]
                case Tag.Plus,Tag.Plus:
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex4])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex4])
                    new_face3 = Face(next_face_id + 2, Flag.Conquered,[vertex1,vertex4,vertex5])
                    vertex1.attached_faces += [new_face1, new_face3]
                    vertex2.attached_faces += [new_face1, new_face2]
                    vertex3.attached_faces.append(new_face2)
                    vertex4.attached_faces += [new_face1, new_face2, new_face3]
                    vertex5.attached_faces.append(new_face3)
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]} f3: {[v.id for v in new_face3.vertices]}")
                    faces += [new_face1,new_face2, new_face3]
                case _ :
                    print(f"    Error : Tag incorecte tag vert1 {vertex1.tag} vert2 {vertex2.tag} ---------------------------------")
        case 6 :
            print(f"        case {valence}")
            vertex6 = patch_bounding_vertices.pop()
            vertex5 = patch_bounding_vertices.pop()
            vertex4 = patch_bounding_vertices.pop()
            vertex3 = patch_bounding_vertices.pop()
            match vertex2.tag:
                case Tag.Minus:
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex3])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex3,vertex4,vertex5])
                    new_face3 = Face(next_face_id + 2, Flag.Conquered,[vertex1,vertex5,vertex6])
                    new_face4 = Face(next_face_id + 3, Flag.Conquered,[vertex1,vertex3,vertex5])
                    vertex1.attached_faces += [new_face1, new_face3, new_face4]
                    vertex2.attached_faces.append(new_face1)
                    vertex3.attached_faces += [new_face1, new_face2, new_face4]
                    vertex4.attached_faces.append(new_face2) 
                    vertex5.attached_faces += [new_face2, new_face3, new_face4]
                    vertex6.attached_faces.append(new_face3)
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]} f3: {[v.id for v in new_face3.vertices]} f4: {[v.id for v in new_face4.vertices]}")
                    faces += [new_face1,new_face2, new_face3, new_face4]
                case Tag.Plus:
                    next_face_id = getNextElementIndex(faces)

                    new_face1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex6])
                    new_face2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex4])
                    new_face3 = Face(next_face_id + 2, Flag.Conquered,[vertex4,vertex5,vertex6])
                    new_face4 = Face(next_face_id + 3, Flag.Conquered,[vertex2,vertex4,vertex6])
                    vertex1.attached_faces.append(new_face1) 
                    vertex2.attached_faces += [new_face1, new_face2, new_face4]
                    vertex3.attached_faces.append(new_face2)  
                    vertex4.attached_faces += [new_face2, new_face3, new_face4]
                    vertex5.attached_faces.append(new_face3) 
                    vertex6.attached_faces += [new_face1, new_face3, new_face4]
                    print(f"        New faces f1: {[v.id for v in new_face1.vertices]} f2: {[v.id for v in new_face2.vertices]} f3: {[v.id for v in new_face3.vertices]} f4: {[v.id for v in new_face4.vertices]}")
                    faces += [new_face1,new_face2, new_face3, new_face4]
                case _ :
                    print(f"    Error : Tag incorecte tag vert2 {vertex2.tag} ---------------------------------")
        case _ :
                print("    Error : ce cas n'est possible.")
            
    # On enlève les faces attachées au vertex dans la liste de toutes les faces
    while attached_faces_to_remove:
        face = attached_faces_to_remove.pop(0)
        if face in faces:
            faces.remove(face)
            print(f"        removed face {face.id} from main list")
        for vertex in face.vertices: 
            if face in vertex.attached_faces:
                vertex.attached_faces.remove(face)
                print(f"        removed face {face.id} from vertex {vertex.id} attached faces")
    
    # On enlève le vertex de la liste des vertex
    print(f"    removed vertex {vertex_to_remove.id}")
    vertices.remove(vertex_to_remove)
