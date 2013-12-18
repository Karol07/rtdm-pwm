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
#define PIN_CHECKER 0x150
#define DUTY_INIT 0

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
	int duty, freq = -1;
	int command = MF2044_IOCTL_GET_DUTY_CYCLE;
	command |= pin;

	if (MF2044_PWM_PNULL>=pin || MF2044_PWM_PMAX <= pin) {
		printf("param failed: pin[%d] is too high or too low.\n", pin);
		return EXIT_FAILURE;
	}

	if (rt_dev_ioctl(fd, command, &duty) == -1)
	{
		printf("TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	freq = mf2044_pwm_frequency_get(pin);

	return (duty/(freq*1.0)) * 100;
}

int mf2044_pwm_duty_cycle_set(MF2044_PWM_PINS pin, int duty)
{
	int freq = mf2044_pwm_frequency_get(pin);
	int duty_cycle = freq  * (duty/100.0);
	int command = MF2044_IOCTL_SET_DUTY_CYCLE;
	command |= pin;
	if (MF2044_PWM_PNULL>=pin || MF2044_PWM_PMAX <= pin) {
		printf("param failed: pin[%d] is too high or too low.\n", pin);
		return EXIT_FAILURE;
	}

	if (rt_dev_ioctl(fd, command, duty_cycle) == -1)
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
	if (MF2044_PWM_PNULL>=pin || MF2044_PWM_PMAX <= pin) {
		printf("param failed: pin[%d] is too high or too low.\n", pin);
		return EXIT_FAILURE;
	}

	if (rt_dev_ioctl(fd, command, &freq) == -1)
	{
		printf("TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	return freq;
}

int mf2044_pwm_frequency_set(MF2044_PWM_PINS pin1, int freq)
{
	int command = MF2044_IOCTL_SET_FREQUENCY;
	command |= pin1;
	int pin2 = -1;
	int duty1 = mf2044_pwm_duty_cycle_get(pin1);
	int duty2 = DUTY_INIT;
	if (MF2044_PWM_PNULL>=pin1 || MF2044_PWM_PMAX <= pin1) {
		printf("param failed: pin[%d] is too high or too low.\n", pin1);
		return EXIT_FAILURE;
	}

	if (pin1 == (PIN_CHECKER & pin1)) {
		pin2 = pin1 << 1;
		duty2 = mf2044_pwm_duty_cycle_get(pin2);
	} else {
		pin2 = pin1 >> 1;
		duty2 = mf2044_pwm_duty_cycle_get(pin2);
	}

	if (duty1 != DUTY_INIT && duty2 != DUTY_INIT) {
		fprintf(stderr,"You can not change frequency after setting both duty cycle in pwmss\n");
		fprintf(stderr,"A[%d] and B[%d]\n",duty1,duty2);
		return EXIT_FAILURE;
	}

	if (rt_dev_ioctl(fd, command, freq) == -1)
	{
		fprintf(stderr,"TIOCMGET failed: %s\n", strerror(errno));
		return EXIT_FAILURE;
	}
	return EXIT_SUCCESS;
}

