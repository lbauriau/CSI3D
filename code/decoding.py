from decimateur_utils import *

# Fonction globale de retriangulation

def discovery(list_valence, list_gate, list_coord_frenet,vertices,faces):
    """
    Fonction effectuant des passes de patch-discovery3 et patch-discovery afin de décompresser la mesh.

    :param [in] list_valence: liste des valences renvoyées par le compresseur sur un schéme de [Bn An ... B1 A1]
                où les listes Bi sont renvoyées par la cleaning conquest et les Ai par la decimating conquest
    :param [in] list_gate: liste des premières gates utilisées dans les différentes conquest afin de ressortir les Ai et Bi
    :param [in] list_coord_frenet: liste des coordonnées de frenet associées aux points de valence list_valence
                list_coord_frenet[i] est associée à list_valence[i]
    :param [in/out] vertices: ensemble des vertices présents dans la mesh
    :param [in/out] faces:  ensemble des faces présentes dans la mesh
    """
    while (list_gate!=[]):
        # On reverse le cleaning
        gate3 = list_gate.pop()
        patchDiscovery3(list_valence,gate3,list_coord_frenet,vertices,faces)
        
        # On reverse le decimateur
        gate_glob = list_gate.pop()
        patchDiscovery(list_valence,gate_glob,list_coord_frenet, vertices, faces)

def creationVertex(frenet, patch):
    """
    Créer le vertex central d'un patch grâce à ses coordonnées de frenet.

    :param [in] frenet: coordonées de frenet
    :param [in] patch: patch sur lequel s'appuie les coordonées de frenet
    :return: le vertex central d'un patch
    """
    [n,t1,t2,b] = patch.getFrenet()
    vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
    vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])

    return vr

def creationFaces(list_vertices, center_vertex, faces):
    """
    créer les différentes faces liant le center_vertex aux autres vertices du patch.

    :param [in] list_vertices: liste des bounding vertices d'un patch
    :param [in] center_vertex:  vertex central du patch
    :param [in/out] faces: ensemble des faces de la mesh
    """
    valence = len(list_vertices)
    for i in range (valence):
        idx = getNextElementIndex(faces)
        new_face = Face(idx, Flag.Conquered, [list_vertices[i], list_vertices[(i+1)%valence],center_vertex])
        faces.append(new_face)

        # Ajout de la face dans les faces attachées aux vertex la composant
        list_vertices[i].attached_faces.append(new_face)
        list_vertices[(i+1)%valence].attached_faces.append(new_face)
        center_vertex.attached_faces.append(new_face)

def supprimerFacesMultiple(list_face, faces):
    """
    Supprime les références aux faces de list_faces

    :param [in] list_face: liste de face devant être supprimées
    :param [in/out] faces: ensemble des faces de la mesh

    """
    for face in list_face:
        supprimerFace(face, faces)

def supprimerFace(face, faces):
    """
    Supprime les références à la face en paramètre

    :param face: face à supprimer
    :param [in/out] faces: ensemble des faces de la mesh
    """
    for vertex in face.vertices:
        vertex.attached_faces.remove(face)
    faces.remove(face)

def ajouterGatesCleaning(output_gates, patch, fifo):
    """
    Ajoute les gates dans le cas d'un patch-discovery3
    où les gates ne sont pas forcément les sorties de Patch.getOutputGates()

    :param [in] output_gates: les gates de sortie de Patch.getOutputGates()
    :param [in] patch: le patch considéré
    :param [in/out] fifo: la pile fifo de gates
    """
    if patch.is_null_patch:
        fifo += output_gates
    else:
        for gate in output_gates:
            gate.front_face.flag = Flag.Conquered
        for gate in output_gates:
            gates = Patch(0,gate, True).getOutputGates()
            fifo += gates

def patchDiscovery3(list_valence,first_gate,list_coord_frenet,vertices,faces):

    """
    Effectue la découverte de patch comme si nous étions dans une cleaning conquest.

    :param [in] list_valence: liste des valences renvoyées par le compresseur sur un schéme de [Bn An ... B1 A1]
                où les listes Bi sont renvoyées par la cleaning conquest et les Ai par la decimating conquest
    :param [in] first_gate: gate de départ de la conquest
    :param [in] list_coord_frenet: liste des coordonnées de frenet associées aux points de valence list_valence
                list_coord_frenet[i] est associée à list_valence[i]
    :param [in/out] vertices: ensemble des vertices présents dans la mesh
    :param [in/out] faces:  ensemble des faces présentes dans la mesh
    """

    fifo_gate = []
    
    fifo_gate.append(first_gate)
    # Boucle de parcours de la mesh
    while fifo_gate != []:
        
        # On récupère la porte d'entrée
        entry_gate = fifo_gate.pop(0)
        list_vertices = entry_gate.vertices
        # On récupère la face commune est free aux deux vertices 
        face_vertices = entry_gate.front_face
        
        if face_vertices[0].flag == Flag.Free: # Juste une vérif mais normalement que des free
            # On récupère la valence et les coordonnées du point à ajouter
            valence = list_valence.pop(0) 
            # On récupère son alpha, beta et gamma
            frenet = list_coord_frenet.pop(0)

            # Création du patch
            patch_add = Patch(0, entry_gate, valence ==0)

            # Récupération des bounding vertices
            list_vertices.append(entry_gate.getFrontVertex())
            patch_add.bounding_vertices = list_vertices # nécessaire pour les méthodes sur patch_add.
            
            # Récupération de la base
            """[n,t1,t2,b] = patch_add.getFrenet()
            vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
            vr = Vertex( 0, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
            """
            vr = creationVertex(frenet, patch_add)
            vertices.append(vr)
            
            
            # Création des nouvelles faces et ajout dans les vertices
            """
            new_face1 = Face(0,Flag.Conquered,[vert1,vert2,vr])
            new_face2 = Face(0,Flag.Conquered,[vert2,vert3,vr])
            new_face3 = Face(0,Flag.Conquered,[vert3,vert1,vr])
            faces += [new_face1,new_face2,new_face3]
            vert1.attached_faces += [new_face1,new_face3]
            vert2.attached_faces += [new_face1,new_face2]
            vert3.attached_faces += [new_face2,new_face3]
            vr.attached_faces = [new_face1,new_face2,new_face3]
            """
            creationFaces(list_vertices, vr, faces)
            
            # Suppression de la face dans les vertices et dans faces
            """
            vert1.attached_faces.removed(face_vertices)
            vert2.attached_faces.removed(face_vertices)
            vert3.attached_faces.removed(face_vertices)
            faces.remove(face_vertices)
            """
            supprimerFace(face_vertices,faces)

            # tagging des vertexs
            for vertex in list_vertices:
                vertex.flag = Flag.Conquered

            # Ajout des gates
            """
            face32 = getFaceWithVertices(vert3,vert2)
            face13 = getFaceWithVertices(vert1,vert3)
            if(face32.flag == Flag.Free):
                fifo_gate.append(Gate(face32,[vert3,vert2]))
            if(face13.flag == Flag.Free):
                fifo_gate.append(Gate(face13,[vert1,vert3]))
            """
            output_gates = patch_add.getOutputGates()
            ajouterGatesCleaning(output_gates,patch_add,fifo_gate)
    
def patchDiscovery(list_valence,first_gate,list_coord_frenet,vertices,faces):

    """
    Effectue la découverte de patch comme si nous étions dans une decimation conquest.

    :param [in] list_valence: liste des valences renvoyées par le compresseur sur un schéme de [Bn An ... B1 A1]
                où les listes Bi sont renvoyées par la cleaning conquest et les Ai par la decimating conquest
    :param [in] first_gate: gate de départ de la conquest
    :param [in] list_coord_frenet: liste des coordonnées de frenet associées aux points de valence list_valence
                list_coord_frenet[i] est associée à list_valence[i]
    :param [in/out] vertices: ensemble des vertices présents dans la mesh
    :param [in/out] faces:  ensemble des faces présentes dans la mesh
    """

    fifo_gate = []
    fifo_gate.append(first_gate)

    # Variable répondant à la question : faut-il passer à la valence suivante ?
    next_valence = True

    while fifo_gate != []:

        entry_gate = fifo_gate[0]
        if next_valence:
            valence = list_valence.pop(0)
            # On récupère son alpha, beta et gamma
            frenet = list_coord_frenet.pop(0)
            # On s'empêche de passer à la valence suivante
            # Tant que celle-ci n'a pas été traitée.
            next_valence = False
        
        # Récupération des bounding vertices
        list_vertices = entry_gate.vertices
        entry_faces = [entry_gate.front_face]

        # On tag les vertices d'entrée
        list_vertices[0].tag = Tag.Plus
        list_vertices[1].tag = Tag.Minus

        match valence :
            case 3:
                # Récupération des bounding vertices
                list_vertices.append(entry_gate.getFrontVertex())

                # Création du patch
                patch_add = Patch(0, entry_gate,False)
                patch_add.bounding_vertices = list_vertices # nécessaire pour les méthodes sur patch_add.
                    
            case 4:
                # Création du patch et
                # Récupération des bounding vertices
                patch_add = Patch(0, entry_gate,False)

                if list_vertices[1].tag == Tag.Minus:
                    list_vertices.append(entry_gate.getFrontVertex())
                    entry_faces.append(getAdjacentFace(entry_faces[0], list_vertices[0], list_vertices[2]))
                    if entry_faces[1] is not None:
                        list_vertices.append(getThirdVertex(entry_faces[1], list_vertices[0], list_vertices[2]))
                else :
                    vert4 = entry_gate.getFrontVertex()
                    face = getAdjacentFace(entry_faces[0], vert4, list_vertices[1])
                    if face is not None:
                        list_vertices.append(getThirdVertex(face, vert4, list_vertices[1]))
                    list_vertices.append(vert4)

                patch_add.bounding_vertices = list_vertices
            
            case 5:
                # Création du patch et
                # Récupération des bounding vertices
                patch_add = Patch(0, entry_gate,False)
                if list_vertices[1].tag == Tag.Minus:
                    # Premiere face sur 3
                    list_vertices.append(entry_gate.getFrontVertex())
                    entry_faces.append(getAdjacentFace(entry_faces[0], list_vertices[0], list_vertices[2]))
                    if entry_faces[1] is not None:
                        # 2e face sur 3
                        vert5 = getThirdVertex(entry_faces[1], list_vertices[0], list_vertices[2])
                        entry_faces.append(getAdjacentFace(entry_faces[1], vert5, list_vertices[2]))
                        if entry_faces[2] is not None:
                            # 3e face sur 3
                            list_vertices.append(getThirdVertex(entry_faces[2], vert5, list_vertices[2]))
                        else:
                            patch_add.is_null_patch = True
                        list_vertices.append(vert5)
                    else:
                        patch_add.is_null_patch = True
                elif list_vertices[0].tag == Tag.Minus:
                    # Premiere face sur 3
                    vert5 =entry_gate.getFrontVertex()
                    entry_faces.append(getAdjacentFace(entry_faces[0], vert5, list_vertices[1]))
                    if entry_faces[1] is not None:
                        # 2e face sur 3
                        list_vertices.append(getThirdVertex(entry_faces[1], vert5, list_vertices[1]))
                        entry_faces.append(getAdjacentFace(entry_faces[1], vert5, list_vertices[2]))
                        if entry_faces[2] is not None:
                            # 3e face sur 3
                            list_vertices.append(getThirdVertex(entry_faces[2], vert5, list_vertices[2]))
                    list_vertices.append(vert5)

                else:
                    # Premiere face sur 3
                    vert4 =entry_gate.getFrontVertex()
                    entry_faces.append(getAdjacentFace(entry_faces[0], vert4, list_vertices[1]))
                    if entry_faces[1] is not None:
                        # 2e face sur 3
                        list_vertices.append(getThirdVertex(entry_faces[1], vert4, list_vertices[1]))
                        list_vertices.append(vert4)
                        entry_faces.append(getAdjacentFace(entry_faces[1], list_vertices[0], list_vertices[3]))
                        if entry_faces[2] is not None:
                            # 3e face sur 3
                            list_vertices.append(getThirdVertex(entry_faces[2], list_vertices[0], list_vertices[3]))

                patch_add.bounding_vertices = list_vertices
                

            case 6:
                # Création du patch et
                # Récupération des bounding vertices
                patch_add = Patch(0, entry_gate,False)
                if list_vertices[1].tag == Tag.Minus:
                    # Premiere face sur 4
                    list_vertices.append(entry_gate.getFrontVertex())
                    entry_faces.append(getAdjacentFace(entry_faces[0], list_vertices[0], list_vertices[2]))
                    if entry_faces[1] is not None:
                        # 2e face sur 4
                        vert5 = getThirdVertex(entry_faces[1], list_vertices[0], list_vertices[2])
                        entry_faces.append(getAdjacentFace(entry_faces[1], vert5, list_vertices[2]))
                        if entry_faces[2] is not None:
                            # 3e face sur 4
                            list_vertices.append(getThirdVertex(entry_faces[2], vert5, list_vertices[2]))
                            list_vertices.append(vert5)
                            entry_faces.append(getAdjacentFace(entry_faces[2], list_vertices[0], list_vertices[4]))
                            if entry_faces[3] is not None:
                                # 4e face sur 4
                                list_vertices.append(getThirdVertex(entry_faces[3], list_vertices[0], list_vertices[4]))
                else:
                    # Premiere face sur 4
                    vert6 =entry_gate.getFrontVertex()
                    entry_faces.append(getAdjacentFace(entry_faces[0], vert6, list_vertices[1]))
                    if entry_faces[1] is not None:
                        # 2e face sur 4
                        vert4 = getThirdVertex(entry_faces[1], vert6, list_vertices[1])
                        entry_faces.append(getAdjacentFace(entry_faces[1], vert4, list_vertices[1]))
                        if entry_faces[2] is not None:
                            # 3e face sur 4
                            list_vertices.append(getThirdVertex(entry_faces[2], vert4, list_vertices[1]))
                            list_vertices.append(vert4)
                            entry_faces.append(getAdjacentFace(entry_faces[1], vert6, list_vertices[3]))
                            if entry_faces[3] is not None:
                                # 4e face sur 4
                                list_vertices.append(getThirdVertex(entry_faces[3], vert6, list_vertices[3]))
                    list_vertices.append(vert6)

                patch_add.bounding_vertices = list_vertices

        # Récupération de la base
        vr = creationVertex(frenet, patch_add)
        vertices.append(vr)


        # Création des nouvelles faces et ajout dans les vertices
        creationFaces(list_vertices, vr, faces)

        # Suppression de la face dans les vertices et dans faces
        supprimerFacesMultiple(entry_faces, faces)

        # tagging des vertexs
        for vertex in list_vertices:
            vertex.flag = Flag.Conquered

        output_gates = patch_add.getOutputGates()
        fifo_gate += output_gates
    return 0


"""
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
"""

def getThirdVertex(face, vert1, vert2):
    """
    Renvoie le 3e vertex d'une face.

    :param [in] face: la face dont on veut connaitre le 3e vertex
    :param [in] vert1: L'un des 3 vertex d'une face
    :param [in] vert2: Un vertex appartenant à la face différent de vert1
    :return: Le dernier vertex de la face
    """
    for i in range(3):
        aux_vert = face.vertices[i]
        if (aux_vert!= vert1 and aux_vert!= vert2):
            return aux_vert