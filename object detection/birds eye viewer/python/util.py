def bbox_to_xyxy(bounding_box_2d):
    xlist = [x for x, _ in bounding_box_2d]
    ylist = [y for _, y in bounding_box_2d]
    xmin = min(xlist)
    xmax = max(xlist)

    ymin = min(ylist)
    ymax = max(ylist)

    return ((xmin, ymin), (xmax, ymax))

if __name__ == "__main__":
    bounding_box_2d = [[ 553.,  232.],
                       [1275., 232.],
                       [1275., 716.],
                       [ 553., 716.]
                       ]
    point = bbox_to_xyxy(bounding_box_2d)
    print(point)

