from decimateur_utils import *

# Fonction globale de retriangulation

def discovery(listValence, listGate, listCoordFrenet,vertices,faces):
    while (listGate!=[]):
        gate3 = listGate.pop()
        patchDiscovery3(listValence,gate3,listCoordFrenet,vertices,faces)
        gateGlob = listGate.pop()
        patchDiscovery(listValence,gateGlob,listCoordFrenet)
    return 1
        
def patchDiscovery3(listValence,firstGate,listCoordFrenet,vertices,faces):
    fifoGate.append(firstGate)
    
    # Boucle de parcours de la mesh
    while fifoGate != []:
        
        # Onrécupère la porte d'entrée
        entryGate = fifoGate.pop(0)
        [vert1, vert2] = entryGate.vertices
        # On récupère la face commune est free aux deux vertices 
        faceVertices = getFaceWithVertices(vert1,vert2)
        
        if (faceVertices!=0):
            # On récupère la valence et les coordonnées du point à ajouter
            valence = listValence.pop(0) 
            # On récupère son alpha, beta et gamma
            frenet = listCoordFrenet.pop(0)
            
            vert3 = getThirdVertex(faceVertices,vert1,vert2)
            
            # Création du patch
            patchAdd = Patch(0, entryGate)
            patchAdd.boundingVertices = [vert1,vert2,vert3]
            
            # Récupération de la base
            [n,t1,t2,b] = getFrenet(patchAdd)
            vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
            vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr[0], vr[1], vr[2])
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
        
        
                
    
def patchDiscovery(listValence,firstGate,listCoordFrenet,vertices,faces):
    fifoGate.append(firstGate)
    while fifoGate != []:
        entryGate = fifoGate[0]
        valence = listValence.pop(0)
        frenet = listCoordFrenet.pop(0)
        
        patchAdd = Patch(0, entryGate)
        [n,t1,t2,b] = getFrenet(patchAdd)
        vr = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
        
        match valence :
            case 3:
                dfdf
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