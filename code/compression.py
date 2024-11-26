import obja
import numpy as np
import sys
import os
from decimateur_utils import *
from func_init import *
from decimating_conquest import decimating_conquest
from Cleaning import cleaningConquest
from retriangulation import retriangulation_conquest

class Compressor(obja.Model):

    def __init__(self):
        super().__init__()
        self.deleted_faces = set()


    def parse_file(self, path):
        vertices, faces = initialize(path)
        self.vertices = vertices
        self.faces = faces

    def compress(self, outputFile):

        i = 0

        # with open(f'../TestModels/OutputIntermediaireOrigin.obj', 'w') as outputIntm:
        #         createOutputModel(self.faces, self.vertices, outputIntm), f'../TestModels/OutputIntermediaireOrigin.obj'

        while i < 10:
            operations = []
            print("")
            print("_________________________________________________________________________________________________")
            print(f"Iteration {i+1}")
            print("")
            output_iter, first_gate_decim, f_coord_decim, d_removed_vertex_indices = decimating_conquest(self.vertices, self.faces)

            print(f"Decimation {i+1} results:")
            #print(f"    - Vertex 2br {[p.center_vertex.id for p in patch_to_be_removed]}")
            #print(f"    - Firstgates: {[v.id for v in first_gate_decim.vertices]}")
            # print(f"    - faces: {[f.id for f in self.faces]}")
            print("")

            #retriangulation_conquest(self.vertices, self.faces, patch_to_be_removed)

            # remise à zéros des flag et tag des vertices et faces après la conquête de décimation
            resetFlagTagParam(self.vertices, self.faces)

            print(f"Retriangulation {i+1} results:")
            # print(f"    - retri faces: {[f.id for f in self.faces]}")

            Bn, first_gate_clean, f_coord_clean, c_removed_vertex_indices = cleaningConquest(self.vertices, self.faces)

            # remise à zéros des flag et tag des vertices et faces après la conquête de cleaning
            resetFlagTagParam(self.vertices, self.faces)

            # création de la mesh
            addMeshToOperations(operations, self.vertices, self.faces)


            with open(f'../TestModels/OutputIntermediaire{i+1}.obj', 'w') as outputIntm:
                createOutputModel(operations, outputIntm, True), f'../TestModels/OutputIntermediaire{i+1}.obj'

            i += 1

        return createOutputModel(operations, outputFile)

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
    model = Compressor()
    model.parse_file(FILE_PATH)

    base = os.path.splitext(FILE_PATH)[0]
    print(base)
    with open(f'{base}2.obja', 'w') as output:
       model.compress(output)


if __name__ == '__main__':
    main()