# ICP-calibration
A method to calibrate the extrinsics of sensors(eg: ouster and realsense D455) using ICP

## bag to pcd
一个终端通过ros发送messages，如:
```
rosbag play XXX.bag
```

另一个终端接收，如:
```
rosrun pcl_ros pointcloud_to_pcd input:=/velodyne_points
```

## pcd to ply
```
pcl_pcd2ply xxx.pcd xxx.ply
```

## trim ply
由于ICP对初值敏感，需要借助Meshlab对scene_01的点云与上一步中获取的主相机下的AprilTag三维点云(optim_ply.ply)进行ICP手动粗配准获得初始外参，详细教程，流程如下：

​ 1.在Meshlab中加载lidar/scene_01/sum.ply和optim_ply.ply。

​ 2.选中Align功能

​ 3.为了方便后续点云可视化，先对sum.ply点云进行简单修建，只保留存在AprilTag的部分区域

​ 4.选中sum.ply，点击Glue Here Mesh

​ 5.选中optim_ply.ply，点击Point Based Glue

​ 6.在画面中分别在左右点云选择对应点

​ 7.点击OK进行Align

​ 此时Align的效果会在窗口中显示，窗口右下角会提示当前的变换矩阵，将此矩阵记录，并保存为T_init.txt放置在config文件夹中作为后续初值。T_init.txt格式如下(用空格分割)：

0 0 -1 -0.13
1 0 0 -0.02
0 -1 0 -0.20
0 0 0 1

## run icp
python icp.py
