#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <condition_variable>

class FaceDetector {
private:
    cv::dnn::Net net;
    std::thread workerThread;
    std::mutex dataMutex;
    std::condition_variable cv;
    std::atomic<bool> isRunning;

    cv::Mat frameToProcess;
    bool hasNewFrame;
    std::vector<cv::Rect> lastDetections;

    void workerLoop();

public:
    FaceDetector(const std::string& prototxtPath, const std::string& modelPath);
    ~FaceDetector();

    void updateFrame(const cv::Mat& frame);
    std::vector<cv::Rect> getDetections();
};
