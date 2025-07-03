#ifndef __SERIAL_H
#define __SERIAL_H

#include <stdio.h>

extern char Serial3_RxPacket[];
extern uint8_t Serial3_RxFlag;

void Serial3_Init(void);
void Serial3_SendByte(uint8_t Byte);
void Serial3_SendArray(uint8_t *Array, uint16_t Length);
void Serial3_SendString(char *String);
void Serial3_SendNumber(uint32_t Number, uint8_t Length);

#endif
