from pathlib import Path
from typing import List
import numpy as np
from tdw.tdw_utils import TDWUtils
from magnebot import ActionStatus, Arm
from transport_challenge import Transport


class SingleRoom(Transport):
    """
    This is an example of how to pick up target objects, put them in a container, and transport them to a goal zone.
    This example does _not_ describe how to implement navigation in the Transport Challenge.
    """

    def get_container(self) -> int:
        """
        This is a VERY naive approach to finding a nearby container. It just returns the nearest one.

        :return: The ID of the nearest container.
        """

        return self._get_nearest(object_ids=self.containers)

    def get_target_object(self) -> int:
        """
        This is a VERY naive approach to finding a nearby target object. It just returns the nearest one.

        :return: The ID of the nearest target object.
        """

        return self._get_nearest(object_ids=self.target_objects)

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
                print("Failed to pick up a container. Trying again...")
                # Back up and try again.
                # This isn't a very robust approach.
                # In an actual use-case, the actions will vary depending on the position of the object,
                # the position of the Magnebot, etc.
                self.move_by(-0.5)
                self.turn_by(15)
                self.move_to(target=container_id)

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
        status = self.move_to(target=object_id)

        # Back up and try again.
        direction = 1
        num_attempts = 0
        while status != ActionStatus.success and num_attempts < 10:
            print(f"Failed to pick up target object {object_id}. Trying again...")
            self.move_by(-0.5)
            self.turn_by(15 * direction)
            # Alternate the direction.
            direction *= -1
            # Try to go to the object again.
            status = self.move_to(target=object_id)
            num_attempts += 1
        if status != ActionStatus.success:
            print(f"Failed to move to target object {object_id}: {status}")
            return False
        print(f"Moved to target object {object_id}")
        status = self.pick_up(target=object_id, arm=Arm.left)
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

    def _get_nearest(self, object_ids: List[int]) -> int:
        """
        Get the nearest object from a list of object IDs.

        :return: The nearest object in the list.
        """

        nearest = -1
        nearest_distance = np.inf
        for object_id in object_ids:
            distance = np.linalg.norm(self.state.object_transforms[object_id].position -
                                      self.state.magnebot_transform.position)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest = object_id
        return nearest


if __name__ == "__main__":
    # Instantiate the controller.
    # For this example, we set the random seed so that we know where the target objects and containers will be.
    m = SingleRoom(launch_build=False, random_seed=12, auto_save_images=True)
    print(f"Images will be saved to: {Path(m.images_directory).resolve()}")

    # We know that there are target objects and a container in this room because of the random seed in the constructor.
    m.init_scene(scene="5a", layout=2, room=2, goal_room=2)

    m.pick_up_container()

    # Put an object in the container.
    in_container = m.put_object_in_container(object_id=m.get_target_object())
    assert in_container

    # If the container is mostly full, bring it to the goal position and pour it out.
    print("Bringing target object to the goal zone.")
    m.move_to(target=TDWUtils.array_to_vector3(m.goal_position))
    m.pour_out()
    print("Poured out objects.")
    num_in_container = 0

    # Not all of the objects that were in the container are in the goal zone.
    # They might have bounced or rolled away.
    print(f"Objects in the goal zone: {m.get_target_objects_in_goal_zone()}")
    print(f"Action cost: {m.action_cost}")
    m.end()
