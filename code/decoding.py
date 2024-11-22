from decimateur_utils import *

# Fonction globale de retriangulation

def discovery(list_valence, list_gate, list_coord_frenet,vertices,faces):
    while (list_gate!=[]):
        # On reverse le cleaning
        gate3 = list_gate.pop()
        patchDiscovery3(list_valence,gate3,list_coord_frenet,vertices,faces)
        
        # On reverse le decimateur
        gate_glob = list_gate.pop()
        patchDiscovery(list_valence,gate_glob,list_coord_frenet)
        
    return 1
        
def patchDiscovery3(list_valence,first_gate,list_coord_frenet,vertices,faces):
    fifo_gate = []
    
    fifo_gate.append(first_gate)
    # Boucle de parcours de la mesh
    while fifo_gate != []:
        
        # On récupère la porte d'entrée
        entry_gate = fifo_gate.pop(0)
        [vert1, vert2] = entry_gate.vertices
        # On récupère la face commune est free aux deux vertices 
        face_vertices = entry_gate.front_face
        
        if (face_vertices.flag == Flag.Free): # Juste une vérif mais normalement que des free
            # On récupère la valence et les coordonnées du point à ajouter
            valence = list_valence.pop(0) 
            # On récupère son alpha, beta et gamma
            frenet = list_coord_frenet.pop(0)
            
            # Récupération des bounding vertices
            vert3 = patch_add.bounding_vertices[3]

            # Création du patch
            patch_add = Patch(0, entry_gate,False)
            
            # Récupération de la base
            [n,t1,t2,b] = patch_add.getFrenet()
            vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
            vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
            vertices.append(vr)
            
            
            # Création des nouvelles faces et ajout dans les vertices
            new_face1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
            new_face2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
            new_face3 = Face(0,Flag.Conquered,[vert3,vert1,vr])
            faces += [new_face1,new_face2,new_face3]
            vert1.attached_faces += [new_face1,new_face3]
            vert2.attached_faces += [new_face1,new_face2]
            vert3.attached_faces += [new_face2,new_face3]
            vr.attached_faces = [new_face1,new_face2,new_face3]
            
            # Suppression de la face dans les vertices et dans faces
            vert1.attached_faces.removed(face_vertices)
            vert2.attached_faces.removed(face_vertices)
            vert3.attached_faces.removed(face_vertices)
            faces.remove(face_vertices)
            
            face32 = getFaceWithVertices(vert3,vert2)
            face13 = getFaceWithVertices(vert1,vert3)
            if(face32.flag == Flag.Free):
                fifo_gate.append(Gate(face32,[vert3,vert2]))
            if(face13.flag == Flag.Free):
                fifo_gate.append(Gate(face13,[vert1,vert3]))        
    
def patchDiscovery(list_valence,first_gate,list_coord_frenet,vertices,faces):
    fifo_gate = []
    fifo_gate.append(first_gate)
    
    while fifo_gate != []:
        entry_gate = fifo_gate[0]
        valence = list_valence.pop(0)
        face1 = entry_gate.front_face
        # On récupère son alpha, beta et gamma
        frenet = list_coord_frenet.pop(0)
        
        # Récupération des bounding vertices
        [vert1,vert2] = entry_gate
        match valence :
            case 3:
                # Récupération des bounding vertices
                vert3 = patch_add.bounding_vertices[3]

                # Création du patch
                patch_add = Patch(0, entry_gate,False)
                
                # Récupération de la base
                [n,t1,t2,b] = patch_add.getFrenet()
                vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
                vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
                vertices.append(vr)
                
                
                # Création des nouvelles faces et ajout dans les vertices
                new_face1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
                new_face2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
                new_face3 = Face(0,Flag.Conquered,[vert3,vert1,vr])
                faces += [new_face1,new_face2,new_face3]
                vert1.attached_faces += [new_face1,new_face3]
                vert2.attached_faces += [new_face1,new_face2]
                vert3.attached_faces += [new_face2,new_face3]
                vr.attached_faces = [new_face1,new_face2,new_face3]
                
                # Suppression de la face dans les vertices et dans faces
                vert1.attached_faces.removed(face1)
                vert2.attached_faces.removed(face1)
                vert3.attached_faces.removed(face1)
                faces.remove(face1)
                
                face32 = getFaceWithVertices(vert3,vert2)
                face13 = getFaceWithVertices(vert1,vert3)
                if(face32.flag == Flag.Free):
                    fifo_gate.append(Gate(face32,[vert3,vert2]))
                if(face13.flag == Flag.Free):
                    fifo_gate.append(Gate(face13,[vert1,vert3]))      
                    
            case 4:
                # Récupération des bounding vertices
                
                if (vert2.tag == Tag.Minus):
                    vert3 = patch_add.bounding_vertices[3]
                    face2 = getFaceWithVertices(vert1,vert3)
                    vert4 = getThirdVertex(face2,vert1,vert3)
                else :
                    vert4 = patch_add.bounding_vertices[3]
                    face2 = getFaceWithVertices(vert4,vert2)
                    vert3 = getThirdVertex(face2,vert4,vert2)

                # Création du patch
                patch_add = Patch(0, entry_gate,False)
                patch_add.bounding_vertices = [vert1,vert2,vert3,vert4]
                
                # Récupération de la base
                [n,t1,t2,b] = patch_add.getFrenet()
                vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
                vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
                vertices.append(vr)
                
                
                # Création des nouvelles faces et ajout dans les vertices
                new_face1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
                new_face2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
                new_face3 = Face(0,Flag.Conquered,[vert3,vert4,vr])
                new_face4 = Face(0,Flag.Conquered,[vert4,vert1,vr])
                faces += [new_face1,new_face2,new_face3, new_face4]
                vert1.attached_faces += [new_face1,new_face4]
                vert2.attached_faces += [new_face1,new_face2]
                vert3.attached_faces += [new_face2,new_face3]
                vert4.attached_faces += [new_face3,new_face4]
                vr.attached_faces = [new_face1,new_face2,new_face3,new_face4]
                
                # Suppression de la face dans les vertices et dans faces
                vert1.attached_faces.removed(face1)
                vert2.attached_faces.removed(face1)
                vert3.attached_faces.removed(face2)
                vert4.attached_faces.removed(face2)
                if (vert2.tag == Tag.Minus):
                    vert1.attached_faces.removed(face2)
                    vert3.attached_faces.removed(face1)
                else :
                    vert2.attached_faces.removed(face2)
                    vert4.attached_faces.removed(face1)

                faces.remove(face1)
                faces.remove(face2)
                
                face32 = getFaceWithVertices(vert3,vert2)
                face43 = getFaceWithVertices(vert4,vert3)
                face14 = getFaceWithVertices(vert1,vert4)
                if(face32.flag == Flag.Free):
                    fifo_gate.append(Gate(face32,[vert3,vert2]))
                if(face43.flag == Flag.Free):
                    fifo_gate.append(Gate(face43,[vert4,vert3]))
                if(face14.flag == Flag.Free):
                    fifo_gate.append(Gate(face14,[vert1,vert4]))
            
            case 5:
                
                if (vert2.tag == Tag.Minus):
                    vert3 = patch_add.bounding_vertices[3]
                    face2 = getFaceWithVertices(vert1,vert3)
                    vert5 = getThirdVertex(face2,vert1,vert3)
                    face3 = getFaceWithVertices(vert5,vert3)
                    vert4 = getThirdVertex(face3,vert5,vert3)
                elif (vert1.tag == Tag.Minus):
                    vert5 = patch_add.bounding_vertices[3]
                    face2 = getFaceWithVertices(vert5,vert2)
                    vert3 = getThirdVertex(face2,vert5,vert2)
                    face3 = getFaceWithVertices(vert5,vert3)
                    vert4 = getThirdVertex(face3,vert5,vert3)
                else:
                    vert4 = patch_add.bounding_vertices[3]
                    face2 = getFaceWithVertices(vert4,vert2)
                    vert3 = getThirdVertex(face2,vert4,vert2)
                    face3 = getFaceWithVertices(vert1,vert4)
                    vert5 = getThirdVertex(face3,vert1,vert4)

                # Création du patch
                patch_add = Patch(0, entry_gate,False)
                patch_add.bounding_vertices = [vert1,vert2,vert3,vert4,vert5]
                
                # Récupération de la base
                [n,t1,t2,b] = patch_add.getFrenet()
                vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
                vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
                vertices.append(vr)
                
                
                # Création des nouvelles faces et ajout dans les vertices
                new_face1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
                new_face2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
                new_face3 = Face(0,Flag.Conquered,[vert3,vert4,vr])
                new_face4 = Face(0,Flag.Conquered,[vert4,vert5,vr])
                new_face5 = Face(0,Flag.Conquered,[vert5,vert1,vr])
                faces += [new_face1,new_face2,new_face3, new_face4,new_face5]
                vert1.attached_faces += [new_face1,new_face5]
                vert2.attached_faces += [new_face1,new_face2]
                vert3.attached_faces += [new_face2,new_face3]
                vert4.attached_faces += [new_face3,new_face4]
                vert5.attached_faces += [new_face4,new_face5]
                vr.attached_faces = [new_face1,new_face2,new_face3,new_face4,new_face5]
                
                # Suppression de la face dans les vertices et dans faces
                vert1.attached_faces.removed(face1)
                vert2.attached_faces.removed(face1)
                vert3.attached_faces.removed(face2)
                vert4.attached_faces.removed(face3)
                vert5.attached_faces.removed(face3)
                if (vert2.tag == Tag.Minus):
                    vert1.attached_faces.removed(face2)
                    vert3.attached_faces.removed(face1)
                    vert3.attached_faces.removed(face3)
                    vert5.attached_faces.removed(face2)
                elif (vert1.tag == Tag.Minus):
                    vert2.attached_faces.removed(face2)
                    vert3.attached_faces.removed(face3)
                    vert5.attached_faces.removed(face1)
                    vert5.attached_faces.removed(face2)
                else:
                    vert1.attached_faces.removed(face3)
                    vert2.attached_faces.removed(face2)
                    vert4.attached_faces.removed(face1)
                    vert4.attached_faces.removed(face2)
                
                faces.remove(face1)
                faces.remove(face2)
                faces.remove(face3)
                
                face32 = getFaceWithVertices(vert3,vert2)
                face43 = getFaceWithVertices(vert4,vert3)
                face54 = getFaceWithVertices(vert5,vert4)
                face15 = getFaceWithVertices(vert1,vert5)
                if(face32.flag == Flag.Free):
                    fifo_gate.append(Gate(face32,[vert3,vert2]))
                if(face43.flag == Flag.Free):
                    fifo_gate.append(Gate(face43,[vert4,vert3]))
                if(face54.flag == Flag.Free):
                    fifo_gate.append(Gate(face54,[vert5,vert4]))
                if(face15.flag == Flag.Free):
                    fifo_gate.append(Gate(face15,[vert1,vert5]))
                    
            
            case 6:
                
                if (vert2.tag == Tag.Minus):
                    vert3 = patch_add.bounding_vertices[3]
                    face4 = getFaceWithVertices(vert1,vert3)
                    vert5 = getThirdVertex(face4,vert1,vert3)
                    face2 = getFaceWithVertices(vert5,vert3)
                    vert4 = getThirdVertex(face2,vert5,vert3)
                    face3 = getFaceWithVertices(vert1,vert5)
                    vert6 = getThirdVertex(face3,vert1,vert5)
                else :
                    vert6 = patch_add.bounding_vertices[3]
                    face4 = getFaceWithVertices(vert6,vert2)
                    vert4 = getThirdVertex(face2,vert6,vert2)
                    face2 = getFaceWithVertices(vert4,vert2)
                    vert3 = getThirdVertex(face2,vert4,vert2)
                    face3 = getFaceWithVertices(vert6,vert4)
                    vert5 = getThirdVertex(face3,vert6,vert4)


                # Création du patch
                patch_add = Patch(0, entry_gate,False)
                patch_add.bounding_vertices = [vert1,vert2,vert3,vert4,vert5,vert6]
                
                # Récupération de la base
                [n,t1,t2,b] = patch_add.getFrenet()
                vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
                vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
                vertices.append(vr)
                
                
                # Création des nouvelles faces et ajout dans les vertices
                new_face1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
                new_face2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
                new_face3 = Face(0,Flag.Conquered,[vert3,vert4,vr])
                new_face4 = Face(0,Flag.Conquered,[vert4,vert5,vr])
                new_face5 = Face(0,Flag.Conquered,[vert5,vert6,vr])
                new_face6 = Face(0,Flag.Conquered,[vert6,vert1,vr])
                faces += [new_face1,new_face2,new_face3, new_face4,new_face5, new_face6]
                vert1.attached_faces += [new_face1,new_face6]
                vert2.attached_faces += [new_face1,new_face2]
                vert3.attached_faces += [new_face2,new_face3]
                vert4.attached_faces += [new_face3,new_face4]
                vert5.attached_faces += [new_face4,new_face5]
                vert6.attached_faces += [new_face5,new_face6]
                vr.attached_faces = [new_face1,new_face2,new_face3,new_face4,new_face5,new_face6]
                
                # Suppression de la face dans les vertices et dans faces
                vert1.attached_faces.removed(face1)
                vert2.attached_faces.removed(face1)
                vert3.attached_faces.removed(face2)
                vert4.attached_faces.removed(face2)
                vert5.attached_faces.removed(face3)
                vert6.attached_faces.removed(face3)
                if (vert2.tag == Tag.Minus):
                    vert1.attached_faces.removed(face3)
                    vert1.attached_faces.removed(face4)
                    vert3.attached_faces.removed(face1)
                    vert3.attached_faces.removed(face4)
                    vert5.attached_faces.removed(face2)
                    vert5.attached_faces.removed(face4)
                else:
                    vert2.attached_faces.removed(face2)
                    vert2.attached_faces.removed(face4)
                    vert4.attached_faces.removed(face3)
                    vert4.attached_faces.removed(face4)
                    vert6.attached_faces.removed(face1)
                    vert6.attached_faces.removed(face4)
                
                faces.remove(face1)
                faces.remove(face2)
                faces.remove(face3)
                faces.remove(face4)
                
                face32 = getFaceWithVertices(vert3,vert2)
                face43 = getFaceWithVertices(vert4,vert3)
                face54 = getFaceWithVertices(vert5,vert4)
                face65 = getFaceWithVertices(vert6,vert5)
                face16 = getFaceWithVertices(vert1,vert6)
                if(face32.flag == Flag.Free):
                    fifo_gate.append(Gate(face32,[vert3,vert2]))
                if(face43.flag == Flag.Free):
                    fifo_gate.append(Gate(face43,[vert4,vert3]))
                if(face54.flag == Flag.Free):
                    fifo_gate.append(Gate(face54,[vert5,vert4]))
                if(face65.flag == Flag.Free):
                    fifo_gate.append(Gate(face65,[vert6,vert5]))
                if(face16.flag == Flag.Free):
                    fifo_gate.append(Gate(face16,[vert1,vert6]))                 
    return 0                



def getFaceWithVertices(vert1,vert2):
    n = len(vert1.attached_faces)
    for i in range(n):
        facei= vert1.attached_faces[i]
        cond1 = (facei[1]==vert1 and facei[2]==vert2 )
        cond2 = (facei[1]==vert1 and facei[2]==vert2 )
        cond3 = (facei[3]==vert1 and facei[1]==vert2 )
        if (cond1 or cond2 or cond3):
            return vert1.attached_faces[i]
    return 0

def getThirdVertex(face, vert1, vert2):
    for i in range(3):
        aux_vert = face.vertices[i]
        if (aux_vert!= vert1 and aux_vert!= vert2):
            return aux_vert