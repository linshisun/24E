#ifndef __LOCATION_H
#define __LOCATION_H

typedef struct
{
    int chess_x; 
    int chess_y; 
	int block_x; 
    int block_y;
} location_t;

typedef enum{
	x = 1,
	y = 2,
	z = 3
}Axis;

extern location_t Motor_Work;//存放棋子和格子坐标

void location_Init(void);
void location_Update(void);

#endif
