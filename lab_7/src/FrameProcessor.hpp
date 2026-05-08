#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"
#include <vector>

class FrameProcessor {
private:
    int brightnessOffset;
    cv::Point rectStart;
    cv::Point rectEnd;
    bool isDrawing;
    bool hasRectangle;

public:
    FrameProcessor();
    cv::Mat process(const cv::Mat& inputFrame, ProcessMode mode, double fps, const std::vector<cv::Rect>& faces = {});
    void setBrightness(int value);
    void handleMouse(int event, int x, int y, int flags);
    static void mouseCallback(int event, int x, int y, int flags, void* userdata);
};
