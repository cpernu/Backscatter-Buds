#include <msp430fr2355.h>


/**
 * main.c
 */
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
	P3DIR = 0X01;
	P3OUT=0X01;   //make bit0 HIGH
	unsigned int i;
    while(1)
    {
        P1OUT ^=0X01;   ////toggle the bits
        for(i=0;i<20000;i++){   // delay till you make LED LOW HIGH
        }
    }
	return 0;
}
