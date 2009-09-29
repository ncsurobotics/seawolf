////////////////////////////////////////////////////////////////////////////////
// Company: 		Analog Devices
// Engineer: 		Alex Arrants
//	Create Date:   01/17/08
// Design Name:   Octal Capture
// Tool versions:	ISE 9.2
// Description: 	 
// 
// Revision:      1.0
//
//////////////////////////////////////////////////////////////////////////////////
`timescale  1 ns / 10 ps
module fifo8k_by_2 (din, wrclk, rdclk, wr_en, rd_en, rst, dout, wr_addr, rd_addr);

input [1:0] din;
input [12:0] wr_addr;
input [12:0] rd_addr;
input wrclk, rdclk, wr_en, rd_en, rst;
output reg [1:0] dout;

wire [1:0] dout1;



always @(rdclk)
	dout <=dout1;

RAMB16 #(
.DOA_REG(0), // Optional output registers on A port (0 or 1)
.DOB_REG(0), // Optional output registers on B port (0 or 1)
.INIT_A(36'h000000000), // Initial values on A output port
.INIT_B(36'h000000000), // Initial values on B output port
.INVERT_CLK_DOA_REG("FALSE"),// Invert clock on A port output registers ("TRUE" or "FALSE")
.INVERT_CLK_DOB_REG("FALSE"),// Invert clock on A port output registers ("TRUE" or "FALSE")
.RAM_EXTENSION_A("NONE"), // "UPPER", "LOWER" or "NONE" when cascaded
.RAM_EXTENSION_B("NONE"), // "UPPER", "LOWER" or "NONE" when cascaded
.READ_WIDTH_A(0), // Valid values are 1, 2, 4, 9, 18, or 36
.READ_WIDTH_B(2), // Valid values are 1, 2, 4, 9, 18, or 36
.SIM_COLLISION_CHECK("ALL"), // Collision check enable "ALL", "WARNING_ONLY",// "GENERATE_X_ONLY" or "NONE"
.SRVAL_A(36'h000000000), // Set/Reset value for A port output
.SRVAL_B(36'h000000000), // Set/Reset value for B port output
.WRITE_MODE_A("WRITE_FIRST"), // "WRITE_FIRST", "READ_FIRST", or "NO_CHANGE"
.WRITE_MODE_B("WRITE_FIRST"), // "WRITE_FIRST", "READ_FIRST", or "NO_CHANGE"
.WRITE_WIDTH_A(2), // Valid values are 1, 2, 4, 9, 18, or 36
.WRITE_WIDTH_B(0) // Valid values are 1, 2, 4, 9, 18, or 36
// INIT_xx declarations specify the initial contents of the RAM and by default are intialized to zero
// INITP_xx are for the parity bits and by default are intialized to zero
) RAMB16_U1 (
.CASCADEOUTA(), // 1-bit cascade output
.CASCADEOUTB(), // 1-bit cascade output
.DOA(), // 32-bit A port data output
.DOB(dout1), // 32-bit B port data output
.DOPA(), // 4-bit A port parity data output
.DOPB(), // 4-bit B port parity data output
.ADDRA({wr_addr[12:0], 1'b0}), // 15-bit A port address input
.ADDRB({rd_addr[12:0], 1'b0}), // 15-bit B port address input
.CASCADEINA(), // 1-bit cascade A input
.CASCADEINB(), // 1-bit cascade B input
.CLKA(wrclk), // 1-bit A port clock input
.CLKB(rdclk), // 1-bit B port clock input
.DIA({30'b0, din}), // 32-bit A port data input
.DIB(), // 32-bit B port data input
.DIPA(), // 4-bit A port parity data input
.DIPB(), // 4-bit B port parity data input
.ENA(1'b1), // 1-bit A port enable input
.ENB(1'b1), // 1-bit B port enable input
.REGCEA(), // 1-bit A port register enable input
.REGCEB(), // 1-bit B port register enable input
.SSRA(rst), // 1-bit A port set/reset input
.SSRB(rst), // 1-bit B port set/reset input
//.WEA({4{mem[0]}}), // 4-bit A port write enable input
.WEA({4{wr_en}}), // 4-bit A port write enable input
.WEB(4'b0) // 4-bit B port write enable input
);
// End of RAMB16_U1 instantiation


endmodule
