#pragma once
#include <opencv2/opencv.hpp>
#include <string>
#include "FrameProcessor.hpp"

class Display {
private:
    std::string windowName;
    int brightnessSliderValue;
    FrameProcessor* processorRef;

public:
    Display(const std::string& name, FrameProcessor* processor);
    ~Display();
    void show(const cv::Mat& frame);
    static void trackbarCallback(int value, void* userdata);
};
