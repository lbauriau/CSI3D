from decimateur_utils import *

# Fonction globale de retriangulation

def discovery(list_valence, list_gate, list_coord_frenet, removed_vertex_indices, vertices, faces, operation):
    """
    Fonction effectuant des passes de patch-discovery3 et patch-discovery afin de décompresser la mesh.

    :param [in] list_valence: liste des valences renvoyées par le compresseur sur un schéme de [Bn An ... B1 A1]
                où les listes Bi sont renvoyées par la cleaning conquest et les Ai par la decimating conquest
    :param [in] list_gate: liste des premières gates utilisées dans les différentes conquest afin de ressortir les Ai et Bi
    :param [in] list_coord_frenet: liste des coordonnées de frenet associées aux points de valence list_valence
                list_coord_frenet[i] est associée à list_valence[i]
    :param [in/out] vertices: ensemble des vertices présents dans la mesh
    :param [in/out] faces:  ensemble des faces présentes dans la mesh
    :param [in/out] operation:  modèle renvoyant un fichier .obja
    """
    i = 1
    while (list_gate!=[]):
        print(f"______________ Debut decoding Cleaning {i} _______________")

        # On reverse le cleaning
        gate_cleaning = list_gate.pop(0)
        patchDiscovery3(list_valence, gate_cleaning, list_coord_frenet, removed_vertex_indices, vertices, faces, operation)
        resetFlagTagParam(vertices, faces)
        
        print("")
        print("______________ Fin C Debut decoding D _______________")

        # On reverse le decimateur
        gate_decim = list_gate.pop(0)
        patchDiscovery(list_valence, gate_decim, list_coord_frenet, removed_vertex_indices, vertices, faces, operation)
        resetFlagTagParam(vertices, faces)

        print("")
        print(f"______________ Fin decoding Decimation {i} _______________")
        print("")
        i += 1

def creationVertex(frenet, patch, idx, vertices, operations):
    """
    Créer le vertex central d'un patch grâce à ses coordonnées de frenet.

    :param [in] frenet: coordonées de frenet
    :param [in] patch: patch sur lequel s'appuie les coordonées de frenet
    """
    [n,t1,t2,b] = patch.getFrenet()
    vr_aux = b + frenet[0]*t1 + frenet[1]*t2 + frenet[2]*n
    vr = Vertex(idx, [], Flag.Conquered, Tag.Plus, vr_aux[0], vr_aux[1], vr_aux[2])
    patch.center_vertex = vr
    vertices.append(vr)
    #print(f"Added vertex {vr.id} at {vr_aux}")
    print(f"Adding vertex {vr.id} to obja: {vr.x} {vr.y} {vr.z}")
    operations.append(('vertex', vr.id, np.array([vr.x,vr.y,vr.z], np.double)))

def creationFaces(patch, faces, operations):
    """
    créer les différentes faces liant le center_vertex aux autres vertices du patch.

    :param [in] patch: patch que l'on traite.
    :param [in/out] faces: ensemble des faces de la mesh.
    :param [in/out] operations: listes des opérations de décompressions
    """
    valence = len(patch.bounding_vertices)
    for i in range (valence):
        new_face = Face(getNextElementIndex(faces),
                        Flag.Conquered,
                        [
                            patch.bounding_vertices[i],
                            patch.bounding_vertices[(i+1)%valence],
                            patch.center_vertex
                        ])
        faces.append(new_face)

        print(f"Adding face {new_face.id} to obja: vertices {[v.id for v in new_face.vertices]}")
        operations.append(('face', new_face.id, obja.Face(new_face.vertices[0].id,
                                                      new_face.vertices[1].id,
                                                      new_face.vertices[2].id,True)))

        # Ajout de la face dans les faces attachées aux vertex la composant
        patch.bounding_vertices[i].attached_faces.append(new_face)
        patch.bounding_vertices[(i+1)%valence].attached_faces.append(new_face)
        patch.center_vertex.attached_faces.append(new_face)

        #print(f"Added face {[v.id for v in new_face.vertices]}")

def supprimerFacesMultiple(list_face, faces, operations):
    """
    Supprime les références aux faces de list_faces

    :param [in] list_face: liste de face devant être supprimées
    :param [in/out] faces: ensemble des faces de la mesh

    """
    for face in list_face:
        supprimerFace(face, faces, operations)

def supprimerFace(face, faces, operations):
    """
    Supprime les références à la face en paramètre

    :param face: face à supprimer
    :param [in/out] faces: ensemble des faces de la mesh
    """
    for vertex in face.vertices:
        print(f"Suppression de la face {[v.id for v in face.vertices]} dans les attached_faces de {vertex.id}")
        # for f in vertex.attached_faces:
        #     print(f"attached face: {[v.id for v in f.vertices]}")
        vertex.attached_faces.remove(face)
    faces.remove(face)

    print(f"Deleting face {face.id} to obja: vertices {[v.id for v in face.vertices]}")
    operations.append(('delete_face', face.id, 0))


def ajouterGatesCleaning(output_gates, patch, fifo):
    """
    Ajoute les gates dans le cas d'un patch-discovery3
    où les gates ne sont pas forcément les sorties de Patch.getOutputGates()

    :param [in] output_gates: les gates de sortie de Patch.getOutputGates()
    :param [in] patch: le patch considéré
    :param [in/out] fifo: la pile fifo de gates
    """
    if patch.is_null_patch:
        for o in output_gates:
                print(f"    Null patch => ajout de la gate à la fifo: {[v.id for v in o.vertices]}, front ver = {o.getFrontVertex().id}")
        fifo += output_gates
    else:
        for gate in output_gates:
            gate.front_face.flag = Flag.Conquered
            print(f"    ________________ Conquered face: {gate.front_face.id}")
        for gate in output_gates:
            gates = Patch(0,gate, True).getOutputGates()
            for o in gates:
                print(f"    Good patch => ajout de la gate à la fifo: {[v.id for v in o.vertices]}, front ver = {o.getFrontVertex().id}")
            fifo += gates

def getActualizedStartingGate(first_gate, vertices, faces):
    print(f"First gate: {first_gate}")
    print(f"vertices {[v.id for v in vertices]}")
    print(f"{[v.id for v in vertices if v.id == first_gate[0]]}")
    print(f"{[v.id for v in vertices if v.id == first_gate[1]]}")
    first_gate_vertices = [next(v for v in vertices if v.id == first_gate[0]),
                           next(v for v in vertices if v.id == first_gate[1])]
    print(f"Available faces:")
    for f in faces:
        print(f"{[v.id for v in f.vertices]}")
    first_gate_front_face = next((f for f in faces if
                                      first_gate[0] in [v.id for v in f.vertices]
                                  and first_gate[1] in [v.id for v in f.vertices]
                                  and first_gate[2]  in [v.id for v in f.vertices]), None)

    gate = Gate(first_gate_front_face, first_gate_vertices)
    print(f"Found entry gate: {[v.id for v in gate.vertices]}")
    print(f"front face = {gate.front_face}")
    print(f"front ver = {gate.getFrontVertex().id}")
    return gate

def patchDiscovery3(list_valence,first_gate,list_coord_frenet, removed_vertex_indices,vertices,faces, operations):

    """
    Effectue la découverte de patch comme si nous étions dans une cleaning conquest.

    :param [in] list_valence: liste des valences renvoyées par le compresseur sur un schéme de [Bn An ... B1 A1]
                où les listes Bi sont renvoyées par la cleaning conquest et les Ai par la decimating conquest
    :param [in] first_gate: gate de départ de la conquest
    :param [in] list_coord_frenet: liste des coordonnées de frenet associées aux points de valence list_valence
                list_coord_frenet[i] est associée à list_valence[i]
    :param [in/out] vertices: ensemble des vertices présents dans la mesh
    :param [in/out] faces:  ensemble des faces présentes dans la mesh
    :param [in/out] operations:  modèle renvoyant un fichier .obja
    """

    fifo_gate = []
    gate = getActualizedStartingGate(first_gate, vertices, faces)
    fifo_gate.append(gate)

    # Boucle de parcours de la mesh
    while fifo_gate != []:
        print(f"valences: {list_valence}")
        # On récupère la porte d'entrée
        entry_gate = fifo_gate.pop(0)

        print("")
        print(f"_____ New patch (cleaning decompression) _____")
        print(f"entry gate: {[v.id for v in entry_gate.vertices]}, front ver = {entry_gate.getFrontVertex().id}, front face id = {entry_gate.front_face.id}, front face flag = {entry_gate.front_face.flag}")
        print(f"entry_gate.front_face in faces {entry_gate.front_face in faces}")

        front_face = entry_gate.front_face
        front_vertex = entry_gate.getFrontVertex()
        bounding_vertices = [entry_gate.vertices[0], entry_gate.vertices[1], front_vertex]

        # for vertex in bounding_vertices:
        #         print(f"attached_faces de {vertex.id}")
        #         for f in vertex.attached_faces:
        #             print(f"    attached face: {[v.id for v in f.vertices]}")
        #         print(f"")

        if front_face.flag == Flag.Free: # Juste une vérif mais normalement que des free
            # On récupère la valence et les coordonnées du point à ajouter
            valence = list_valence.pop(0)

            is_null_patch = valence == 0

            
            # Création du patch
            patch_add = Patch(0, entry_gate, is_null_patch, bounding_vertices)
            print(f"valence liste: {valence}, patch valence: {patch_add.getValence()}")
            print(f"is null patch: {patch_add.is_null_patch}")
            print(f"bounding: {[v.id for v in patch_add.bounding_vertices]}")
            
            if not is_null_patch:
                # On récupère son alpha, beta et gamma
                frenet = list_coord_frenet.pop(0)

                idx = removed_vertex_indices.pop(0)

                # Récupération de la base
                creationVertex(frenet, patch_add, idx, vertices, operations)
            
                # Création des nouvelles faces et ajout dans les vertices
                creationFaces(patch_add, faces, operations)
            
                # Suppression de la face dans les vertices et dans faces
                supprimerFace(front_face,faces, operations)
            else:
                entry_gate.front_face.flag = Flag.Conquered
                print(f"   ____________ Conquered face: {entry_gate.front_face.id}")

            # tagging des vertexs
            for vertex in bounding_vertices:
                vertex.flag = Flag.Conquered

            # Ajout des gates
            output_gates = patch_add.getOutputGates()
            # for o in output_gates:
            #     print(f"    Output gates: {[v.id for v in o.vertices]}, front ver = {o.getFrontVertex().id}")

            ajouterGatesCleaning(output_gates,patch_add,fifo_gate)
        else:
            print(f"Front face already conquered")
    
def patchDiscovery(list_valence, first_gate, list_coord_frenet, removed_vertex_indices, vertices, faces, operations):

    """
    Effectue la découverte de patch comme si nous étions dans une decimation conquest.

    :param [in] list_valence: liste des valences renvoyées par le compresseur sur un schéme de [Bn An ... B1 A1]
                où les listes Bi sont renvoyées par la cleaning conquest et les Ai par la decimating conquest
    :param [in] first_gate: gate de départ de la conquest
    :param [in] list_coord_frenet: liste des coordonnées de frenet associées aux points de valence list_valence
                list_coord_frenet[i] est associée à list_valence[i]
    :param [in/out] vertices: ensemble des vertices présents dans la mesh
    :param [in/out] faces:  ensemble des faces présentes dans la mesh
    :param [in/out] operations:  modèle renvoyant un fichier .obja
    """

    fifo_gate = []
    gate = getActualizedStartingGate(first_gate, vertices, faces)

    # On tag les vertices d'entrée
    gate.vertices[0].tag = Tag.Plus
    gate.vertices[1].tag = Tag.Minus

    fifo_gate.append(gate)

    # Variable répondant à la question : faut-il passer à la valence suivante ?

    while fifo_gate != []:
        # print(f"valences: {list_valence}")
        # On récupère la porte d'entrée
        entry_gate = fifo_gate.pop(0)

        print("")
        print(f"_____ New patch (Decimating decompression) _____")
        print(f"entry gate: {[v.id for v in entry_gate.vertices]}, front ver = {entry_gate.getFrontVertex().id}, front face id = {entry_gate.front_face.id}, front face flag = {entry_gate.front_face.flag}")
        print(f"entry_gate.front_face in faces {entry_gate.front_face in faces}")

        front_face = entry_gate.front_face
        front_vertex = entry_gate.getFrontVertex()

        if front_face.flag == Flag.Free:

            valence = list_valence.pop(0)

            print(f"valence liste: {valence}")
        
            # --------------- Récupération des bounding vertices --------------- 
            bounding_vertices = entry_gate.vertices[:]
            entry_faces = [front_face]
            match valence :
                case 0:
                    patch_add = Patch(0, entry_gate,True)
                    print(f"null patch entry gate: {[v.id for v in entry_gate.vertices]}, front ver = {entry_gate.getFrontVertex().id}")
                case 3:
                    # Récupération des bounding vertices
                    bounding_vertices.append(entry_gate.getFrontVertex())

                    # Création du patch
                    patch_add = Patch(0, entry_gate,False, bounding_vertices)

                    print(f"center vertex: {patch_add.center_vertex.id}")
                    
                case 4:
                    # Récupération des bounding vertices
                    if bounding_vertices[1].tag == Tag.Minus:
                        bounding_vertices.append(entry_gate.getFrontVertex())
                        entry_faces.append(getAdjacentFace(entry_faces[0], bounding_vertices[0], bounding_vertices[2]))
                        if entry_faces[1] is not None:
                            bounding_vertices.append(getThirdVertex(entry_faces[1], bounding_vertices[0], bounding_vertices[2]))
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                    else :
                        vert4 = entry_gate.getFrontVertex()
                        face = getAdjacentFace(entry_faces[0], vert4, bounding_vertices[1])
                        if face is not None:
                            bounding_vertices.append(getThirdVertex(face, vert4, bounding_vertices[1]))
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        bounding_vertices.append(vert4)

                    # Création du patch
                    patch_add = Patch(0, entry_gate,False, bounding_vertices)
                case 5:
                    # Récupération des bounding vertices
                    if bounding_vertices[1].tag == Tag.Minus:
                        # Premiere face sur 3
                        bounding_vertices.append(entry_gate.getFrontVertex())
                        entry_faces.append(getAdjacentFace(entry_faces[0], bounding_vertices[0], bounding_vertices[2]))
                        if entry_faces[1] is not None:
                            # 2e face sur 3
                            vert5 = getThirdVertex(entry_faces[1], bounding_vertices[0], bounding_vertices[2])
                            entry_faces.append(getAdjacentFace(entry_faces[1], vert5, bounding_vertices[2]))
                            if entry_faces[2] is not None:
                                # 3e face sur 3
                                bounding_vertices.append(getThirdVertex(entry_faces[2], vert5, bounding_vertices[2]))
                            else:
                                raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                            bounding_vertices.append(vert5)
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                    elif bounding_vertices[0].tag == Tag.Minus:
                        # Premiere face sur 3
                        vert5 =entry_gate.getFrontVertex()
                        entry_faces.append(getAdjacentFace(entry_faces[0], vert5, bounding_vertices[1]))
                        if entry_faces[1] is not None:
                            # 2e face sur 3
                            bounding_vertices.append(getThirdVertex(entry_faces[1], vert5, bounding_vertices[1]))
                            entry_faces.append(getAdjacentFace(entry_faces[1], vert5, bounding_vertices[2]))
                            if entry_faces[2] is not None:
                                # 3e face sur 3
                                bounding_vertices.append(getThirdVertex(entry_faces[2], vert5, bounding_vertices[2]))
                            else:
                                raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        bounding_vertices.append(vert5)
                    else:
                        # Premiere face sur 3
                        vert4 =entry_gate.getFrontVertex()
                        entry_faces.append(getAdjacentFace(entry_faces[0], vert4, bounding_vertices[1]))
                        if entry_faces[1] is not None:
                            # 2e face sur 3
                            bounding_vertices.append(getThirdVertex(entry_faces[1], vert4, bounding_vertices[1]))
                            bounding_vertices.append(vert4)
                            entry_faces.append(getAdjacentFace(entry_faces[1], bounding_vertices[0], bounding_vertices[3]))
                            if entry_faces[2] is not None:
                                # 3e face sur 3
                                bounding_vertices.append(getThirdVertex(entry_faces[2], bounding_vertices[0], bounding_vertices[3]))
                            else:
                                raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")

                    # Création du patch
                    print(f"entry_gate {entry_gate}")
                    print(f"entry_gate vertices {[v.id for v in entry_gate.vertices]}")
                    print(f"front_face {entry_gate.front_face}")
                    print(f"FrontVertex {entry_gate.getFrontVertex()}")
                    patch_add = Patch(0, entry_gate,False, bounding_vertices)

                case 6:
                    # Récupération des bounding vertices
                    if bounding_vertices[1].tag == Tag.Minus:
                        # Premiere face sur 4
                        bounding_vertices.append(entry_gate.getFrontVertex())
                        entry_faces.append(getAdjacentFace(entry_faces[0], bounding_vertices[0], bounding_vertices[2]))
                        if entry_faces[1] is not None:
                            # 2e face sur 4
                            vert5 = getThirdVertex(entry_faces[1], bounding_vertices[0], bounding_vertices[2])
                            entry_faces.append(getAdjacentFace(entry_faces[1], vert5, bounding_vertices[2]))
                            if entry_faces[2] is not None:
                                # 3e face sur 4
                                bounding_vertices.append(getThirdVertex(entry_faces[2], vert5, bounding_vertices[2]))
                                bounding_vertices.append(vert5)
                                entry_faces.append(getAdjacentFace(entry_faces[2], bounding_vertices[0], bounding_vertices[4]))
                                if entry_faces[3] is not None:
                                    # 4e face sur 4
                                    bounding_vertices.append(getThirdVertex(entry_faces[3], bounding_vertices[0], bounding_vertices[4]))
                                else:
                                    raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                            else:
                                raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                    else:
                        # Premiere face sur 4
                        vert6 =entry_gate.getFrontVertex()
                        entry_faces.append(getAdjacentFace(entry_faces[0], vert6, bounding_vertices[1]))
                        if entry_faces[1] is not None:
                            # 2e face sur 4
                            vert4 = getThirdVertex(entry_faces[1], vert6, bounding_vertices[1])
                            entry_faces.append(getAdjacentFace(entry_faces[1], vert4, bounding_vertices[1]))
                            if entry_faces[2] is not None:
                                # 3e face sur 4
                                bounding_vertices.append(getThirdVertex(entry_faces[2], vert4, bounding_vertices[1]))
                                bounding_vertices.append(vert4)
                                entry_faces.append(getAdjacentFace(entry_faces[1], vert6, bounding_vertices[3]))
                                if entry_faces[3] is not None:
                                    # 4e face sur 4
                                    bounding_vertices.append(getThirdVertex(entry_faces[3], vert6, bounding_vertices[3]))
                                else:
                                    raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                            else:
                                raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        else:
                            raise Exception(f"pas de face trouvée cas {valence} tag {bounding_vertices[1].tag}")
                        bounding_vertices.append(vert6)

                    # Création du patch
                    patch_add = Patch(0, entry_gate,False,bounding_vertices)

            print(f"Patch bounding discovery results:")
            print(f"    bounding: {[v.id for v in patch_add.bounding_vertices]}")
            print(f"    center vertex: {patch_add.center_vertex.id}")
            print(f"    valence liste: {valence}, (patch valence: {patch_add.getValence()})")
            print(f"    is null patch: {patch_add.is_null_patch}")
            # --------------- Fin Récupération des bounding vertices --------------- 

            if not patch_add.is_null_patch:
                # On récupère son alpha, beta et gamma
                frenet = list_coord_frenet.pop(0)

                idx = removed_vertex_indices.pop(0)

                # Récupération de la base
                creationVertex(frenet, patch_add, idx, vertices, operations)

                # Création des nouvelles faces et ajout dans les vertices
                creationFaces(patch_add, faces,operations)

                # Suppression de la face dans les vertices et dans faces
                supprimerFacesMultiple(entry_faces, faces, operations)
            else:
                entry_gate.front_face.flag = Flag.Conquered

            # flagging des vertexs
            for vertex in patch_add.bounding_vertices:
                vertex.flag = Flag.Conquered

            if patch_add.is_null_patch:
                patch_add.entry_gate.front_face.flag = Flag.Conquered

            output_gates = patch_add.getOutputGates()
            fifo_gate += output_gates
        else:
            print(f"Front face already conquered")
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