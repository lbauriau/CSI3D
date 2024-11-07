from decimateur_utils import *


def retriangulation_conquest(vertices, faces, listPatchBeRemoved):
    while (listPatchBeRemoved !=[]):
        patchRemoved = listPatchBeRemoved.pop([0])
        removedVertex(patchRemoved,vertices,faces)
    return 1


def removedVertex(patchToRemoved,vertices, faces):
    vertexPatch = patchToRemoved.boundingVertices
    
    # On récupère le vertex à enlever ainsi que ces faces attachées
    vertexToRemoved = patchToRemoved.center_vertex
    vertexRemovedAttachedFaces = vertexToRemoved.attachedFaces
    
    # On enlève les faces attachées au vertex dans la liste de toutes les faces
    for face in vertexRemovedAttachedFaces:
        faces.remove(face)
        for vertex in vertexPatch : 
            if face in vertex.attachedFaces:
                vertex.attachedFaces.remove(face)
    
    # On enlève le vertex de la liste des vertex
    vertices.remove(vertexToRemoved)
    
    # On récupère la valence du vertex centrale pour pouvoir retrianguler
    valence = patchToRemoved.getValence()
    
    # On récupère la face d'entrée pour faire correctement le flag
    faceEntry = patchToRemoved.entryGate
    [vertex1,vertex2] = faceEntry.vertices
    flag1 = vertex1.flag
    flag2 = vertex2.flag

    match valence :
        case 3 :
            newFace = Face(0,Flag.Conquered,vertexPatch)
            faces.append(newFace)
            for vertex in vertexPatch:
                vertex.attachedFaces.append(newFace)
        case 4 :
            indexVertex1 = vertexPatch.index(vertex1)
            vertex3 = vertexPatch.pop((indexVertex1+2)%4)
            vertex4 = vertexPatch.pop((indexVertex1+3)%4)  
            match vertex2.flag:
                case Tag.Minus:                                                                                                                                                             
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex3])
                    newFace2 = Face(0,Flag.Conquered,[vertex1,vertex3,vertex4])
                    vertex1.attachedFaces += [newFace1, newFace2]
                    vertex2.attachedFaces.append(newFace1)
                    vertex3.attachedFaces += [newFace1, newFace2]
                    vertex4.attachedFaces.append(newFace2)
                    faces += [newFace1,newFace2]
                case Tag.Plus:                                                                                                                                                           
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex4])
                    newFace2 = Face(0,Flag.Conquered,[vertex2,vertex3,vertex4])
                    vertex1.attachedFaces.append(newFace1)
                    vertex2.attachedFaces += [newFace1, newFace2]
                    vertex3.attachedFaces.append(newFace2)
                    vertex4.attachedFaces += [newFace1, newFace2]
                    faces += [newFace1,newFace2]
        case 5 :
            indexVertex1 = vertexPatch.index(vertex1)
            vertex3 = vertexPatch.pop((indexVertex1+2)%5)
            vertex4 = vertexPatch.pop((indexVertex1+3)%5)
            vertex5 = vertexPatch.pop((indexVertex1+4)%5)
            match vertex1.flag, vertex2.flag:
                case _,Tag.Minus:
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex3])
                    newFace2 = Face(0,Flag.Conquered,[vertex1,vertex3,vertex5])
                    newFace3 = Face(0,Flag.Conquered,[vertex3,vertex4,vertex5])
                    vertex1.attachedFaces += [newFace1, newFace2]
                    vertex2.attachedFaces.append(newFace1)
                    vertex3.attachedFaces += [newFace1, newFace2, newFace3]
                    vertex4.attachedFaces.append(newFace3)
                    vertex5.attachedFaces += [newFace2, newFace3]
                    faces += [newFace1,newFace2, newFace3]
                case Tag.Minus,Tag.Plus:
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex5])
                    newFace2 = Face(0,Flag.Conquered,[vertex2,vertex3,vertex5])
                    newFace3 = Face(0,Flag.Conquered,[vertex3,vertex4,vertex5])
                    vertex1.attachedFaces.append(newFace1) 
                    vertex2.attachedFaces += [newFace1, newFace2]
                    vertex3.attachedFaces += [newFace2, newFace3]
                    vertex4.attachedFaces.append(newFace3)
                    vertex5.attachedFaces += [newFace1, newFace2, newFace3]
                    faces += [newFace1,newFace2, newFace3]
                case Tag.Plus,Tag.Plus:
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex4])
                    newFace2 = Face(0,Flag.Conquered,[vertex2,vertex3,vertex4])
                    newFace3 = Face(0,Flag.Conquered,[vertex1,vertex4,vertex5])
                    vertex1.attachedFaces += [newFace1, newFace3]
                    vertex2.attachedFaces += [newFace1, newFace2]
                    vertex3.attachedFaces.append(newFace2)
                    vertex4.attachedFaces += [newFace1, newFace2, newFace3]
                    vertex5.attachedFaces.append(newFace3)
                    faces += [newFace1,newFace2, newFace3]
        case 6 :
            indexVertex1 = vertexPatch.index(vertex1)
            vertex3 = vertexPatch.pop((indexVertex1+2)%6)
            vertex4 = vertexPatch.pop((indexVertex1+3)%6)
            vertex5 = vertexPatch.pop((indexVertex1+4)%6)
            vertex6 = vertexPatch.pop((indexVertex1+5)%6)
            match vertex2.flag:
                case Tag.Minus:
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex3])
                    newFace2 = Face(0,Flag.Conquered,[vertex3,vertex4,vertex5])
                    newFace3 = Face(0,Flag.Conquered,[vertex1,vertex5,vertex6])
                    newFace4 = Face(0,Flag.Conquered,[vertex1,vertex3,vertex5])
                    vertex1.attachedFaces += [newFace1, newFace3, newFace4]
                    vertex2.attachedFaces.append(newFace1)
                    vertex3.attachedFaces += [newFace1, newFace2, newFace4]
                    vertex4.attachedFaces.append(newFace2) 
                    vertex5.attachedFaces += [newFace2, newFace3, newFace4]
                    vertex6.attachedFaces.append(newFace3)
                    faces += [newFace1,newFace2, newFace3, newFace4]
                case Tag.Plus:
                    newFace1 = Face(0,Flag.Conquered,[vertex1,vertex2,vertex6])
                    newFace2 = Face(0,Flag.Conquered,[vertex2,vertex3,vertex4])
                    newFace3 = Face(0,Flag.Conquered,[vertex4,vertex5,vertex6])
                    newFace4 = Face(0,Flag.Conquered,[vertex2,vertex4,vertex6])
                    vertex1.attachedFaces.append(newFace1) 
                    vertex2.attachedFaces += [newFace1, newFace2, newFace4]
                    vertex3.attachedFaces.append(newFace2)  
                    vertex4.attachedFaces += [newFace2, newFace3, newFace4]
                    vertex5.attachedFaces.append(newFace3) 
                    vertex6.attachedFaces += [newFace1, newFace3, newFace4]
                    faces += [newFace1,newFace2, newFace3, newFace4]
        case _ :
                print("Error : ce cas n'est possible.")