#!/bin/bash
sudo apt-get update
sudo apt-get install -y build-essential cmake libopencv-dev gcc g++ \
    v4l-utils libv4l-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav gstreamer1.0-tools
chmod +x build.sh run.sh
