#include "CameraProvider.hpp"
#include <iostream>
#include <stdexcept>

CameraProvider::CameraProvider(int deviceId) {
    cap.open(deviceId);
    if (!cap.isOpened()) {
        throw std::runtime_error("Error: could not open camera.");
    }
}

CameraProvider::~CameraProvider() {
    if (cap.isOpened()) {
        cap.release();
    }
}

bool CameraProvider::isOpened() const {
    return cap.isOpened();
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}
