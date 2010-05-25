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
module bfInterfaceSSRAM
#(
	parameter BANK0_MASK =  3'h0,
	parameter BANK1_MASK =  3'h1
)
(
	input					 I_rst,
	output reg			 O_dataRdy,
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
	input					 I_dataRead,
	output		[15:0] O_ADC_addr,
	output				 O_bankLastFilled //0 if bank 0 being written to, 1 if bank 1
);
	
	//NOT REGISTERS
	reg bankEnable;
	reg [15:0] dataOut;
	reg dataOutRdy;
	reg RAMbankSelect;
	reg bankChange;
	
	
	//registers
	reg [ 1:0] sr_RAMbankSelect;
	reg [13:0] fifoCount;
	reg validAddress;
	
	//wires
	wire bankRdy, bank1Rdy;
	wire bank0adrseek, bank1adrseek;
	wire [13:0] fifoCountN;
	
	//RAM outputs
	wire [15:0] bankOut;
	
	//Bank Select output
	assign O_bankLastFilled = fifoCount[13];
	assign O_ADC_addr = fifoCount;
	
	//fifo count N
	assign fifoCountN = fifoCount + 1;
	
	//FIFO Counter
	always@(posedge ADC_I_clk)
		if (I_rst)
			fifoCount <= 0;	
		else if (ADC_I_dataValid)		//Data must be valid for counter to increment
			fifoCount <= fifoCountN;
		else
			fifoCount <= fifoCount;

	//module instantiation
	sram_bank_large channelBank
	(
		//PortA ADC Side
		.addra		(fifoCount),
		.dina		(ADC_I_data),
		.wea		(ADC_I_dataValid),
		.ena		(1'b1),
		.clka		(ADC_I_clk),
		//PortB BF Side
		.addrb		( {RAMbankSelect, BF_I_addr[12:0]} ),
		.doutb		(bankOut),
		.enb		(bankEnable),
		.ndb		(1'b1),
		.rfdb		(),
		.rdyb		(bankRdy),
		.clkb		(BF_I_clk)
	);

	//output tristate control
	always @(*)
		case({ BF_I_are, BF_I_bankSelect, bankEnable, bankRdy })
			4'b1111	:	dataOutRdy = 1'b1;
			default	:	dataOutRdy = 1'b0;
		endcase

	//output tristate
	assign		BF_OT_dataBus = dataOutRdy ? bankOut : 16'bzzzzzzzzzzzzzzzz;
	
	//ardy control
	assign 	BF_O_ardy = ( BF_I_are && BF_I_bankSelect && bankEnable ) ? bankRdy : 1'bz ;
	
	//Bank Enabling
	always @(*)
		case (BF_I_addr[15:13])
			BANK0_MASK	:	bankEnable = 1'b1;
			BANK1_MASK	:	bankEnable = 1'b1;
			default		:	bankEnable = 1'b0;
		endcase
	
	//Address Masking/Tracking
	always @(*)
		case (BF_I_addr[15:13])
			BANK0_MASK	:	RAMbankSelect = 1'b0;
			BANK1_MASK	:	RAMbankSelect = 1'b1;
			default		:	RAMbankSelect = 1'b0;
		endcase
		
	//RAMBankShiftRegister
	always @(posedge BF_I_clk)
		sr_RAMbankSelect <= { sr_RAMbankSelect[0], fifoCount[13] };
		
	//BankChange Flag, high when RAM bank select changes
	always @(*)
		case (sr_RAMbankSelect)
			2'b10		:	bankChange = 1'b1;
			2'b01		:	bankChange = 1'b1;
			default	:	bankChange = 1'b0;
		endcase

	//Data Ready Flag
	always @(posedge BF_I_clk)
		if (I_rst || I_dataRead)
			O_dataRdy <= 1'b0;
		else if (bankChange) //When bank select chnages
			O_dataRdy <= 1'b1;
		else
			O_dataRdy <= O_dataRdy;
			
		
endmodule

