#include "FaceDetector.hpp"
#include <iostream>
#include <chrono>

FaceDetector::FaceDetector(const std::string& prototxtPath, const std::string& modelPath)
    : isRunning(true), hasNewFrame(false) {
    try {
        net = cv::dnn::readNetFromCaffe(prototxtPath, modelPath);
    } catch (const cv::Exception& e) {
        std::cerr << "Model load error: " << e.what() << std::endl;
    }
    workerThread = std::thread(&FaceDetector::workerLoop, this);
}

FaceDetector::~FaceDetector() {
    isRunning = false;
    cv.notify_all();
    if (workerThread.joinable()) {
        workerThread.join();
    }
}

void FaceDetector::updateFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(dataMutex);
    frame.copyTo(frameToProcess);
    hasNewFrame = true;
    cv.notify_one();
}

std::vector<cv::Rect> FaceDetector::getDetections() {
    std::lock_guard<std::mutex> lock(dataMutex);
    return lastDetections;
}

void FaceDetector::workerLoop() {
    while (isRunning) {
        cv::Mat frame;
        {
            std::unique_lock<std::mutex> lock(dataMutex);
            cv.wait(lock, [this] { return hasNewFrame || !isRunning; });

            if (!isRunning) break;

            frameToProcess.copyTo(frame);
            hasNewFrame = false;
        }

        if (frame.empty() || net.empty()) continue;

        cv::Mat blob = cv::dnn::blobFromImage(frame, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
        net.setInput(blob);
        cv::Mat detections = net.forward();

        cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());
        std::vector<cv::Rect> faces;

        for (int i = 0; i < detectionMat.rows; i++) {
            float confidence = detectionMat.at<float>(i, 2);
            if (confidence > 0.5) {
                int xLeftBottom = static_cast<int>(detectionMat.at<float>(i, 3) * frame.cols);
                int yLeftBottom = static_cast<int>(detectionMat.at<float>(i, 4) * frame.rows);
                int xRightTop = static_cast<int>(detectionMat.at<float>(i, 5) * frame.cols);
                int yRightTop = static_cast<int>(detectionMat.at<float>(i, 6) * frame.rows);
                faces.push_back(cv::Rect(cv::Point(xLeftBottom, yLeftBottom), cv::Point(xRightTop, yRightTop)));
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        {
            std::lock_guard<std::mutex> lock(dataMutex);
            lastDetections = faces;
        }
    }
}
