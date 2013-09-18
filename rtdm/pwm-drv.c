/**
 * This kernel driver demonstrates how an RTDM device can be set up.
 *
 * It is a simple device, only 4 operation are provided:
 *  - open:  start device usage
 *  - close: ends device usage
 *  - write: store transfered data in an internal buffer
 *  - read:  return previously stored data and erase buffer
 *
 */

#include <linux/module.h>
#include <rtdm/rtdm_driver.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Kim");

#define SIZE_MAX		1024
#define DEVICE_NAME		"pwm-drv"
#define SOME_SUB_CLASS		4711

static volatile short *pMMAP = (short*)0x44c00000;
static volatile short *pEPWM1 = (short*)0x48302200 - pMMAP;
static volatile short *pEPWM2 = (short*)0x48304200 - pMMAP;
static volatile short *pPCCTL1 = pEPWM1 + 0x3c;
static volatile short *pPCCTL2 = pEPWM2 + 0x3c;

/**
 * The context of a device instance
 *
 * A context is created each time a device is opened and passed to
 * other device handlers when they are called.
 *
 */
typedef struct buffer_s {
	int size;
	char data[SIZE_MAX];
} buffer_t;

/**
 * Open the device
 *
 * This function is called when the device shall be opened.
 *
 */
static int rtdm_pwm_open_nrt(struct rtdm_dev_context *context,
				rtdm_user_info_t * user_info, int oflags)
{
	buffer_t * buffer = (buffer_t *) context->dev_private;
	buffer->size = 0; /* clear the buffer */

	return 0;
}

/**
 * Close the device
 *
 * This function is called when the device shall be closed.
 *
 */
static int rtdm_pwm_close_nrt(struct rtdm_dev_context *context,
				 rtdm_user_info_t * user_info)
{
	return 0;
}

/**
 * Read from the device
 *
 * This function is called when the device is read in non-realtime context.
 *
 */
static ssize_t rtdm_pwm_read_nrt(struct rtdm_dev_context *context,
				    rtdm_user_info_t * user_info, void *buf,
				    size_t nbyte)
{
	buffer_t * buffer = (buffer_t *) context->dev_private;
	int size = (buffer->size > nbyte) ? nbyte : buffer->size;

	buffer->size = 0;
	if (rtdm_safe_copy_to_user(user_info, buf, buffer->data, size))
		rtdm_printk("ERROR : can't copy data from driver\n");

	return size;
}

/**
 * Write in the device
 *
 * This function is called when the device is written in non-realtime context.
 *
 */
static ssize_t rtdm_pwm_write_nrt(struct rtdm_dev_context *context,
				     rtdm_user_info_t * user_info,
				     const void *buf, size_t nbyte)
{
	buffer_t * buffer = (buffer_t *) context->dev_private;

	buffer->size = (nbyte > SIZE_MAX) ? SIZE_MAX : nbyte;
	if (rtdm_safe_copy_from_user(user_info, buffer->data, buf, buffer->size))
		rtdm_printk("ERROR : can't copy data to driver\n");

	return nbyte;
}

/**
 * This structure describe the RTDM device
 *
 */
static struct rtdm_device device = {
	.struct_version = RTDM_DEVICE_STRUCT_VER,

	.device_flags = RTDM_NAMED_DEVICE,
	.context_size = sizeof(buffer_t),
	.device_name = DEVICE_NAME,

	.open_nrt = rtdm_pwm_open_nrt,

	.ops = {
		.close_nrt = rtdm_pwm_close_nrt,
		.read_nrt = rtdm_pwm_read_nrt,
		.write_nrt = rtdm_pwm_write_nrt,
	},

	.device_class = RTDM_CLASS_EXPERIMENTAL,
	.device_sub_class = SOME_SUB_CLASS,
	.profile_version = 1,
	.driver_name = "PWM rtdm",
	.driver_version = RTDM_DRIVER_VER(0, 1, 2),
	.peripheral_name = "PWM rtdm",
	.provider_name = "Kim",
	.proc_name = device.device_name,
};

/**
 * This function is called when the module is loaded
 *
 * It simply registers the RTDM device.
 *
 */
int __init rtdm_pwm_init(void)
{
	*pPCCTL1 |= 0x1;
	*pPCCTL2 |= 0x1;

	res = rtdm_dev_register(&device);
	if(res == 0) 
		rtdm_printk("PWM driver registered without errors\n");
	else
	{
		rtdm_printk("PWM driver registration failed: \n");
		switch(res)
		{
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
}

/**
 * This function is called when the module is unloaded
 *
 * It unregister the RTDM device, polling at 1000 ms for pending users.
 *
 */
void __exit rtdm_pwm_exit(void)
{
	rtdm_printk("PWM: stopping pwm tasks \n");
	rtdm_dev_unregister(&device, 1000);
	rtdm_printk("PWM: uninitialized\n");
}

module_init(rtdm_pwm_init);
module_exit(rtdm_pwm_exit);
