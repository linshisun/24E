#include "stm32f10x.h"                  // Device header

EXTI_InitTypeDef EXTI_InitStructure; //����ṹ�����
volatile uint8_t exti_flag;

void Stopper_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);		//����GPIOB��ʱ��
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);		//����AFIO��ʱ�ӣ��ⲿ�жϱ��뿪��AFIO��ʱ��
	
	/*GPIO��ʼ��*/
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);						//��PB14���ų�ʼ��Ϊ��������
	
	/*AFIOѡ���ж�����*/
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource6);//���ⲿ�жϵ�14����ӳ�䵽GPIOB����ѡ��PB14Ϊ�ⲿ�ж�����
	GPIO_EXTILineConfig(GPIO_PortSourceGPIOB, GPIO_PinSource7);//���ⲿ�жϵ�14����ӳ�䵽GPIOB����ѡ��PB14Ϊ�ⲿ�ж�����
	
	/*EXTI��ʼ��*/
	EXTI_InitStructure.EXTI_Line = EXTI_Line6;					//ѡ�������ⲿ�жϵ�14����
	EXTI_InitStructure.EXTI_LineCmd = DISABLE;					//ָ���ⲿ�ж���ʧ�ܣ�����
	EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;			//ָ���ⲿ�ж���Ϊ�ж�ģʽ
	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;		//ָ���ⲿ�ж���Ϊ�½��ش���
	EXTI_Init(&EXTI_InitStructure);								//���ṹ���������EXTI_Init������EXTI����
	
	EXTI_InitStructure.EXTI_Line = EXTI_Line7;					//ѡ�������ⲿ�жϵ�14����
	EXTI_Init(&EXTI_InitStructure);								//���ṹ���������EXTI_Init������EXTI����
		
	/*NVIC����*/
	NVIC_InitTypeDef NVIC_InitStructure;						//����ṹ�����
	NVIC_InitStructure.NVIC_IRQChannel = EXTI9_5_IRQn;			//ѡ������NVIC��EXTI15_10��
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;				//ָ��NVIC��·ʹ��
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;	//ָ��NVIC��·����ռ���ȼ�Ϊ1
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;			//ָ��NVIC��·����Ӧ���ȼ�Ϊ1
	NVIC_Init(&NVIC_InitStructure);								//���ṹ���������NVIC_Init������NVIC����
}

void EXTI9_5_IRQHandler(void)
{
	if (EXTI_GetITStatus(EXTI_Line6) == SET)		//x����λ������
	{
		/*��������������������󣬿��ٴ��ж����ŵ�ƽ���Ա��ⶶ��*/
		if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_6) == 0)
		{
			exti_flag = 1;
			EXTI_InitStructure.EXTI_Line = EXTI_Line6;
			EXTI_InitStructure.EXTI_LineCmd = DISABLE;
			EXTI_Init(&EXTI_InitStructure);
		}
		EXTI_ClearITPendingBit(EXTI_Line6);		//����ⲿ�ж��ߵ��жϱ�־λ
												//�жϱ�־λ�������
												//�����жϽ��������ϵش�����������������
	}
	if (EXTI_GetITStatus(EXTI_Line7) == SET)	//y����λ������
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
