#ifndef MF2044_PWM_LIB_H
#define MF2044_PWM_LIB_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
	MF2044_PWM_PNULL=0,
	MF2044_PWM_P9_14=(1<<4), //EHRPWM1 A
	MF2044_PWM_P9_16=(1<<5), //EHRPWM1 B
	MF2044_PWM_P9_22=(1<<6), //EHRPWM0 A
	MF2044_PWM_P9_21=(1<<7), //EHRPWM0 B
	MF2044_PWM_P8_19=(1<<8), //EHRPWM2 A
	MF2044_PWM_P8_13=(1<<9), //EHRPWM2 B
	MF2044_PWM_PMAX,
} MF2044_PWM_PINS;

int mf2044_pwm_open(void);
int mf2044_pwm_close(void);
int mf2044_pwm_duty_cycle_set(MF2044_PWM_PINS pin, int duty);
int mf2044_pwm_freqency_set(MF2044_PWM_PINS pin, int freq);
int mf2044_pwm_duty_cycle_get(MF2044_PWM_PINS pin);
int mf2044_pwm_frequency_get(MF2044_PWM_PINS pin);

#ifdef __cplusplus
}
#endif

#endif //MF2044_PWM_LIB_H
