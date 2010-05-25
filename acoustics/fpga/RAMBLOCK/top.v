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
module topLevel
(	
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
);

wire enTest;
wire bs;
wire softReset;
wire dataRdyLED;

assign led1 = ~dataRdyLED;
assign led2 = 1'b0;
assign sma1 = are;
assign sma2 = bank_select[3];
assign ardy = 1'bz;
//assign data_bus = ((~sma2) & (~are)) ? 16'hbeef : 16'hzzzz;

bfInterfaceDP 
#(
	.BANK0_MASK(3'h0),
	.BANK1_MASK(3'h4)
) 
chARAM
(
	 .I_rst				(softReset),
    .BF_I_addr			(addr[16:1]), 
    .BF_OT_dataBus	(data_bus), 
    .BF_I_bankSelect	(~bank_select[3]), 
    .BF_I_are			(~are), 
    .BF_I_awe			(~awe), 
    .BF_I_clk			(testClk), 
	 .BF_O_ardy			(), //(ardy),
    .ADC_I_clk			(testClk), 
    .ADC_I_dataValid	(1'b1), 
    .ADC_I_data		(16'h1)
);

bfInterfaceDP 
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
	 .BF_O_ardy			(), //(ardy),
    .ADC_I_clk			(testClk), 
    .ADC_I_dataValid	(1'b1), 
    .ADC_I_data		(16'h2)
);

bfInterfaceDP 
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
	 .BF_O_ardy			(), //(ardy),
    .ADC_I_clk			(testClk), 
    .ADC_I_dataValid	(1'b1), 
    .ADC_I_data		(16'h3)
);

bfInterfaceDP 
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
	 .BF_O_ardy			(), //(ardy),
    .ADC_I_clk			(testClk), 
    .ADC_I_dataValid	(1'b1), 
    .ADC_I_data		(16'h4)
);


// Memory Mapped Registers
memMapCntrl U1
(
    .BF_I_addr(addr[16:1]), 
    .BF_OT_dataBus(data_bus), 
    .BF_I_bankSelect(~bank_select[2]), 
    .BF_I_are(~are), 
    .BF_I_awe(~awe), 
    .BF_I_clk(testClk),
	 .I_rst(softReset),
    .sampleRdy(),
	 .bankSelect(),
    .softReset(softReset),
	 .dataRdyLED(dataRdyLED)
);




endmodule
