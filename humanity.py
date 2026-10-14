import random
import traci

class Humanity:
    def __init__(self, veh_id, update_interval: float=10):
        self.veh_id = veh_id

        self._update_interval = update_interval
        self._last_update_time = 0
        self._base_rand_lc_prob = 0.0 / 200
        self._keep_lane_sec = 0
        self._last_lc_time = 0

    def update(self, now):
        if self._last_update_time + self._update_interval > now:
            return
        self._keep_lane_sec += now - self._last_lc_time
        self._last_lc_time = now
        rand_lc_prob = self._base_rand_lc_prob * self._keep_lane_sec
        if random.random() < rand_lc_prob:
            if self.change_lane(duration=3.0):
                self._keep_lane_sec = 0

    def change_lane(self, duration):
        has_left_lane, has_right_lane = self.get_lane_info(self.veh_id)
        if has_left_lane and has_right_lane:
            target_lane = -1 if (random.random()) < 0.5 else 1
        elif has_left_lane or has_right_lane:
            target_lane = -1 if has_left_lane else 1
        else:
            return False

        print(f'{self.veh_id} Changing lane to => ', target_lane)
        traci.vehicle.changeLaneRelative(vehID=self.veh_id, indexOffset=target_lane, duration=duration)
        return True

    @staticmethod
    def get_lane_info(vehicle_id):
        # 剔除路口内部道路
        road_id = traci.vehicle.getRoadID(vehicle_id)
        if road_id.startswith(":"):
            return False, False

        # 当前车道索引
        lane_index = traci.vehicle.getLaneIndex(vehicle_id)
        # 当前道路的车道总数
        lane_count = traci.edge.getLaneNumber(road_id)
        # SUMO 通常是索引越大越靠左，0 为最右侧
        has_left_lane = lane_index < lane_count - 1
        has_right_lane = lane_index > 0

        return has_left_lane, has_right_lane

    def __call__(self, *args, **kwargs):
        self.update(*args, **kwargs)


