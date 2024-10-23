import decimateur_utils

def initialize(nomFichier):

    with open(nomFichier, 'r') as f:
        lines = f.readlines()

    vertex = {}
    faces = {}
    gates = {}
    idVertex = 1
    idFace = 1
    idGate = 1

    for line in lines:

        split = line.split()

        if len(split) == 0:
            return

        elif split[0] == 'v':
            x = split[1]
            y = split[2]
            z = split[3]
            v_temp = decimateur_utils.Vertex([],
                                             decimateur_utils.Flag.Free,
                                             None,
                                             float(x), float(y), float(z))

            vertex[str(idVertex)] = v_temp
            idVertex +=1

        elif split[0] == 'f':
            keyvertex1 = split[1]
            keyvertex2 = split[2]
            keyvertex3 = split[3]
            f_temp = decimateur_utils.Face(decimateur_utils.Flag.Free,
                                           [keyvertex1, keyvertex2, keyvertex3])
            faces[str(idFace)] = f_temp
            idFace +=1

    return vertex , faces


(v,f) =initialize('../TestModels/6ValenceShape.obj')
for j in range (len(v)):
    vert = v[str(j+1)]
    print(vert.x)
    print(vert.y)
    print(vert.z)

for j in range (len(f)):
    face = f[str(j+1)]
    print(face.keyVertices)