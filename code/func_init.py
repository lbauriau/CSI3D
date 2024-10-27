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
            #note: on rempli la liste "attachedFaces" du vertex dans la
            #boucle d'après car les faces n'existent pas encore 
            v_temp = decimateur_utils.Vertex(idVertex,
                                             [],
                                             decimateur_utils.Flag.Free,
                                             None,
                                             float(x), float(y), float(z))

            #On ajoute le vertex à la liste des vertex
            vertex.append(v_temp)
            idVertex +=1
    
    #Maintenant que la liste de vertex est pleine on peu créer les faces
    #(On ne peu le faire que maintenant car les faces ont des références
    #vers les vertex, il nous faut donc la liste des vertex)
    for line in lines:

        split = line.split()

        if len(split) == 0:
            return
        
        elif split[0] == 'f':
            #On crée la face
            #Note: les indices des vertex commencent à 1 et non à 0
            vert1 = vertex[int(split[1])-1]
            vert2 = vertex[int(split[2])-1]
            vert3 = vertex[int(split[3])-1]
            f_temp = decimateur_utils.Face(idFace,
                                           decimateur_utils.Flag.Free,
                                           [vert1, vert2, vert3])
            
            #On ajoute la face à la liste des faces
            faces.append(f_temp)

            #Pour chaque vertex formant la face on ajoute cette dernière à la
            #liste des faces connecté
            vert1.attachedFaces.append(f_temp)
            vert2.attachedFaces.append(f_temp)
            vert3.attachedFaces.append(f_temp)
            
            idFace +=1

    return vertex , faces


(v,f) = initialize('../TestModels/3ValenceShape.obj')
decimateur_utils.printVertsAndFaces(v,f)