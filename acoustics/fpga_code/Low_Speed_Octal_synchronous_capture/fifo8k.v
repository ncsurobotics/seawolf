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
module fifo8k(din, rdclk, rden, rst, wrclk, wren, dout, bw_bits, wr_addr, rd_addr);

input [13:0] din; 
input [12:0] wr_addr;
input [12:0] rd_addr;
input rdclk, wren, wrclk, rden, rst;
input [1:0] bw_bits;

output reg [15:0] dout;


wire dout_13, dout_12, dout_11, dout_10;
wire dout_09, dout_08; 
wire dout_07, dout_06, dout_05, dout_04;
wire dout_03, dout_02, dout_01, dout_00;  

reg sel;

fifo8k_by_2 U06 (.din(din[13:12]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_13, dout_12}), .rd_addr(rd_addr), .wr_addr(wr_addr));
fifo8k_by_2 U05 (.din(din[11:10]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_11, dout_10}), .rd_addr(rd_addr), .wr_addr(wr_addr));
fifo8k_by_2 U04 (.din(din[9:8]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_09, dout_08}), .rd_addr(rd_addr), .wr_addr(wr_addr));
fifo8k_by_2 U03 (.din(din[7:6]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_07, dout_06}), .rd_addr(rd_addr), .wr_addr(wr_addr));
fifo8k_by_2 U02 (.din(din[5:4]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_05, dout_04}), .rd_addr(rd_addr), .wr_addr(wr_addr));
fifo8k_by_2 U01 (.din(din[3:2]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_03, dout_02}), .rd_addr(rd_addr), .wr_addr(wr_addr));
fifo8k_by_2 U00 (.din(din[1:0]), .wrclk(wrclk), .rdclk(rdclk), .wr_en(wren), .rd_en(rden&sel), 
				   .rst(rst), .dout({dout_01, dout_00}), .rd_addr(rd_addr), .wr_addr(wr_addr));

always @(posedge rdclk or posedge rst)
  if (rst) 
    sel <= 1'b0;
  else
    sel <= 1'b1;

always@(dout_13 or dout_12 or dout_11 or dout_10 or
		  dout_09 or dout_08 or
		  dout_07 or dout_06 or dout_05 or dout_04 or 
		  dout_03 or dout_02 or dout_01 or dout_00 or sel)

//bw_bits
case (bw_bits) //00=8bit, 01=10bit, 10=12bit, 11=14bit
		2'b00 : dout <= {dout_07, dout_06, dout_05, dout_04, dout_03, 
				 dout_02, dout_01, dout_00,8'b0};
		2'b01 : dout <= {dout_09, dout_08, dout_07, dout_06, dout_05, 
				 dout_04, dout_03, dout_02, dout_01, 
				 dout_00, 6'b0};
		2'b10 : dout <= {dout_11, dout_10, dout_09, dout_08, dout_07, 
				 dout_06, dout_05, dout_04, dout_03, 
				 dout_02, dout_01, dout_00, 4'b0};
		2'b11 : dout <= {dout_13, dout_12, dout_11, dout_10, dout_09, 
				 dout_08, dout_07, dout_06, dout_05, 
				 dout_04, dout_03, dout_02, dout_01, 
				 dout_00, 2'b0};
	
endcase

endmodule
