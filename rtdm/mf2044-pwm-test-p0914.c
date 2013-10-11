#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <rtdm/rtdm.h>
#include <unistd.h>
#include "mf2044-pwm-lib.h"
#include <assert.h>

int main(int argc, char** argv)
{
	// P8_19
	int param_opt;
	int freq = 0;
	int duty = 0;
	opterr = 0;
	while (-1 != (param_opt = getopt(argc, argv, "f:od:o")))
	{
		switch (param_opt)
		{
			case 'f':
				freq = atoi(optarg);
				break;
			case 'd':
				duty = atoi(optarg);
				break;
			default:
				assert(0);
		}
	}

	printf("freq : %d\n", freq);
	printf("duty : %d\n", duty);

	int close = 0;
	int sleep_interval = 1000;

	mf2044_pwm_open();
	mf2044_pwm_init(MF2044_PWM_P9_14);

	mf2044_pwm_frequency_set(MF2044_PWM_P9_14,freq);
	mf2044_pwm_duty_cycle_set(MF2044_PWM_P9_14,duty);

	mf2044_pwm_deinit(MF2044_PWM_P9_14);
	mf2044_pwm_close();
}
