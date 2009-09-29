`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 	   Underwater Robtics Club
// Engineer: 	   Baird Hendrix
// 
// Create Date:    17:20:33 07/05/2009 
// Design Name: 
// Module Name:    bfInterface 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module bfInterfaceDP 
#(
	parameter BANK0_MASK =  3'h0,
	parameter BANK1_MASK =  3'h1
)
(
	input					 I_rst,
	output reg			 O_dataRdy,
	output reg			 O_bankSelect,
	input 		[15:0] BF_I_addr,
	output tri 	[15:0] BF_OT_dataBus,
	input 				 BF_I_bankSelect,
	input 				 BF_I_are,
	input 				 BF_I_awe,
	input					 BF_I_clk,
	output tri			 BF_O_ardy,
	input 				 ADC_I_clk,
	input 				 ADC_I_dataValid,
	input 		[15:0] ADC_I_data,
	output				 O_bankInUse //0 if bank 0 being written to, 1 if bank 1
);
	
	//NOT REGISTERS
	reg [1:0] bankEnables;
	reg [15:0] dataOut;
	reg dataOutRdy;
	
	
	//registers
	reg [13:0] fifoCount;
	reg [3:0] bankSelectTrans;
	
	//wires
	wire bank0Rdy, bank1Rdy;
	wire bank0adrseek, bank1adrseek;
	
	//RAM outputs
	wire [15:0] bank0Out, bank1Out;
	
	//select active bank based on address
	assign bank0adrseek = BF_I_addr[15:13] == BANK0_MASK;
	assign bank1adrseek = BF_I_addr[15:13] == BANK1_MASK;
	
	//do not remove
	//assign BF_O_ardy = 1'bz;
	assign O_bankInUse = fifoCount[13];
	
	//bank select 0
	always @(*)
		casex( {	 
					 BF_I_are, 							//3 - MSB
					 BF_I_bankSelect, 				//2
					 bank0adrseek,						//1
					 bank1adrseek						//0
				} )
			4'b1110	:	bankEnables <= 2'b01; //Bank 0 on,  Bank 1 off
			4'b1101	:	bankEnables <= 2'b10; //Bank 0 off, Bank 1 on
			default	:	bankEnables <= 2'b00;
		endcase
	
	//address counters
	always @(posedge ADC_I_clk)
		if(I_rst)
			fifoCount <= 16'h0000;
		else if(ADC_I_dataValid)
			fifoCount <= fifoCount + 1;
		else
			fifoCount <= fifoCount;
	
	//module instantiation
	sram_bank bank0
	(
		//PortA ADC Side
		.addra	(fifoCount[12:0]),
		.dina		(ADC_I_data),
		.wea		(ADC_I_dataValid && ~fifoCount[13]),
		.ena		(~fifoCount[13]),
		.clka		(ADC_I_clk),
		//PortB BF Side
		.addrb	( BF_I_addr[12:0] ),
		.doutb	(bank0Out),
		.enb		(bankEnables[0]),
		.ndb		(1'b1),
		.rfdb		(),
		.rdyb		(bank0Rdy),
		.clkb		(BF_I_clk)
	);
	
	sram_bank bank1
	(
		//PortA ADC Side
		.addra	(fifoCount[12:0]),
		.dina		(ADC_I_data + 4),
		.wea		(ADC_I_dataValid && fifoCount[13]),
		.ena		(fifoCount[13]),
		.clka		(ADC_I_clk),
		//PortB BF Side
		.addrb	( BF_I_addr[12:0] ),
		.doutb	(bank1Out),
		.enb		(bankEnables[1]),
		.ndb		(1'b1),
		.rfdb		(),
		.rdyb		(bank1Rdy),
		.clkb		(BF_I_clk)
	);
	

	//Output select
	always@(*)
		if (bankEnables == 2'b10)
			dataOut <= bank1Out;
		else
			dataOut <= bank0Out;
	
	//Output ready flag
	always@(*)
		casex ( { 
					bankEnables[1],
					bankEnables[0],
					bank1Rdy,
					bank0Rdy
				} )
					
					4'b1x1x	:	dataOutRdy <= 1'b1;
					4'b0101	:	dataOutRdy <= 1'b1;
					default	:  dataOutRdy <= 1'b0;
		endcase
	
	//Tristate output control
	assign BF_OT_dataBus = dataOutRdy ? dataOut : 16'hzzzz;
	
/*	//Output data ready pin control
	assign BF_O_ardy = (BF_I_are && BF_I_bankSelect) ? dataOutRdy : 1'bz;
	
	always @(posedge BF_I_clk)
		O_bankSelect <= bankEnables == 2'b01;
	
	//bank select
	always @(posedge BF_I_clk)
		bankSelectTrans <= {bankSelectTrans[1:0], bankEnables};
	
	always @(posedge BF_I_clk)
		O_dataRdy <= (bankSelectTrans[3:2] != bankSelectTrans[1:0]);
	*/
	
endmodule

