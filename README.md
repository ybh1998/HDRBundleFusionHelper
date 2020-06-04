# HDRBundleFusionHelper

Helper for [HDRBundleFusion](https://github.com/ybh1998/HDRBundleFusion). 

HDRBundleFusionHelper include functions to:
Scan scenes with sweeping exposure time using PrimeSense RGB-D sensors;
Replay scenes;
Render reconstructed HDR model with different brightness

HDRBundleFusionHelper is under GNU General Public License v3. (Please see [LICENSE](LICENSE)).

## Installation
Clone git repo:

git clone https://github.com/ybh1998/HDRBundleFusionHelper.git

Install python requirements:

pip3 install --user -r requirements.txt

Install [OpenNI2](https://structure.io/openni)

Run:

python3 run.py

## Usage
There are three modes for HDRBundleFusionHelper scan, play and render

## Scan
Scan mode has several procedures:
1. Auto adjust white-balance
2. Lock white-balance, sweep exposure times to calibrate response function
3. Scan with sweeping exposure times
4. Replay to annotate exposure time for each frame

The sweeping strategy is going upward until over 1/2 pixels are overexposed and then going downward until 1/2 pixels are underexposed.

The sequence, exposure time and response curve are saved as data/*.oni, data/*_frame_exp.txt and data/*_curve.txt

## Play
Relay recorded sequence, annotate frame exposure time at the same time.

Require data/*.oni as sequence input and data/*_exposure.txt as exposure time transition order.

## Render
Render HDR model in .ply format with 8 brightnesses.

Require data/*.ply as sequence input.

## End
