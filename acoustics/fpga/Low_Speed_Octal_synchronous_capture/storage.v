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
module storage(_ffa, dinA, dinB, dinC, dinD, dinE, dinF, dinG, dinH, cntrl_bits, wrclk, load, rst, rdclk, rdenA, rdenB, dout, bw_bits);

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

wire [15:0] doutA;
wire [15:0] doutB;
wire [15:0] doutC;
wire [15:0] doutD;
wire [15:0] doutE;
wire [15:0] doutF;
wire [15:0] doutG;
wire [15:0] doutH;

wire [11:0] dinA_2s;
wire [15:0] decA;
wire rdy;

//decimator

decimate decimA 
		(  
			.din( {~dinA[11], dinA[10:0]} ),
			.dout(decA),
			.rdy(rdy),
			.nd(1'b1),
			.rfd(),
			.clk(wrclk)
		);

//////////////NEW STUFF////////////////////////////

reg full;
reg [12:0] wr_addr;
reg [12:0] rd_addr;
reg [2:0] prev_cntrl_bits;
reg rst_addr;

// generate write address
always @(posedge wrclk or posedge rst)
	if(rst)
		wr_addr <= 13'b0;
	else if(load && ~&wr_addr && rdy) // do not write past max count
		wr_addr <= wr_addr + 1;

// generate full flag
always @(posedge wrclk)
    full <= &wr_addr;

assign _ffa = ~full;

always @ (negedge rdclk)
	prev_cntrl_bits <= cntrl_bits;

always @ (negedge rdclk or posedge rst)
	if (rst)
		rst_addr <= 1'b1;
	else
		rst_addr <= (prev_cntrl_bits != cntrl_bits);

// generate read address
always @(negedge rdclk or posedge rst_addr)
	if(rst_addr)
		rd_addr <= 13'b0;
	else if(rdenA)
		rd_addr <= rd_addr + 1;
		
////////////END NEW STUFF//////////////////////////


`ifndef EXTERNAL_RAM
fifo8k F1(
	 .din({~decA[15], decA[14:0]}),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutA),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F2(
	 .din(dinB),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst), 
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutB),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F3(
	 .din(dinC),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutC),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F4(
	 .din(dinD),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutD),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F5(
	 .din(dinE),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutE),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F6(
	 .din(dinF),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutF),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F7(
	 .din(dinG),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutG),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
fifo8k F8(
	 .din(dinH),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && rdy),
	 .dout(doutH),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));

always @(posedge rdclk)
	//if(rdenA)
		begin
			case(cntrl_bits[2:0])
				 3'b000: dout <= doutA;
				 3'b001: dout <= doutB;
				 3'b010: dout <= doutC;
				 3'b011: dout <= doutD;
				 3'b100: dout <= doutE;
				 3'b101: dout <= doutF;
				 3'b110: dout <= doutG;
				 3'b111: dout <= doutH;
			endcase
		end
`else
    // insert code for external SRAM here
`endif

endmodule
