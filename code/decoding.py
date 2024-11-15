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
    print (hello)
    
def patchDiscovery(listValence,firstGate,listCoordFrenet,vertices,faces):
    print (hello)