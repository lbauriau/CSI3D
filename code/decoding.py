from decimateur_utils import *

# Fonction globale de retriangulation

def discovery(listValence, listGate, listCoordFrenet,vertices,faces):
    while (listGate!=[]):
        # On reverse le cleaning
        gate3 = listGate.pop()
        patchDiscovery3(listValence,gate3,listCoordFrenet,vertices,faces)
        
        # On reverse le decimateur
        gateGlob = listGate.pop()
        patchDiscovery(listValence,gateGlob,listCoordFrenet)
        
    return 1
        
def patchDiscovery3(listValence,firstGate,listCoordFrenet,vertices,faces):
    fifoGate = []
    
    fifoGate.append(firstGate)
    # Boucle de parcours de la mesh
    while fifoGate != []:
        
        # On récupère la porte d'entrée
        entryGate = fifoGate.pop(0)
        [vert1, vert2] = entryGate.vertices
        # On récupère la face commune est free aux deux vertices 
        faceVertices = entryGate.frontFace
        
        if (faceVertices.flag == Flag.Free): # Juste une vérif mais normalement que des free
            # On récupère la valence et les coordonnées du point à ajouter
            valence = listValence.pop(0) 
            # On récupère son alpha, beta et gamma
            frenet = listCoordFrenet.pop(0)
            
            # Récupération des bounding vertices
            vert3 = patchAdd.boundingVertices[3]

            # Création du patch
            patchAdd = Patch(0, entryGate,False)
            
            # Récupération de la base
            [n,t1,t2,b] = patchAdd.getFrenet()
            vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
            vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
            vertices.append(vr)
            
            
            # Création des nouvelles faces et ajout dans les vertices
            newFace1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
            newFace2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
            newFace3 = Face(0,Flag.Conquered,[vert3,vert1,vr])
            faces += [newFace1,newFace2,newFace3]
            vert1.attachedFaces += [newFace1,newFace3]
            vert2.attachedFaces += [newFace1,newFace2]
            vert3.attachedFaces += [newFace2,newFace3]
            vr.attachedFaces = [newFace1,newFace2,newFace3]
            
            # Suppression de la face dans les vertices et dans faces
            vert1.attachedFaces.removed(faceVertices)
            vert2.attachedFaces.removed(faceVertices)
            vert3.attachedFaces.removed(faceVertices)
            faces.remove(faceVertices)
            
            face32 = getFaceWithVertices(vert3,vert2)
            face13 = getFaceWithVertices(vert1,vert3)
            if(face32.flag == Flag.Free):
                fifoGate.append(Gate(face32,[vert3,vert2]))
            if(face13.flag == Flag.Free):
                fifoGate.append(Gate(face13,[vert1,vert3]))        
    
def patchDiscovery(listValence,firstGate,listCoordFrenet,vertices,faces):
    fifoGate = []
    fifoGate.append(firstGate)
    
    while fifoGate != []:
        entryGate = fifoGate[0]
        valence = listValence.pop(0)
        face1 = entryGate.frontFace
        
        match valence :
            case 3:
                # On récupère son alpha, beta et gamma
                frenet = listCoordFrenet.pop(0)
                
                # Récupération des bounding vertices
                vert3 = patchAdd.boundingVertices[3]

                # Création du patch
                patchAdd = Patch(0, entryGate,False)
                
                # Récupération de la base
                [n,t1,t2,b] = patchAdd.getFrenet()
                vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
                vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
                vertices.append(vr)
                
                
                # Création des nouvelles faces et ajout dans les vertices
                newFace1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
                newFace2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
                newFace3 = Face(0,Flag.Conquered,[vert3,vert1,vr])
                faces += [newFace1,newFace2,newFace3]
                vert1.attachedFaces += [newFace1,newFace3]
                vert2.attachedFaces += [newFace1,newFace2]
                vert3.attachedFaces += [newFace2,newFace3]
                vr.attachedFaces = [newFace1,newFace2,newFace3]
                
                # Suppression de la face dans les vertices et dans faces
                vert1.attachedFaces.removed(face1)
                vert2.attachedFaces.removed(face1)
                vert3.attachedFaces.removed(face1)
                faces.remove(face1)
                
                face32 = getFaceWithVertices(vert3,vert2)
                face13 = getFaceWithVertices(vert1,vert3)
                if(face32.flag == Flag.Free):
                    fifoGate.append(Gate(face32,[vert3,vert2]))
                if(face13.flag == Flag.Free):
                    fifoGate.append(Gate(face13,[vert1,vert3]))      
                    
            case 4:
                # On récupère son alpha, beta et gamma
                frenet = listCoordFrenet.pop(0)
                
                # Récupération des bounding vertices
                [vert1,vert2] = entryGate
                if (vert2.tag == Tag.Minus):
                    vert3 = patchAdd.boundingVertices[3]
                    face2 = getFaceWithVertices(vert1,vert3)
                    vert4 = getThirdVertex(face2,vert1,vert3)
                else :
                    vert4 = patchAdd.boundingVertices[3]
                    face2 = getFaceWithVertices(vert4,vert2)
                    vert3 = getThirdVertex(face2,vert4,vert2)

                # Création du patch
                patchAdd = Patch(0, entryGate,False)
                patchAdd.boundingVertices = [vert1,vert2,vert3,vert4]
                
                # Récupération de la base
                [n,t1,t2,b] = patchAdd.getFrenet()
                vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
                vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
                vertices.append(vr)
                
                
                # Création des nouvelles faces et ajout dans les vertices
                newFace1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
                newFace2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
                newFace3 = Face(0,Flag.Conquered,[vert3,vert4,vr])
                newFace4 = Face(0,Flag.Conquered,[vert4,vert1,vr])
                faces += [newFace1,newFace2,newFace3, newFace4]
                vert1.attachedFaces += [newFace1,newFace4]
                vert2.attachedFaces += [newFace1,newFace2]
                vert3.attachedFaces += [newFace2,newFace3]
                vert4.attachedFaces += [newFace3,newFace4]
                vr.attachedFaces = [newFace1,newFace2,newFace3,newFace4]
                
                # Suppression de la face dans les vertices et dans faces
                vert1.attachedFaces.removed(face1)
                vert1.attachedFaces.removed(face2)
                vert2.attachedFaces.removed(face1)
                vert3.attachedFaces.removed(face1)
                vert3.attachedFaces.removed(face2)
                vert4.attachedFaces.removed(face2)
                faces.remove(face1)
                faces.remove(face2)
                
                face32 = getFaceWithVertices(vert3,vert2)
                face43 = getFaceWithVertices(vert4,vert3)
                face14 = getFaceWithVertices(vert1,vert4)
                if(face32.flag == Flag.Free):
                    fifoGate.append(Gate(face32,[vert3,vert2]))
                if(face43.flag == Flag.Free):
                    fifoGate.append(Gate(face43,[vert4,vert3]))
                if(face14.flag == Flag.Free):
                    fifoGate.append(Gate(face14,[vert1,vert4]))      
    return 0                

def getFaceWithVertices(vert1,vert2):
    n = len(vert1.attachedFaces)
    for i in range(n):
        if (vert1.attachedFaces[i] in vert2.attachedFaces):
            if (vert1.attachedFace[1].flag == Flag.Free):
                return vert1.attachedFaces[i]
    return 0

def getThirdVertex(face, vert1, vert2):
    for i in range(3):
        auxVert = face.vertices[i]
        if (auxVert!= vert1 and auxVert!= vert2):
            return auxVert