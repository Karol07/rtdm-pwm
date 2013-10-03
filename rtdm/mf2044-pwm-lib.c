#include <termios.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/ioctl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <rtdm/rtdm.h>

#define DEVICE_NAME "mf2044-pwm-drv"

#define MF2044_IOCTL_MAGIC 0x00
#define MF2044_IOCTL_ON _IO(MF2044_IOCTL_MAGIC, 1)
#define MF2044_IOCTL_OFF _IO(MF2044_IOCTL_MAGIC, 2)
#define MF2044_IOCTL_GET_DUTY_CYCLE _IOW(MF2044_IOCTL_MAGIC, 3, int)
#define MF2044_IOCTL_SET_DUTY_CYCLE _IOW(MF2044_IOCTL_MAGIC, 4, int)
#define MF2044_IOCTL_GET_FREQUENCY _IOW(MF2044_IOCTL_MAGIC, 5, int)
#define MF2044_IOCTL_SET_FREQUENCY _IOW(MF2044_IOCTL_MAGIC, 6, int)

int main()
{
	int fd, status, k, f, sc;
	printf("ioctl %d", MF2044_IOCTL_GET_DUTY_CYCLE);
	printf("ioctl %d", MF2044_IOCTL_SET_DUTY_CYCLE);

	fd = rt_dev_open(DEVICE_NAME, 0);
	if (fd < 0) {
		printf("ERROR : can't open device %s (%s)\n",
		       DEVICE_NAME, strerror(-fd));
		fflush(stdout);
		exit(1);
	}

	if (rt_dev_ioctl(fd, MF2044_IOCTL_SET_FREQUENCY, f) == -1)
		printf("TIOCMGET failed: %s\n", strerror(errno));

	if (rt_dev_ioctl(fd, MF2044_IOCTL_SET_DUTY_CYCLE, k) == -1)
		printf("TIOCMGET failed: %s\n", strerror(errno));

	printf("%d",ioctl(fd, MF2044_IOCTL_GET_FREQUENCY, sc));
	printf("\n%d",ioctl(fd, MF2044_IOCTL_GET_DUTY_CYCLE, sc));

	rt_dev_close(fd);
}

