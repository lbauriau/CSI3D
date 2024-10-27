# coding: iso-8859-1 -*-

import decimateur_utils

def initialize(nomFichier):

    with open(nomFichier, 'r') as f:
        lines = f.readlines()

    vertex = []
    faces = []
    #Les id sont finalement utiles, notanemnt pour du debug
    idVertex = 1
    idFace = 1

    #On fait un premier parcours pour "d�couvrir" tous les vertex.
    for line in lines:

        split = line.split()

        if len(split) == 0:
            return

        elif split[0] == 'v':
            #On cr�e le vertex
            x = split[1]
            y = split[2]
            z = split[3]
            #note: on rempli la liste "attachedFaces" du vertex dans la
            #boucle d'apr�s car les faces n'existent pas encore 
            v_temp = decimateur_utils.Vertex(idVertex,
                                             [],
                                             decimateur_utils.Flag.Free,
                                             None,
                                             float(x), float(y), float(z))

            #On ajoute le vertex � la liste des vertex
            vertex.append(v_temp)
            idVertex +=1
    
    #Maintenant que la liste de vertex est pleine on peu cr�er les faces
    #(On ne peu le faire que maintenant car les faces ont des r�f�rences
    #vers les vertex, il nous faut donc la liste des vertex)
    for line in lines:

        split = line.split()

        if len(split) == 0:
            return
        
        elif split[0] == 'f':
            #On cr�e la face
            #Note: les indices des vertex commencent � 1 et non � 0
            vert1 = vertex[int(split[1])-1]
            vert2 = vertex[int(split[2])-1]
            vert3 = vertex[int(split[3])-1]
            f_temp = decimateur_utils.Face(idFace,
                                           decimateur_utils.Flag.Free,
                                           [vert1, vert2, vert3])
            
            #On ajoute la face � la liste des faces
            faces.append(f_temp)

            #Pour chaque vertex formant la face on ajoute cette derni�re � la
            #liste des faces connect�
            vert1.attachedFaces.append(f_temp)
            vert2.attachedFaces.append(f_temp)
            vert3.attachedFaces.append(f_temp)
            
            idFace +=1

    return vertex , faces


(v,f) = initialize('../TestModels/3ValenceShape.obj')
decimateur_utils.printVertsAndFaces(v,f)