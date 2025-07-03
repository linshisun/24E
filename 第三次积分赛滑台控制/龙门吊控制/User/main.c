#include "stm32f10x.h"                  // Device header
#include "Delay.h"
#include "Timer.h"
#include "OLED.h"
#include "Serial.h"
#include "Key.h"
#include "StepMotor.h"
#include "Menu.h"
#include "Location.h"
#include "magnet.h"
#include "Stopper.h"

uint8_t KeyNum,p;
int Distance;//mm

int main(void)
{
	Key_Init();
	Serial3_Init();
	OLED_Init();
	location_Init();
	Magnet_Init();
	Motor_Init();
	Stopper_Init();
	Timer_Init();
	
	OLED_ShowString(1,1,"MENU");
	
	while(1)
	{
		KeyNum = Key_GetNum();
		menu();
		if (Serial3_RxFlag ==  1)		 //如果接收到数据包
		{ 
			sscanf(Serial3_RxPacket,"X%d,Y%d,XX%d,YY%d",
						&Motor_Work.chess_x,&Motor_Work.chess_y,
						&Motor_Work.block_x,&Motor_Work.block_y);
			
			location_Update();//阻塞式移动
			Serial3_RxFlag = 0;			//处理完成后，需要将接收数据包标志位清零，否则将无法接收后续数据包
		} 
//		if(KeyNum == 1)
//		{Motor_Back();}
//		if(KeyNum == 1)
//		{Serial3_SendString("OK");
//		p=1;}
//		if(KeyNum == 2)
//		{Serial3_SendNumber(4,1);
//		p=2;}
	}	
}

void TIM2_IRQHandler(void)//20ms
{
	if(TIM_GetITStatus(TIM2, TIM_IT_Update) == SET)
	{
		Key_Tick();
		
		TIM_ClearITPendingBit(TIM2, TIM_IT_Update);
	}
}
