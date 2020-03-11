/**********************************************
*  �t���\���퐧�䃉�C�u����
*  �����֐��͈ȉ�
*    lcd_init()    ----- ������
*    lcd_cmd(cmd)  ----- �R�}���h�o��
*    lcd_data(chr) ----- �P�����\���o��
*    lcd_clear()   ----- �S����
************************************************/
/********* �f�[�^�o�̓T�u�֐� **************/
void lcd_out(int code, int flag)
{
	//output_x((code & 0xF0) | (input_x() & 0x0F));

	if((code & 0x80) == 0){
		output_bit(DB7, 0);
	}
	else{
		output_bit(DB7, 1);
	}

	if((code & 0x40) == 0){
		output_bit(DB6, 0);
	}
	else{
		output_bit(DB6, 1);
	}

	if((code & 0x20) == 0){
		output_bit(DB5, 0);
	}
	else{
		output_bit(DB5, 1);
	}

	if((code & 0x10) == 0){
		output_bit(DB4, 0);
	}
	else{
		output_bit(DB4, 1);
	}

	if (flag == 0){
		output_high(rs);		//�\���f�[�^�̏ꍇ
	}
	else{
		output_low(rs);			//�R�}���h�f�[�^�̏ꍇ
	}
	delay_cycles(1);			//NOP		
	output_high(stb);			//strobe out
	delay_cycles(2);			//NOP
	output_low(stb);			//reset strobe

}
/******** �P�����\���֐� **********/
void lcd_data(int asci)
{
	lcd_out(asci, 0);			//��ʂS�r�b�g�o��
	lcd_out(asci<<4, 0);		//���ʂS�r�b�g�o��
	delay_us(50);				//50��sec�҂�
}
/******** �R�}���h�o�͊֐� ********/
void lcd_cmd(int cmd)
{
	lcd_out(cmd, 1);			//��ʂS�r�b�g�o��
	lcd_out(cmd<<4, 1);			//���ʂS�r�b�g�o��
	delay_ms(2);				//2msec�҂�
}
/********** �S�����֐� *********/
void lcd_clear()
{
	lcd_cmd(0x01);				//�������R�}���h�o��
	delay_ms(15);				//15msec�҂�
}
/******** �������֐� *********/
void lcd_init()
{
	set_tris_x(mode);			//���[�h�Z�b�g
//
//	set_tris_A(0xF0);
//	
	delay_ms(15);
	lcd_out(0x30, 1);			//8bit mode set
	delay_ms(5);
	lcd_out(0x30, 1);			//8bit mode set
	delay_ms(1);
	lcd_out(0x30, 1);			//8bit mode set
	delay_ms(1);
	lcd_out(0x20, 1);			//4bit mode set
	delay_ms(1);
	lcd_cmd(0x2E);				//DL=0 4bit mode
	lcd_cmd(0x08);				//display off C=D=B=0
	lcd_cmd(0x0D);				//display on C=D=1 B=0
	lcd_cmd(0x06);				//entry I/D=1 S=0
	lcd_cmd(0x02);				//cursor home
}

