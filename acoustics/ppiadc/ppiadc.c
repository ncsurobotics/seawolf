
/**
 * PPI ADC Kernel Module
 */

/*
 * Memory scheme
 *
 * Samples from the ADC are interleaved
 *
 * DMA ping-pongs between two 64kB buffers. This size of this buffer is
 * determined as follows,
 *
 * 8192 samples, 2 bytes (14 bit) per sample, 4 channels
 *
 * 8192 * 2 * 4 = 64kB
 *
 * Two of these buffers are populated by the DMA engine in an alternating,
 * "ping-pong" fashion
 */

#include <asm/blackfin.h>
#include <asm/cacheflush.h>
#include <asm/dma.h>
#include <asm/gptimers.h>
#include <asm/portmux.h>
#include <asm/uaccess.h>

#include <linux/cdev.h>
#include <linux/completion.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/mm.h>
#include <linux/module.h>

#define DRIVER_NAME "ppi_adc"

/* Major number of the device */
#define PPI_CHR_MAJOR 157

/* Number of conversion requests to generate per second */
#define ADC_CONVST_PER_SEC (96 * 1024)

/* Number of samples from each channel to store in a single buffer */
#define SAMPLES_PER_CHANNEL (8 * 1024)

/* Number of bytes used for a single sample on a single channel */
#define BYTES_PER_SAMPLE 2

/* Number of channels */
#define CHANNELS 4

#define BUFFER_SIZE (SAMPLES_PER_CHANNEL * CHANNELS * BYTES_PER_SAMPLE)

/* Number of buffers for the DMA engine to use. This should always be 2 */
#define BUFFER_COUNT 2

/* Frequency to run the PPI port at (PPI_CLK) */
#define PPI_CLK_FREQ 1000000

/* See Blackfin Hardware Reference Manual 3.2, page 7-27, "PPI Control Register" */
#define PPI_MODE 0xe80c

static irqreturn_t buffer_full_handler(int irq, void* data);
static int page_alloc_order(size_t size);

static ssize_t ppi_chr_read(struct file* filp, char __user* buffer, size_t count, loff_t* offset);
static ssize_t ppi_chr_write(struct file* filp, const char __user* buffer, size_t count, loff_t* offset);
static int ppi_chr_open(struct inode* i, struct file* filp);
static int ppi_chr_release(struct inode* i, struct file* filp);

static int timers_init(void);
static int ppi_init(void);
static int dma_init(void);
static int device_init(void);
static int __init ppi_adc_init(void);

static void timers_close(void);
static void ppi_close(void);
static void dma_close(void);
static void device_close(void);
static void __exit ppi_adc_close(void);

/* PPI pins to reserve */
static unsigned short ppi_pins[] = {P_PPI0_D0, P_PPI0_D1,
                                    P_PPI0_D2, P_PPI0_D3,
                                    P_PPI0_D4, P_PPI0_D5,
                                    P_PPI0_D6, P_PPI0_D7,
                                    P_PPI0_D8, P_PPI0_D9,
                                    P_PPI0_D10, P_PPI0_D11,
                                    P_PPI0_D12, P_PPI0_D13,
                                    P_PPI0_CLK, P_PPI0_FS1,
                                    0};

/* Pointer to the DMA buffer */
static unsigned long dma_buffer = 0;

/* Index of the currently filling buffer. The interrupt handler uses this to know which buffer just filled */
static unsigned short current_buffer_index = 0;
static unsigned long current_buffer_pointer = 0;

/* Buffer full completion flag */
DECLARE_COMPLETION(buffer_ready);

static struct cdev* dev = NULL;
static struct file_operations fops = {
    .read = ppi_chr_read,
    .write = ppi_chr_write,
    .open = ppi_chr_open,
    .release = ppi_chr_release
};

static irqreturn_t buffer_full_handler(int irq, void* data) {
    /* Compute the absolute address of the individual buffer */
    current_buffer_pointer = dma_buffer + (current_buffer_index * BUFFER_SIZE);

    /* Advance the buffer number */
    current_buffer_index = (current_buffer_index + 1) % BUFFER_COUNT;
    complete(&buffer_ready);

#ifdef PPIADC_DEBUG
    printk(KERN_INFO DRIVER_NAME ": 0x%08lX 0x%04X\n", current_buffer_pointer, ((unsigned short*) current_buffer_pointer)[0]);
#endif
    
    clear_dma_irqstat(CH_PPI);
    return IRQ_HANDLED;
}

/* Compute the required order of a page allocation */
static int page_alloc_order(size_t size) {
    size_t pages;
    int order;
    short extra;
    
    pages = size / PAGE_SIZE;
    if(size % PAGE_SIZE) {
        pages += 1;
    }

    extra = 0;
    order = 0;
    while(pages > 1) {
        if(pages & 1) {
            extra = 1;
        }
        pages >>= 1;
        order += 1;
    }

    return order + extra;
}

static ssize_t ppi_chr_read(struct file* filp, char __user* buffer, size_t count, loff_t* offset) {
    if(sizeof(current_buffer_pointer) != count) {
        return -EINVAL;
    }

    /* Wait for buffer to fill and pointer to be set */
    if(wait_for_completion_interruptible(&buffer_ready)) {
        return -EINTR;
    }

    /* Copy value of the pointer to the just filled buffer to the user buffer */
    if(copy_to_user(buffer, &current_buffer_pointer, count)) {
        return -EFAULT;
    }

    /* Reset the completion flag so completions don't pile up */
    INIT_COMPLETION(buffer_ready);

    return 0;
}

static ssize_t ppi_chr_write(struct file* filp, const char __user* buffer, size_t count, loff_t* offset) {
    uint8_t opcode = 0;

    if(count != 1) {
        printk(KERN_WARNING DRIVER_NAME ": Invalid size on write\n");
        return -EINVAL;
    }

    if(copy_from_user(&opcode, buffer, count)) {
        printk(KERN_WARNING DRIVER_NAME ": Could not copy from user buffer\n");
        return -EFAULT;
    }

    switch(opcode) {
    case 1:
        /* Reset the completion flag */
        INIT_COMPLETION(buffer_ready);
        break;
    default:
        printk(KERN_WARNING DRIVER_NAME ": invalid opcode %d\n", opcode);
        return -EINVAL;
    }

    return 0;
}

static int ppi_chr_open(struct inode* i, struct file* filp) {
    return 0;
}

static int ppi_chr_release(struct inode* i, struct file* filp) {
    return 0;
}

static int timers_init(void) {
    unsigned long ppi_clk_period_sclk = get_sclk() / PPI_CLK_FREQ;
    unsigned long adc_convst_period_sclk = get_sclk() / ADC_CONVST_PER_SEC;

    /* Timer 2 drives the PPI clock and timer 1 drives the convst clock for the adc */
    peripheral_request(P_TMR1, DRIVER_NAME);
    peripheral_request(P_TMR2, DRIVER_NAME);
    
    /* Configure timers for PWM */
    set_gptimer_config(TIMER1_id, TIMER_MODE_PWM | TIMER_PERIOD_CNT);
    set_gptimer_config(TIMER2_id, TIMER_MODE_PWM | TIMER_PERIOD_CNT);

    /* For the convst clock, use ADC_CONVST_PER_SEC and a 10% duty cycle */
    set_gptimer_period(TIMER1_id, adc_convst_period_sclk);
    set_gptimer_pwidth(TIMER1_id, adc_convst_period_sclk / 10);

    /* For the PPI clock, set the period as given by PPI_CLK_FREQ and use a
       fixed 50% duty cycle */
    set_gptimer_period(TIMER2_id, ppi_clk_period_sclk);
    set_gptimer_pwidth(TIMER2_id, ppi_clk_period_sclk / 2);

    /* Enable both timers simultaneously */
    enable_gptimers(TIMER1bit|TIMER2bit);

    return 0;
}

static int ppi_init(void) {
    /* Request peripheral pins for PPI */
    peripheral_request_list(ppi_pins, DRIVER_NAME);

    /* No delay between frame sync and read */
    bfin_write_PPI_DELAY(0);
    
    /* Read one sample per frame sync (the number given for COUNT is always one
       less than the desired count) */
    bfin_write_PPI_COUNT(0);
    bfin_write_PPI_STATUS(0);

    /* PPI control mode (assert on falling edge, 14 data bits, general purpose
       rx with 1 frame sync */
    bfin_write_PPI_CONTROL(PPI_MODE);

    /* Enable PPI */
    bfin_write_PPI_CONTROL(bfin_read_PPI_CONTROL() | PORT_EN);

    return 0;
}

static int dma_init(void) {
    int ret;

    /* Request DMA channel */
    ret = request_dma(CH_PPI, DRIVER_NAME);
    if(ret < 0) {
        printk(KERN_WARNING DRIVER_NAME ": Could not allocate DMA channel\n");
        return ret;
    }

    /* Disable channel while it is being configured */
    disable_dma(CH_PPI);

    /* Allocate buffer space for the DMA engine to use */
    dma_buffer = __get_dma_pages(GFP_KERNEL, page_alloc_order(BUFFER_SIZE * BUFFER_COUNT));
    if(dma_buffer == 0) {
        printk(KERN_WARNING DRIVER_NAME ": Could not allocate dma_pages\n");
        free_dma(CH_PPI);
        return -ENOMEM;
    }

    /* Invalid caching on the DMA buffer */    /* Enable PPI */
    bfin_write_PPI_CONTROL(bfin_read_PPI_CONTROL() | PORT_EN);


    invalidate_dcache_range(dma_buffer, dma_buffer + (BUFFER_SIZE * BUFFER_COUNT));

    /* Set DMA configuration */
    set_dma_start_addr(CH_PPI, dma_buffer);
    set_dma_config(CH_PPI, (DMAFLOW_AUTO | WNR | RESTART | DI_EN | WDSIZE_16 | DMA2D | DI_SEL));
    set_dma_x_count(CH_PPI, SAMPLES_PER_CHANNEL * CHANNELS);
    set_dma_x_modify(CH_PPI, BYTES_PER_SAMPLE);
    set_dma_y_count(CH_PPI, BUFFER_COUNT);
    set_dma_y_modify(CH_PPI, BYTES_PER_SAMPLE);
    set_dma_callback(CH_PPI, &buffer_full_handler, NULL);

    /* Enable DMA */
    enable_dma(CH_PPI);

    return 0;
}

static int device_init(void) {
    dev = cdev_alloc();
    dev->ops = &fops;
    dev->owner = THIS_MODULE;

    return cdev_add(dev, MKDEV(PPI_CHR_MAJOR, 0), 1);
}

static int __init ppi_adc_init(void) {
    int ret;
    
    ret = timers_init();
    if(ret) {
        return ret;
    }

    ret = dma_init();
    if(ret) {
        timers_close();
        return ret;
    }

    ret = ppi_init();
    if(ret) {
        dma_close();
        timers_close();
        return ret;
    }
    
    ret = device_init();
    if(ret) {
        ppi_close();
        dma_close();
        timers_close();
        return ret;
    }

    SSYNC();

    return 0;
}

static void timers_close(void) {
    /* Disable timers and free the pins */
    disable_gptimers(TIMER1bit|TIMER2bit);
    peripheral_free(P_TMR1);
    peripheral_free(P_TMR2);
}

static void ppi_close(void) {
    bfin_write_PPI_CONTROL(0);
    peripheral_free_list(ppi_pins);
}

static void dma_close(void) {
    disable_dma(CH_PPI);
    free_pages(dma_buffer, page_alloc_order(BUFFER_SIZE * BUFFER_COUNT));
    free_dma(CH_PPI);
}

static void device_close(void) {
    cdev_del(dev);
}

static void __exit ppi_adc_close(void) {
    device_close();
    ppi_close();
    dma_close();
    timers_close();
}

MODULE_LICENSE("BSD");
module_init(ppi_adc_init);
module_exit(ppi_adc_close);
