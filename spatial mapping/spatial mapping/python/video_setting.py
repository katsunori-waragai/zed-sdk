import inspect

import pyzed.sl as sl

zed = sl.Camera()
for k, v in inspect.getmembers(zed):
    if k.find("__") > -1:
        continue
    print("###")
    if inspect.ismethod(v) or inspect.isfunction(v):
        print(f"\t{k}: {inspect.getdoc(v)}")
    else:
        print(f"\t{k}: {v} {inspect.getdoc(v)}")

    for k2, v2 in inspect.getmembers(v):
        if k2.find("__") > -1:
            continue

        if inspect.ismethod(v2) or inspect.isfunction(v2):
            print(f"\t{k2}: {inspect.getdoc(v2)}")
        else:
            print(f"\t{k2}: {v2} {inspect.getdoc(v2)}")

print(inspect.getdoc(zed.get_region_of_interest))