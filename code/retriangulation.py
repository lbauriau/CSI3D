def retriangulation_conquest(vertices, faces, listPatchBeRemoved):
    while (listPatchBeRemoved !=[]):
        patchRemoved = listPatchBeRemoved.pop([0])
        removedVertex(patchRemoved,vertices,faces)
    return 0


    
