`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    15:39:45 06/28/2009 
// Design Name: 
// Module Name:    ram_justbf 
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
module ram_justbf
(	
	input [18:0] addr,
	output tri [15:0] data_bus,
	input [3:0] bank_select,
	output tri ardy,
	input are,
	input awe,
	input vr,
	input clk,
	output enTest,
	output ardyTest
);

	wire outEn, enB, outRdy, rfd;
	wire [15:0] dataOut;
	reg  [15:0] counter;
	
	sram testSram 
	(
		.addra(counter),
		.addrb(addr),
		.clka(clk),
		.clkb(clk),
		.dina(counter),
		.dinb(data_bus),
		.doutb(dataOut),
		.ena(1'b1),
		.enb(enB),
		.ndb(enB && ~awe),
		.rfdb(rfd),
		.rdyb(outRdy),
		.wea(1'b1),
		.web(enB && ~awe)
	);
		

	
	assign enB = ( ~bank_select[3] );
	assign outEn = enB;
	
	//assign ardy = (enB && (rfd || outRdy)) ? 1'b1 : 
		//(enB) ? 1'b0 : 1'bz;
	assign ardy = 1'bz;	
		
	assign data_bus = (outEn && ~are) ? dataOut : 16'hzzzz;
	
	always @(posedge clk)
		counter <= counter + 1;
		
	

endmodule
