这是一个基于 **SUMO (Simulation of Urban MObility)** 和 **TraCI (Traffic Control Interface)** 的微观交通仿真 Python 项目。本项目通过引入差异化的车辆类型、动态路径生成以及自定义的“驾驶员人性化（Humanity）”行为层，实现了异质交通流（Heterogeneous Traffic Flow）的逼真模拟。

## 🌟 核心特点与功能

1. **车辆建模参数 (`veh_types.py`)**：

   * 将sumo车辆的基本属性和基于lc2013的变道参数规范化为一个2层结构的字典，便于人工配置车辆类型

2. **自定义“人性化”驾驶行为层 (`humanity.py`)**：

   * sumo内置车辆驾驶模型和lc2013变道模型实现不了我需要的细粒度和多因素驾驶行为，所以我使用python基于traci实现了一个Humanity类和sumo内置驾驶模型组成了更加强大的驾驶行为模型，目前实现了人类驾驶员的随机变道行为，后续还会实现人类情绪等维度

3. **动态路径与流量生成** ：

   * 为了在减少人工配置参数的情况下也能最大化控制车流，我编写了VehicleCreator类，可以通过配置少量形参实现自动预定义车流