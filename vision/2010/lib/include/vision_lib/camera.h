#ifndef __SEAWOLF_VISION_LIB_CAMERA_INCLUDE_H
#define __SEAWOLF_VISION_LIB_CAMERA_INCLUDE_H

#define DOWN_CAM 0
#define FORWARD_CAM 1
#define UP_CAM 2

int frame_number; // XXX: Is this needed?

CvCapture* init_camera_from_args(int argc, char** argv);
CvCapture* init_camera_from_string(char* str);

void multicam_set_camera(int camnumber, char* camstr);
void multicam_reset_camera(void);

IplImage* multicam_get_frame(int camnumber);
IplImage* get_frame(CvCapture* capture);

#endif
