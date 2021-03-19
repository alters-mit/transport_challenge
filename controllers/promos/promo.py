from os import chdir
from typing import List
from pathlib import Path
from subprocess import call
from json import loads
import numpy as np
from tdw.tdw_utils import TDWUtils
from magnebot import ActionStatus, Arm
from transport_challenge.promo_controller import PromoController


class Demo(PromoController):
    """
    A demo of a Magnebot using a container to transport target objects to a new room.

    **This is NOT a use-case example.** It should only be used to generate a demo video of the Transport Challenge.

    Key differences:

    - Navigation is pre-calculated (see `PATH`).
    - Only the `img` pass is captured (not `id` or `depth`).
    - The screen is large, there is an overhead camera, and images are saved per-frame instead of per-action. This means that this controller will run *much* slower than a use-case controller.
    - There are some low-level commands to optimize the demo such as teleporting containers and target objects and hiding the roof.
    """

    # This is a pre-calculated path that the Magnebot will use to move between rooms.
    PATH: np.array = np.array([[6.396355, 0, -2.465405],
                               [5.41636, 0, -1.4854207],
                               [4.615, 0, -0.9954208],
                               [3.946356, 0, 0.66],
                               [0.4, 0, 0.66],
                               [0.02635, 0, -1.975]])

    def __init__(self, port: int = 1071, screen_width: int = 1024, screen_height: int = 1024,
                 images_directory: str = "images", image_pass_only: bool = False, overhead_camera_only: bool = False):
        super().__init__(port=port, screen_width=screen_width, screen_height=screen_height,
                         images_directory=images_directory, random_seed=16, image_pass_only=image_pass_only,
                         overhead_camera_only=overhead_camera_only)
        self._to_transport: List[int] = list()

    def init_scene(self, scene: str, layout: int, room: int = None, goal_room: int = None,
                   random_seed: int = None) -> ActionStatus:
        status = super().init_scene(scene=scene, layout=layout, room=room)

        self._to_transport = self.target_objects[:]
        return status

    def transport(self) -> None:
        """
        Transport some objects to the other room.
        """

        for i in range(4):
            # Get the closest object that still needs to be transported.
            self._to_transport = list(sorted(self._to_transport, key=lambda x: np.linalg.norm(
                self.state.object_transforms[x].position - self.state.magnebot_transform.position)))
            object_id = self._to_transport[0]
            # Go to the object and pick it up.
            self.move_to(target=object_id, stop_on_collision=False)
            self.pick_up(target=object_id, arm=Arm.right)
            # Put the object in the container.
            self.put_in()
            # Record this object as done.
            self._to_transport = self._to_transport[1:]

        # Follow the path to the other room.
        path = Demo.PATH[1:]
        for waypoint in path:
            self.move_to(target=TDWUtils.array_to_vector3(waypoint), stop_on_collision=False)
        self.pour_out()

    def go_to_start(self) -> None:
        """
        Navigate back to the start position.
        """

        path = np.flip(Demo.PATH[:-1], axis=0)
        for waypoint in path:
            self.move_to(target=TDWUtils.array_to_vector3(waypoint), stop_on_collision=False)

    def teleport_objects(self) -> None:
        """
        Teleport objects to where they should be for this demo.
        """

        data = loads(Path("init.json").read_text(encoding="utf-8"))
        # Iterate through the containers and the target objects.
        for k, lst in zip(["containers", "target_objects"], [self.containers, self.target_objects]):
            # Set the positions and rotations.
            for object_id, data_object_id in zip(lst, data[k]):
                object_data = data[k][data_object_id]
                self._next_frame_commands.extend([{"$type": "teleport_object",
                                                   "id": object_id,
                                                   "position": object_data["position"]},
                                                  {"$type": "rotate_object_to",
                                                   "id": object_id,
                                                   "rotation": object_data["rotation"]}])
        self._end_action()


if __name__ == "__main__":
    m = Demo(images_directory="D:/transport_challenge_demo", image_pass_only=True, overhead_camera_only=True)
    m.init_scene(scene="2a", layout=1, room=4)
    # Add an overhead camera.
    m.add_camera(position={"x": -3.6, "y": 8, "z": -0.67}, look_at=True, follow=True)

    m.teleport_objects()

    # Pick up the  container.
    m.move_to(target=m.containers[0])
    m.pick_up(target=m.containers[0], arm=Arm.left)

    # Pick up some objects and put them in another room.
    m.transport()
    # Go back to the starting room.
    m.go_to_start()
    m.end()

    # Create a video.
    if m.overhead_camera_only:
        chdir(str(m.image_directories["c"]))
        call(["ffmpeg.exe",
              "-r", "90",
              "-i", "img_%08d.jpg",
              "-vcodec", "libx264",
              "-pix_fmt", "yuv420p",
              str(m.images_directory.joinpath("transport_challenge_demo.mp4").resolve())])
