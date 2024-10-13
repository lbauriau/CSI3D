import decimateur_utils

def initialize(nomFichier):

    with open(nomFichier, 'r') as f:
        lines = f.readlines()

    vertex = []
    faces = []
    idVertex = 0
    idFace = 0

    for line in lines:

        split = line.split()

        if len(split) == 0:
            return

        elif split[0] == 'v':
            v_temp = decimateur_utils.Vertex(idVertex,
                                             decimateur_utils.Flag(1),
                                             decimateur_utils.Tag(1),
                                             split[1], split[2], split[3])
            vertex.append(v_temp)
            idVertex +=1

        elif split[0] == 'f':
            f_temp = decimateur_utils.Face(idFace,
                                             decimateur_utils.Flag(1),
                                             split[1])
            faces.append(f_temp)
            idFace +=1

    return vertex , faces


(v,f) =initialize('../TestModels/6ValenceShape.obj')
for vert in v:
    print(vert.id)
    print(vert.x)
    print(vert.y)
    print(vert.z)

for face in f:
    print(face.id)
    print(face.vertex)