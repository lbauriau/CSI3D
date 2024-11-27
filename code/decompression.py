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
            operations_compression = []
            print("")
            print("_________________________________________________________________________________________________")
            print(f"Iteration {i+1}")
            print("")
            output_iter, first_gate_decim, f_coord_decim, d_removed_vertex_indices = decimating_conquest(self.vertices, self.faces)

            print(f"Decimation {i+1} results:")
            #print(f"    - Firstgates: {[v.id for v in first_gate_decim.vertices]}")
            print("")

            # remise à zéros des flag et tag des vertices et faces après la conquête de décimation
            resetFlagTagParam(self.faces, self.vertices)

            # Récupération des variables à transmettre au decoder pour le cleaning
            list_valence = output_iter + list_valence
            liste_frenet = f_coord_decim + liste_frenet
            first_gates = [first_gate_decim] + first_gates
            removed_vertex_indices = d_removed_vertex_indices + removed_vertex_indices

            print(f"Retriangulation {i+1} results:")
            # print(f"    - retri faces: {[f.id for f in self.faces]}")

            Bn, first_gate_clean, f_coord_clean, c_removed_vertex_indices = cleaningConquest(self.vertices, self.faces)

            # remise à zéros des flag et tag des vertices et faces après la conquête de cleaning
            resetFlagTagParam(self.faces, self.vertices)

            # Récupération des variables à transmettre au decoder pour le cleaning
            list_valence = Bn + list_valence
            liste_frenet = f_coord_clean + liste_frenet
            first_gates = [first_gate_clean] + first_gates
            removed_vertex_indices = c_removed_vertex_indices + removed_vertex_indices

            # création de la mesh
            addMeshToOperations(operations_compression, self.vertices, self.faces)

            with open(f'../TestModels/OutputIntermediaire{i+1}.obj', 'w') as outputIntm:
                createOutputModel(operations_compression, outputIntm), f'../TestModels/CompressionIntermediaire{i+1}.obj'

            i += 1

        ##############################
        # Boucle de decompression
        ##############################
        operations_decompression = []
        # Initialisation des operation en créant tous les vertex et faces de la mesh compressée
        addMeshToOperations(operations_decompression, self.vertices, self.faces)

        print("")
        print("_________________ Decoding _________________")
        print("")

        print(f"valences: {list_valence}")

        discovery(list_valence,first_gates,liste_frenet, removed_vertex_indices,self.vertices, self.faces,operations_decompression)

        operations_decompression_ob = []
        addMeshToOperations(operations_decompression_ob, self.vertices, self.faces)
        with open(f'../TestModels/Decompress.obj', 'w') as outputIntm:
                createOutputModel(operations_decompression_ob, outputIntm, True), f'../TestModels/Decompress.obj'

        return createOutputModel(operations_decompression, outputFile, random_color=True)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    base = "IcoSphere"
    if len(args) > 0:
        base = args[-1]

    FILE_PATH = f"../TestModels/{base}.obj"
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Decompressor()
    model.parse_file(FILE_PATH)

    with open(f'example/{base}.obja', 'w') as output:
       model.decompress(output)
    print(base)

if __name__ == '__main__':
    main()