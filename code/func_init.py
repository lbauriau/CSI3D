# coding: iso-8859-1 -*-

import decimateur_utils

def initialize(nom_fichier):

    with open(nom_fichier, 'r') as f:
        lines = f.readlines()

    vertex = []
    faces = []
    #Les id sont finalement utiles, notanemnt pour du debug
    id_vertex = 1
    id_face = 1

    #On fait un premier parcours pour "découvrir" tous les vertex.
    for line in lines:

        split = line.split()

        if len(split) == 0:
            return

        elif split[0] == 'v':
            #On crée le vertex
            x = split[1]
            y = split[2]
            z = split[3]
            #note: on remplit la liste "attached_faces" du vertex dans la
            #boucle d'après car les faces n'existent pas encore 
            v_temp = decimateur_utils.Vertex(id_vertex,
                                             [],
                                             decimateur_utils.Flag.Free,
                                             None,
                                             float(x), float(y), float(z))

            #On ajoute le vertex à la liste des vertex
            vertex.append(v_temp)
            id_vertex +=1
    
    #Maintenant que la liste de vertex est pleine, on peut créer les faces
    #(On ne peut le faire que maintenant, car les faces ont des références
    #vers les vertex, il nous faut donc la liste des vertex).
    for line in lines:

        split = line.split()

        if len(split) == 0:
            return
        
        elif split[0] == 'f':
            #On crée la face
            #Note: les indices des vertex commencent à 1 et non à 0.
            vert1 = vertex[int(split[1])-1]
            vert2 = vertex[int(split[2])-1]
            vert3 = vertex[int(split[3])-1]
            f_temp = decimateur_utils.Face(id_face,
                                           decimateur_utils.Flag.Free,
                                           [vert1, vert2, vert3])
            
            #On ajoute la face à la liste des faces
            faces.append(f_temp)

            #Pour chaque vertex formant la face, on ajoute cette dernière à la
            #liste des faces connectées.
            vert1.attached_faces.append(f_temp)
            vert2.attached_faces.append(f_temp)
            vert3.attached_faces.append(f_temp)
            
            id_face +=1

    return vertex , faces


#(v,f) = initialize('../TestModels/3ValenceShape.obj')
#decimateur_utils.printVertsAndFaces(v,f)