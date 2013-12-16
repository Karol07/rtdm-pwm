#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <rtdm/rtdm.h>
#include <unistd.h>
#include "mf2044-enc-lib.h"
#include <assert.h>

int main(int argc, char** argv)
{
	uint64_t period = 0;
	int32_t position = -1;
	double velocity = 0.0;
	mf2044_enc_open();
	MF2044_ENC_PINS pin = MF2044_ENC_1;
	mf2044_enc_mode_set(pin,MF2044_ENC_MODE_ABSOLUTE);

	mf2044_enc_period_set(pin,100000000L);
	while (1) {
		period = mf2044_enc_period_get(pin);
		printf ("[eQEP] Period = %llu ns\n",period);
		position = mf2044_enc_position_get(pin);
		printf ("[eQEP] Position = [%ld]\n",position);
		velocity = mf2044_enc_velocity_get(pin);
		printf ("[eQEP] Velocity = [%f]\n",velocity);
		sleep(1);
	}

	return 0;
}
