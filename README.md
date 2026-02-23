## 项目简介

**在YOLOv8中替换卷积为DCNv3，实现有效涨点**

YOLOv8代码地址：https://github.com/ultralytics/ultralytics

DCNv3代码地址：https://github.com/OpenGVLab/InternImage

本项目参考：https://blog.csdn.net/java1314777/article/details/134193399
https://blog.csdn.net/zyw2002/article/details/132405324?ops_request_misc=elastic_search_misc&request_id=b8017897e9f5d4fa658a2f18c4c529ff&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-132405324-null-null.142^v102^pc_search_result_base2&utm_term=YOLOv8%E6%94%B9%E8%BF%9B%E2%80%94%E2%80%94%E5%BC%95%E5%85%A5%E5%8F%AF%E5%8F%98%E5%BD%A2%E5%8D%B7%E7%A7%AFDCNv3&spm=1018.2226.3001.4187

## 开始使用
### 环境安装
```
pip uninstall ultralytics
cd ultralytics\ops_dcnv3
python setup.py install
```
**注意一定要卸载ultralytics包**

若setup.py安装出现问题，请升级gcc至8.0及以上版本（Linux）

### 训练及预测
自行配置并运行主目录中的train.py和predict.py
详情见https://github.com/ultralytics/ultralytics
