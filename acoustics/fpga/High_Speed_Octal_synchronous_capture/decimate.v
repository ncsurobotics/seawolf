//Simple Averaging Decimator
//Baird Hendrix
module decimate (	
			input I_clk,
			input I_rst,
			input [13:0] I_din,
			output reg O_rdy,
			output reg [13:0] O_dout
			);
			
			reg [6:0] counter;
			reg [20:0] dint;
			reg int_rdy;
			
			//Control block (counter control, rdy high every 16th cycle)
			always @(posedge I_clk)
				if (I_rst)
					counter <= 7'h0;
				else
					counter <= 7'h1 + counter;
			
			always @(posedge I_clk)
				if(&counter)
					int_rdy <= 1'b1;
				else
					int_rdy <= 1'b0;
					
			//execute block
			
			//clear block every 16th cycle, otherwise add
			always @(posedge I_clk)
				if (int_rdy)
					dint <= {7'h0, I_din};
				else
					dint <= {7'h0, I_din} + dint;
			
			//bit shift output w/reg
			always @(posedge I_clk)
				O_dout <= dint[20:7];
				
			always @(posedge I_clk)
				O_rdy <= int_rdy;
				
endmodule
