from tdw.tdw_utils import TDWUtils
from magnebot import ActionStatus
from transport_challenge import Transport


class ContainerCollision(Transport):
    """
    Test collisions between the Magnebot and a container.
    """

    def init_scene(self, scene: str = None, layout: int = None, room: int = None,
                   goal_room: int = None, random_seed: int = 0) -> ActionStatus:
        commands = [{"$type": "load_scene",
                     "scene_name": "ProcGenScene"},
                    TDWUtils.create_empty_room(12, 12)]
        self._add_container(model_name="basket_18inx18inx12iin",
                            position={"x": 0.235, "y": 0, "z": 1.5})
        self._add_container(model_name="basket_18inx18inx12iin",
                            position={"x": 0.235, "y": 1, "z": 1.25})
        commands.extend(self._get_scene_init_commands())
        resp = self.communicate(commands)
        self._cache_static_data(resp=resp)
        # Wait for the Magnebot to reset to its neutral position.
        status = self._do_arm_motion()
        self._end_action()
        return status


if __name__ == "__main__":
    m = ContainerCollision(launch_build=False, random_seed=0, skip_frames=0)
    m.init_scene()
    print(m.move_by(8))
    print(m.turn_by(70))
    print(m.turn_by(-70))
    print(m.move_by(-8))
    m.end()
