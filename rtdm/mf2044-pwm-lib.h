#ifndef MF2044_PWM_LIB_H
#define MF2044_PWM_LIB_H

typedef enum {
	MF2044_PWM_PNULL=0,
	MF2044_PWM_P8_13=1 << 9,
	MF2044_PWM_P8_19=1 << 8,
//	MF2044_PWM_P8_34=1 << 4,
//	MF2044_PWM_P8_36=1 << 4,
	MF2044_PWM_P9_14=1 << 4,
	MF2044_PWM_P9_16=1 << 5,
//	MF2044_PWM_P9_21=1 << 4,
//	MF2044_PWM_P9_22=1 << 4,
//	MF2044_PWM_P9_28=1 << 4,
//	MF2044_PWM_P9_39=1 << 4,
//	MF2044_PWM_P9_31=1 << 4,
//	MF2044_PWM_P9_42=1 << 4,
	MF2044_PWM_PMAX,
} MF2044_PWM_PINS;

int mf2044_pwm_open(void);
int mf2044_pwm_close(void);
int mf2044_pwm_init(MF2044_PWM_PINS pin);
int mf2044_pwm_deinit(MF2044_PWM_PINS pin);
int mf2044_pwm_duty_cycle_set(MF2044_PWM_PINS pin, unsigned int duty);
int mf2044_pwm_freqency_set(MF2044_PWM_PINS pin, int freq);

#endif //MF2044_PWM_LIB_H
