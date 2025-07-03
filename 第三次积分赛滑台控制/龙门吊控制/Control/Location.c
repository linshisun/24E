#include "stm32f10x.h"                  // Device header
#include "Delay.h"
#include "Stepmotor.h"
#include "Location.h"
#include "Magnet.h"

location_t Motor_Work;//存放棋子,格子,电磁铁目前坐标
int x_distance,y_distance;

void location_Init(void)//电磁铁初始坐标默认(0,0)
{
	Motor_Work.chess_x = 0;
	Motor_Work.chess_y = 0;
	Motor_Work.block_x = 0;
	Motor_Work.block_y = 0;   
}

void location_Update(void)//执行一次下棋
{
	TIM_Cmd(TIM2, DISABLE);
	/*棋子抓取*/
	x_distance = Motor_Work.chess_x;
	y_distance = Motor_Work.chess_y;
	
	Motor_SetStep(y_distance,y);
	Motor_SetStep(x_distance,x);
	Motor_SetStep(-10,z);//待改动
	Magnet_Catch();
	Delay_ms(500);
	Motor_SetStep(10,z);//待改动
	
	/*放置棋子*/
	x_distance = Motor_Work.block_x - Motor_Work.chess_x;
	y_distance = Motor_Work.block_y - Motor_Work.chess_y;
	
	Motor_SetStep(x_distance,x);
	Motor_SetStep(y_distance,y);
	Motor_SetStep(-10,z);//待改动
	Magnet_Release();
	Delay_ms(500);
	Motor_SetStep(10,z);//待改动
	
	if(Motor_Work.block_y<=10)
	{Motor_SetStep(10,y);}
	if(Motor_Work.block_x<=10)
	{Motor_SetStep(10,x);}
		
//	/*磁铁归位*/
//	x_distance = -Motor_Work.magnet_x;
//	y_distance = -Motor_Work.magnet_y;
//	
//	Motor_SetStep(y_distance,y);
//	Motor_SetStep(x_distance,x);
//	Delay_s(1);
//	
//	Motor_Work.magnet_x = 0;
//	Motor_Work.magnet_y = 0;
	Motor_Back();
	Delay_s(1);
	TIM_Cmd(TIM2, ENABLE);
}
