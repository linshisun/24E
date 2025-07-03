#include "stm32f10x.h"                  // Device header

uint8_t Key_Num;

/**
  * 函    数：按键初始化
  * 参    数：无
  * 返 回 值：无
  */
void Key_Init(void)
{
	/*开启时钟*/
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);		//开启GPIOB的时钟
	
	/*GPIO初始化*/
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3|GPIO_Pin_5;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);						//将PB0和PB10引脚初始化为上拉输入

}

/*
	返回键码值
*/
uint8_t Key_GetNum(void)
{
	uint8_t Temp;
	if (Key_Num)
	{
		Temp = Key_Num;
		Key_Num = 0;
		return Temp;
	}
	return 0;
}

uint8_t Key_GetState(void)
{
	if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_5) == 0)
	{
		return 1;
	}
	if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_3) == 0)
	{
		return 2;
	}

	return 0;
}

/*
	每隔20ms扫描一次按键
*/
void Key_Tick(void)
{
	//static uint8_t Count;
	static uint8_t CurrState, PrevState;

		
	PrevState = CurrState;
	CurrState = Key_GetState();
		
	if (CurrState == 0 && PrevState != 0)
	{
		Key_Num = PrevState;
	}
}
