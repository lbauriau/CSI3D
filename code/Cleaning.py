# coding: iso-8859-1 -*-

from decimateur_utils import *
import func_init

def cleaningConquest(vertices, faces):
    print("")
    print("________ Cleaning ________")
    bn = []
    fren_coord = []
    
    first_gate = getFirstGate(faces)
    fifo = [first_gate]

    print(f"first gate: {[v.id for v in first_gate.vertices]}")
    
    #Tant qu'il y en a, on traite les gates de la fifo
    while len(fifo) > 0:
        
        current_gate = fifo[0]
        print("")
        print("    ________ New patch ________")
        print(f"    current gate vertices: {[v.id for v in current_gate.vertices]} front face id:{current_gate.front_face.id}")
        
        #On crée une instance de l'objet patch à l'aide de la gate traitï¿½e
        current_patch = Patch(0,current_gate, False)
        
        print(f"    current patch center vertex:{current_patch.center_vertex.id} valence: {current_patch.getValence()}")
        
        #On vérifie si le patch a déjà été conquis et si oui, on retire la gate de la fifo.
        if(current_gate.front_face.flag == Flag.Conquered) or (current_gate.front_face.flag == Flag.ToBeRemoved):
            print(f"    Patch has already been conquered")

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() <= 3):
            print(f"    Patch is going to be simplified")

            #On traite le patch
            current_gate.center_vertex.flag = Flag.ToBeRemoved #Pas très utile, car on traite le patch ici
            bn.append(current_patch.getValence())
            fren_coord.append(current_patch.getFrenetCoordinates())

            #On récupère les portes de sorties liées à ce patch
            output_gates = current_patch.getOutputGates()
            print(f"    -> Patch exit gate: {output_gates}")

            for v in current_patch.bounding_vertices:
                v.flag = Flag.Conquered

            #On marque les faces des outputs gates comme étant conquered et on
            #ajoute à la fifo les outputs gates correctes
            for gate in output_gates:
                gate.front_face.flag = Flag.Conquered
            for gate in output_gates:
                gates = Patch(0,gate, True).getOutputGates()
                fifo += gates
                print(f"        -> outputgate added to fifo: {[g for g in gates]}")

            #Suppression des éléments du patch
            for face in current_patch.center_vertex.attached_faces:
                #On enlève toutes les références aux faces que l'on enlève
                for v in current_patch.bounding_vertices:
                    if face in v.attached_faces:
                        v.attached_faces.remove(face)
                #On enlève la face de la liste des faces
                faces.remove(face)
                #On enlève le center vertex de la liste des vertices
                vertices.remove(current_patch.center_vertex)
                print(f"    -> Removed vertex: {current_patch.center_vertex.id}")
            #On ajoute la nouvelle face à la liste des faces
            new_face = Face(0,Flag.Conquered,current_patch.bounding_vertices)
            faces.append(new_face)

        elif(current_patch.center_vertex.flag == Flag.Free) and (current_patch.getValence() > 3) or current_patch.center_vertex.flag == Flag.Conquered:
            print(f"    -> null patch found")
            current_gate.front_face.flag == Flag.Conquered
            fifo += Patch(0,current_gate, True).getOutputGates()
            bn.append(0)
            
        #On enlève la gate que nous venons de traiter de la fifo
        fifo.pop(0)
        print(f"len(fifo) = {len(fifo)}")

        return bn, first_gate
        
#(v,f) = func_init.initialize('../TestModels/3ValenceShape.obj')
#(v,f) = func_init.initialize('../TestModels/TestCleaningSimple.obj')
#printVertsAndFaces(v,f)
#cleaningConquest(v,f)