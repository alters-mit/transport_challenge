from magnebot import ActionStatus, Arm
from transport_challenge.promo_controller import PromoController


class Failure(PromoController):
    """
    Demo of a Magnebot trying an failing to do a task.
    """

    def init_scene(self, scene: str = "1a", layout: int = 1, room: int = 0, goal_room: int = None,
                   random_seed: int = 0) -> ActionStatus:
        super().init_scene(scene=scene, layout=layout, room=room, random_seed=random_seed)
        # Move a target object under a chair and another target object nearby on the floor.
        self._next_frame_commands.extend([{"$type": "teleport_object",
                                           "id": self.target_objects[0],
                                           "position": {"x": -0.689, "y": 0, "z": 2.567}},
                                          {"$type": "teleport_object",
                                           "id": self.target_objects[1],
                                           "position": {"x": -1.34, "y": 0, "z": 1.894}}])
        self._end_action()
        return ActionStatus.success


if __name__ == "__main__":
    m = Failure(images_directory="D:/transport_challenge_failure_demo", screen_height=1024, screen_width=1024)
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
    # Go around the chair.
    m.move_by(-0.8, stop_on_collision=False)
    m.move_to(target={"x": -0.448, "y": 0, "z": 1.605}, stop_on_collision=False)
    m.turn_to(target=target, stop_on_collision=False)
    # Collide with the table leg or chair.
    m.move_by(0.8, stop_on_collision=False)
    # Try to pick up the object. This sometimes succeeds, and sometimes doesn't (due to Unity physics).
    m.grasp(target=target, arm=Arm.right)
    # Immediately drop the object to simulate a failure.
    if target in m.state.held[Arm.right]:
        m.drop(target=target, arm=Arm.right, wait_for_objects=False)
    m.reset_arm(arm=Arm.right)
    m.move_by(-0.2, arrived_at=0.05, stop_on_collision=False)
    m.pick_up(target=target, arm=Arm.right)
    m.move_by(-0.8, stop_on_collision=False)
    target = m.target_objects[1]
    m.move_to(target=target, stop_on_collision=False)
    m.pick_up(target=target, arm=Arm.left)
    m.move_by(0.5)
    m.end()
