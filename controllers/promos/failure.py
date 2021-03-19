from magnebot import ActionStatus, Arm
from transport_challenge.promo_controller import PromoController


class Failure(PromoController):
    """
    Demo of a Magnebot trying an failing to do a task.
    """

    def init_scene(self, scene: str = "1a", layout: int = 1, room: int = 0, goal_room: int = None,
                   random_seed: int = 0) -> ActionStatus:
        super().init_scene(scene=scene, layout=layout, room=room, random_seed=random_seed)
        # Move a target object under a chair.
        self._next_frame_commands.append({"$type": "teleport_object",
                                          "id": self.target_objects[0],
                                          "position": {"x": -0.689, "y": 0, "z": 2.567}})
        self._end_action()
        return ActionStatus.success


if __name__ == "__main__":
    m = Failure(images_directory="D:/transport_challenge_failure_demo")
    m.init_scene()
    target = m.target_objects[0]
    # Add an overhead camera. Note that `position` is relative to the Magnebot, not absolute worldspace coordinates.
    m.add_camera(position={"x": -1.64, "y": 1.6, "z": -0.166}, look_at=True, follow=True)
    # Collide with a chair.
    m.move_to(target=target)
    # Back away from the chair.
    m.move_by(-0.5, stop_on_collision=False)
    # Run into the chair again.
    m.move_to(target=target)
    # Run into it a little more.
    m.move_by(0.3, stop_on_collision=False)
    # Back up.
    m.move_by(-0.6, stop_on_collision=False)
    # Go around the chair.
    m.turn_by(-35)
    m.move_by(1.4, stop_on_collision=False)
    m.turn_to(target=target, stop_on_collision=False)
    # Collide with the table leg or chair.
    m.move_by(0.8, stop_on_collision=False)
    # Try to pick up the object. This sometimes succeeds, and sometimes doesn't (due to Unity physics).
    status = m.pick_up(target=target, arm=Arm.right)
    if status != ActionStatus.success:
        m.pick_up(target=target, arm=Arm.left)
    # Back away from the table.
    m.move_by(-0.8, stop_on_collision=False)
    m.end()
