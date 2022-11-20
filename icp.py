#coding=utf-8

import open3d as o3d
import numpy as np
import copy

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4459,
                                      front=[0.9288, -0.2951, -0.2242],
                                      lookat=[1.6784, 2.0612, 1.4451],
                                      up=[-0.3402, -0.9189, -0.1996])




realsense_pc = o3d.io.read_point_cloud("realsense/ply/realsense.ply")
ouster_pc = o3d.io.read_point_cloud("ouster/ply/ouster.ply")

voxel_down_realsense = realsense_pc.voxel_down_sample(voxel_size=0.005)
voxel_down_ouster = ouster_pc.voxel_down_sample(voxel_size=0.005)


# 为两个点云上上不同的颜色
realsense_pc.paint_uniform_color([0, 0.651, 0.929]) #target 为蓝色
ouster_pc.paint_uniform_color([1, 0.706, 0])    #source 为黄色

# 切记，将稠密点云当作src，将稀疏点云当作target
processed_source, outlier_index = voxel_down_realsense.remove_radius_outlier(nb_points=16, radius=0.5)

processed_target, outlier_index = voxel_down_ouster.remove_radius_outlier(nb_points=16, radius=0.5)

#o3d.geometry.radius_outlier_removal 这个函数是使用球体判断一个特例的函数，它需要
#两个参数：nb_points 和 radius。 它会给点云中的每个点画一个半径为 radius 的球体，如
#果在这个球体中其他的点的数量小于 nb_points, 这个算法会将这个点判断为特例，并删除。


threshold = 0.2  #移动范围的阀值
# src2target,using mechanical params
trans_init = np.asarray([[ 0.01, 0.99, -0.11, -0.11],
[-0.24, 0.11, 0.99, 0.18],
[ 0.99, 0.12, 0.24, -0.03],
[ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

trans_init = np.linalg.inv(trans_init)

#运行icp
reg_p2p = o3d.pipelines.registration.registration_icp(
        processed_source, processed_target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())

#将我们的矩阵依照输出的变换矩阵进行变换
print(reg_p2p)
print("Transformation is:")
print(reg_p2p.transformation)
# processed_source.transform(reg_p2p.transformation)

draw_registration_result(processed_source, processed_target, reg_p2p.transformation)
# #创建一个 o3d.visualizer class
# vis = o3d.visualization.Visualizer()
# vis.create_window()

# #将两个点云放入visualizer
# vis.add_geometry(processed_source)
# vis.add_geometry(processed_target)

# #让visualizer渲染点云
# vis.update_geometry()
# vis.poll_events()
# vis.update_renderer()

# vis.run()





