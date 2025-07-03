#ifndef __STEPMOTOR_H
#define __STEPMOTOR_H

void Motor_Init(void);
void Motor_SetStep(int distance,uint8_t axis);
void Motor_Back(void);

#endif
