#include "FrameProcessor.hpp"
#include <vector>
#include <string>

FrameProcessor::FrameProcessor() : brightnessOffset(0), isDrawing(false), hasRectangle(false) {}

void FrameProcessor::setBrightness(int value) {
    brightnessOffset = value - 50;
}

void FrameProcessor::handleMouse(int event, int x, int y, int flags) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        isDrawing = true;
        hasRectangle = false;
        rectStart = cv::Point(x, y);
        rectEnd = rectStart;
    } else if (event == cv::EVENT_MOUSEMOVE) {
        if (isDrawing) {
            rectEnd = cv::Point(x, y);
        }
    } else if (event == cv::EVENT_LBUTTONUP) {
        isDrawing = false;
        hasRectangle = true;
        rectEnd = cv::Point(x, y);
    } else if (event == cv::EVENT_RBUTTONDOWN) {
        hasRectangle = false;
    }
}

void FrameProcessor::mouseCallback(int event, int x, int y, int flags, void* userdata) {
    FrameProcessor* processor = static_cast<FrameProcessor*>(userdata);
    if (processor) {
        processor->handleMouse(event, x, y, flags);
    }
}

cv::Mat FrameProcessor::process(const cv::Mat& inputFrame, ProcessMode mode, double fps) {
    cv::Mat result;
    inputFrame.copyTo(result);

    if (brightnessOffset != 0) {
        result.convertTo(result, -1, 1.0, brightnessOffset);
    }

    if (mode == ProcessMode::INVERT) {
        cv::bitwise_not(result, result);
    } else if (mode == ProcessMode::BLUR) {
        cv::GaussianBlur(result, result, cv::Size(15, 15), 0);
    } else if (mode == ProcessMode::CANNY) {
        cv::cvtColor(result, result, cv::COLOR_BGR2GRAY);
        cv::Canny(result, result, 50, 150);
        cv::cvtColor(result, result, cv::COLOR_GRAY2BGR);
    } else if (mode == ProcessMode::GLITCH) {
        std::vector<cv::Mat> channels;
        cv::split(result, channels);
        
        cv::Mat shiftR = cv::Mat::zeros(channels[2].size(), channels[2].type());
        cv::Mat shiftB = cv::Mat::zeros(channels[0].size(), channels[0].type());
        
        channels[2](cv::Rect(10, 0, result.cols - 10, result.rows)).copyTo(shiftR(cv::Rect(0, 0, result.cols - 10, result.rows)));
        channels[0](cv::Rect(0, 0, result.cols - 10, result.rows)).copyTo(shiftB(cv::Rect(10, 0, result.cols - 10, result.rows)));
        
        channels[2] = shiftR;
        channels[0] = shiftB;
        
        cv::merge(channels, result);
    }

    if (isDrawing || hasRectangle) {
        cv::rectangle(result, rectStart, rectEnd, cv::Scalar(0, 255, 0), 2);
    }

    std::string fpsText = "FPS: " + std::to_string(static_cast<int>(fps));
    cv::putText(result, fpsText, cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 255), 2);

    return result;
}
