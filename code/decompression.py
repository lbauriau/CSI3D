import obja
import numpy as np
import sys
import os
from decimateur_utils import *
from func_init import *
from decimating_conquest import decimating_conquest
from Cleaning import cleaningConquest
from retriangulation import retriangulation_conquest
from decoding import discovery, patchDiscovery

class Decompressor(obja.Model):
    """
    Sous-classe de la classe Model d'obja afin de pouvoir écrire dans un fichier .obja
    """

    def __init__(self):
        super().__init__()
        self.deleted_faces = set()


    def parse_file(self, path):
        """
        Override de la fonction afin d'utiliser les classe Face et Vertex que nous avons créés.

        :param [in] path: chemin d'accès au fichier .obj
        """
        vertices, faces = initialize(path)
        self.vertices = vertices
        self.faces = faces

    def decompress(self, outputFile):
        """

        Effectue la compression puis de décompression d'une mesh(.obj)
        :param [in/out] outputFile: Fichier dans lequel sont écritent les instructions obja
        """

        # déclaration des variables remplies par l'encoder et utilisées par le decoder
        list_valence = []
        liste_frenet = []
        first_gates = []
        removed_vertex_indices = []

        ##############################
        # Boucle de compression
        ##############################
        i = 0

        while i < 10:
            print("")
            print("_________________________________________________________________________________________________")
            print(f"Iteration {i+1}")
            print("")
            output_iter, first_gate_decim, f_coord_decim, d_removed_vertex_indices = decimating_conquest(self.vertices, self.faces)

            print(f"Decimation {i+1} results:")
            #print(f"    - Firstgates: {[v.id for v in first_gate_decim.vertices]}")
            print("")

            # remise à zéros des flag et tag des vertices et faces après la conquête de décimation
            resetFlagTagParam(self.vertices, self.faces)

            # Récupération des variables à transmettre au decoder pour le cleaning
            list_valence = output_iter + list_valence
            liste_frenet = f_coord_decim + liste_frenet
            first_gates = [first_gate_decim] + first_gates
            removed_vertex_indices = d_removed_vertex_indices + removed_vertex_indices

            print(f"Retriangulation {i+1} results:")
            # print(f"    - retri faces: {[f.id for f in self.faces]}")

            Bn, first_gate_clean, f_coord_clean, c_removed_vertex_indices = cleaningConquest(self.vertices, self.faces)

            # remise à zéros des flag et tag des vertices et faces après la conquête de cleaning
            resetFlagTagParam(self.vertices, self.faces)

            # Récupération des variables à transmettre au decoder pour le cleaning
            list_valence = Bn + list_valence
            liste_frenet = f_coord_clean + liste_frenet
            first_gates = [first_gate_clean] + first_gates
            removed_vertex_indices = c_removed_vertex_indices + removed_vertex_indices

            with open(f'../TestModels/OutputIntermediaire{i+1}.obj', 'w') as outputIntm:
                createOutputModel(self.faces, self.vertices, outputIntm), f'../TestModels/CompressionIntermediaire{i+1}.obj'

            i += 1

        ##############################
        # Boucle de decompression
        ##############################
        print("")
        print("_________________ Decoding _________________")
        print("")

        print(f"valences: {list_valence}")

        discovery(list_valence,first_gates,liste_frenet, removed_vertex_indices,self.vertices, self.faces)

        with open(f'../TestModels/Decompress.obj', 'w') as outputIntm:
                createOutputModel(self.faces, self.vertices, outputIntm), f'../TestModels/Decompress.obj'

        return createOutputModel(self.faces, self.vertices, outputFile)

def createOutputModel(faces, vertices, outputFile):
    """
    Écrit dans le fichier de sortie les instructions obja

    :param [in] faces: ensemble des faces de la mesh.
    :param [in] vertices: ensemble des vertices de la mesh.
    :param [in/out] outputFile: Fichier dans lequel sont écritent les instructions obja
    """
    operations = []

    # Iterate through the vertex
    for (_, vertex) in enumerate(vertices):
        #print(f"Adding vertex {vertex.id} to obja: {vertex.x} {vertex.y} {vertex.z}")
        operations.append(('vertex', vertex.id, np.array([vertex.x,vertex.y,vertex.z], np.double)))

    # Iterate through the faces
    for (_, face) in enumerate(faces):
        #print(f"Adding face {face.id} to obja: vertices {[v.id for v in face.vertices]}")
        operations.append(('face', face.id, obja.Face(face.vertices[0].id,
                                                            face.vertices[1].id,
                                                            face.vertices[2].id,True)))
    #  Write the result in output file
    output_model = obja.Output(outputFile, random_color= False)
    for (ty, index, value) in operations:
        if ty == "vertex":
            output_model.add_vertex(index, value)
        elif ty == "face":
            output_model.add_face(index, value)
        else:
            output_model.edit_vertex(index, value)

    return output_model

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    FILE_PATH = "../TestModels/IcoSphere.obj"
    if len(args) > 0:
        FILE_PATH = f"../TestModels/{args[-1]}.obj"
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decompressor()
    model.parse_file(FILE_PATH)

    base = os.path.splitext(FILE_PATH)[0]
    print(base)
    with open(f'{base}2.obj', 'w') as output:
       model.decompress(output)


if __name__ == '__main__':
    main()