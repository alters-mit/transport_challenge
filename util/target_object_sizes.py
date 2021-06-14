from csv import DictReader
import numpy as np
from tdw.librarian import ModelLibrarian
from tdw.tdw_utils import TDWUtils
from transport_challenge.paths import TARGET_OBJECTS_PATH

"""
Prints the sizes of each of the target objects.
"""

lib = ModelLibrarian()
with TARGET_OBJECTS_PATH.open("rt", encoding="utf-8") as f:
    reader = DictReader(f)
    for row in reader:
        record = lib.get_record(row["name"])
        # Get the bounds dimensions.
        width = np.linalg.norm(TDWUtils.vector3_to_array(record.bounds["left"]) -
                               TDWUtils.vector3_to_array(record.bounds["right"]))
        height = np.linalg.norm(TDWUtils.vector3_to_array(record.bounds["top"]) -
                                TDWUtils.vector3_to_array(record.bounds["bottom"]))
        length = np.linalg.norm(TDWUtils.vector3_to_array(record.bounds["front"]) -
                                TDWUtils.vector3_to_array(record.bounds["back"]))
        # Get the size times the scale.
        size = np.array([width, height, length]) * float(row["scale"])
        print(row["name"], size)
