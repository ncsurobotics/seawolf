#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include "opencv/cv.h"
//#include "SDL/SDL.h"
#include <stdio.h>

#define NFRAMES 600


int getFrames(char * file, IplImage ** frames, int colorSpace, int channels) {
  // tutorial01.c
  // Code based on a tutorial by Martin Bohme (boehme@inb.uni-luebeckREMOVETHIS.de)
  // Tested on Gentoo, CVS version 5/01/07 compiled with GCC 4.1.1

  // A small sample program that shows how to use libavformat and libavcodec to
  // read video from a file.
  //
  // Use
  //
  // gcc -o tutorial01 tutorial01.c -lavformat -lavcodec -lz
  //
  // to build (assuming libavformat and libavcodec are correctly installed
  // your system).
  //
  // Run using
  //
  // tutorial01 myvideofile.mpg
  //
  // to write the first five frames from "myvideofile.mpg" to disk in PPM
  // format.

  AVFormatContext *pFormatCtx;
  int             i, videoStream;
  AVCodecContext  *pCodecCtx;
  AVCodec         *pCodec;
  AVFrame         *pFrame;
  AVFrame         *pFrameRGB;
  AVPacket        packet;
  int             frameFinished;
  int             numBytes;
  uint8_t         *buffer;
  int m = 0, n = 0, p = 0, count = 0;

  // Register all formats and codecs
  av_register_all();

  // Open video file
  if(av_open_input_file(&pFormatCtx, file, NULL, 0, NULL)!=0)
    return -1; // Couldn't open file

  // Retrieve stream information
  if(av_find_stream_info(pFormatCtx)<0)
    return -1; // Couldn't find stream information

  // Dump information about file onto standard error
  dump_format(pFormatCtx, 0, file, 0);

  // Find the first video stream
  videoStream=-1;
  for(i=0; i<pFormatCtx->nb_streams; i++)
    if(pFormatCtx->streams[i]->codec->codec_type==CODEC_TYPE_VIDEO) {
      videoStream=i;
      break;
    }
  if(videoStream==-1)
    return -1; // Didn't find a video stream

  // Get a pointer to the codec context for the video stream
  pCodecCtx=pFormatCtx->streams[videoStream]->codec;

  // Find the decoder for the video stream
  pCodec=avcodec_find_decoder(pCodecCtx->codec_id);
  if(pCodec==NULL) {
    fprintf(stderr, "Unsupported codec!\n");
    return -1; // Codec not found
  }

  // Open codec
  if(avcodec_open(pCodecCtx, pCodec)<0)
    return -1; // Could not open codec

  // Allocate video frame
  pFrame=avcodec_alloc_frame();

  // Allocate an AVFrame structure
  pFrameRGB=avcodec_alloc_frame();
  if(pFrameRGB==NULL)
    return -1;

  // Determine required buffer size and allocate buffer
  numBytes=avpicture_get_size(PIX_FMT_RGB24, pCodecCtx->width,
                  pCodecCtx->height);
  buffer=(uint8_t *)av_malloc(numBytes*sizeof(uint8_t));

  // Assign appropriate parts of buffer to image planes in pFrameRGB
  // Note that pFrameRGB is an AVFrame, but AVFrame is a superset
  // of AVPicture
  avpicture_fill((AVPicture *)pFrameRGB, buffer, PIX_FMT_RGB24,
         pCodecCtx->width, pCodecCtx->height);

  //Read frames and store to IplImages
  i=0;
  unsigned char *ptr1, *ptr2;

  while(av_read_frame(pFormatCtx, &packet)>=0 && count < NFRAMES) {
    // Is this a packet from the video stream?
    if(packet.stream_index==videoStream) {
      // Decode video frame
      avcodec_decode_video(pCodecCtx, pFrame, &frameFinished,
               packet.data, packet.size);

      // Did we get a video frame?
      if(frameFinished) {
        // Convert the image from its native format to RGB
        //img_convert((AVPicture *)pFrameRGB, PIX_FMT_RGB24,
        //    (AVPicture*)pFrame, pCodecCtx->pix_fmt, pCodecCtx->width,
       //    pCodecCtx->height);

        //store the frame in an IplImage
        frames[count] =
        cvCreateImage(cvSize(pCodecCtx->width, pCodecCtx->height), colorSpace, 3);

        for(m = 0; m < pCodecCtx->height; m++) {
          ptr1 = pFrameRGB->data[0]+ m*pFrameRGB->linesize[0];

          ptr2 = frames[count]->imageData + m*frames[count]->widthStep;

          for(n = 0; n < 3*pCodecCtx->width; n++)
          {
            ptr2[n] =  ptr1[n];
          }
        }

        count++;
      }
    }

    // Free the packet that was allocated by av_read_frame
    av_free_packet(&packet);
  }

  // Free the RGB image
  av_free(buffer);
  av_free(pFrameRGB);

  // Free the YUV frame
  av_free(pFrame);

  // Close the codec
  avcodec_close(pCodecCtx);

  // Close the video file
  av_close_input_file(pFormatCtx);

  return count;
}
