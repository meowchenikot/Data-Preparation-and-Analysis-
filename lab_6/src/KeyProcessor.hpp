#pragma once

enum class ProcessMode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    GLITCH
};

class KeyProcessor {
private:
    ProcessMode currentMode;

public:
    KeyProcessor();
    void processKey(int key);
    ProcessMode getMode() const;
};
