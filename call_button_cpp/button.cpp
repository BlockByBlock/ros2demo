#include <wiringPi.h>
#include <string.h>
#include <stdio.h>


int main(void)
{
    int LED_PIN = 7 ;
    int BTN_PIN_1 = 12 ;
    int btn_state_1 = 0;
    char msg ;

    wiringPiSetupPhys() ;
    pinMode (LED_PIN, OUTPUT) ;
    pinMode (BTN_PIN_1, INPUT) ;
    for(;;)
    {
        btn_state_1 = digitalRead(BTN_PIN_1);
        if(btn_state_1 == 1){
            msg = 1;
            digitalWrite(LED_PIN, HIGH) ;
        }
        else{
            msg = 0;
            digitalWrite(LED_PIN, LOW) ;
        }
        printf("%d\n",msg);
        delay (100) ;
  }
}
