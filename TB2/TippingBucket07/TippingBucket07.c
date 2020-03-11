/****************************************
*	Tipping Bucket07
*	ó éYééå±ã@
*	ì]ì|Ç‹Ç∑ï˚éÆ(2017.1.31)
***************************************/
#include  <16f1827.h>
 
#fuses HS,WDT_SW,NOPROTECT,PUT,BROWNOUT,NOLVP,MCLR,NOIESO,NOFCMEN,NODEBUG,BORV25,PLL_SW

#use delay(CLOCK = 10000000)			//Specification of a clock frequency
//#use fast_io(B)

////// LCD library setup
#define 	mode			0x05				//B0,B2:Input
#define 	output_x		output_B			//PortB use
#define 	set_tris_x	set_tris_B
#define	stb			PIN_B1			//breadboard:PIN_A0 printed board:PIN_B1
#define	rs			PIN_B4			//breadboard:PIN_A1 printed board:PIN_B4
#define	DB7			PIN_B6
#define	DB6			PIN_B7
#define	DB5			PIN_B3
#define	DB4			PIN_A1			//breadboard:PIN_B1 printed board:PIN_A1
#define  Pulse		PIN_A2			//Pulse Output Pin
#include  "lcd_lib.c"

////// Define Address
#bit		T1Start = 0x018.0	// 0:Stop Timer1, 1:Start Timer1

////// RS-232C use setup
#use rs232(BAUD =19200, XMIT=PIN_B5, RCV=PIN_B2)

////// Flow Meter setup
#define	r_bucket		0.180				// Capacity of Right Bucket
//ver1:0.19925 ver2:0.1944
#define	l_bucket		0.180				// Capacity of Left Bucket
//ver1:0.1906 ver2:0.179
const	float 		bucket_flow =  0.180;// Average Capacity of Bucket (r_bucket+l_bucket)/2
//ver1:0.194925 ver2: 0.1867
static	long		g_tcnt;				// Timer0 overflow counter
static	int			g_tx_flag;			// Data Request-to-Send Flag
static	long		g_tcnt_ms =0;			// Time measurement of a RSW pulse interval[msec.]
static	int			g_tcnt_min =0;			// Time measurement of a RSW pulse interval[min.]
static	long		g_tcnt_result =0;		// The latest RSW pulse cycle[msec.]
static	int			g_tcnt_result_min =0;		// The latest RSW pulse cycle[min.]
static 	float		g_drainage_flow = 0.0;	// The amount of discharge of a liquid 
static 	float		g_before_offset = 0.0; // Liquid that has not been pulsed output

static	int			g_cal_flag;			// Flow calculation flag 


///Timer0 interruption processing
#INT_TIMER0
void tip_cnt(){
	g_tcnt++;
	//printf("OK\n"); ////debug
}

// CCP1 interruption processingÅ@(1msec Cycle)
#INT_CCP1
void isr_ccp1(void){
	if(g_tcnt_ms < 60000){
		g_tcnt_ms++;
	}
    else if(g_tcnt_min < 3 && g_tcnt_ms >= 60000){
        g_tcnt_min++;
		g_tcnt_ms = 0;
		
		T1Start = 0;
		set_timer1(0);
		T1Start = 1;	// Start Timer1
	}
	else{
		T1Start = 0;	// Stop Timer1
	}	
}

///EXT interruption processing (time measurement of a RSW pulse interval)
#INT_EXT
void isr_ext(void){
	g_cal_flag = 1;
	g_tcnt_result = g_tcnt_ms;
	g_tcnt_result_min = g_tcnt_min;
	g_tcnt_ms = 0;
	g_tcnt_min = 0;
		
	T1Start = 0;
	set_timer1(0);
	T1Start = 1;	// Start Timer1
}	


///RS232c reception interruption processing
#INT_RDA
void isr_rcv(){
	char RcvData;
	RcvData = getc();
	
	if(RcvData == 0x61){ 		//When transmitting "a"(Shift JIS) 
		g_tx_flag = 1;
	}
	
	else if(RcvData == 0x62){	//When transmitting "b"(Shift JIS) 
		g_tcnt = 0;
		g_tcnt_ms = 0;
		g_tcnt_min = 0;
		g_tcnt_result = 0;
		g_tcnt_result_min = 0; 
		g_drainage_flow = 0.0;
		set_timer0(0);
	}
	else{}
}



void main()
{
	////-- Initialization --////
	
	/////Pulse Output Pin
	output_bit(Pulse,1);
	
	//// LCD Initialization
	lcd_init();	
	lcd_cmd(0x0C);
	lcd_clear();
	
	//// Timer0 InitializationÅ@External clock 1/1
	setup_timer_0(RTCC_EXT_L_TO_H | RTCC_DIV_1);
	set_timer0(0);
	
	/// Timer1 Initialization Internal clock prescaler 1/1	
	setup_timer_1(T1_INTERNAL | T1_DIV_BY_1);
	T1Start = 0;		// Stop Timer1
	set_timer1(0);
	
	/// CCP1InitializationÅ@1msec
	setup_ccp1(CCP_COMPARE_RESET_TIMER);
	CCP_1 = 2500; 	//1kHz(=10MHz/(4*1*2500))
	
	//Edge of external interruption(RB0)
	ext_int_edge(L_TO_H);	
	
	//WDT Initialization
	setup_wdt(WDT_2S);	

	enable_interrupts(INT_TIMER0);
	enable_interrupts(INT_CCP1);
	enable_interrupts(INT_EXT);
	enable_interrupts(INT_RDA);
	enable_interrupts(GLOBAL);
	
	long	drainage_cnt;			//The number of times of Tipping Bucket
	//float	flow_v;				//The present flow velocity
	float 	bucket_offset;		//The offset value of bucket capacity
	float 	Pulse_flow;			//Liquid pulse output before
	g_tcnt = 0;
	
	//----------- Debug ------------
	//float	bucket_flow;
	//bucket_flow = (r_bucket+l_bucket)/2;
	//------------------------------
	
	lcd_clear();
	printf(lcd_data,"restart");
	delay_ms(1000);
	
	T1Start = 1;	// Start Timer1
	
	while(1)							
	{
		restart_wdt();
		drainage_cnt =g_tcnt * 256 + (long)get_timer0();
		//printf("ms= %Ldms\n", g_tcnt_ms); ////debug

		if(g_cal_flag == 1){
			if((g_tcnt_result_min == 0) && (g_tcnt_result < 2000) ){
				bucket_offset =  0.063;
				//ver1:0.163 ver2: 0.1565
				g_drainage_flow = g_drainage_flow + bucket_flow + bucket_offset;
				Pulse_flow = g_before_offset + bucket_flow + bucket_offset;
				//printf("<2.0sec\n");////debug
			}
    		else if(g_tcnt_result_min >= 2){
                g_drainage_flow = g_drainage_flow + bucket_flow;
				Pulse_flow = g_before_offset + bucket_flow;
				//printf(">=2min.\n"); ////debug
			}
			else{
				bucket_offset = (517.8 * bucket_flow) / ((float)g_tcnt_result-517.8);
				g_drainage_flow = g_drainage_flow + bucket_flow + bucket_offset;
				Pulse_flow = g_before_offset + bucket_flow + bucket_offset;
				//printf("2sec< <2min.\n"); ////debug
			}
		
			if( Pulse_flow >= 0.3){
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				delay_ms(20);
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				delay_ms(20);
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				
				g_before_offset= Pulse_flow - 0.3;
			}
			else if( Pulse_flow >= 0.2 && Pulse_flow < 0.3 ){
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				delay_ms(20);
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				
				g_before_offset= Pulse_flow - 0.2;
			}
			else if( Pulse_flow >= 0.1 && Pulse_flow < 0.2 ){
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				
				g_before_offset= Pulse_flow - 0.1;
			}
			
			else{}
		
		g_cal_flag = 0;	
		//printf("Pulse cycle= %Ldms\n", g_tcnt_result); ////debug
		
		}
		else{}
	
	
		if(g_tx_flag ==1){
			printf("%5.1f\n",g_drainage_flow);
			g_tx_flag = 0;
		}
		else{}
		
		if(g_drainage_flow >900){
			g_tcnt = 0;
			set_timer0(0);
			g_drainage_flow=0.0;
		}
		else{}
		
		if(g_before_offset >= 0.1){
				delay_ms(20);
				output_bit(Pulse,0);
				delay_ms(15);
				output_bit(Pulse,1);
				delay_ms(20);
				
				g_before_offset= g_before_offset - 0.1;
		}
		else{}
			
		lcd_cmd(0x80);				//To the head of the 1st line
		printf(lcd_data,"C= %5lu    %1umin",drainage_cnt,g_tcnt_result_min);
		lcd_cmd(0xC0);				//To the head of the 2nd line
		//printf(lcd_data,"Flow= %6.1fL",g_drainage_flow);
        printf(lcd_data,"%6lums %6.1fL",g_tcnt_result,g_drainage_flow);
		delay_ms(500);				//0.5secä‘äu
	}
}

