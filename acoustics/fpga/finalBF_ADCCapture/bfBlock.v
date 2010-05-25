`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: Brooks Stephenson and Baird Hendrix
// 
// Create Date:    18:21:31 06/27/2009 
// Design Name: 	
// Module Name:    top 
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
module bfBlock
(	
	input 		[18:0] addr,
	output tri  [15:0] data_bus,
	input 		[ 3:0] bank_select,
	input 		[15:0] chanA,
	input 		[15:0] chanB,
	input 		[15:0] chanC,
	input 		[15:0] chanD,
	input					 chanAvalid,
	input					 chanBvalid,
	input					 chanCvalid,
	input					 chanDvalid,
	output tri 			 ardy,
	input 				 are,
	input 				 awe,
	output 				 led1,
	output 				 led2,
	input 				 testClk,
	output 				 sma1,
	output 				 sma2,
	input					 adcClk
);

wire enTest;
wire bs;
wire softReset;
wire dataRdyLED;
wire dataRdyA, dataRdyB, dataRdyC, dataRdyD;

wire sampleRdy;
wire read;
wire bankSelectWireA, bankSelectWireB, bankSelectWireC, bankSelectWireD;

wire [15:0] adcAddr;
//reg [15:0] counter;

reg [2:0] dataTimer;
reg dataRdy;
reg bankSelectWire;
reg bsW, bsWC;
wire dataRdyAnd;

assign led1 = ~dataRdy;
assign led2 = 1'b0;
assign sma1 = are;
assign sma2 = bank_select[3];
//assign ardy = 1'bz;
//assign data_bus = ((~sma2) & (~are)) ? 16'hbeef : 16'hzzzz;

/*
always @(posedge adcClk)
	if (chanAvalid)
		counter <= counter + 1;
	else
		counter <= counter;
*/

bfInterfaceSSRAM 
#(
	.BANK0_MASK(3'h0),
	.BANK1_MASK(3'h4)
) 
chARAM
(
	 .I_rst					(softReset),
    .BF_I_addr				(addr[16:1]), 
    .BF_OT_dataBus		(data_bus), 
    .BF_I_bankSelect		(~bank_select[3]), 
    .BF_I_are				(~are), 
    .BF_I_awe				(~awe), 
    .BF_I_clk				(testClk), 
	 .BF_O_ardy				(ardy),
    .ADC_I_clk				(adcClk), 
    .ADC_I_dataValid		(chanAvalid), 
    .ADC_I_data			(chanA),
	 .O_dataRdy				(dataRdyA),
	 .O_bankLastFilled 	(bankSelectWireA),
	 .O_ADC_addr			(),
	 .I_dataRead			(read)
);



bfInterfaceSSRAM
#(
	.BANK0_MASK(3'h1),
	.BANK1_MASK(3'h5)
) 
chBRAM
(
	 .I_rst				(softReset),
    .BF_I_addr			(addr[16:1]), 
    .BF_OT_dataBus	(data_bus), 
    .BF_I_bankSelect	(~bank_select[3]), 
    .BF_I_are			(~are), 
    .BF_I_awe			(~awe), 
    .BF_I_clk			(testClk), 
	 .BF_O_ardy			(ardy),
    .ADC_I_clk			(adcClk), 
    .ADC_I_dataValid	(chanBvalid), 
    .ADC_I_data		(chanB),
	 .O_dataRdy				(dataRdyB),
	 .O_bankLastFilled 	(bankSelectWireB),
	 .O_ADC_addr			(),
	 .I_dataRead			(read)

);

bfInterfaceSSRAM
#(
	.BANK0_MASK(3'h2),
	.BANK1_MASK(3'h6)
) 
chCRAM
(
	 .I_rst				(softReset),
    .BF_I_addr			(addr[16:1]), 
    .BF_OT_dataBus	(data_bus), 
    .BF_I_bankSelect	(~bank_select[3]), 
    .BF_I_are			(~are), 
    .BF_I_awe			(~awe), 
    .BF_I_clk			(testClk), 
	 .BF_O_ardy			(ardy),
    .ADC_I_clk			(adcClk), 
    .ADC_I_dataValid	(chanCvalid), 
    .ADC_I_data		(chanC),
	 .O_dataRdy				(dataRdyC),
	 .O_bankLastFilled 	(bankSelectWireC),
	 .O_ADC_addr			(),
	 .I_dataRead			(read)

);

bfInterfaceSSRAM
#(
	.BANK0_MASK(3'h3),
	.BANK1_MASK(3'h7)
) 
chDRAM
(
	 .I_rst				(softReset),
    .BF_I_addr			(addr[16:1]), 
    .BF_OT_dataBus	(data_bus), 
    .BF_I_bankSelect	(~bank_select[3]), 
    .BF_I_are			(~are), 
    .BF_I_awe			(~awe), 
    .BF_I_clk			(testClk), 
	 .BF_O_ardy			(ardy),
    .ADC_I_clk			(adcClk), 
    .ADC_I_dataValid	(chanDvalid), 
    .ADC_I_data		(chanD),
	 .O_dataRdy				(dataRdyD),
	 .O_bankLastFilled 	(bankSelectWireD),
	 .O_ADC_addr			(),
	 .I_dataRead			(read)
);

assign dataRdyAnd = dataRdyA && dataRdyB && dataRdyC && dataRdyD;

always @(posedge testClk)
	case ({ bankSelectWireA, bankSelectWireB, bankSelectWireC, bankSelectWireD })
		4'b1111:	bsWC <= 1;
		4'b0000:	bsWC <= 0;
		default: bsWC <= bsWC;
	endcase

always @(posedge testClk)
	if (&dataTimer)
		bsW <= bsWC;
	else
		bsW <= bsW;

always @(posedge testClk)
	if (!dataRdyAnd)
		dataTimer <= 0;
	else if (&dataTimer)
		dataTimer <= dataTimer;
	else
		dataTimer <= dataTimer + 1;

always @(posedge testClk)
	dataRdy <= &dataTimer;

// Memory Mapped Registers
memMapCntrl U1
(
    .BF_I_addr			(addr[16:1]), 
    .BF_OT_dataBus	(data_bus), 
    .BF_I_bankSelect	(~bank_select[2]), 
    .BF_I_are			(~are), 
    .BF_I_awe			(~awe), 
    .BF_I_clk			(testClk),
	 .I_rst				(softReset),
	 .O_read				(read),
    .sampleRdy			(dataRdy),
	 .bankSelect		(~bankSelectWireB),
    .softReset			(softReset),
	 .dataRdyLED		(dataRdyLED),
	 .ADC_I_addr		(adcAddr)
);




endmodule
