import os
import time
import numpy as np
from src.common import show_image
from openni import openni2
from src.gsolve import process_imgs
exposures = [1, 2, 4, 8, 16, 32, 64]


def scan(name, exposure_strategy='sweep'):
    # exposure_strategy can be 'sweep' 'auto' or 'lock'
    if exposure_strategy not in ['sweep', 'auto', 'lock']:
        print('Invalid exposure_strategy:', exposure_strategy)
        return
    dev = openni2.Device.open_any()
    print(dev.get_device_info())
    depth_mode = dev.get_sensor_info(openni2.SENSOR_DEPTH).videoModes[5]
    depth_stream = dev.create_depth_stream()
    depth_stream.set_video_mode(depth_mode)
    depth_stream.set_mirroring_enabled(False)
    depth_stream.start()
    print(depth_mode)
    color_mode = dev.get_sensor_info(openni2.SENSOR_COLOR).videoModes[9]
    color_stream = dev.create_color_stream()
    color_stream.set_video_mode(color_mode)
    color_stream.set_mirroring_enabled(False)
    color_stream.start()
    print(color_mode)
    filename = os.path.join('data', name)
    recorder = openni2.Recorder((filename + '.oni').encode('utf-8'))
    recorder_exposure = open(filename + '_exposure.txt', 'w')
    recorder.attach(color_stream, allow_lossy_compression=True)
    recorder.attach(depth_stream, allow_lossy_compression=True)
    dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
    color_camera_settings = openni2.CameraSettings(color_stream)
    ldr_imgs = []
    while True:
        _, _, is_end, _, _ = show_image(depth_stream, color_stream)
        if is_end:
            break
    color_camera_settings.auto_exposure = False
    color_camera_settings.auto_white_balance = False
    for camera_exposure in exposures:
        color_camera_settings.exposure = camera_exposure
        time.sleep(0.15)
        _, _, _, _, image_color = show_image(depth_stream, color_stream)
        ldr_imgs.append(np.copy(image_color))
    g = process_imgs(np.array(ldr_imgs), exposures, 'data')
    with open(filename + '_curve.txt', 'w') as w:
        for i in g:
            w.write(str(i) + '\n')
    camera_exposure = 4
    color_camera_settings.exposure = exposures[camera_exposure]
    while True:
        _, _, is_end, _, _ = show_image(depth_stream, color_stream)
        if is_end:
            break
    print('Record Start')
    recorder.start()
    is_end = False
    direction = 1
    time.sleep(0.15)
    allow_up = True
    allow_down = True
    if exposure_strategy == 'auto':
        color_camera_settings.auto_exposure = True
    while not is_end:
        if exposure_strategy == 'sweep':
            if direction == 1 and \
                    (not allow_up or camera_exposure == len(exposures) - 1):
                direction = -1
            elif direction == -1 and \
                    (not allow_down or camera_exposure == 0):
                direction = 1
            camera_exposure += direction
            color_camera_settings.exposure = exposures[camera_exposure]
        print(exposures[camera_exposure])
        recorder_exposure.write(str(exposures[camera_exposure]) + '\n')
        time.sleep(0.1)
        for i in range(3):
            allow_up, allow_down, is_end, _, _ = show_image(
                depth_stream, color_stream)
            if is_end:
                break
    recorder.stop()
    recorder_exposure.close()
    depth_stream.stop()
    color_stream.stop()
