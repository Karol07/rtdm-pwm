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

#include <rtdm/rtdm_driver.h>
#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/pwm.h>
#include <linux/slab.h>
#include <linux/io.h>
#include <linux/err.h>
#include <linux/clk.h>
#include <linux/pm_runtime.h>
#include <linux/pinctrl/consumer.h>

static unsigned int index;
module_param(index,uint,0400);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Seonghyun Kim");

#define SIZE_MAX		1024
#define DEVICE_NAME		"mf2044-pwm-drv"
#define SOME_SUB_CLASS		4711

void __iomem *cm_per_map;
void __iomem *epwm1_0_map;

#define CM_PER_BASE 0x44e00000
#define CM_PER_SZ 0x44e03fff-CM_PER_BASE
#define EPWMSS1_CLK_CTRL 0xcc
#define EPWMSS0_CLK_CTRL 0xd4
#define EPWMSS2_CLK_CTRL 0xd8

#define EPWM1_0_BASE 0x48302200
#define EPWM1_0_SZ 0x4830225f-EPWM1_0_BASE
#define TBPRD 0xa
#define CMPAHR 0x10

#define MF2044_IOCTL_MAGIC 0x00
#define MF2044_IOCTL_ON _IO(MF2044_IOCTL_MAGIC, 1)
#define MF2044_IOCTL_OFF _IO(MF2044_IOCTL_MAGIC, 2)
#define MF2044_IOCTL_GET_DUTY_CYCLE _IOW(MF2044_IOCTL_MAGIC, 3, int)
#define MF2044_IOCTL_SET_DUTY_CYCLE _IOW(MF2044_IOCTL_MAGIC, 4, int)
#define MF2044_IOCTL_GET_FREQUENCY _IOW(MF2044_IOCTL_MAGIC, 5, int)
#define MF2044_IOCTL_SET_FREQUENCY _IOW(MF2044_IOCTL_MAGIC, 6, int)

static dev_t dev;
static struct device *dev_ret;
static struct class *cl;

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
static int simple_rtdm_open_nrt(struct rtdm_dev_context *context,
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
static int simple_rtdm_close_nrt(struct rtdm_dev_context *context,
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
static ssize_t simple_rtdm_read_nrt(struct rtdm_dev_context *context,
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
static ssize_t simple_rtdm_write_nrt(struct rtdm_dev_context *context,
				     rtdm_user_info_t * user_info,
				     const void *buf, size_t nbyte)
{
	buffer_t * buffer = (buffer_t *) context->dev_private;

	buffer->size = (nbyte > SIZE_MAX) ? SIZE_MAX : nbyte;
	if (rtdm_safe_copy_from_user(user_info, buffer->data, buf, buffer->size))
		rtdm_printk("ERROR : can't copy data to driver\n");

	return nbyte;
}

static int mf2044_rtdm_ioctl_nrt(struct rtdm_dev_context *context,
		rtdm_user_info_t *user_info, 
		unsigned int request, void __user *arg)
{
	unsigned int res=0;
	rtdm_printk("request - %d\n",request);

	switch(request)
	{
		case MF2044_IOCTL_ON:
			break;
		case MF2044_IOCTL_OFF:
			break;
		case MF2044_IOCTL_GET_DUTY_CYCLE:
			res = ioread32(epwm1_0_map+CMPAHR);
			*(int *)arg = res;
			break;
		case MF2044_IOCTL_SET_DUTY_CYCLE:
			iowrite32(0x568d0000, epwm1_0_map+CMPAHR); //tbprd
			break;
		case MF2044_IOCTL_GET_FREQUENCY:
			break;
		case MF2044_IOCTL_SET_FREQUENCY:
			iowrite32(0xf424, epwm1_0_map+CMPAHR); //tbprd
			break;
	}
}

/**
 * This structure describe the simple RTDM device
 *
 */
static struct rtdm_device device = {
	.struct_version = RTDM_DEVICE_STRUCT_VER,

	.device_flags = RTDM_NAMED_DEVICE | RTDM_EXCLUSIVE,
	.context_size = sizeof(buffer_t),
	.device_name = DEVICE_NAME,

	.open_nrt = simple_rtdm_open_nrt,

	.ops = {
		.close_nrt = simple_rtdm_close_nrt,
//		.read_nrt = simple_rtdm_read_nrt,
//		.write_nrt = simple_rtdm_write_nrt,
		.ioctl_rt = mf2044_rtdm_ioctl_nrt,
		.ioctl_nrt = mf2044_rtdm_ioctl_nrt,
	},

	.device_class = RTDM_CLASS_EXPERIMENTAL,
	.device_sub_class = SOME_SUB_CLASS,
	.profile_version = 1,
	.driver_name = "mf2044_pwm",
	.driver_version = RTDM_DRIVER_VER(0, 1, 0),
	.peripheral_name = "pwm driver for mf2044",
	.provider_name = "Seonghyun Kim",
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
	unsigned int tbprd = -1;
	res = rtdm_dev_register(&device);

	if (0 == res) {
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
	cm_per_map = ioremap(CM_PER_BASE,CM_PER_SZ);
	epwm1_0_map = ioremap(EPWM1_0_BASE,EPWM1_0_SZ);

	iowrite32(0x2, cm_per_map+EPWMSS1_CLK_CTRL);
	iowrite32(0x2, cm_per_map+EPWMSS0_CLK_CTRL);
	iowrite32(0x2, cm_per_map+EPWMSS2_CLK_CTRL);

	iowrite32(0x124f8, epwm1_0_map+CMPAHR);
	tbprd = ioread32(epwm1_0_map+CMPAHR);
	rtdm_printk("tbprd %08x\n",tbprd);
//
//	iowrite32(0xf424, epwm1_0_map+TBPRD);
//	tbprd = ioread32(epwm1_0_map+TBPRD);
//	rtdm_printk("tbprd %08x\n",tbprd);
//
//	iowrite32(0x568d0000, epwm1_0_map+CMPAHR); //tbprd

//	rtdm_printk("ioctl %d", MF2044_IOCTL_GET_DUTY_CYCLE);
//	rtdm_printk("ioctl %d", MF2044_IOCTL_SET_DUTY_CYCLE);
//
//	if (IS_ERR(cl = class_create(THIS_MODULE,"char")))
//		rtdm_printk("class_create failed\n");
//	rtdm_printk("class_create\n");
//
//	if (IS_ERR(dev_ret = device_create(cl,NULL,dev,NULL,"zedoul")))
//		rtdm_printk("device_create failed\n");
//	rtdm_printk("device_create\n");

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
	iowrite32(0x0, cm_per_map+0xcc);
	iowrite32(0x0, cm_per_map+0xd4);
	iowrite32(0x0, cm_per_map+0xd8);

	rtdm_dev_unregister(&device, 1000);
}

module_init(simple_rtdm_init);
module_exit(simple_rtdm_exit);
