#!/bin/bash
sudo apt-get update
sudo apt-get install -y build-essential cmake libopencv-dev gcc g++ wget \
    v4l-utils libv4l-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav gstreamer1.0-tools

if [ ! -f deploy.prototxt ]; then
    wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
fi
if [ ! -f res10_300x300_ssd_iter_140000.caffemodel ]; then
    wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
fi

chmod +x build.sh run.sh
