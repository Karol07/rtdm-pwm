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
	MF2044_PWM_PINS pin=1;
	int freq = 100;
	int duty = 75;
	opterr = 0;
	while (-1 != (param_opt = getopt(argc, argv, "f:od:op:o")))
	{
		switch (param_opt)
		{
			case 'p':
				pin = atoi(optarg);
				break;
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
	printf("pin : %d\n", pin);
	printf("freq : %d\n", freq);
	printf("duty : %d\n", duty);

	switch(pin)
	{
		case 1:
			pin = MF2044_PWM_P9_14;
			break;
		case 2:
			pin = MF2044_PWM_P9_16;
			break;
		case 3:
			pin = MF2044_PWM_P9_21;
			break;
		case 4:
			pin = MF2044_PWM_P9_22;
			break;
		case 5:
			pin = MF2044_PWM_P8_13;
			break;
		case 6:
			pin = MF2044_PWM_P8_19;
			break;
		default:
			assert(0);
	}

	mf2044_pwm_open();
	mf2044_pwm_frequency_set(pin,freq);
	mf2044_pwm_duty_cycle_set(pin,duty);

	unsigned int df = mf2044_pwm_frequency_get(pin);
	unsigned int du = mf2044_pwm_duty_cycle_get(pin);
	printf("freq %d\n", df);
	printf("duty %d\n", du);
//	mf2044_pwm_close();
}

