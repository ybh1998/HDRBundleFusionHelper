import os
import numpy as np
import open3d as o3d


def render(name):
    filename = os.path.join('data', name)
    mesh = o3d.io.read_triangle_mesh(filename + '.ply')
    print('color: ', mesh.has_vertex_colors())
    print(np.shape(np.asarray(mesh.vertex_colors)))
    mesh.vertex_colors = o3d.utility.Vector3dVector(
        np.asarray(mesh.vertex_colors)[:, ::-1] * 20)
    for i in range(8):
        o3d.visualization.draw_geometries([mesh], width=640, height=480)
        mesh.vertex_colors = o3d.utility.Vector3dVector(
            np.asarray(mesh.vertex_colors) * 1.75)
