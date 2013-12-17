#include <termios.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/ioctl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <rtdm/rtdm.h>
#include "mf2044-pwm-lib.h"

#define DEVICE_NAME "mf2044_pwm_drv"

#define MF2044_IOCTL_MAGIC 0x00
#define MF2044_IOCTL_ON _IO(MF2044_IOCTL_MAGIC, 1)
#define MF2044_IOCTL_OFF _IO(MF2044_IOCTL_MAGIC, 2)
#define MF2044_IOCTL_GET_DUTY_CYCLE _IO(MF2044_IOCTL_MAGIC, 3)
#define MF2044_IOCTL_SET_DUTY_CYCLE _IO(MF2044_IOCTL_MAGIC, 4)
#define MF2044_IOCTL_GET_FREQUENCY _IO(MF2044_IOCTL_MAGIC, 5)
#define MF2044_IOCTL_SET_FREQUENCY _IO(MF2044_IOCTL_MAGIC, 6)

static int fd = -1;

int mf2044_pwm_open(void)
{
	fd = rt_dev_open(DEVICE_NAME, 0);
	if (fd < 0) {
		printf("ERROR : can't open device %s (%s)\n",
		       DEVICE_NAME, strerror(-fd));
		fflush(stdout);
		return EXIT_FAILURE;
	}
}

int mf2044_pwm_close(void)
{
	rt_dev_close(fd);
	return EXIT_SUCCESS;
}

int mf2044_pwm_duty_cycle_get(MF2044_PWM_PINS pin)
{
	int duty;
	int command = MF2044_IOCTL_GET_DUTY_CYCLE;
	command |= pin;

	if (rt_dev_ioctl(fd, MF2044_IOCTL_GET_DUTY_CYCLE, &duty) == -1)
	{
		printf("TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	return duty;
}

int mf2044_pwm_duty_cycle_set(MF2044_PWM_PINS pin, int duty)
{
	int command = MF2044_IOCTL_SET_DUTY_CYCLE;
	command |= pin;

	if (rt_dev_ioctl(fd, command, duty) == -1)
	{
		printf("TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	return EXIT_SUCCESS;
}

int mf2044_pwm_frequency_get(MF2044_PWM_PINS pin)
{
	int freq;
	int command = MF2044_IOCTL_GET_FREQUENCY;
	command |= pin;

	if (rt_dev_ioctl(fd, command, &freq) == -1)
	{
		printf("TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	return freq;
}

int mf2044_pwm_frequency_set(MF2044_PWM_PINS pin, int freq)
{
	#warning TODO - we need to have some error messages fixing it in A-B
	int command = MF2044_IOCTL_SET_FREQUENCY;
	command |= pin;

	if (rt_dev_ioctl(fd, command, freq) == -1)
	{
		printf("TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	return EXIT_SUCCESS;
}

