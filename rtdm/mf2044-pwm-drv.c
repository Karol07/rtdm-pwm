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

#define LSIZE_MAX		1024
#define DEVICE_NAME		"mf2044_pwm_drv"
#define SOME_SUB_CLASS		4711

#define SYSCLK 15000000

void __iomem *cm_per_map;
void __iomem *epwm1_0_map;
void __iomem *epwm1_1_map;
void __iomem *epwm0_0_map;
void __iomem *epwm0_1_map;
void __iomem *epwm2_0_map;
void __iomem *epwm2_1_map;

#define CM_PER_BASE 0x44e00000
#define CM_PER_SZ 0x44e03fff-CM_PER_BASE
#define EPWMSS1_CLK_CTRL 0xcc
#define EPWMSS0_CLK_CTRL 0xd4
#define EPWMSS2_CLK_CTRL 0xd8

#pragma warning TODO - implement more pin handlers
#define EPWM1_0_BASE 0x48302200
#define EPWM1_1_BASE 0x48302260
#define EPWM0_0_BASE 0x48300200
#define EPWM0_1_BASE 0x48300260
#define EPWM2_0_BASE 0x48304200
#define EPWM2_1_BASE 0x48304260

#define EPWM_SZ 0x5f

#define TBCNT 0x8
#define CMPAHR 0x10
#define TBPRD 0xa
#define CMPA 0x12

#define MF2044_PWM_1_0 1 << 4 //P9.14
#define MF2044_PWM_1_1 1 << 5 //P9.16
#define MF2044_PWM_0_0 1 << 6 //P9.22
#define MF2044_PWM_0_1 1 << 7 //P9.21
#define MF2044_PWM_2_0 1 << 8 //P8.19
#define MF2044_PWM_2_1 1 << 9 //P8.13

#define MF2044_IOCTL_MAGIC 0x00
#define MF2044_IOCTL_ON _IO(MF2044_IOCTL_MAGIC, 1)
#define MF2044_IOCTL_OFF _IO(MF2044_IOCTL_MAGIC, 2)
#define MF2044_IOCTL_GET_DUTY_CYCLE _IO(MF2044_IOCTL_MAGIC, 3)
#define MF2044_IOCTL_SET_DUTY_CYCLE _IO(MF2044_IOCTL_MAGIC, 4)
#define MF2044_IOCTL_GET_FREQUENCY _IO(MF2044_IOCTL_MAGIC, 5)
#define MF2044_IOCTL_SET_FREQUENCY _IO(MF2044_IOCTL_MAGIC, 6)

/**
 * The context of a device instance
 *
 * A context is created each time a device is opened and passed to
 * other device handlers when they are called.
 *
 */
typedef struct buffer_s {
	int size;
	char data[LSIZE_MAX];
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
static int mf2044_rtdm_close_nrt(struct rtdm_dev_context *context,
				 rtdm_user_info_t * user_info)
{
	return 0;
}

static int mf2044_rtdm_ioctl_nrt(struct rtdm_dev_context *context,
		rtdm_user_info_t *user_info, 
		unsigned int request, void __user *arg)
{
	unsigned int res=0;
	void __iomem *target;

//	rtdm_printk("%s %d - before %x\n", __func__, __LINE__, request);
//	rtdm_printk("%s %d - %x\n", __func__, __LINE__, MF2044_PWM_1_0);
//	rtdm_printk("%s %d - %x\n", __func__, __LINE__, ~(MF2044_PWM_1_0));

	if (request & MF2044_PWM_1_0) {
//		rtdm_printk("P9.14\n");
		target = epwm1_0_map;
		request &= ~(MF2044_PWM_1_0);
	} else if (request & MF2044_PWM_1_1) {
//		rtdm_printk("P9.16\n");
		target = epwm1_1_map;
		request &= ~(MF2044_PWM_1_1);
	} else if (request & MF2044_PWM_0_0) {
//		rtdm_printk("P9.22\n");
		target = epwm0_0_map;
		request &= ~(MF2044_PWM_0_0);
	} else if (request & MF2044_PWM_0_1) {
//		rtdm_printk("P9.21\n");
		target = epwm0_1_map;
		request &= ~(MF2044_PWM_0_1);
	} else if (request & MF2044_PWM_2_0) {
//		rtdm_printk("P8.19\n");
		target = epwm2_0_map;
		request &= ~(MF2044_PWM_2_0);
	} else if (request & MF2044_PWM_2_1) {
//		rtdm_printk("P8.13\n");
		target = epwm2_1_map;
		request &= ~(MF2044_PWM_2_1);
	}

//	rtdm_printk("command 0x%x\n", request);

	switch(request)
	{
		case MF2044_IOCTL_ON:
			iowrite32(0x2, cm_per_map+EPWMSS1_CLK_CTRL);
			iowrite32(0x2, cm_per_map+EPWMSS0_CLK_CTRL);
			iowrite32(0x2, cm_per_map+EPWMSS2_CLK_CTRL);
			break;
		case MF2044_IOCTL_OFF:
			iowrite32(0x0, cm_per_map+EPWMSS1_CLK_CTRL);
			iowrite32(0x0, cm_per_map+EPWMSS0_CLK_CTRL);
			iowrite32(0x0, cm_per_map+EPWMSS2_CLK_CTRL);
			break;
		case MF2044_IOCTL_GET_DUTY_CYCLE:
#pragma warning - need to implement more regarding CMPA / CMPB 
			res = ioread32(target+CMPA);
			*(int*)arg = (int)res;
			break;
		case MF2044_IOCTL_SET_DUTY_CYCLE:
			iowrite32(arg, target+CMPAHR);
			break;
		case MF2044_IOCTL_GET_FREQUENCY:
			res = ioread32(target+TBPRD);
			*(int*)arg = (int)res;
			break;
		case MF2044_IOCTL_SET_FREQUENCY:
			iowrite32(arg, target+TBCNT);
			break;
	}

	return 0;
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
		.close_nrt = mf2044_rtdm_close_nrt,
		.ioctl_rt = mf2044_rtdm_ioctl_nrt,
		.ioctl_nrt = mf2044_rtdm_ioctl_nrt,
	},

	.device_class = RTDM_CLASS_EXPERIMENTAL,
	.device_sub_class = SOME_SUB_CLASS,
	.profile_version = 1,
	.driver_name = DEVICE_NAME,
	.driver_version = RTDM_DRIVER_VER(0, 0, 1),
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
	epwm1_0_map = ioremap(EPWM1_0_BASE,EPWM_SZ);
	epwm1_1_map = ioremap(EPWM1_1_BASE,EPWM_SZ);
	epwm0_0_map = ioremap(EPWM0_0_BASE,EPWM_SZ);
	epwm0_1_map = ioremap(EPWM0_1_BASE,EPWM_SZ);
	epwm2_0_map = ioremap(EPWM2_0_BASE,EPWM_SZ);
	epwm2_1_map = ioremap(EPWM2_1_BASE,EPWM_SZ);

	iowrite32(0x2, cm_per_map+EPWMSS1_CLK_CTRL);
	iowrite32(0x2, cm_per_map+EPWMSS0_CLK_CTRL);
	iowrite32(0x2, cm_per_map+EPWMSS2_CLK_CTRL);

	iowrite32(0xf4240000, epwm1_0_map+TBCNT);
	iowrite32(0x568d0000, epwm1_0_map+CMPAHR);

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
	iowrite32(0x0, cm_per_map+EPWMSS1_CLK_CTRL);
	iowrite32(0x0, cm_per_map+EPWMSS0_CLK_CTRL);
	iowrite32(0x0, cm_per_map+EPWMSS2_CLK_CTRL);

	rtdm_dev_unregister(&device, 1000);
}

module_init(simple_rtdm_init);
module_exit(simple_rtdm_exit);
