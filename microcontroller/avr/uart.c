
#include <string.h>

#include <sw.h>

#define UART_RX_BUFF_SIZE 128

static volatile unsigned char buffer[UART_RX_BUFF_SIZE];
static volatile int windex = 0;
static volatile int rindex = 0;

ISR(USARTC1_RXC_vect) {
    buffer[windex] = USARTC1.DATA;
    windex = (windex + 1) % UART_RX_BUFF_SIZE;
}

void init_serial(void) {
    PORTC.OUTSET = 0x80;
    PORTC.DIRSET = 0x80;

    /* Set baud to 57600 approximately (57554 exactly) */
    USARTC1.BAUDCTRLA = 150;
    USARTC1.BAUDCTRLB = 0x90;

    /* UART, 1 stop bit, no parity bits, 8 data bits (8N1) */
    USARTC1.CTRLC = 0x03;

    /* Enable Rx interrupt */
    USARTC1.CTRLA = USART_RXCINTLVL_LO_gc;

    /* Enable transmit and receive */
    USARTC1.CTRLB = 0x18;
}

/* Send a single byte of data */
void serial_send_byte(char c) {
    while((USARTC1.STATUS & USART_DREIF_bm) == 0x00) {
        ;;
    }

    USARTC1.DATA = c;
}

/* Send multiple bytes with interrupts disabled */
void serial_send_bytes(char* s, int n) {
    cli();
    while(n) {
        serial_send_byte(*s);
        s++;
        n--;
    }
    sei();
}

/* Write a string */
void serial_print(char* s) {
    serial_send_bytes(s, strlen(s));
}

int serial_available(void) {
    if(rindex <= windex) {
        return (windex - rindex);
    } else {
        return (UART_RX_BUFF_SIZE - rindex) + windex;
    }
}

/* Read a single byte */
int serial_read_byte(void) {
    int c;

    /* Wait for data to be available */
    while(serial_available() <= 0) {
        ;;
    }

    c = buffer[rindex];
    rindex = (rindex + 1) % UART_RX_BUFF_SIZE;

    return c;
}

/* Read multiple bytes */
void serial_read_bytes(char* s, int n) {
    while(serial_available() < n) {
        ;;
    }

    cli();
    if(rindex <= windex) {
        memcpy(s, (void*) buffer + rindex, n);
    } else {
        /* Size of first chunk */
        int chunk_size = UART_RX_BUFF_SIZE - rindex;

        memcpy(s, (void*) buffer + rindex, chunk_size);
        memcpy(s + chunk_size, (void*) buffer, n - chunk_size);
    }
    sei();

    rindex = (rindex + n) % UART_RX_BUFF_SIZE;
}
