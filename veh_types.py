import traci

# 1. 集中定义各车型的差异化参数（参数项可以完全不一致）
VEHICLE_TYPES = {
    "veh_1": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 3.5,   # 加速性能
        "decel": 4.5,   # 减速性能
        "emergencyDecel": 9.0,  # 急刹车减速性能
        "maxSpeed": 41.0,   # 车辆物理最大速度
        "speedFactor": 1.2, # 根据道路限速缩放速度上限
        "color": (255, 0, 0, 255),

        # 跟车与间隙参数
        "minGap": 2,
        "tau": 0.2,

        "laneChangeModel": {
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 3,   # 变道强硬度
            "lcCooperative": -1.0,   # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 5.0, # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 0.5, # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 0.0, # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },
    "veh_2": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 3.5,  # 加速性能        "tau": 1.0,
        "decel": 4.5,  # 减速性能
        "emergencyDecel": 9.0,  # 急刹车减速性能
        "maxSpeed": 41.0,  # 车辆物理最大速度
        "speedFactor": 1.2,  # 根据道路限速缩放速度上限

        # 跟车与间隙参数
        "minGap": 2,
        "tau": 0.4,

        "laneChangeModel":{
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 2,  # 变道强硬度
            "lcCooperative": 0.0,  # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 3.0,  # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 0.5,  # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 0.0,  # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },
    "veh_3": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 3,  # 加速性能
        "decel": 4.5,  # 减速性能
        "emergencyDecel": 9.0,  # 急刹车减速性能
        "maxSpeed": 39.0,  # 车辆物理最大速度
        "speedFactor": 1.1,  # 根据道路限速缩放速度上限

        # 跟车与间隙参数
        "minGap": 2,
        "tau": 0.5,

        "laneChangeModel": {
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 1,  # 变道强硬度
            "lcCooperative": 0.5,  # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 2.0,  # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 0.5,  # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 0.0,  # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },
    "veh_4": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 2.5,  # 加速性能
        "decel": 4.5,  # 减速性能
        "emergencyDecel": 9.0,  # 急刹车减速性能
        "maxSpeed": 37.0,  # 车辆物理最大速度
        "speedFactor": 1.0,  # 根据道路限速缩放速度上限
        "color": (255, 0, 255, 255),

        # 跟车与间隙参数
        "minGap": 2,
        "tau": 1.0,

        "laneChangeModel": {
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 1,  # 变道强硬度
            "lcCooperative": 1.0,  # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 1.0,  # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 1.0,  # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 1.0,  # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },
    "veh_5": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 2.0,  # 加速性能
        "decel": 4.5,  # 减速性能
        "emergencyDecel": 9.0,  # 急刹车减速性能
        "maxSpeed": 37.0,  # 车辆物理最大速度
        "speedFactor": 0.9,  # 根据道路限速缩放速度上限

        # 跟车与间隙参数
        "minGap": 2,
        "tau": 1.5,

        "laneChangeModel": {
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 0.5,  # 变道强硬度
            "lcCooperative": 1.0,  # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 0.5,  # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 3.0,  # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 1.0,  # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },
    "veh_6": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 2.0,  # 加速性能
        "decel": 4.5,  # 减速性能
        "emergencyDecel": 9.0,  # 急刹车减速性能
        "maxSpeed": 37.0,  # 车辆物理最大速度
        "speedFactor": 0.7,  # 根据道路限速缩放速度上限

        # 跟车与间隙参数
        "minGap": 2,
        "tau": 3.0,

        "laneChangeModel": {
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 1.0,  # 变道强硬度
            "lcCooperative": 1.0,  # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 1.0,  # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 1.0,  # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 1.0,  # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },

    "veh_7": {
        # 车辆物理参数
        "length": 4.5,
        "accel": 2.0,  # 加速性能
        "decel": 4.5,  # 减速性能
        "emergencyDecel": 7.0,  # 急刹车减速性能
        "maxSpeed": 41.0,  # 车辆物理最大速度
        "speedFactor": 0.7,  # 根据道路限速缩放速度上限
        "color": (0, 0, 255, 255),

        # 跟车与间隙参数
        "minGap": 4,
        "tau": 1.5,

        "laneChangeModel": {
            # 变道模型参数 (基于默认 LC2013 模型)
            "lcAssertive": 3.0,  # 变道强硬度
            "lcCooperative": -1.0,  # 协作变道意愿，越小越不协助它车变道，越利己
            "lcSpeedGain": 0.5,  # 速度收益权重，越大越急切，为了更快频繁超车
            "lcStrategic": 0.5,  # 控制车辆为了“驶入正确出口/匝道/转向车道”而提前变道的积极程度，越大越早进入最右侧车道等待
            "lcKeepRight": 0.0,  # 控制车辆在超车后“返回慢车道（或靠右行驶）”的意愿强度
        }
    },



}


def register_veh_types(veh_types):
    for veh_type_id, params in veh_types.items():
        traci.vehicletype.copy(
            "DEFAULT_VEHTYPE",
            veh_type_id
        )

        # 遍历该车型独有的参数项
        for attr_name, value in params.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    traci.vehicletype.setParameter(objectID=veh_type_id, key=f"{attr_name}.{subkey}", value=str(subvalue))
            else:
                # 处理通用属性设置（如 setLength, setMaxSpeed）
                set_method_name = f"set{attr_name[0].upper()}{attr_name[1:]}"

                if hasattr(traci.vehicletype, set_method_name):
                    method = getattr(traci.vehicletype, set_method_name)
                    method(veh_type_id, value)

                else:
                    print(f"警告: traci.vehicletype 没有找到方法 {set_method_name}，参数{attr_name}无法设置")
