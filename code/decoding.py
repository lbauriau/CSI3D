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
    while fifoGate != []:
        entryGate = fifoGate[0]
        valence = listValence.pop(0)
        frenet = listCoordFrenet.pop(0)
        
        patchAdd = Patch(0, entryGate)
        [n,t1,t2,b] = getFrenet(patchAdd)
        vr = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
        
        
                
    
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

def getFaceWithVerteces(vert1,vert2,vert3):
    n = len(vert1.attachedFaces)
    for i in range(n):
        if (vert1.attachedFaces[i] in vert2.attachedFaces and vert1.attachedFaces[i] in vert3.attachedFaces):
            return vert1.attachedFaces[i]
    return KeyError