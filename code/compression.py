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

        while i < 4:
            print("")
            print("_________________________________________________________________________________________________")
            print(f"Iteration {i+1}")
            print("")
            patch_to_be_removed, output_iter, first_gate_decim = decimating_conquest(self.vertices, self.faces)

            print(f"Decimation {i+1} results:")
            print(f"    - Vertex 2br {[p.center_vertex.id for p in patch_to_be_removed]}")
            print(f"    - Firstgates: {[v.id for v in first_gate_decim.vertices]}")
            # print(f"    - faces: {[f.id for f in self.faces]}")
            print("")

            retriangulation_conquest(self.vertices, self.faces, patch_to_be_removed)


            print(f"Retriangulation {i+1} results:")
            # print(f"    - retri faces: {[f.id for f in self.faces]}")

            #Bn, firstgate_clean = cleaningConquest(self.vertices, self.faces)

            for face in self.faces:
                face.flag = Flag.Free
            for vertex in self.vertices:
                vertex.flag = Flag.Free
                vertex.tag = None

            with open(f'../TestModels/OutputIntermediaire{i+1}.obj', 'w') as outputIntm:
                createOutputModel(self.faces, self.vertices, outputIntm), f'../TestModels/OutputIntermediaire{i+1}.obj'

            i += 1

        return createOutputModel(self.faces, self.vertices, outputFile)

def createOutputModel(faces, vertices, outputFile):
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
    model = Compressor()
    model.parse_file(FILE_PATH)

    base = os.path.splitext(FILE_PATH)[0]
    print(base)
    with open(f'{base}2.obj', 'w') as output:
       model.compress(output)


if __name__ == '__main__':
    main()