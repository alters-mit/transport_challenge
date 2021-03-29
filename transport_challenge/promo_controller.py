from typing import Dict, List, Union
from pathlib import Path
from tdw.tdw_utils import TDWUtils
from tdw.output_data import OutputData, Images
from magnebot import ActionStatus
from transport_challenge import Transport


class PromoController(Transport):
    """
    This class is meant to be used for generating promo videos.
    It will automatically save every image per physics simulation step (NOT per-action) from 1-2 cameras (Magnebot and/or overhead).
    This means that this controller will run very slowly.
    """

    def __init__(self, port: int = 1071, screen_width: int = 1024, screen_height: int = 1024,
                 images_directory: str = "images", image_pass_only: bool = False, overhead_camera_only: bool = False,
                 random_seed: int = None):
        super().__init__(port=port, launch_build=False, screen_width=screen_width, screen_height=screen_height,
                         auto_save_images=False, debug=False, images_directory=images_directory, random_seed=random_seed,
                         img_is_png=False, skip_frames=0)

        self.image_directories: Dict[str, Path] = dict()
        self.image_pass_only = image_pass_only
        self.overhead_camera_only = overhead_camera_only
        if not overhead_camera_only:
            self._create_images_directory(avatar_id="a")

        self._image_count = 0

    def add_camera(self, position: Dict[str, float], roll: float = 0, pitch: float = 0, yaw: float = 0,
                   look_at: bool = True, follow: bool = False, camera_id: str = "c") -> ActionStatus:
        """
        See: `Magnebot.add_camera()`.

        Adds some instructions to render images per-frame.
        """

        self._create_images_directory(avatar_id=camera_id)
        status = super().add_camera(position=position, roll=roll, pitch=pitch, yaw=yaw, look_at=look_at, follow=follow,
                                    camera_id=camera_id)
        # Always save images.
        if not self._debug:
            if self.overhead_camera_only:
                self._per_frame_commands.extend([{"$type": "enable_image_sensor",
                                                  "enable": True},
                                                 {"$type": "send_images",
                                                  "ids": ["c"]}])
            else:
                self._per_frame_commands.extend([{"$type": "enable_image_sensor",
                                                  "enable": True},
                                                 {"$type": "send_images"}])
        return status

    def communicate(self, commands: Union[dict, List[dict]]) -> List[bytes]:
        """
        See `Magnebot.communicate()`.

        Images are saved per-frame.
        """

        resp = super().communicate(commands=commands)
        if not self._debug:
            # Save all images.
            got_images = False
            for i in range(len(resp) - 1):
                r_id = OutputData.get_data_type_id(resp[i])
                if r_id == "imag":
                    got_images = True
                    images = Images(resp[i])
                    avatar_id = images.get_avatar_id()
                    if avatar_id in self.image_directories:
                        TDWUtils.save_images(filename=TDWUtils.zero_padding(self._image_count, 8),
                                             output_directory=self.image_directories[avatar_id],
                                             images=images)
            if got_images:
                self._image_count += 1
        return resp

    def _create_images_directory(self, avatar_id: str) -> None:
        """
        :param avatar_id: The ID of the avatar.

        :return: An images directory for the avatar.
        """

        # Build the images directory.
        a_dir = self.images_directory.joinpath(avatar_id)
        if not a_dir.exists():
            a_dir.mkdir(parents=True)
        self.image_directories[avatar_id] = a_dir

    def _get_scene_init_commands(self, magnebot_position: Dict[str, float] = None) -> List[dict]:
        commands = super()._get_scene_init_commands(magnebot_position=magnebot_position)
        # Hide the roof.
        commands.append({"$type": "set_floorplan_roof",
                         "show": False})
        if self.image_pass_only:
            commands.append({"$type": "set_pass_masks",
                             "pass_masks": ["_img"]})
        return commands
