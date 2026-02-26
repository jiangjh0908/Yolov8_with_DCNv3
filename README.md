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

### 对比实验
**数据集**：**GC10-DET钢板表面缺陷数据集**

| 模型配置 | 参数量 (Parameters) | 计算量 (GFLOPs) | 推理速度 (ms/im) | 预处理 (ms) | 后处理 (ms) |
|:--------:|:-------------------:|:---------------:|:-----------------:|:-----------:|:-----------:|
| **YOLOv8m + DCNv3 (backbone)** | **25.59M** | **78.8** | **4.0** | 0.2 | 0.2 |
| YOLOv8m (baseline) | 25.85M | 78.7 | 2.7 | 0.2 | 0.4 |
| **对比** | **-0.26M** | **+0.1** | **+1.3ms** | 0 | **-0.2ms** |


| 缺陷类别 | YOLOv8m + DCNv3 (mAP50) | YOLOv8m + DCNv3 (mAP50-95) | YOLOv8m (mAP50) | YOLOv8m (mAP50-95) | 涨点幅度 (mAP50) | 涨点幅度 (mAP50-95) |
|:--------:|:-----------------------:|:--------------------------:|:----------------:|:-------------------:|:-----------------:|:-------------------:|
| **全部 (all)** | **0.563** | **0.279** | **0.535** | **0.255** | **+2.8%** | **+2.4%** |
| crazing (轧制氧化皮) | 0.947 | 0.535 | 0.978 | 0.578 | -3.1% | -4.3% |
| inclusion (夹杂物) | 0.882 | 0.314 | 0.535 | 0.161 | **+34.7%** | **+15.3%** |
| patches (斑块) | 0.894 | 0.625 | 0.946 | 0.658 | -5.2% | -3.3% |
| pitted_surface (麻点表面) | 0.841 | 0.449 | 0.843 | 0.433 | -0.2% | +1.6% |
| rolled-in_scale (轧入氧化皮) | 0.505 | 0.210 | 0.547 | 0.241 | -4.2% | -3.1% |
| scratches (划痕) | 0.605 | 0.261 | 0.580 | 0.231 | **+2.5%** | **+3.0%** |
| gouges (凿槽) | 0.322 | 0.107 | 0.319 | 0.099 | **+0.3%** | **+0.8%** |
| blow_hole (气孔) | 0.241 | 0.109 | 0.185 | 0.057 | **+5.6%** | **+5.2%** |
| kinking (折弯) | 0.380 | 0.174 | 0.367 | 0.085 | **+1.3%** | **+8.9%** |
| breakage (断裂) | 0.0157 | 0.0076 | 0.0542 | 0.0124 | -3.85% | -0.48% |

### 总结
**DCNv3最适合检测形状不规则、边界模糊、需要精确定位的小目标和变形物体，在工业缺陷检测、医学图像分析等场景具有显著优势，但对规则形状和大面积物体的检测效果可能不如传统卷积。**
