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


    def parse_file(self, path):
        vertices, faces = initialize(path)
        self.vertices = vertices
        self.faces = faces

    def compress(self, output):

        operations = []
        i = 5

        while i != 0:
            patch2BeRemoved, output, firstgates = decimating_conquest(self.vertices, self.faces)

            retriangulation_conquest(self.vertices, self.faces, patch2BeRemoved)

            Bn, firstgate = cleaningConquest(self.vertices, self.faces)

            i += 1

        # Write the result in output file
        output_model = obja.Output(output, random_color=True)

        for (ty, index, value) in operations:
            if ty == "vertex":
                output_model.add_vertex(index, value)
            elif ty == "face":
                output_model.add_face(index, value)
            else:
                output_model.edit_vertex(index, value)
        return output

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    FILE_PATH = "../TestModels/SimpleCube.obj"
    if len(args) > 0:
        FILE_PATH = args[-1]
    """
    Runs the program on the model given as parameter.
    """
    np.seterr(invalid = 'raise')
    model = Compressor()
    model.parse_file(FILE_PATH)

    base = os.path.splitext(FILE_PATH)[0]
    with open(f'{base}{'.obja'}', 'w') as output:
        model.compress(output)


if __name__ == '__main__':
    main()