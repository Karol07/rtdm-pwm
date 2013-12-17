#ifndef MF2044_ENC_LIB_H
#define MF2044_ENC_LIB_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
	MF2044_ENC_PIN_NULL=0,
	MF2044_ENC_0=1 << 4,
	MF2044_ENC_1=1 << 5,
	MF2044_ENC_2=1 << 6,
	MF2044_ENC_PIN_MAX,
} MF2044_ENC_PINS;

typedef enum {
	MF2044_ENC_MODE_NULL=0,
	MF2044_ENC_MODE_ABSOLUTE,
	MF2044_ENC_MODE_RELATIVE,
	MF2044_ENC_MODE_MAX,
} MF2044_ENC_MODES;

int mf2044_enc_open(void);
int mf2044_enc_close(void);

MF2044_ENC_MODES mf2044_enc_mode_get(MF2044_ENC_PINS pin);
int mf2044_enc_mode_set(MF2044_ENC_PINS pin, MF2044_ENC_MODES mode);

uint64_t mf2044_enc_period_get(MF2044_ENC_PINS pin);
int mf2044_enc_period_set(MF2044_ENC_PINS pin, uint64_t period);

int32_t mf2044_enc_position_get(MF2044_ENC_PINS pin);
int mf2044_enc_position_set(MF2044_ENC_PINS pin, int32_t position);

double mf2044_enc_velocity_get(MF2044_ENC_PINS pin);

#ifdef __cplusplus
}
#endif

#endif //MF2044_ENC_LIB_H
