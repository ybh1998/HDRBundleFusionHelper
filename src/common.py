import cv2
import numpy as np
colormap_l = np.zeros([480, 640, 3], dtype=np.uint32)
colormap_h = np.zeros([480, 640, 3], dtype=np.uint32)
colormap_h[:, :, 1] = 255
colormap_h[:, :, 2] = 255
colormap_range = [0, 30000]


def show_image(depth_stream, color_stream):
    frame_depth = depth_stream.read_frame()
    frame_depth = frame_depth.get_buffer_as_uint16()
    image_depth = np.frombuffer(frame_depth, dtype=np.uint16)
    image_depth.shape = (480, 640, 1)
    image_depth[image_depth > colormap_range[1]] = 0
    image_depth_show = \
        colormap_h * (image_depth - colormap_range[0]) // \
        (colormap_range[1] - colormap_range[0]) + \
        colormap_l * (colormap_range[1] - image_depth) // \
        (colormap_range[1] - colormap_range[0])
    cv2.imshow('depth', image_depth_show.astype(np.uint8))
    frame_color = color_stream.read_frame()
    frame_color = frame_color.get_buffer_as_uint8()
    image_color = np.frombuffer(frame_color, dtype=np.uint8)
    image_color.shape = (480, 640, 3)
    image_color = cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB)
    allow_up = np.percentile(image_color.min(axis=2), 25) < 64
    allow_down = np.percentile(image_color.max(axis=2), 75) > 64
    cv2.imshow('color', image_color)
    if (cv2.waitKey(1) & 0xFF) != 0xFF:
        is_end = True
    else:
        is_end = False
    return allow_up, allow_down, is_end, image_depth, image_color
