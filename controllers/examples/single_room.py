from tdw.tdw_utils import TDWUtils
from magnebot import Magnebot, ActionStatus, Arm
from transport_challenge import Transport


class SingleRoom(Transport):
    """
    This is an example of how to pick up target objects, put them in a container, and transport them to a goal zone.
    This example does _not_ describe how to implement navigation in the Transport Challenge.
    """

    def get_container(self) -> int:
        """
        This is a VERY naive approach to finding a nearby container.
        The Magnebot will rotate around and record the IDs of each container it sees.

        :return: The ID of a container within visual range of the Magnebot.
        """

        d_turn: int = 90
        turn: int = 0
        while turn < 270:
            # Look around you.
            d_cam_theta = 45
            # First pitch the camera and then yaw the camera.
            for axis in ["pitch", "yaw"]:
                if axis == "pitch":
                    s = self.rotate_camera(pitch=-Magnebot.CAMERA_RPY_CONSTRAINTS[1])
                else:
                    s = self.rotate_camera(yaw=-Magnebot.CAMERA_RPY_CONSTRAINTS[2])
                # Rotate the camera until we get an ActionStatus that the angle has been clamped to the RPY constraints.
                # That means that we've rotated the camera as far as it will go.
                while s == ActionStatus.success:
                    visible_objects = self.get_visible_objects()
                    for object_id in visible_objects:
                        # We found a container.
                        if object_id in self.containers:
                            return object_id
                    # Keep rotating the camera.
                    if axis == "pitch":
                        s = self.rotate_camera(pitch=d_cam_theta)
                    else:
                        s = self.rotate_camera(yaw=d_cam_theta)
                self.reset_camera()
            # Turn the Magnebot.
            self.turn_by(d_turn)
            turn += d_turn
        raise Exception("No container found!")

    def pick_up_container(self) -> None:
        """
        Go to a container in the room and pick it up.
        """

        # Find a container in the room.
        container_id = self.get_container()
        # Go to the container and pick it up.
        self.move_to(target=container_id)
        # Try to pick up the container.
        got_container = False
        while not got_container:
            self.pick_up(target=container_id, arm=Arm.right)
            if container_id in self.state.held[Arm.right]:
                print("Picked up a container.")
                got_container = True
            else:
                self.reset_arm(arm=Arm.right)
                self.move_by(-0.5)
                self.turn_by(15)
                self.move_to(target=container_id)
                print("Failed to pick up a container. Trying again...")

    def put_object_in_container(self, object_id: int) -> bool:
        """
        Go to a target object, pick it up, and put it in the container.

        This is a VERY naive function because:

        - It assumes that the Magnebot is holding a container.
        - It doesn't handle navigation; it assumes that there is a clear path between the Magnebot and the object.
        - If the Magnebot fails to put the object in the container, it won't try again.

        :param object_id: The ID of the target object.

        :return: True if the Magnebot put the object in the container.
        """

        # Try to go to the object and pick it up.
        # This is a VERY naive navigation solution. It doesn't check for obstructions.
        # And, if the Magnebot fails to pick up the object, it will simply skip it.
        status = self.move_to(target=object_id)
        if status != ActionStatus.success:
            print(f"Failed to move to target object {object_id}: {status}")
            return False
        print(f"Moved to target object {object_id}")
        self.pick_up(target=object_id, arm=Arm.left)
        if object_id not in self.state.held[Arm.left]:
            print(f"Failed to pick up target object {object_id}: {status}")
            return False
        print(f"Picked up target object {object_id}")
        status = self.put_in()
        if status != ActionStatus.success:
            print(f"Failed to put target object {object_id} in the container: {status}")
            return False
        print(f"Put target object {object_id} in the container.")
        return True


if __name__ == "__main__":
    # Instantiate the controller.
    # For this example, we set the random seed so that we know where the target objects and containers will be.
    m = SingleRoom(launch_build=False, random_seed=12)

    # We know that there are target objects and a container in this room because of the random seed in the constructor.
    m.init_scene(scene="5a", layout=2, room=2, goal_room=2)

    m.pick_up_container()

    num_in_container = 0
    # Transport objects to the goal position.
    for target_object in m.target_objects:
        # If the container is mostly full, bring it to the goal position and pour it out.
        if num_in_container == 3:
            print("Bringing target objects to the goal zone.")
            m.move_to(target=TDWUtils.array_to_vector3(m.goal_position))
            m.pour_out()
            print("Poured out objects.")
            num_in_container = 0
            break
        # Check if we're done now.
        if m.done:
            print("DONE!")
            print(f"Number of actions: {m.num_actions}")
            break

        in_container = m.put_object_in_container(object_id=target_object)
        if in_container:
            # Record the object as being in the container.
            num_in_container += 1
    m.end()