from typing import Any
import random
import traci

from veh_types import VEHICLE_TYPES, register_veh_types
from humanity import Humanity

class Vehicle:
    def __init__(self, veh_type_id, base_attrs: dict[str, Any], lc_model_attrs: dict[str, Any], humanity: Humanity):
        self.veh_type_id = veh_type_id
        self.base_attrs = base_attrs
        self.lc_model_attrs = lc_model_attrs
        self.humanity = humanity
        self.register_veh_type()

    def register_veh_type(self):
        traci.vehicletype.copy("DEFAULT_VEHTYPE", self.veh_type_id)
        # ### 设置基本参数
        for attr_name, value in self.base_attrs.items():
            set_method_name = f"set{attr_name[0].upper()}{attr_name[1:]}"
            if hasattr(traci.vehicletype, set_method_name):
                method = getattr(traci.vehicletype, set_method_name)
                method(self.veh_type_id, value)
            else:
                print(f"警告: traci.vehicletype 没有找到方法 {set_method_name}，参数{attr_name}无法设置")

        # ### 设置变道参数
        for attr_name, value in self.lc_model_attrs.items():
            traci.vehicletype.setParameter(objectID=self.veh_type_id, key=f"laneChangeModel.{attr_name}",
                                           value=str(value))

class SimpleVehicle:
    def __init__(self, veh_id, type_id, humanity: Humanity):
        self.veh_id = veh_id
        self.type_id = type_id
        self.humanity = humanity

    def update(self, now):
        self.humanity(now)

    def __call__(self, *args, **kwargs):
        self.update(*args, **kwargs)


class VehicleCreator:
    def __init__(self, entrance_edge, per_hour, exit_edges: dict[str, float], vehicle_types: dict[str, float]):
        self.entrance_edge = entrance_edge
        self.per_hour = per_hour
        self.vehicle_interval = 3600.0 / per_hour   # 生成车辆间隔
        self.next_vehicle_time = 0.0
        # self.exit_edges = self.get_reachable_exits(entrance_edge, exit_edges)
        self.exit_edges = exit_edges


        self.vehicle_types = vehicle_types
        self._veh_types = tuple(vehicle_types.keys())
        self._veh_probabilities = tuple(vehicle_types.values())

        self._edge_id_str = str(entrance_edge)
        self._vehicle_counter = 0
        self._route_counter = 0

    def run(self, simu_time):
        if simu_time >= self.next_vehicle_time:
            self.next_vehicle_time += self.vehicle_interval
            return self.create_vehicle()
        return None

    def create_vehicle(self):
        """
        创建一辆车辆，并随机选择出口
        """
        vehicle_id = f"car_{self._edge_id_str}_{self._vehicle_counter}"
        self._vehicle_counter += 1
        # 随机选择出口
        exit_edge = self.choose_exit()
        # 计算入口 -> 出口的最短路线
        route = traci.simulation.findRoute(fromEdge=self.entrance_edge, toEdge=exit_edge)
        if not route.edges:
            print(
                f"警告：找不到 {self.entrance_edge} -> {exit_edge} 的路线"
            )
            return

        # ### 创建 route
        route_id = f"route_{self.entrance_edge}_{self._route_counter}"
        self._route_counter += 1
        traci.route.add(routeID=route_id, edges=route.edges)

        # 创建车辆
        veh_type = random.choices(self._veh_types, weights=self._veh_probabilities)[0]
        traci.vehicle.add(typeID=veh_type, vehID=vehicle_id, routeID=route_id)
        print(f"创建车辆: {veh_type}：{vehicle_id} -> {exit_edge}")
        return SimpleVehicle(vehicle_id, veh_type, Humanity(vehicle_id))

    def choose_exit(self):
        """
        根据概率随机选择一个出口
        """
        exit_edges_name = tuple(self.exit_edges.keys())
        exit_edges_probabilities = tuple(self.exit_edges.values())
        return random.choices(
            exit_edges_name,
            weights=exit_edges_probabilities,
            k=1
        )[0]

    @staticmethod
    def get_reachable_exits(entrance_edge, exit_candidates: dict[str, float]):
        reachable = {}
        for exit_edge in tuple(exit_candidates.keys()):
            try:
                route = traci.simulation.findRoute(
                    fromEdge=entrance_edge,
                    toEdge=exit_edge
                )

                if route.edges and route.edges[-1] == exit_edge:
                    reachable[exit_edge] = exit_candidates[exit_edge]

            except traci.TraCIException:
                pass

        return reachable

    def __call__(self, simu_time):
        return self.run(simu_time)



entrance_edges = ["E0", "E1", "E5", "E7", "E9"]
e0_exit_edges = {
    "E3": 0.1,
    "E6": 0.2,
    "E8": 0.2,
    "E10": 0.2,
    "E0.8629": 0.3,
}

e1_exit_edges = {
    "E3": 0.1,
    "E6": 0.2,
    "E8": 0.2,
    "E10": 0.2,
    "E0.8629": 0.3,
}

e5_exit_edges = {
    "E6": 0.2,
    "E8": 0.2,
    "E10": 0.2,
    "E0.8629": 0.4,
}

e7_exit_edges = {
    "E8": 0.2,
    "E10": 0.2,
    "E0.8629": 0.6,
}

e9_exit_edges = {
    "E10": 0.2,
    "E0.8629": 0.8,
}

entrance_edges_dict = {
    "E0": e0_exit_edges,
    "E1": e1_exit_edges,
    "E5": e5_exit_edges,
    "E7": e7_exit_edges,
    "E9": e9_exit_edges,
}


SUMO_CONFIG = "run.sumocfg"
SUMO_BINARY = "sumo-gui"
# 仿真时间
SIMULATION_TIME = 3600       # 秒，1小时

# ### 如果希望每次运行得到相同的随机结果，可以设置 seed
random.seed(59)

# ### 启动 SUMO
sumo_cmd = [
    SUMO_BINARY,
    "-c",
    SUMO_CONFIG,
    "--seed",
    "42",
    "--end",
    str(SIMULATION_TIME),
    # 输出车辆行程统计
    "--tripinfo-output",
    "run/tripinfo.xml",
]
print("启动 SUMO...")
traci.start(sumo_cmd)
print("SUMO 启动成功")
# ### 注册车辆类型
register_veh_types(VEHICLE_TYPES)
# ### 仿真主循环
all_vehicles = {}
# 每个类型车出现的概率
VEHICLE_TYPE_PROBABILITIES = [0.05, 0.2, 0.4, 0.2, 0.05, 0.05, 0.05]
vehicle_types_id_dict = {k: v for k, v in zip(tuple(VEHICLE_TYPES.keys()), VEHICLE_TYPE_PROBABILITIES)}
vehicle_creator_list = [VehicleCreator(e, 1200, exit_edges, vehicle_types_id_dict) for e, exit_edges in entrance_edges_dict.items()]

# ### 统计数据
# 记录每辆车的车型、进入时间
vehicle_info = {}
# 各车型累计平均通行速度（m/s）
speed_sum = {veh_type: 0.0 for veh_type in VEHICLE_TYPES.keys()}
# 各车型完成通行的车辆数
vehicle_count = {veh_type: 0 for veh_type in VEHICLE_TYPES.keys()}

try:
    while (current_time := traci.simulation.getTime()) < SIMULATION_TIME:
        # ### 生成车辆
        for vehicle_creator in vehicle_creator_list:
            vehicle = vehicle_creator(current_time)
            if vehicle is not None:
                all_vehicles[vehicle.veh_id] = vehicle
        # ### 推进 SUMO 一个 simulation step
        traci.simulationStep()
        ### 剔除离网车辆
        active_vehicles = set(traci.vehicle.getIDList())
        all_vehicles = {k: v for k, v in all_vehicles.items() if k in active_vehicles}
        # ### 车辆动作
        for veh in all_vehicles.values():
            veh(current_time)

finally:
    print("关闭 SUMO...")
    traci.close()

# ### 输出统计结果
print()
print("=" * 50)
print("仿真结束")
print("=" * 50)
print()


import xml.etree.ElementTree as ET
from collections import defaultdict
# 每种车型的累计通行速度（m/s）
speed_sum = defaultdict(float)
# 每种车型完成通行的车辆数量
vehicle_count = defaultdict(int)
# 所有车型的总体统计
total_speed_sum = 0.0
total_distance = 0.0
total_duration = 0.0
total_vehicle_count = 0
# 读取 SUMO 输出的行程统计文件
tree = ET.parse("run/tripinfo.xml")
root = tree.getroot()

for trip in root.findall("tripinfo"):
    veh_type = trip.get("vType")

    duration = float(trip.get("duration"))
    distance = float(trip.get("routeLength"))

    if duration <= 0:
        continue

    # 单辆车平均通行速度（m/s）
    avg_speed = distance / duration

    # 按车型累计
    speed_sum[veh_type] += avg_speed
    vehicle_count[veh_type] += 1

    # 所有车型累计
    total_speed_sum += avg_speed
    total_distance += distance
    total_duration += duration
    total_vehicle_count += 1

# 输出统计结果
print("\n各车型平均通行速度")
print("=" * 50)

for veh_type in VEHICLE_TYPES.keys():
    count = vehicle_count[veh_type]

    if count > 0:
        avg_speed = speed_sum[veh_type] / count

        print(
            f"车型 {veh_type}: "
            f"平均通行速度 = {avg_speed * 3.6:.2f} km/h, "
            f"完成通行车辆数 = {count}"
        )
    else:
        print(f"车型 {veh_type}: 没有完成通行的车辆")

print("\n所有车型总体通行速度")
print("=" * 50)

if total_vehicle_count > 0:
    # 所有车辆平均通行速度的算术平均值
    avg_vehicle_speed = total_speed_sum / total_vehicle_count

    # 所有车辆总行驶距离 / 总通行时间
    overall_speed = total_distance / total_duration

    print(
        f"所有车辆平均速度的算术平均值: "
        f"{avg_vehicle_speed * 3.6:.2f} km/h"
    )

    print(
        f"所有车辆总体通行速度: "
        f"{overall_speed * 3.6:.2f} km/h"
    )

    print(f"完成通行车辆总数: {total_vehicle_count}")
else:
    print("没有完成通行的车辆")

print("=" * 50)