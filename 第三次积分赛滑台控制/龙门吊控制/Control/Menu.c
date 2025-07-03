#include "stm32f10x.h"                  // Device header
#include "Serial.h"
#include "Key.h"
#include "OLED.h"

extern uint8_t KeyNum;
uint8_t mode,block,count,step,m_flag;

void menu(void)
{
	if(KeyNum==1||step==1)//进入下一级菜单
	{
		switch(mode)
		{
			case 1:{//黑棋下5号格
				Serial3_SendString("OK");
				mode = 0;//mode置0，不要在下一次循环中重复case中语句
				break;
			}
			case 2:{//2黑2白下指定格
				step = 1;//持续处于下一级菜单
				if(KeyNum==1 && m_flag == 1){//防止并发
					Serial3_SendNumber(block,1);
					block = 0;
					count++;
					if(count>=4){//发送次数超过4次，则该模式结束
						step = 0;
						mode = 0;
						count = 0;
						m_flag = 0;
					}
					break;
				}
				if(KeyNum==2){
					block++;
					if(block>=9){
						block = 0;
					}					
				}
				m_flag = 1;
				break;
			}
			case 3:{//机先手
				step = 1;
				if(KeyNum==1 && m_flag == 1){
					Serial3_SendNumber(block,1);
					block = 0;
					m_flag = 0;
					mode = 5;//进入对弈
					break;
				}
				if(KeyNum==2){
					block++;
					if(block>=9){
						block = 0;
					}					
				}
				m_flag = 1;
				break;
			}
			case 4:{//人先手
				step = 1;
				mode = 5;
				break;
			}
			case 5:{//正在对弈
				if(KeyNum == 1){
					Serial3_SendString("OK");
				}
				if(KeyNum == 2){
					step = 0;
					mode = 0;
				}
				break;
			}
		}
	}
	if(KeyNum == 2 && step == 0)
	{
		mode++;
		if(mode>=5){
			mode = 0;//限制mode在0~4范围内
		}
	}
	OLED_ShowNum(2,1,mode,1);
	OLED_ShowNum(3,1,block,1);
}
