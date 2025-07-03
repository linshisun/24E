#include "stm32f10x.h"                  // Device header
#include "stm32f10x.h"

void Timer_Init(void)//20ms
{
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
		
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStruct;//配置时基单元
	TIM_TimeBaseInitStruct.TIM_ClockDivision = TIM_CKD_DIV1;//不分频
	TIM_TimeBaseInitStruct.TIM_CounterMode = TIM_CounterMode_Up;//向上计数
	TIM_TimeBaseInitStruct.TIM_Period = 1000 - 1;
	TIM_TimeBaseInitStruct.TIM_Prescaler = 720 - 1;
	TIM_TimeBaseInitStruct.TIM_RepetitionCounter = 0;//重复计数器，
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStruct);
	
	TIM_ClearFlag(TIM2, TIM_FLAG_Update);//清除标志位
	TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);//打开更新中断到NVIC的通路
	
	NVIC_InitTypeDef NVIC_InitStruct;
	NVIC_InitStruct.NVIC_IRQChannel = TIM2_IRQn;//定时器1在NVIC中的通道
	NVIC_InitStruct.NVIC_IRQChannelCmd = ENABLE;
	NVIC_InitStruct.NVIC_IRQChannelPreemptionPriority = 2;//抢占优先级
	NVIC_InitStruct.NVIC_IRQChannelSubPriority = 2;//响应优先级
	NVIC_Init(&NVIC_InitStruct);
	
	TIM_Cmd(TIM2, ENABLE);
}
