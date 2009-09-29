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
`timescale  1 ns / 10 ps
module Top (dco_p, dco_n,    
				fco_p, fco_n, 
				din_ap, din_an,  
				din_bp, din_bn, 
				din_cp, din_cn,  
				din_dp, din_dn, 
				din_ep, din_en,  
				din_fp, din_fn, 
				din_gp, din_gn,  
				din_hp, din_hn, 				
				_wen, rclk, _renA, _renB, _mr,  
				dout,	chan_a_led, chan_b_led, 
				chan_c_led, chan_d_led, sdi_in, sclk_in, csb_in,
				_ffa);
          
input _wen;	               // active-low FIFO write enable
input rclk;                // read clk
input	_mr;                 // active-low master reset
input _renA, _renB;        // active-low FIFO read enable
input dco_p, dco_n;        // clk inputs 
input fco_p, fco_n;         
input	din_ap, din_an;      // data inputs
input	din_bp, din_bn;
input	din_cp, din_cn;
input	din_dp, din_dn;
input	din_ep, din_en;      // data inputs
input	din_fp, din_fn;
input	din_gp, din_gn;
input	din_hp, din_hn;
input csb_in, sdi_in, sclk_in; //SPI lines

output chan_a_led;
output chan_b_led;
output chan_c_led;
output chan_d_led;
output [15:0] dout;        // data output
output _ffa;

wire data_clk;
wire [13:0] captured_dataA;
wire [13:0] captured_dataB;
wire [13:0] captured_dataC;
wire [13:0] captured_dataD;
wire [13:0] captured_dataE;
wire [13:0] captured_dataF;
wire [13:0] captured_dataG;
wire [13:0] captured_dataH;
wire [7:0] SPI_Register;
wire dco_locked;
wire fco_locked;
wire load;


wire sdi_buf, sclk_buf, csb_buf;

assign chan_a_led = ~(load && dco_locked && fco_locked) ; // CAPTURE LED
assign chan_b_led = ~dco_locked; // LED1
assign chan_c_led = ~fco_locked; // LED2
assign chan_d_led = ~(~_renA || ~_renB); // UPLOAD LED


IBUF #(.IOSTANDARD("DEFAULT")   
	)IBUF_1 (
      .O(sclk_buf),    
      .I(sclk_in)     
   );
	
IBUF #(.IOSTANDARD("DEFAULT")   
	)IBUF_2 (
      .O(csb_buf),    
      .I(csb_in)     
   );

IBUF #(.IOSTANDARD("DEFAULT")   
	)IBUF_3 (
      .O(sdi_buf),    
      .I(sdi_in)     
   );

// SPI register block
spi_write_8b U3 (.sdi(sdi_buf), .csb(csb_buf), .sclk(sclk_buf), .cntrl_bits(SPI_Register[7:0]));

// capture data block
capture U1 (.rst(~_mr), .wren(~_wen),				
				.dco_p(dco_p), .dco_n(dco_n), 
				.fco_p(fco_p), .fco_n(fco_n), 
				.din_ap(din_ap), .din_an(din_an),  
				.din_bp(din_bp), .din_bn(din_bn),  
				.din_cp(din_cp), .din_cn(din_cn),  
				.din_dp(din_dp), .din_dn(din_dn),
				.din_ep(din_ep), .din_en(din_en),  
				.din_fp(din_fp), .din_fn(din_fn),  
				.din_gp(din_gp), .din_gn(din_gn),  
				.din_hp(din_hp), .din_hn(din_hn),				
				.doutA(captured_dataA), .doutB(captured_dataB),
				.doutC(captured_dataC), .doutD(captured_dataD),
				.doutE(captured_dataE), .doutF(captured_dataF),
				.doutG(captured_dataG), .doutH(captured_dataH),
				.clkout(data_clk), 
				.load(load), .dco_locked(dco_locked), .fco_locked(fco_locked));

				
// write to and read from FIFO block
storage U2 (.dinA(captured_dataA), .dinB(captured_dataB), 
				.dinC(captured_dataC), .dinD(captured_dataD), 
				.dinE(captured_dataE), .dinF(captured_dataF), 
				.dinG(captured_dataG), .dinH(captured_dataH),
				.cntrl_bits(SPI_Register[2:0]),
				.wrclk(data_clk), 
				.load(load), .rst(~_mr), 
				.rdclk(rclk_b), .rdenA(~_renA), .rdenB(~_renB),
				.dout(dout), .bw_bits(SPI_Register[7:6]), ._ffa(_ffa));

//RCLK
IBUF I36 (.O(rclk_i), .I(rclk));
BUFG B32 (.O(rclk_b), .I(rclk_i));

endmodule
