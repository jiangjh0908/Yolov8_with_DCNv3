## 项目简介

**在YOLOv8中替换卷积为DCNv3，实现有效涨点**

YOLOv8代码地址：https://github.com/ultralytics/ultralytics

DCNv3代码地址：https://github.com/OpenGVLab/InternImage

本项目参考：https://blog.csdn.net/java1314777/article/details/134193399


## 开始使用
### 环境安装
```
pip uninstall ultralytics
cd ultralytics\ops_dcnv3
python setup.py
```
**注意一定要卸载ultralytics包**

若setup.py安装出现问题，请升级gcc至8.0及以上版本（Linux）

### 训练及预测
自行配置并运行主目录中的train.py和predict.py
详情见https://github.com/ultralytics/ultralytics
