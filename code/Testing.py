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

class Testing(obja.Model):
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
        


        operations_decompression = []
        # Initialisation des operation en créant tous les vertex et faces de la mesh compressée
        addMeshToOperations(operations_decompression, self.vertices, self.faces)

        with open(f'../TestModels/Decompress.obj', 'w') as outputIntm:
                createOutputModel(operations_decompression, outputIntm, True), f'../TestModels/Decompress.obj'

        return createOutputModel(operations_decompression, outputFile)


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
    model = Testing()
    model.parse_file(FILE_PATH)

    base = os.path.splitext(FILE_PATH)[0]
    print(base)
    with open(f'{base}2.obja', 'w') as output:
       model.decompress(output)


if __name__ == '__main__':
    main()