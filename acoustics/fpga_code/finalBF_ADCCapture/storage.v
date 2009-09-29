////////////////////////////////////////////////////////////////////////////////
// Company: 			Analog Devices
// Engineer: 			Alex Arrants
// Create Date:   	01/18/08
// Design Name:   	Quad & Octal Synchronous data capture FIFO5. 
// Module Name:   	
// Project Name:  	 
// Target Device:  
// Tool versions:	ISE 9.2.01i  
// Description: 	  
// Revision:
// Comments:
// 	
////////////////////////////////////////////////////////////////////////////////  
`timescale 1ns / 1ps
module storage(
					_ffa, 
					dinA, 
					dinB, 
					dinC, 
					dinD, 
					dinE, 
					dinF, 
					dinG, 
					dinH, 
					cntrl_bits, 
					wrclk, 
					load, 
					rst, 
					rdclk, 
					rdenA, 
					rdenB, 
					dout, 
					bw_bits,
					BF_I_addr,
					BF_I_data_bus,
					BF_I_ams,
					BF_O_ardy,
					BF_I_are,
					BF_I_awe,
					dataRdyOut,
					testClk,
					led1
					);

/*

	input 		[18:0] addr,
	output tri  [15:0] data_bus,
	input 		[ 3:0] bank_select,
	output tri 			 ardy,
	input 				 are,
	input 				 awe,
	output 				 led1,
	output 				 led2,
	input 				 testClk,
	output 				 sma1,
	output 				 sma2
	*/
//BF interface stuff
input testClk;

input	[18:0]	BF_I_addr;
output tri[15:0]	BF_I_data_bus;
input [3:0]		BF_I_ams;
output tri		BF_O_ardy;
input				BF_I_are;
input				BF_I_awe;
output			dataRdyOut;

input wrclk, rst;
input rdclk, rdenA, rdenB, load;
input [13:0] dinA;
input [13:0] dinB;
input [13:0] dinC;
input [13:0] dinD;
input [13:0] dinE;
input [13:0] dinF;
input [13:0] dinG;
input [13:0] dinH;
input [1:0] bw_bits;
input [2:0] cntrl_bits;
output reg [15:0] dout;
output _ffa;
output led1;

wire [15:0] doutA;
wire [15:0] doutB;
wire [15:0] doutC;
wire [15:0] doutD;
wire [15:0] doutE;
wire [15:0] doutF;
wire [15:0] doutG;
wire [15:0] doutH;

wire [11:0] dinA_2s;
wire [15:0] decA, decB, decC, decD;
wire rdyA, rdyB, rdyC, rdyD;

//decimator

decimate decimA 
		(  
			.din( {~dinA[11], dinA[10:0]} ),
			.dout(decA),
			.rdy(rdyA),
			.nd(1'b1),
			.rfd(),
			.clk(wrclk)
		);


decimate decimB
		(  
			.din( {~dinB[11], dinB[10:0]} ),
			.dout(decB),
			.rdy(rdyB),
			.nd(1'b1),
			.rfd(),
			.clk(wrclk)
		);
		
decimate decimC 
		(  
			.din( {~dinC[11], dinC[10:0]} ),
			.dout(decC),
			.rdy(rdyC),
			.nd(1'b1),
			.rfd(),
			.clk(wrclk)
		);

decimate decimD 
		(  
			.din( {~dinD[11], dinD[10:0]} ),
			.dout(decD),
			.rdy(rdyD),
			.nd(1'b1),
			.rfd(),
			.clk(wrclk)
		);

bfBlock bfinInterface
(	
	.addr(BF_I_addr),
	.data_bus(BF_I_data_bus),
 	.bank_select(BF_I_ams),
	.ardy(BF_O_ardy),
	.are(BF_I_are),
	.awe(BF_I_awe),
	.led1(dataRdyOut),
	.led2(),
	.testClk(testClk),
	.sma1(),
	.sma2(),
	.chanA(decA),
	.chanB(decB),
	.chanC(decC),
	.chanD(decD),
	.chanAvalid(rdyA),
	.chanBvalid(rdyB),
	.chanCvalid(rdyC),
	.chanDvalid(rdyD),
	.adcClk(wrclk)
);

/*
input	[18:0]	BF_I_addr;
input [15:0]	BF_I_data_bus;
input [3:0]		BF_I_ams;
output tri		BF_O_ardy;
input				BF_I_are;
input				BF_I_awe;
*/

endmodule
