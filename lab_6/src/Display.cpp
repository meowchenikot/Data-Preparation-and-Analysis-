#include "Display.hpp"

Display::Display(const std::string& name, FrameProcessor* processor) 
    : windowName(name), brightnessSliderValue(50), processorRef(processor) {
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);
    cv::createTrackbar("Brightness", windowName, &brightnessSliderValue, 100, trackbarCallback, this);
    cv::setMouseCallback(windowName, FrameProcessor::mouseCallback, processorRef);
}

Display::~Display() {
    cv::destroyWindow(windowName);
}

void Display::show(const cv::Mat& frame) {
    cv::imshow(windowName, frame);
}

void Display::trackbarCallback(int value, void* userdata) {
    Display* display = static_cast<Display*>(userdata);
    if (display && display->processorRef) {
        display->processorRef->setBrightness(value);
    }
}
