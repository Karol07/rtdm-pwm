/**
 * This kernel driver demonstrates how an RTDM device can be called from
 * a RT task and how to use a semaphore to create a blocking device operation.
 *
 * It is a simple device, only 4 operation are provided:
 *  - open:  start device usage
 *  - close: ends device usage
 *  - write: store transfered data in an internal buffer (realtime context)
 *  - read:  return previously stored data and erase buffer (realtime context)
 *
 */

#include <linux/module.h>
#include <rtdm/rtdm_driver.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Kim Seonghyun");


#define BUF_SIZE_MAX			1024
#define DEVICE_NAME			"mf2044-pwm-drv"
#define SOME_SUB_CLASS			4711

#define AUTHOR "Kim Seonghyun"

//system
#define SYSTEM_CLOCK 234E3
#define TBCLK 234E3
#define PWM_CARRIER 50

//defines
volatile short *pCM_PER_BASE = (short*)0x44e00000;
volatile short *pCM_PER_EPWMSS1_CLKCTRL = (short*)0x44e000cc;
volatile short *pCM_PER_EPWMSS0_CLKCTRL = (short*)0x44e000d4;
volatile short *pCM_PER_EPWMSS2_CLKCTRL = (short*)0x44e000d8;

volatile short *pPWM_CTRL = (short*)0x44e00664;
volatile short *pPWMSS1 = (short*)0x48302000;
volatile short *pPWMSS1_EPWM1 = (short*)0x48302200;
volatile short *pPWMSS1_EPWM2 = (short*)0x48304200;

volatile short *pPWMSS1_EPWM1_CMPA = (short*)0x48302212;

/**
 * The structure of the buffer
 *
 */
typedef struct buffer_s {
	int size;
	char data[BUF_SIZE_MAX];
} buffer_t;

/**
 * The global buffer
 *
 */
buffer_t buffer;

/**
 * The global semaphore
 *
 */
rtdm_sem_t sem;

/**
 * Open the device
 *
 * This function is called when the device shall be opened.
 *
 */
static int simple_rtdm_open(struct rtdm_dev_context *context,
				rtdm_user_info_t * user_info, int oflags)
{
	return 0;
}

/**
 * Close the device
 *
 * This function is called when the device shall be closed.
 *
 */
static int simple_rtdm_close(struct rtdm_dev_context *context,
				rtdm_user_info_t * user_info)
{
	return 0;
}

/**
 * Read from the device
 *
 * This function is called when the device is read in realtime context.
 *
 */
static ssize_t simple_rtdm_read_rt(struct rtdm_dev_context *context,
				    rtdm_user_info_t * user_info, void *buf,
				    size_t nbyte)
{
	int ret, size;

	/* take the semaphore */
	rtdm_sem_down(&sem);

	/* read the kernel buffer and sent it to user space */
	size = (buffer.size > nbyte) ? nbyte : buffer.size;
	ret = rtdm_safe_copy_to_user(user_info, buf, buffer.data, size);

	/* if an error has occured, send it to user */
	if (ret)
		return ret;

	/* clean the kernel buffer */
	buffer.size = 0;

	return size;
}

/**
 * Write in the device
 *
 * This function is called when the device is written in realtime context.
 *
 */
static ssize_t simple_rtdm_write_rt(struct rtdm_dev_context *context,
				     rtdm_user_info_t * user_info,
				     const void *buf, size_t nbyte)
{
	int ret;
	unsigned long duty_perc = 0;

	/* write the user buffer in the kernel buffer */
	buffer.size = (nbyte > BUF_SIZE_MAX) ? BUF_SIZE_MAX : nbyte;
	ret = rtdm_safe_copy_from_user(user_info, buffer.data, buf, buffer.size);

	/* if an error has occured, send it to user */
	if (ret)
		return ret;

	duty_perc = simple_strtoul(buf, NULL, 0);
	rtdm_printk("Write value %lu", duty_perc);

//	*pCM_PER_EPWMSS2_CLKCTRL &= (0x2);

	/* release the semaphore */
	rtdm_sem_up(&sem);

	return nbyte;
}

/**
 * This structure describe the simple RTDM device
 *
 */
static struct rtdm_device device = {
	.struct_version = RTDM_DEVICE_STRUCT_VER,

	.device_flags = RTDM_NAMED_DEVICE,
	.context_size = 0,
	.device_name = DEVICE_NAME,

	.open_nrt = simple_rtdm_open,
	.open_rt  = simple_rtdm_open,

	.ops = {
		.close_nrt = simple_rtdm_close,
		.close_rt  = simple_rtdm_close,
		.read_rt   = simple_rtdm_read_rt,
		.write_rt  = simple_rtdm_write_rt,
	},

	.device_class = RTDM_CLASS_EXPERIMENTAL,
	.device_sub_class = SOME_SUB_CLASS,
	.profile_version = 1,
	.driver_name = "RTDM-PWM",
	.driver_version = RTDM_DRIVER_VER(0, 1, 2),
	.peripheral_name = "RTDM-PWM",
	.provider_name = AUTHOR,
	.proc_name = device.device_name,
};

/**
 * This function is called when the module is loaded
 *
 * It simply registers the RTDM device.
 *
 */
int __init simple_rtdm_init(void)
{
	int res = -1;
	buffer.size = 0;		/* clear the buffer */
	rtdm_sem_init(&sem, 0);		/* init the global semaphore */

	res =  rtdm_dev_register(&device);
	if (res) {
		rtdm_printk("PWM driver registered without errors\n");
	} else {
		rtdm_printk("PWM driver registration failed: \n");
		switch(res) {
			case -EINVAL: 
				rtdm_printk("The device structure contains invalid entries. "
						"Check kernel log for further details.");
				break;
			case -ENOMEM: 
				rtdm_printk("The context for an exclusive device cannot be allocated.");
				break;
			case -EEXIST:
				rtdm_printk("The specified device name of protocol ID is already in use.");
				break;
			case -EAGAIN: 
				rtdm_printk("Some /proc entry cannot be created.");
				break;
			default:
				rtdm_printk("Unknown error code returned");
				break;
		}
		rtdm_printk("\n");
	}

	*pCM_PER_EPWMSS1_CLKCTRL &= (0x2);
	*pCM_PER_EPWMSS0_CLKCTRL &= (0x2);
	*pCM_PER_EPWMSS2_CLKCTRL &= (0x2);

	return res;
}

/**
 * This function is called when the module is unloaded
 *
 * It unregister the RTDM device, polling at 1000 ms for pending users.
 *
 */
void __exit simple_rtdm_exit(void)
{
	rtdm_printk("PWM: stopping pwm tasks\n");

	*pCM_PER_EPWMSS1_CLKCTRL &= (0x0);
	*pCM_PER_EPWMSS0_CLKCTRL &= (0x0);
	*pCM_PER_EPWMSS2_CLKCTRL &= (0x0);

	rtdm_dev_unregister(&device, 1000);
	rtdm_printk("PWM: uninitialized\n");
}

module_init(simple_rtdm_init);
module_exit(simple_rtdm_exit);
