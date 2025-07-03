#include "stm32f10x.h"                  // Device header

void Magnet_Init(void)
{
	/*开启时钟*/
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);

	/*结构体定义*/
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	TIM_OCInitTypeDef TIM_OCInitStructure;
	TIM_OCStructInit(&TIM_OCInitStructure);//OC结构体赋初始值
	
	/*GPIO配置*/
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);

	/*时基单元配置*/
	TIM_TimeBaseStructure.TIM_Period = 100 - 1;				// 设置自动重装载寄存器周期的值
	TIM_TimeBaseStructure.TIM_Prescaler = 10 - 1;				// 设置时钟频率除数的预分频值
	TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;		// 输入捕获分频
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up; // TIM 向上计数
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

	/*输出比较配置*/
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;               //输出比较模式，选择PWM模式1
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;       //输出极性，选择为高，若选择极性为低，则输出高低电平取反
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;   //输出使能
	TIM_OCInitStructure.TIM_Pulse = 0;								//初始的CCR值
	TIM_OC4Init(TIM3, &TIM_OCInitStructure);
	
	TIM_Cmd(TIM3, ENABLE);									  			
}

void Magnet_Catch(void)
{
	TIM_SetCompare4(TIM3,80);
}

void Magnet_Release(void)
{
	TIM_SetCompare4(TIM3,0);
}
