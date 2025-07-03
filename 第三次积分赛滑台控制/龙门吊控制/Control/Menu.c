#include "stm32f10x.h"                  // Device header
#include "Serial.h"
#include "Key.h"
#include "OLED.h"

extern uint8_t KeyNum;
uint8_t mode,block,count,step,m_flag;

void menu(void)
{
	if(KeyNum==1||step==1)//������һ���˵�
	{
		switch(mode)
		{
			case 1:{//������5�Ÿ�
				Serial3_SendString("OK");
				mode = 0;//mode��0����Ҫ����һ��ѭ�����ظ�case�����
				break;
			}
			case 2:{//2��2����ָ����
				step = 1;//����������һ���˵�
				if(KeyNum==1 && m_flag == 1){//��ֹ����
					Serial3_SendNumber(block,1);
					block = 0;
					count++;
					if(count>=4){//���ʹ�������4�Σ����ģʽ����
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
			case 3:{//������
				step = 1;
				if(KeyNum==1 && m_flag == 1){
					Serial3_SendNumber(block,1);
					block = 0;
					m_flag = 0;
					mode = 5;//�������
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
			case 4:{//������
				step = 1;
				mode = 5;
				break;
			}
			case 5:{//���ڶ���
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
			mode = 0;//����mode��0~4��Χ��
		}
	}
	OLED_ShowNum(2,1,mode,1);
	OLED_ShowNum(3,1,block,1);
}
