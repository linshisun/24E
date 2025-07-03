#include "stm32f10x.h"                  // Device header
#include "Delay.h"
#include "Stepmotor.h"
#include "Location.h"
#include "Magnet.h"

location_t Motor_Work;//�������,����,�����Ŀǰ����
int x_distance,y_distance;

void location_Init(void)//�������ʼ����Ĭ��(0,0)
{
	Motor_Work.chess_x = 0;
	Motor_Work.chess_y = 0;
	Motor_Work.block_x = 0;
	Motor_Work.block_y = 0;   
}

void location_Update(void)//ִ��һ������
{
	TIM_Cmd(TIM2, DISABLE);
	/*����ץȡ*/
	x_distance = Motor_Work.chess_x;
	y_distance = Motor_Work.chess_y;
	
	Motor_SetStep(y_distance,y);
	Motor_SetStep(x_distance,x);
	Motor_SetStep(-10,z);//���Ķ�
	Magnet_Catch();
	Delay_ms(500);
	Motor_SetStep(10,z);//���Ķ�
	
	/*��������*/
	x_distance = Motor_Work.block_x - Motor_Work.chess_x;
	y_distance = Motor_Work.block_y - Motor_Work.chess_y;
	
	Motor_SetStep(x_distance,x);
	Motor_SetStep(y_distance,y);
	Motor_SetStep(-10,z);//���Ķ�
	Magnet_Release();
	Delay_ms(500);
	Motor_SetStep(10,z);//���Ķ�
	
	if(Motor_Work.block_y<=10)
	{Motor_SetStep(10,y);}
	if(Motor_Work.block_x<=10)
	{Motor_SetStep(10,x);}
		
//	/*������λ*/
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
