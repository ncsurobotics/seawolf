#ifndef CB_HEADER__
#define CB_HEADER__

short* cBuff();
int fillBuffer();
short windowFun(short data, short window);
short writeData(short* buffAddr, int index, short data);
short readData(short* buffAddr, int* index);

short* buffAddr;

#endif // #ifndef CB_HEADER__
