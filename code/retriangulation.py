from decimateur_utils import *


def retriangulation_conquest(vertices, faces, listPatchBeRemoved):
    print("________ Retriangulation ________")
    while (listPatchBeRemoved !=[]):
        patchRemoved = listPatchBeRemoved.pop(0)
        removedVertex(patchRemoved,vertices,faces)
        if len(listPatchBeRemoved) > 0:
            print("")
    print("________ Fin Retriangulation ________")
    print("")
    return 1



def removedVertex(patchToRemove,vertices, faces):

    print(f"    Computing patch with center vertex {patchToRemove.center_vertex.id} (valence {patchToRemove.getValence()}).")# Available faces: {[f.id for f in faces]}")

    patchBoundingVertices = patchToRemove.boundingVertices
    
    # On récupère le vertex à enlever ainsi que ces faces attachées
    vertexToRemove = patchToRemove.center_vertex
    attachedFacesToRemove = vertexToRemove.attachedFaces

    print(f"    faces to remove {[f.id for f in attachedFacesToRemove]}")

    
    # On récupère la valence du vertex centrale pour pouvoir retrianguler
    valence = patchToRemove.getValence()
    
    # On récupère la face d'entrée pour faire correctement le flag
    entryGate = patchToRemove.entry_gate
    [vertex1,vertex2] = entryGate.vertices
    flag1 = vertex1.flag
    flag2 = vertex2.flag

    match valence :
        case 3 :
            print(f"        case {valence}")
            newFace = Face(getNextElementIndex(faces), Flag.Conquered,patchBoundingVertices)
            print(f"        New faces {[v.id for v in newFace.vertices]}")
            faces.append(newFace)
            for vertex in patchBoundingVertices:
                vertex.attachedFaces.append(newFace)
        case 4 :
            print(f"        case {valence}")
            vertex4 = patchBoundingVertices.pop()
            vertex3 = patchBoundingVertices.pop()
            match vertex2.tag:
                case Tag.Minus:     
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex3])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex1,vertex3,vertex4])
                    vertex1.attachedFaces += [newFace1, newFace2]
                    vertex2.attachedFaces.append(newFace1)
                    vertex3.attachedFaces += [newFace1, newFace2]
                    vertex4.attachedFaces.append(newFace2)
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]}")
                    faces += [newFace1,newFace2]
                case Tag.Plus:          
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex4])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex4])
                    vertex1.attachedFaces.append(newFace1)
                    vertex2.attachedFaces += [newFace1, newFace2]
                    vertex3.attachedFaces.append(newFace2)
                    vertex4.attachedFaces += [newFace1, newFace2]
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]}")
                    faces += [newFace1,newFace2]
                case _ :
                    print(f"    Error : Tag incorecte tag vert2 {vertex2.tag} ---------------------------------")
        case 5 :
            print(f"        case {valence}")
            vertex5 = patchBoundingVertices.pop()
            vertex4 = patchBoundingVertices.pop()
            vertex3 = patchBoundingVertices.pop()
            match vertex1.tag, vertex2.tag:
                case _,Tag.Minus:
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex3])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex1,vertex3,vertex5])
                    newFace3 = Face(next_face_id + 2, Flag.Conquered,[vertex3,vertex4,vertex5])
                    vertex1.attachedFaces += [newFace1, newFace2]
                    vertex2.attachedFaces.append(newFace1)
                    vertex3.attachedFaces += [newFace1, newFace2, newFace3]
                    vertex4.attachedFaces.append(newFace3)
                    vertex5.attachedFaces += [newFace2, newFace3]
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]} f3: {[v.id for v in newFace3.vertices]}")
                    faces += [newFace1,newFace2, newFace3]
                case Tag.Minus,Tag.Plus:
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex5])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex5])
                    newFace3 = Face(next_face_id + 2, Flag.Conquered,[vertex3,vertex4,vertex5])
                    vertex1.attachedFaces.append(newFace1) 
                    vertex2.attachedFaces += [newFace1, newFace2]
                    vertex3.attachedFaces += [newFace2, newFace3]
                    vertex4.attachedFaces.append(newFace3)
                    vertex5.attachedFaces += [newFace1, newFace2, newFace3]
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]} f3: {[v.id for v in newFace3.vertices]}")
                    faces += [newFace1,newFace2, newFace3]
                case Tag.Plus,Tag.Plus:
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex4])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex4])
                    newFace3 = Face(next_face_id + 2, Flag.Conquered,[vertex1,vertex4,vertex5])
                    vertex1.attachedFaces += [newFace1, newFace3]
                    vertex2.attachedFaces += [newFace1, newFace2]
                    vertex3.attachedFaces.append(newFace2)
                    vertex4.attachedFaces += [newFace1, newFace2, newFace3]
                    vertex5.attachedFaces.append(newFace3)
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]} f3: {[v.id for v in newFace3.vertices]}")
                    faces += [newFace1,newFace2, newFace3]
                case _ :
                    print(f"    Error : Tag incorecte tag vert1 {vertex1.tag} vert2 {vertex2.tag} ---------------------------------")
        case 6 :
            print(f"        case {valence}")
            vertex6 = patchBoundingVertices.pop()
            vertex5 = patchBoundingVertices.pop()
            vertex4 = patchBoundingVertices.pop()
            vertex3 = patchBoundingVertices.pop()
            match vertex2.tag:
                case Tag.Minus:
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex3])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex3,vertex4,vertex5])
                    newFace3 = Face(next_face_id + 2, Flag.Conquered,[vertex1,vertex5,vertex6])
                    newFace4 = Face(next_face_id + 3, Flag.Conquered,[vertex1,vertex3,vertex5])
                    vertex1.attachedFaces += [newFace1, newFace3, newFace4]
                    vertex2.attachedFaces.append(newFace1)
                    vertex3.attachedFaces += [newFace1, newFace2, newFace4]
                    vertex4.attachedFaces.append(newFace2) 
                    vertex5.attachedFaces += [newFace2, newFace3, newFace4]
                    vertex6.attachedFaces.append(newFace3)
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]} f3: {[v.id for v in newFace3.vertices]} f4: {[v.id for v in newFace4.vertices]}")
                    faces += [newFace1,newFace2, newFace3, newFace4]
                case Tag.Plus:
                    next_face_id = getNextElementIndex(faces)

                    newFace1 = Face(next_face_id, Flag.Conquered,[vertex1,vertex2,vertex6])
                    newFace2 = Face(next_face_id + 1, Flag.Conquered,[vertex2,vertex3,vertex4])
                    newFace3 = Face(next_face_id + 2, Flag.Conquered,[vertex4,vertex5,vertex6])
                    newFace4 = Face(next_face_id + 3, Flag.Conquered,[vertex2,vertex4,vertex6])
                    vertex1.attachedFaces.append(newFace1) 
                    vertex2.attachedFaces += [newFace1, newFace2, newFace4]
                    vertex3.attachedFaces.append(newFace2)  
                    vertex4.attachedFaces += [newFace2, newFace3, newFace4]
                    vertex5.attachedFaces.append(newFace3) 
                    vertex6.attachedFaces += [newFace1, newFace3, newFace4]
                    print(f"        New faces f1: {[v.id for v in newFace1.vertices]} f2: {[v.id for v in newFace2.vertices]} f3: {[v.id for v in newFace3.vertices]} f4: {[v.id for v in newFace4.vertices]}")
                    faces += [newFace1,newFace2, newFace3, newFace4]
                case _ :
                    print(f"    Error : Tag incorecte tag vert2 {vertex2.tag} ---------------------------------")
        case _ :
                print("    Error : ce cas n'est possible.")
            
    # On enlève les faces attachées au vertex dans la liste de toutes les faces
    while attachedFacesToRemove:
        face = attachedFacesToRemove.pop(0)
        if face in faces:
            faces.remove(face)
            print(f"        removed face {face.id} from main list")
        for vertex in face.vertices: 
            if face in vertex.attachedFaces:
                vertex.attachedFaces.remove(face)
                print(f"        removed face {face.id} from vertex {vertex.id} attached faces")
    
    # On enlève le vertex de la liste des vertex
    vertices.remove(vertexToRemove)
