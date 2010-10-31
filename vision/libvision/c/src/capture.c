
#include "vision_lib.h"

#include <ctype.h>

CvCapture* capture_from_string(char* str) {
        CvCapture* capture;
        if (strlen(str)==1 && isdigit(str[0]))
        {
            capture = cvCaptureFromCAM(atoi(str));
        } else {
            capture = cvCaptureFromFile(str);
        }
        return capture;
}
