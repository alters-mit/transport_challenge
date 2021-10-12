# Transport Challenge

In the Transport Challenge API, the [**Magnebot**](https://github.com/alters-mit/magnebot) must transport **target objects** (small objects scattered throughout the scene) with the aid of **containers** (box-shaped objects without lids that can hold target objects) to the **goal zone** (a circle defined by a position and a radius in the center of a room and the scene).

If all of the target objects are in the goal zone, the task is successful.

**[Read the API documentation here.](https://github.com/alters-mit/transport_challenge/blob/main/doc/transport_controller.md)**

The Transport Challenge API is an extension of the [Magnebot API](https://github.com/alters-mit/magnebot) which in turn is built on the [TDW simulation platform](https://github.com/threedworld-mit/tdw).

<img src="doc/images/api_hierarchy.png" style="zoom:50%;" />

# Installation

Check if you've already installed `magnebot` or `tdw` on your computer: if `pip3 show magnebot` or `pip3 show tdw` prints any text, then the module is installed.

If `magnebot` or `tdw` is *not* already installed on this computer:

1. [Download TDW build v1.8.7](https://github.com/threedworld-mit/tdw/releases/tag/v1.8.7)
2. `git clone https://github.com/alters-mit/transport_challenge.git`
3. `cd transport_challenge` 
4. `pip3 install -e .` This will install all underlying modules, including `magnebot` and `tdw`
5. Make sure that the underlying TDW system is working correctly. See: [Getting Started With TDW](https://github.com/threedworld-mit/tdw/blob/master/Documentation/getting_started.md#Requirements) ***Ignore warnings about upgrading TDW!***

If `magnebot` or `tdw` *is* already installed on this computer:

1. `pip3 uninstall magnebot`
2. `pip3 uninstall tdw`
3. `pip3 unintall ikpy`
4. [Download TDW build v1.8.7](https://github.com/threedworld-mit/tdw/releases/tag/v1.8.7)
5. `git clone https://github.com/alters-mit/transport_challenge.git`
6. `cd transport_challenge` 
7. `pip3 install -e .` This will install all underlying modules, including `magnebot` and `tdw`
8. Make sure that the underlying TDW system is working correctly. See: [Getting Started With TDW](https://github.com/threedworld-mit/tdw/blob/master/Documentation/getting_started.md#Requirements) ***Ignore warnings about upgrading TDW!***

# Usage

1. Run this controller: `python3 controller.py` If you're running on an IBM server, you'll need to set a custom S3 bucket for the scenes, models, and materials: `TRANSPORT_CHALLENGE=https://bucket_url python3 controller`

```python
from transport_challenge import Transport

m = Transport()
# Initializes the scene.
status = m.init_scene(scene="2a", layout=1)
print(status)  # ActionStatus.success

# Prints a list of all container IDs.
print(m.containers)
# Prints a list of all target object IDs.
print(m.target_objects)

m.end()
```

2. [Launch the TDW build.](https://github.com/threedworld-mit/tdw/blob/master/Documentation/getting_started.md)

# Documentation

- **[API documentation](https://github.com/alters-mit/transport_challenge/blob/main/doc/transport_controller.md)**
- [Changelog](https://github.com/alters-mit/transport_challenge/blob/main/doc/changelog.md)

# Example controllers

- [This controller](https://github.com/alters-mit/transport_challenge/tree/main/controllers/examples/single_room.py) is an *example use-case*. It uses very naive logic to navigate (it assumes that everything is in the same room and that there aren't obstructions between objects) but it should be a good example of how to use this API.
- [This controller](https://github.com/alters-mit/transport_challenge/tree/main/controllers/demos/demo.py) is a *promo controller*. It is visually indicative of an actual use-case and includes an overhead camera so that it's easy to see what's going on. However, this controller includes a lot of code that you shouldn't add to your controller because it's unnecessary, inflexible, and slow.
- [These controllers](https://github.com/alters-mit/transport_challenge/tree/main/controllers/tests) are *test controllers*. They are meant only for testing the API.
