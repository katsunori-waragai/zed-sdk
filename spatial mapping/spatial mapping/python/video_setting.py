import inspect

import pyzed.sl as sl

for k, v in inspect.getmembers(sl.VIDEO_SETTINGS):
    print(f"{k}: {v}")
