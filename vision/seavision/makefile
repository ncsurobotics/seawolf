CC=gcc
# -gp for profiling with gprof
CFLAGS=-g --std=c99
OPENCV_FLAGS=$(shell pkg-config --libs --cflags opencv)
SEAWOLF_FLAGS = -I../../libseawolf/include/ -lseawolf -L../../libseawolf/

# Debug Compiler Flags
# All debug flags that aren't in a toplevel program go here
#CFLAGS += -Ddebug_blob
#CFLAGS += -Ddebug_blob_area
#CFLAGS += -Ddebug_color
#CFLAGS += -Ddebug_color_thresholds
#CFLAGS += -Ddebug_edge
#CFLAGS += -Ddebug_edge_args
#CFLAGS += -Ddebug_hough_lines
#CFLAGS += -Ddebug_hough_graph
#CFLAGS += -Ddebug_image_typecheck
#CFLAGS += -Ddebug_hough_threshold
#CFLAGS += -Ddebug_controls
#CFLAGS += -Ddebug_remove_edges
#CFLAGS += -Ddebug_remove_edges_thresholds
#CFLAGS += -Ddebug_heading
CFLAGS += -Dimage_record
#CFLAGS += -Ddebug_tuna
#CFLAGS += -Ddebug_grid
#CFLAGS += -Ddebug_bins
CFLAGS += -Ddebug_skip_go_wait

all: mission switcher

mission: hough_opencv.o edge_opencv.o colorfilter.o blob.o mission.o camera.o remove_edges.o bmpio.o cvimg.o image.o imageproc.o misc.o grid.o mission_state.o motion.o
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) hough_opencv.o edge_opencv.o colorfilter.o blob.o mission.o camera.o remove_edges.o bmpio.o cvimg.o image.o imageproc.o misc.o grid.o mission_state.o motion.o -o mission

mission.o: mission.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) -c mission.c

switcher: camera.o switcher.o
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) camera.o switcher.o -o switcher

switcher.o: switcher.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) -c switcher.c

mission_state.o: mission_state.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) -c mission_state.c

motion.o: motion.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) -c motion.c

grid.o: grid.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) -c grid.c

camera.o: camera.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c camera.c

edge_opencv.o: edge_opencv.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c edge_opencv.c

hough_opencv.o: hough_opencv.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c hough_opencv.c

avi_read.o: avi_read.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c avi_read.c

colorfilter.o: colorfilter.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c colorfilter.c

blob.o: blob.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c blob.c

remove_edges.o: remove_edges.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c remove_edges.c

bmpio.o: bmpio.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c bmpio.c

cvimg.o: cvimg.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c cvimg.c

image.o: image.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c image.c

imageproc.o: imageproc.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) $(SEAWOLF_FLAGS) -c imageproc.c

misc.o: misc.c
	$(CC) $(CFLAGS) $(OPENCV_FLAGS) -c misc.c

clean:
	rm -rf *.o test_transforms track_bouey mission
