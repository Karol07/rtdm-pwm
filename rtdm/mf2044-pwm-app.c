#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>	/* for MCL_CURRENT and MCL_FUTURE */
#include <rtdm/rtdm.h>
#include <native/task.h>

#define DEVICE_NAME		"mf2044-pwm-drv"

RT_TASK rt_task_desc;

int main(int argc, char *argv[])
{
	char buf[1024];
	ssize_t size;
	int device;
	int ret;

	/* no memory-swapping for this programm */
	ret = mlockall(MCL_CURRENT | MCL_FUTURE);
	if (ret) {
		perror("ERROR : mlockall has failled");
		exit(1);
	}

	/*
	 * Turn the current task into a RT-task.
	 * The task has no name to allow multiple program instances to be run
	 * at the same time.
	 */
	ret = rt_task_shadow(&rt_task_desc, NULL, 1, 0);
	if (ret)
	{
		fprintf(stderr, "ERROR : rt_task_shadow: %s\n",
			strerror(-ret));
		exit(1);
	}

	/* open the device */
	device = rt_dev_open(DEVICE_NAME, 0);
	if (device < 0) {
		printf("ERROR : can't open device %s (%s)\n",
		       DEVICE_NAME, strerror(-device));
		exit(1);
	}

	/*
	 * If an argument was given on the command line, write it to the device,
	 * otherwise, read from the device.
	 */
	if (argc == 2)
	{
		sprintf(buf, "%s", argv[1]);
		size = rt_dev_write (device, (const void *)buf, strlen(buf) + 1);
		printf("Write from device %s\t: %d bytes\n", DEVICE_NAME, size);
	} else {
		size = rt_dev_read (device, (void *)buf, 1024);
		printf("Read in device %s\t: %s\n", DEVICE_NAME, buf);
	}

	/* close the device */
	ret = rt_dev_close(device);
	if (ret < 0) {
		printf("ERROR : can't close device %s (%s)\n",
		       DEVICE_NAME, strerror(-ret));
		exit(1);
	}

	return 0;
}
