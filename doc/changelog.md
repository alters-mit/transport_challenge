# Changelog

## 0.3.7

- Fixed: Crash because Magnebot 1.1.1 is installed

## 0.3.6

- Requires: Magnebot 1.1.1 (was 1.1.2, which was incorrect)
- Requires: ikpy 3.1
- Added install instructions to the README for downgrading `magnebot` and `tdw`

## 0.3.5

- Fixed: README points to the wrong version of the build.

## 0.3.4

- Added: `util/target_object_sizes.py` Print the size of each target object.
- Documentation now includes the capacity of the containers.

## 0.3.3

- Requires: TDW 1.8.7.0

## 0.3.2

- **The Transport Challenge API requires Magnebot v1.1.2 and should NOT be upgraded past this version!**
  - pip will install the correct version of Magnebot
  - Added: `Transport.MAGNEBOT_VERSION` The required version of the Magnebot Python module
- Added: `promo_controller.y` Base class for promo controllers
- Added: `failure.py` Demo of the Magnebot failing a task
- Added: `success.py` Demo of the Magnebot succeeding at a task

## 0.3.1

- Fixed: Object URLs are not set correctly if the `TRANSPORT_CHALLENGE` environment variable is provided
- Fixed: `promo.py` doesn't work as intended due to collisions with containers

## 0.3.0

- Requires: Magnebot 1.1.0 (see changelog notes regarding collision detection)
  - Added optional parameter `stop_on_collision` to `move_by()`, `move_to()`, `turn_by()` and `turn_to()` Set this to False to ignore collision detection during the action
- Fixed: Crash-to-desktop because a container gets caught in the Magnebot's wheels. Now, the Magnebot will stop moving as soon as a wheel collides with a container.
- Added: `tests/container_collision.py`

## 0.2.3

- Added optional parameter `check_pypi_version` to the constructor
- Simplified the format of this changelog

## 0.2.2

- Added: Set the `TRANSPORT_CHALLENGE` environment variable to use an alternative S3 bucket URL.

## 0.2.1

- Added optional parameter `random_seed` to `init_scene()` to reset the random seed.

## 0.2.0

- Added `scipy` as a required module
- There are always 8 target objects in the scene (previously, there are 8-12 target objects)
- Target objects can spawn in any room (previously, they spawned in the same room)
- Fixed: Target objects sometimes spawn on the edges of the occupancy map
- Fixed: Containers sometimes spawn in very small rooms
- Added optional parameter `fov` to the constructor
- Simplified the logic of `single_room.py` and made it work with the changes in this update
- `promo.py` uses init data from `init.json` to reload its state

## 0.1.7

- Fixed: Default value of `img_is_png` is True (it's now False)

## 0.1.6

- Fixed: JSONDecodeError because version check doesn't work (version check for this module has been removed)

## 0.1.5

- Added license
- Default value of `skip_frames` is 10 (was 20)
- Renamed `controllers/demo/demo.py` to `controllers/promos/promo.py`

## 0.1.4

- `put_in()` will immediately stop moving the arm holding the object if the magnet or the object is within the container.
- Improved the speed of `put_in()` and `pour_out()`.
- Fixed: `put_in()` is too slow because the arm holding the object isn't sufficiently above the container.

## 0.1.3

- Added optional parameter `skip_frames` (required in Magnebot 0.4.0)
- Improved the speed of `put_in()`.
- Fixed: `pick_up()` doesn't reset the arm if the magnet fails to grasp the target object.
- Fixed: `pick_up()` often misses the object (it now aims for positions on the top of the object).
- Fixed: `put_in()` sometimes doesn't stop the Magnebot's wheels from turning.
- Fixed: `put_in()` often aims for the wrong target position above the container.
- Fixed: `pour_out()` sometimes doesn't stop the Magnebot's wheels from turning.
- Fixed: while objects are being dropped into a container during `put_in()`, they sometimes glitch (now they use the `discrete` collision detection mode).
- Fixed: `single_room.py` doesn't work. Added simple navigation to make multiple attempts to pick up the target object.
- Removed: `level.py`

## 0.1.2

- Set `launch_build` default value to False (was True)
- Fixed: `put_in()` often thinks that an object isn't in a container when it actually is.
- Fixed: `put_in()` sometimes fails because the magnet holding the target object is in the way. Now, the wrist of that magnet will tilt down, allowing for a clearer trajectory.
- Fixed: Sometimes in `put_in()` the arm that was holding the target object gets caught on the container. Now, the arm that was holding the target object resets first, rather than vice versa.
- Backend:
  - `_get_objects_in_container()` uses trigger event data (`self._trigger_events`) to determine if an object is in a container rather than `Overlap` output data. It no longer advances the simulation an extra frame.

## 0.1.1

- Added optional parameter `img_is_png` to the constructor
- Renamed `num_actions` to `action_cost`
- Added: `get_target_objects_in_goal_zone()`
- Cleaned up the code of `single_room.py`
- Added links to controllers in README