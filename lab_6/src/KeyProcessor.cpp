#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(ProcessMode::NORMAL) {}

void KeyProcessor::processKey(int key) {
    if (key == -1) return;
    
    char c = static_cast<char>(key);
    switch (c) {
        case '1': currentMode = ProcessMode::NORMAL; break;
        case '2': currentMode = ProcessMode::INVERT; break;
        case '3': currentMode = ProcessMode::BLUR; break;
        case '4': currentMode = ProcessMode::CANNY; break;
        case '5': currentMode = ProcessMode::GLITCH; break;
        default: break;
    }
}

ProcessMode KeyProcessor::getMode() const {
    return currentMode;
}
