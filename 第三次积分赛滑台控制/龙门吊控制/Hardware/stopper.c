#include "stm32f10x.h"                  // Device header

EXTI_InitTypeDef EXTI_InitStructure; //定义结构体变量
volatile uint8_t exti_flag;

void Stopper_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);		//开启GPIOB的时钟
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);		//开启AFIO的时钟，外部中断必须开启AFIO的时钟
	
	/*GPIO初始化*/
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);						//将PB14引脚初始化为上拉输入
	
	/*AFIO选择中断引脚*/
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource6);//将外部中断的14号线映射到GPIOB，即选择PB14为外部中断引脚
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource7);//将外部中断的14号线映射到GPIOB，即选择PB14为外部中断引脚
	
	/*EXTI初始化*/
	EXTI_InitStructure.EXTI_Line = EXTI_Line6;					//选择配置外部中断的14号线
	EXTI_InitStructure.EXTI_LineCmd = DISABLE;					//指定外部中断线失能！！！
	EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;			//指定外部中断线为中断模式
	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;		//指定外部中断线为下降沿触发
	EXTI_Init(&EXTI_InitStructure);								//将结构体变量交给EXTI_Init，配置EXTI外设
	
	EXTI_InitStructure.EXTI_Line = EXTI_Line7;					//选择配置外部中断的14号线
	EXTI_Init(&EXTI_InitStructure);								//将结构体变量交给EXTI_Init，配置EXTI外设
		
	/*NVIC配置*/
	NVIC_InitTypeDef NVIC_InitStructure;						//定义结构体变量
	NVIC_InitStructure.NVIC_IRQChannel = EXTI9_5_IRQn;			//选择配置NVIC的EXTI15_10线
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;				//指定NVIC线路使能
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;	//指定NVIC线路的抢占优先级为1
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;			//指定NVIC线路的响应优先级为1
	NVIC_Init(&NVIC_InitStructure);								//将结构体变量交给NVIC_Init，配置NVIC外设
}

void EXTI9_5_IRQHandler(void)
{
	if (EXTI_GetITStatus(EXTI_Line6) == SET)		//x轴限位器触发
	{
		/*如果出现数据乱跳的现象，可再次判断引脚电平，以避免抖动*/
		if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_6) == 0)
		{
			exti_flag = 1;
			EXTI_InitStructure.EXTI_Line = EXTI_Line6;
			EXTI_InitStructure.EXTI_LineCmd = DISABLE;
			EXTI_Init(&EXTI_InitStructure);
		}
		EXTI_ClearITPendingBit(EXTI_Line6);		//清除外部中断线的中断标志位
												//中断标志位必须清除
												//否则中断将连续不断地触发，导致主程序卡死
	}
	if (EXTI_GetITStatus(EXTI_Line7) == SET)	//y轴限位器触发
	{
		if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_7) == 0)
		{
			exti_flag = 2;
			EXTI_InitStructure.EXTI_Line = EXTI_Line7;
			EXTI_InitStructure.EXTI_LineCmd = DISABLE;
			EXTI_Init(&EXTI_InitStructure);
		}
		EXTI_ClearITPendingBit(EXTI_Line7);	
	}
}
