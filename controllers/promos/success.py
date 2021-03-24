from transport_challenge import Transport
from magnebot import Arm
from tdw.tdw_utils import TDWUtils

"""
An example of the Magnebot successfully completing a transport task.
"""

if __name__ == '__main__':
    m = Transport(launch_build=False, screen_width=1024, screen_height=1024, fov=90)
    m.init_scene(scene="5a", layout=2, random_seed=9420)
    m.add_camera(position={"x": -2, "y": 0.75, "z": 0}, look_at=True, follow=True)
    # This is the closest container.
    m.move_to(target=m.containers[0])
    m.pick_up(target=m.containers[0], arm=Arm.right)
    # Go to the other room.
    for waypoint in [[-4.91, 0, -0.73], [-4.91, 0, 1.09]]:
        m.move_to(target=TDWUtils.array_to_vector3(waypoint))
    # Pick up some objects.
    for target_object_index in [1, 5, 0]:
        m.move_to(target=m.target_objects[target_object_index], stop_on_collision=False)
        m.pick_up(target=m.target_objects[target_object_index], arm=Arm.left)
        m.put_in()
    # Go to the other room.
    for waypoint in [[-0.49, 0, 4.49], [1.23, 0, 4.49]]:
        m.move_to(target=TDWUtils.array_to_vector3(waypoint))
    # Move to the table.
    for waypoint in [[3.44, 0, 3.09], [4.49, 0, 2.58]]:
        m.move_to(target=TDWUtils.array_to_vector3(waypoint))
    m.pour_out()
    m.reset_arm(arm=Arm.right)
    m.move_by(-1)
    m.end()
