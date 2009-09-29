////////////////////////////////////////////////////////////////////////////////
// Company: 		Analog Devices
// Engineer: 		Alex Arrants
//	Create Date:   01/18/08
// Design Name:   SPI for FIFO5
// Tool versions:	ISE 9.2.01i  
// Description: 	8 bit SPI register
// 
// Revision:      1.1
// 
//////////////////////////////////////////////////////////////////////////////////
`timescale  1 ns / 10 ps
module spi_write_8b(sdi, csb, sclk, cntrl_bits);

input sdi, csb, sclk;

output [7:0] cntrl_bits;

reg gate;
reg [7:0] data, cntrl_bits;
reg [4:0] count;


always @(posedge sclk)
	if(!csb)
		gate <= 1'b1;
	else if (count == 5'b11000) //11000 = 24, 8 address + 16 data
		gate <= 1'b0;

always @(posedge sclk)	
	if(gate)
		begin
			count <= count + 1;
			data[0] <= sdi;
			data[1] <= data[0];
			data[2] <= data[1];
			data[3] <= data[2];
			data[4] <= data[3];
			data[5] <= data[4];
			data[6] <= data[5];
			data[7] <= data[6];
		end
	else
		count <= 5'b0;

always @(posedge csb)
	cntrl_bits <= data;

endmodule						 
