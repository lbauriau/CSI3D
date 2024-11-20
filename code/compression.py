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

    def compress(self, output):

        operations = []
        i = 3

        while i != 0:
            patch2BeRemoved, output_iter, firstgate_decim = decimating_conquest(self.vertices, self.faces)

            print(f"Vertex 2br {[p.center_vertex.id for p in patch2BeRemoved]}")
            print(f"Firstgates: {[v.id for v in firstgate_decim.vertices]}")
            print(f"old faces: {[f.id for f in self.faces]}")

            retriangulation_conquest(self.vertices, self.faces, patch2BeRemoved)

            print(f"retri faces: {[f.id for f in self.faces]}")

            #Bn, firstgate_clean = cleaningConquest(self.vertices, self.faces)

            i -= 1

        # Iterate through the vertex
        for (vertex_index, vertex) in enumerate(self.vertices):
            # Delete the vertex
            vertex.id = vertex_index
            operations.append(('vertex', vertex_index, np.array([vertex.x,vertex.y,vertex.z], np.double)))

        # Iterate through the faces
        for (face_index, face) in enumerate(self.faces):

            operations.append(('face', face_index, obja.Face(face.vertices[0].id,
                                                             face.vertices[1].id,
                                                             face.vertices[2].id,True)))


        #  Write the result in output file
        output_model = obja.Output(output, random_color= False)
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
    model = Compressor()
    model.parse_file(FILE_PATH)

    base = os.path.splitext(FILE_PATH)[0]
    print(base)
    with open(f'{base}{'2.obj'}', 'w') as output:
       model.compress(output)


if __name__ == '__main__':
    main()