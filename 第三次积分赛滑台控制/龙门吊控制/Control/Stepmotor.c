#include "stm32f10x.h"                  // Device header
#include "Delay.h"
#include "Key.h"
#include <stdlib.h>

extern uint8_t KeyNum,exti_flag;
extern EXTI_InitTypeDef EXTI_InitStructure;

void Motor_Init(void)//GPIO��ʼ��
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	/*GPIO����*/
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12 | GPIO_Pin_13 | GPIO_Pin_14 | GPIO_Pin_15;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8 | GPIO_Pin_9 | GPIO_Pin_10 | GPIO_Pin_11 | GPIO_Pin_12;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	GPIO_ResetBits(GPIOB, GPIO_Pin_14);//ʹ��
	GPIO_ResetBits(GPIOA, GPIO_Pin_9);//ʹ��
	GPIO_ResetBits(GPIOA, GPIO_Pin_12);//ʹ��
}

void Motor_SetStep(int distance,uint8_t axis)
{
	uint16_t PulseNum;
	uint16_t Current_Delay = 500;//Ŀǰ����1/(500*2*10^-6)=1000Hz,1000/200=5ת/s��5*4=20mm/s
	uint16_t i;
	
	PulseNum=abs(distance)*50;//������=����/(һȦ�ƶ�����)4mm*360��/(������)1.8��
	
	switch(axis)
	{
		case 1:{//x
			if(distance>0){
				GPIO_ResetBits(GPIOB, GPIO_Pin_13);//ǰ��
			}
			else{
				GPIO_SetBits(GPIOB, GPIO_Pin_13);//����
			}
			break;
		}
		case 2:{
			if(distance>0){
				GPIO_SetBits(GPIOA, GPIO_Pin_8);//ǰ��
			}
			else{
				GPIO_ResetBits(GPIOA, GPIO_Pin_8);//����
			}
			break;
		}
		case 3:{
			if(distance>0){
				GPIO_SetBits(GPIOA, GPIO_Pin_11);//ǰ��
			}
			else{
				GPIO_ResetBits(GPIOA, GPIO_Pin_11);//����
			}
			break;
		}
	}
	
	//����
	for(i = 0; i < PulseNum; i++)
    {
		switch(axis)
		{
			case 1:{
				// ��������
				GPIO_SetBits(GPIOB, GPIO_Pin_12);
				Delay_us(Current_Delay);
				GPIO_ResetBits(GPIOB, GPIO_Pin_12);
				Delay_us(Current_Delay);
				break;
			}
			case 2:{
				// ��������
				GPIO_SetBits(GPIOB, GPIO_Pin_15);
				Delay_us(Current_Delay);
				GPIO_ResetBits(GPIOB, GPIO_Pin_15);
				Delay_us(Current_Delay);
				break;
			}
			case 3:{
				// ��������
				GPIO_SetBits(GPIOA, GPIO_Pin_10);
				Delay_us(Current_Delay);
				GPIO_ResetBits(GPIOA, GPIO_Pin_10);
				Delay_us(Current_Delay);
				break;
			}
		}
    }
    Delay_ms(500);
}

void Motor_Back(void)
{
	uint16_t Back_Delay=500;
	GPIO_ResetBits(GPIOB, GPIO_Pin_14);//ʹ��x
	GPIO_ResetBits(GPIOA, GPIO_Pin_9);//ʹ��y
	
	exti_flag = 0;
	EXTI_InitStructure.EXTI_Line = EXTI_Line6;
	EXTI_InitStructure.EXTI_LineCmd = ENABLE;
	EXTI_Init(&EXTI_InitStructure);
	EXTI_ClearITPendingBit(EXTI_Line6);
	
	EXTI_InitStructure.EXTI_Line = EXTI_Line7;
	EXTI_Init(&EXTI_InitStructure);
	EXTI_ClearITPendingBit(EXTI_Line7);
	
	GPIO_SetBits(GPIOB, GPIO_Pin_13);//����x
	GPIO_ResetBits(GPIOA, GPIO_Pin_8);//����y
	while(exti_flag == 0)//�Ȼ�λx��
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_12);
		Delay_us(Back_Delay);
		GPIO_ResetBits(GPIOB, GPIO_Pin_12);
		Delay_us(Back_Delay);
	}
	Delay_s(1);
	while(exti_flag == 1)//�ٻ�λy��
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_15);
		Delay_us(Back_Delay);
		GPIO_ResetBits(GPIOB, GPIO_Pin_15);
		Delay_us(Back_Delay);
	}
}
