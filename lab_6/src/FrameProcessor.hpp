#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
private:
    int brightnessOffset;
    cv::Point rectStart;
    cv::Point rectEnd;
    bool isDrawing;
    bool hasRectangle;

public:
    FrameProcessor();
    cv::Mat process(const cv::Mat& inputFrame, ProcessMode mode, double fps);
    void setBrightness(int value);
    void handleMouse(int event, int x, int y, int flags);
    static void mouseCallback(int event, int x, int y, int flags, void* userdata);
};
