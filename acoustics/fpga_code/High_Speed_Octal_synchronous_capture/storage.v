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
module storage(dec_rdyA,
					dinA, dinB, dinC, dinD, dinE, dinF, dinG, dinH, 
					cntrl_bits, wrclk, load, rst, rdclk, rdenA, rdenB, dout, bw_bits, full);

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
input dec_rdyA;
output reg [15:0] dout;
output full;

wire [15:0] doutA;
wire [15:0] doutB;
wire [15:0] doutC;
wire [15:0] doutD;
wire [15:0] doutE;
wire [15:0] doutF;
wire [15:0] doutG;
wire [15:0] doutH;

//////////////NEW STUFF////////////////////////////

reg full;
reg [12:0] wr_addr;
reg [12:0] rd_addr;
reg [2:0] prev_cntrl_bits;
reg rst_addr;
reg [13:0] test;
wire test_ctl;

// generate write address
always @(posedge wrclk or posedge rst)
	if(rst)
		wr_addr <= 13'b0;
	else if(dec_rdyA && load && ~&wr_addr) // do not write past max count
		wr_addr <= wr_addr + 1;
	else
		wr_addr <= wr_addr;

// generate full flag
always @(posedge wrclk)
    full <= &wr_addr;

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
	else
		rd_addr <= rd_addr;

//test ring counter
/*
always @(posedge wrclk)
	if (load && dec_rdyA)
		test <= {test[12:0], test_ctl};
	else
		test <= test;
	
assign test_ctl = ~test[13];
*/
		
////////////END NEW STUFF//////////////////////////


`ifndef EXTERNAL_RAM
fifo8k F1(
	 .din(dinA),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && dec_rdyA),
	 .dout(doutA),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
	 /*
fifo8k F2(
	 .din(dinB),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst), 
	 .wrclk(wrclk),
	 .wren(load && dec_rdyA),
	 .dout(doutB),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
	 */
/*
fifo8k F3(
	 .din(dinC),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load && dec_rdyA),
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
	 .wren(load && dec_rdyA),
	 .dout(doutD),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
	 */
	 /*
fifo8k F5(
	 .din(dinE),
	 .rdclk(rdclk),
	 .rden(rdenA),
	 .rst(rst),
	 .wrclk(wrclk),
	 .wren(load),
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
	 .wren(load),
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
	 .wren(load),
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
	 .wren(load),
	 .dout(doutH),
	 .bw_bits(bw_bits),
	 .wr_addr(wr_addr),
	 .rd_addr(rd_addr));
*/

always @(posedge rdclk)
	//if(rdenA)
		begin
			case(cntrl_bits[2:0])
				 3'b000: dout <= doutA;
				 3'b001: dout <= 16'h0;
				 3'b010: dout <= 16'h0; //doutC;
				 3'b011: dout <= 16'h0; //doutD;
				 3'b100: dout <= 16'h0; //doutE;
				 3'b101: dout <= 16'h0; //doutF;
				 3'b110: dout <= 16'h0; //doutG;
				 3'b111: dout <= 16'h0; //doutH;
			endcase
		end
`else
    // insert code for external SRAM here
`endif

endmodule
