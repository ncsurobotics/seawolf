vision:	main.c bitmap_io.c process_image.c bitmap.h
		gcc -c bitmap_io.c
		gcc -c process_image.c
		gcc -c main.c
		gcc -o vision main.o bitmap_io.o process_image.o
		rm main.o
		rm bitmap_io.o
		rm process_image.o		
run:	
		make vision
		./vision -f test_3.bmp -o output.bmp -t 48 -d 32
