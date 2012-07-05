
#include <string.h>

#include <sw.h>

#define UART_RX_BUFF_SIZE 128

enum BufferState {
    NORMAL = 0,
    REALIGN = 1
};

/* Rx buffer */
static volatile unsigned char buffer[UART_RX_BUFF_SIZE];
static volatile int windex = 0;
static volatile int rindex = 0;

static enum BufferState state = NORMAL;
static int marker_count = 0;

ISR(USARTC1_RXC_vect) {
    int next_windex = (windex + 1) % UART_RX_BUFF_SIZE;

    switch(state) {
    case NORMAL:
        if((USARTC1.STATUS & USART_BUFOVF_bm) || next_windex == rindex) {
            char message[3];

            message[0] = SW_ERROR;
            message[1] = SERIAL_ERROR;

            if(next_windex == rindex) {
                message[2] = 0;
            } else {
                message[2] = 1;
            }

            serial_send_bytes(message, 3);
            realign_buffer();
        }

        buffer[windex] = USARTC1.DATA;
        windex = next_windex;
        break;

    case REALIGN:
        buffer[windex] = USARTC1.DATA;

        if(buffer[windex] == SW_MARKER) {
            marker_count++;

            if(marker_count == 3) {
                state = NORMAL;

                /* Clear buffer */
                rindex = windex;
            }
        } else {
            marker_count = 0;
            windex = next_windex;
        }
        break;
    }
}

void init_serial(void) {
    PORTC.OUTSET = 0x80;
    PORTC.DIRSET = 0x80;

    /* Set baud to 57600 approximately (57606 exactly) */
    USARTC1.BAUDCTRLA = 110;
    USARTC1.BAUDCTRLB = 0xa8;

    /* UART, 1 stop bit, no parity bits, 8 data bits (8N1) */
    USARTC1.CTRLC = 0x03;

    /* Enable Rx interrupt */
    USARTC1.CTRLA = USART_RXCINTLVL_MED_gc;

    /* Enable transmit and receive */
    USARTC1.CTRLB = 0x18;
}

void realign_buffer(void) {
    char message[3];

    if(state == REALIGN) {
        return;
    }

    message[0] = SW_REALIGN;
    message[1] = 0;
    message[2] = 0;

    state = REALIGN;
    marker_count = 0;

    serial_send_bytes(message, 3);
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
    volatile int r, w;

    cli();
    r = rindex;
    w = windex;
    sei();

    if(r <= w) {
        return (w - r);
    } else {
        return (UART_RX_BUFF_SIZE - r) + w;
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
    if(rindex + n <= UART_RX_BUFF_SIZE) {
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
