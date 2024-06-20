import inspect

import pyzed.sl as sl

# for k, v in inspect.getmembers(sl.VIDEO_SETTINGS):
#     print(f"{k}: {v}")
#     for k2, v2 in inspect.getmembers(v):
#         print(f"\t{k2}: {v2}")

zed = sl.Camera()
for k, v in inspect.getmembers(zed):
    if k.find("__") == -1:
        print(f"{k}: {v}")
        for k2, v2 in inspect.getmembers(v):
            if k2.find("__") == -1:
                print(f"\t{k2}: {v2}")