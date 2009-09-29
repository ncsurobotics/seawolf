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
	input			[15:0] ADC_I_addr,
	//Inputs from FPGA
	input					 sampleRdy,
	input					 bankSelect,
	//Outputs to FPGA
	output				 softReset,
	output				 dataRdyLED,
	output				 O_read
);
	
	//register mappings
	parameter POINTER0_ADDR			= 16'h0001;//also a read only register
	parameter POINTER1_ADDR 		= 16'h0000;//address 0x20200000, a read only register
	parameter DATA_READ_ADDR 	= 16'h0002;//address 0x20200002, a read/write register
	parameter DATA_RDY_ADDR 	= 16'h0004;//address 0x20200004, a read only register
	parameter SOFT_RESET			= 16'h0006;//soft reset at 0x20200006
	parameter CURR_WRITE_ADDR	= 16'h0008; //msb of current address being written too

	
	//registers to memory map
	reg [15:0] pointer1;	//address 0x20200000, a read only register
	reg [15:0] pointer0;
	reg [15:0] dataRead;    //address 0x20200001, a read/write register
	reg [15:0] dataRdy; 
	reg [15:0] softResetReg;
	
	//not registers
	reg [15:0] out;
	reg outValid;
	
	//memory map controls
	//inputs
	always @(posedge BF_I_clk)
		if (bankSelect == 1'b0)	
			pointer1 <= 16'h0000;
		else if (bankSelect == 1'b1)
			pointer1 <= 16'h0000;
	
	always @(posedge BF_I_clk)
		if (bankSelect == 1'b0)	
			pointer0 <= 16'h2030;
		else if (bankSelect == 1'b1)
			pointer0 <= 16'h2031;	//MSB of pointer, never changes	

	//dataRdy control
	always @(posedge BF_I_clk)
		if (I_rst)
			dataRdy <= 0;
		else if (dataRead)
			dataRdy <= 16'h0000;
		else
			dataRdy <= {15'h0000, sampleRdy };
	
	//outputs
	assign sample_out = dataRead[0];	//Assign LSB of 0x20200001 to sample_out line
	
	//Memory interface control
	//output
	always @(*)
		case(BF_I_addr)
			POINTER0_ADDR		:	out = pointer0;
			POINTER1_ADDR		:	out = pointer1;
			DATA_READ_ADDR 	:	out = dataRead;
			DATA_RDY_ADDR		:	out = dataRdy;
			SOFT_RESET			:	out = softResetReg;
			CURR_WRITE_ADDR	:	out = ADC_I_addr;
			default				:	out = 16'h0000;
		endcase
	
	//output valid
	always @(*)
		if (BF_I_awe)
			outValid = 1'b0;
		else if (BF_I_are && BF_I_bankSelect)
			case(BF_I_addr)
				POINTER0_ADDR		:	outValid = 1'b1;
				POINTER1_ADDR		:	outValid = 1'b1;
				DATA_READ_ADDR		:	outValid = 1'b1;
				DATA_RDY_ADDR		:  outValid = 1'b1;
				CURR_WRITE_ADDR	:  outValid = 1'b1;
				SOFT_RESET			:	outValid = 1'b1;
				default				:	outValid = 1'b0;
			endcase
		else
			outValid = 1'b0;
	
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
	assign dataRdyLED = dataRdy[0];
	
	assign O_read = dataRead;
	
endmodule
