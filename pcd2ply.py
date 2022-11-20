#coding=utf-8
import open3d as o3d
import numpy as np

pointcloud_in = o3d.io.read_point_cloud("realsense/pcd/1668756185025264.pcd")
o3d.io.write_point_cloud("realsense/ply/1668756185025264.ply", pointcloud=pointcloud_in, write_ascii=True)