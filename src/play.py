import os
import cv2
import numpy as np
from src.common import show_image
from openni import openni2


def play(name):
    filename = os.path.join('data', name)
    recorder_exposure = open(filename + '_exposure.txt', 'r')
    frame_exposure = open(filename + '_frame_exp.txt', 'w')
    dev = openni2.Device.open_file((filename + '.oni').encode('utf-8'))
    pc = openni2.PlaybackSupport(dev)
    pc.set_speed(-1.0)
    pc.set_repeat_enabled(False)
    print(dev.get_device_info())
    depth_stream = dev.create_depth_stream()
    depth_mode = depth_stream.get_video_mode()
    depth_stream.start()
    print(depth_mode)
    color_stream = dev.create_color_stream()
    color_mode = color_stream.get_video_mode()
    color_stream.start()
    print(color_mode)
    print('Replay Start')
    is_end = False
    g = np.loadtxt(filename + '_curve.txt')
    img_cnt = 0
    exposure = 64
    exposure_next = int(recorder_exposure.readline())
    last_median = [0, 0]
    for t in range(pc.get_number_of_frames(color_stream)):
        _, _, is_end, _, image_color = show_image(
            depth_stream, color_stream)
        if is_end:
            break
        curr_median = [np.percentile(image_color, 25) + 5,
                       np.percentile(image_color, 75) + 5]
        if img_cnt > 1 and \
            ((exposure_next > exposure or exposure == 0) and
                (curr_median[1] / last_median[1] > 1.2 or
                 curr_median[0] / last_median[0] > 1.2)) or \
            ((exposure_next < exposure or exposure == 0) and
                (last_median[1] / curr_median[1] > 1.2 or
                 last_median[0] / curr_median[0] > 1.2)):
            img_cnt = 0
            exposure = exposure_next
            exposure_next = recorder_exposure.readline()
            if exposure_next == '':
                is_end = True
            else:
                exposure_next = int(exposure_next)
            print(exposure)
        frame_exposure.write(str(exposure) + '\n')
        frame_exposure.flush()
        last_median[0] = curr_median[0]
        last_median[1] = curr_median[1]
        print('\t', img_cnt)
        img_cnt += 1
        if exposure > 0:
            image_color = np.exp(g[image_color]) / exposure * 10
            cv2.imshow('linear', image_color)
        cv2.waitKey(1)
    recorder_exposure.close()
    frame_exposure.close()
    depth_stream.stop()
    color_stream.stop()
