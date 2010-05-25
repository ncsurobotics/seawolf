//Simple memory map module
//Baird Hendrix

//NOTE:  If data corrupt from Blackfin read, try addding
// ardy line.  May slow down Blackfin read.

module memMapCntrl
(
	//Blackfin Memory Interface
	input					 I_rst,
	input 		[15:0] BF_I_addr,
	output tri 	[15:0] BF_OT_dataBus,
	input 				 BF_I_bankSelect,
	input 				 BF_I_are,
	input 				 BF_I_awe,
	input					 BF_I_clk,
	//Inputs from FPGA
	input					 sampleRdy,
	input					 bankSelect,
	//Outputs to FPGA
	output				 softReset,
	output				 dataRdyLED
);
	
	//register mappings
	parameter POINTER_ADDR 		= 16'h0000;//address 0x20200000, a read only register
	parameter DATA_READ_ADDR 	= 16'h0001;//address 0x20200002, a read/write register
	parameter DATA_RDY_ADDR 	= 16'h0002;//address 0x20200004, a read only register
	parameter SOFT_RESET			= 16'h0003;//soft reset at 0x20200006
	
	//registers to memory map
	reg [15:0] pointer;	//address 0x20200000, a read only register
	reg [15:0] dataRead;    //address 0x20200001, a read/write register
	reg [15:0] dataRdy; 
	reg [15:0] softResetReg;
	
	//not registers
	reg [15:0] out;
	reg outValid;
	
	//memory map controls
	//inputs
	always @(posedge BF_I_clk)
		if (BF_I_bankSelect == 1'b0)	
			pointer <= 16'h0000;
		else if (BF_I_bankSelect == 1'b1)
			pointer <= 16'h8000;
	
	//dataRdy control
	always @(posedge BF_I_clk)
		if (I_rst)
			dataRdy <= 1'b0;
		else if (dataRead)
			dataRdy <= 1'b0;
		else if (sampleRdy)
			dataRdy <= 1'b1;
		else
			dataRdy <= dataRdy;
	
	//outputs
	assign sample_out = dataRead[0];	//Assign LSB of 0x20200001 to sample_out line
	
	//Memory interface control
	//output
	always @(*)
		case(BF_I_addr)
			POINTER_ADDR	:	out <= pointer;
			DATA_READ_ADDR :	out <= dataRead;
			DATA_RDY_ADDR	:	out <= dataRdy;
			default			:	out <= 16'h0000;
		endcase
	
	//output valid
	always @(*)
		if (BF_I_awe)
			outValid <= 1'b0;
		else if (BF_I_are && BF_I_bankSelect)
			case(BF_I_addr)
				POINTER_ADDR	:	outValid <= 1'b1;
				DATA_READ_ADDR	:	outValid <= 1'b1;
				DATA_RDY_ADDR	:  outValid <= 1'b1;
				default			:	outValid <= 1'b0;
			endcase
		else
			outValid <= 1'b0;
	
	//write control for one writeable register (dataRead)
	//register write (0x20200001)
	//reset registers as well (defalut values)
	// read as in past tense, set by Blackfin after it reads one page of data for 4 channels
	always @(posedge BF_I_clk)
		if (I_rst)
			dataRead <= 1'b0;
		else if (BF_I_awe && BF_I_bankSelect && (BF_I_addr == DATA_READ_ADDR) )
			dataRead <= BF_OT_dataBus;
		else if (dataRead)
			dataRead <= 1'b0;
		else
			dataRead <= dataRead;
			
	//soft reset control
	always @(posedge BF_I_clk)
		if (I_rst)
			softResetReg <= 1'b0;
		else if (BF_I_awe && BF_I_bankSelect && (BF_I_addr == SOFT_RESET) )
			softResetReg <= BF_OT_dataBus;
		else if (softResetReg)
			softResetReg <= 1'b0;
		else
			softResetReg <= softResetReg;
	
	//dataBus tristate control
	assign BF_OT_dataBus = outValid ? out : 16'hzzzz;
	
	//reset assignment
	assign softReset  = |softResetReg; // if softResetReg =/= 0, reset
	assign dataRdyLED = |dataRdy;
	
endmodule
