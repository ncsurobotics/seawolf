/**
 * dc1394.c
 * This is a minimal wrapper for libdc1394 that is meant to be used with python
 * ctypes.
 */

#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>

#include <dc1394/dc1394.h>
#include <highgui.h>

dc1394_t * dc = NULL;

/**
 * init
 * This is called automatically by open_camera().
 */
dc1394_t* init() {
    if (!dc) {
        dc = dc1394_new();
    }
    return dc;
}

/**
 * close_camera
 * Closes the camera.  This must be called for each camera before uninit().
 */
void close_camera(dc1394camera_t* camera) {
    dc1394_video_set_transmission(camera, DC1394_OFF);
    dc1394_capture_stop(camera);
    dc1394_camera_free(camera);
}

/**
 * get_height
 * Gets the height of the frames that will be returned by the camera.
 */
int get_height(dc1394camera_t* camera) {
    // TODO: For now this is fixed.  If more compatability is needed in the
    //       future, this method can be implemented.
    return 480;
}

/**
 * get_width
 * Gets the width of the frames that will be returned by the camera.
 */
int get_width(dc1394camera_t* camera) {
    // TODO: For now this is fixed.  If more compatability is needed in the
    //       future, this method can be implemented.
    return 640;
}

/**
 * get_channels
 * Gets the number of channels of the frames that will be returned by the
 * camera.
 */
int get_channels(dc1394camera_t* camera) {
    // TODO: For now this is fixed.  If more compatability is needed in the
    //       future, this method can be implemented.
    return 3;
}

/**
 * open_camera
 * Opens the camera at the given index.
 * Returns a dc1394camera_t* for the camera on success.
 * Prints an error message and returns NULL on failure.
 *
 * For the time being, this method has some hard coded camera settings, such as
 * YUV color coding.
 */
dc1394camera_t* open_camera(int index) {

    if (!dc) {
        init();
    }

    // Get camera list
    dc1394camera_list_t* camera_list = 0;
    dc1394error_t err = dc1394_camera_enumerate(dc, &camera_list);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not enumerate cameras.  (error code %d)\n", (int)err);
        if (camera_list) dc1394_camera_free_list(camera_list);
        return NULL;
    }
    if(!camera_list) {
        printf("Error: Could not get camera list.\n");
        return NULL;
    }
    if (camera_list->num == 0) {
        printf("Error: No cameras found!\n");
        return NULL;
    }
    if ((unsigned) index >= (unsigned) camera_list->num) {
        printf("Error: %d cameras found, but index given was %d\n", camera_list->num, index);
        dc1394_camera_free_list(camera_list);
        return NULL;
    }

    // Get camera
    uint64_t guid = camera_list->ids[index].guid;
    dc1394camera_t* camera = dc1394_camera_new(dc, guid);
    dc1394_camera_free_list(camera_list);
    if (!camera) return NULL;

    // Get video modes:
    dc1394video_modes_t video_modes;
    err=dc1394_video_get_supported_modes(camera,&video_modes);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not get supported camera modes (error code %d)\n", err);
        return NULL;
    }

    // Get highest resolution mode
    int i;
    dc1394color_coding_t coding;
    dc1394video_mode_t video_mode = 0;
    for (i=video_modes.num-1;i>=0;i--) {
        if (!dc1394_is_video_mode_scalable(video_modes.modes[i])) {
            dc1394_get_color_coding_from_video_mode(camera,video_modes.modes[i], &coding);
            if (coding==DC1394_COLOR_CODING_YUV422) {
                video_mode=video_modes.modes[i];
                break;
            }
        }
    }
    if (i < 0) {
        printf("Error: Could not get a valid YUV422 mode.\n");
        close_camera(camera);
        return NULL;
    }

    // Get color coding
    err=dc1394_get_color_coding_from_video_mode(camera, video_mode,&coding);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not get color coding (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }

    // Get highest framerate
    dc1394framerates_t framerates;
    dc1394framerate_t framerate;
    err=dc1394_video_get_supported_framerates(camera,video_mode,&framerates);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not get framerates (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }
    framerate=framerates.framerates[framerates.num-1];

    // Set ISO
    err=dc1394_video_set_iso_speed(camera, DC1394_ISO_SPEED_400);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set iso speed (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }

    // Set mode
    err=dc1394_video_set_mode(camera, video_mode);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set video mode (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }

    // Set framerate
    err=dc1394_video_set_framerate(camera, framerate);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set frame rate (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }

    // Set auto gain
    err = dc1394_feature_set_mode(camera, DC1394_FEATURE_GAIN, DC1394_FEATURE_MODE_AUTO);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set auto gain (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }

    // Set auto shutter
    err = dc1394_feature_set_mode(camera, DC1394_FEATURE_SHUTTER, DC1394_FEATURE_MODE_AUTO);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set auto shutter (error code %d)\n", err);
        close_camera(camera);
        return NULL;
    }

    // Setup camera
    err=dc1394_capture_setup(camera,4, DC1394_CAPTURE_FLAGS_DEFAULT);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set up camera. (error code %d)\n", err);
        printf("       Make sure the video mode and framerate are supported\n");
        close_camera(camera);
        return NULL;
    }

    return camera;
}

/**
 * grab_frame
 * Gets a frame from the given camera.
 * On success, the frame is returned.  The frame must be freed with
 * free_image_data().  On failure, NULL is returned.
 *
 * The frame returned is in the format:
 *   char frame[width][height][channels]
 * At the moment, the only option is to have 3 channels (r, g, b).
 */
unsigned char* grab_frame(dc1394camera_t* camera) {

    if (!dc || !camera) return NULL;

    // Start capturing a frame
    dc1394error_t err = dc1394_video_set_one_shot(camera, DC1394_ON);
    if (err != DC1394_SUCCESS) {
        printf("Error: Could not set one shot (error code %d)\n", err);
        return NULL;
    }

    // Grab the frame
    dc1394video_frame_t* raw_frame = NULL;
    int i;
    for (i=0; raw_frame == NULL; i++) {
        dc1394_capture_dequeue(camera, DC1394_CAPTURE_POLICY_POLL, &raw_frame);
        if (raw_frame == NULL) {
            if (i > 50) {
                printf("Warning: Had to re-call one_shot!!\n");
                err = dc1394_video_set_one_shot(camera, DC1394_ON);
                if (err != DC1394_SUCCESS) {
                    printf("Warning: dc1394_video_set_one_shot failed!\n");
                }
                i = 0;
            }
            usleep(10000);
        }
    }
    if (!raw_frame) {
        printf("Error: Could not grab frame from camera.\n");
        return NULL;
    }
    if (dc1394_capture_is_frame_corrupt(camera, raw_frame) == DC1394_TRUE) {
        dc1394_capture_enqueue(camera, raw_frame);
        printf("Error: Frame from camera was currupt!\n");
        return NULL;
    }

    bool is_color = raw_frame->color_coding != DC1394_COLOR_CODING_MONO8 &&
                    raw_frame->color_coding != DC1394_COLOR_CODING_MONO16 &&
                    raw_frame->color_coding != DC1394_COLOR_CODING_MONO16S;
    int num_channels = is_color ? 3 : 1;

    // Convert to RGB8 or MONO8 if needed
    dc1394video_frame_t* color_converted;
    bool color_conversion_performed;
    if (raw_frame->color_coding != DC1394_COLOR_CODING_MONO8 &&
        raw_frame->color_coding != DC1394_COLOR_CODING_RGB8)
    {

        color_conversion_performed = true;
        color_converted = (dc1394video_frame_t*) calloc(1, sizeof(dc1394video_frame_t));
        if (num_channels == 3) {
            color_converted->color_coding = DC1394_COLOR_CODING_RGB8;
        } else {
            color_converted->color_coding = DC1394_COLOR_CODING_MONO8;
        }
        err = dc1394_convert_frames(raw_frame, color_converted);
        if (err != DC1394_SUCCESS) {
            dc1394_capture_enqueue(camera, raw_frame);
            printf("Error: Could not convert to RGB8 or MONO8 format!  Error code: %d\n", err);
            return NULL;
        }

    } else {
        color_conversion_performed = false;
        color_converted = raw_frame;
    }

    // Put this in its final format
    // TODO: The compiler complains here about assigning a signed char to an
    //       unsigned char:
    //           "warning: pointer targets in initialization differ in signedness"
    //       I want to fix this, but I don't have a firewire camera with me to test it.
    unsigned char* image_data = (char*) calloc(sizeof(char), color_converted->size[0]*color_converted->size[1]*3);
    memmove(image_data, color_converted->image, sizeof(char)*color_converted->size[0]*color_converted->size[1]*3);

    // Free memory
    dc1394_capture_enqueue(camera, raw_frame);
    if (color_conversion_performed) {
        free(color_converted->image);
        free(color_converted);
    }

    return image_data;
}

/**
 * free_image_data
 * This must be called to free image data returned from grab_frame.
 */
void free_image_data(unsigned char* image_data) {
    free(image_data);
}

/**
 * uninit
 * Uninitializes the dc1394 interface.
 */
void uninit() {
    if (dc) dc1394_free(dc);
}
