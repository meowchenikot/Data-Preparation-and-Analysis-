#include <iostream>
#include <chrono>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"

int main() {
    try {
        CameraProvider camera(0);
        KeyProcessor keyProc;
        FrameProcessor frameProc;
        Display display("Main Window", &frameProc);
        
        FaceDetector faceDetector("../deploy.prototxt", "../res10_300x300_ssd_iter_140000.caffemodel");

        auto timeStart = std::chrono::high_resolution_clock::now();
        int frameCount = 0;
        double fps = 0.0;

        std::cout << "Program started. Press ESC to exit." << std::endl;
        std::cout << "Keys 1-5 change modes. 'F' for Face Detection." << std::endl;

        while (true) {
            cv::Mat frame = camera.getFrame();
            
            if (frame.empty()) {
                std::cerr << "Error: empty frame." << std::endl;
                break;
            }

            frameCount++;
            auto timeNow = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> elapsed = timeNow - timeStart;
            
            if (elapsed.count() >= 1.0) {
                fps = frameCount / elapsed.count();
                frameCount = 0;
                timeStart = timeNow;
            }

            std::vector<cv::Rect> currentFaces;
            if (keyProc.getMode() == ProcessMode::FACE) {
                faceDetector.updateFrame(frame);
                currentFaces = faceDetector.getDetections();
            }

            cv::Mat processedFrame = frameProc.process(frame, keyProc.getMode(), fps, currentFaces);
            display.show(processedFrame);

            int key = cv::waitKey(1);
            if (key == 27) {
                break;
            }
            keyProc.processKey(key);
        }
    } catch (const std::exception& e) {
        std::cerr << "Critical error: " << e.what() << std::endl;
        return -1;
    }

    return 0;
}
