#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <rtdm/rtdm.h>
#include "mf2044-pwm-lib.h"

int main()
{
	mf2044_pwm_open();
	mf2044_pwm_init(MF2044_PWM_P9_14);

	// P8_19
	mf2044_pwm_frequency_set(MF2044_PWM_P8_19,100);
	mf2044_pwm_duty_cycle_set(MF2044_PWM_P8_19,25);

	mf2044_pwm_deinit(MF2044_PWM_P9_14);
	mf2044_pwm_close();
}

