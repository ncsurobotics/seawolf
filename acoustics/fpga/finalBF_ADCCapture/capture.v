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
`timescale  1 ns / 1 ps
module capture(
					rst, wren,
					dco_p, dco_n, fco_p, fco_n, 
					din_ap, din_an, din_bp, din_bn,  
					din_cp, din_cn, din_dp, din_dn,  
					//din_ep, din_en, din_fp, din_fn,  
					//din_gp, din_gn, din_hp, din_hn,
					doutA, doutB, doutC, doutD, 
					//doutE, doutF, doutG, doutH, 
					clkout, load, 
					dco_locked, fco_locked
					);

input rst, wren; 
input dco_p, dco_n;
input fco_p, fco_n;
input din_ap, din_an;
input din_bp, din_bn;
input din_cp, din_cn;
input din_dp, din_dn;
//input din_ep, din_en;
//input din_fp, din_fn;
//input din_gp, din_gn;
//input din_hp, din_hn;

output clkout, load;          
output [13:0] doutA; 
output [13:0] doutB; 
output [13:0] doutC; 
output [13:0] doutD; 
//output [13:0] doutE; 
//output [13:0] doutF; 
//output [13:0] doutG; 
//output [13:0] doutH; 
output dco_locked;
output fco_locked;

reg load, gate;
reg [6:0] dat_q1_a, dat_q2_a;
reg [6:0] dat_q1_b, dat_q2_b;
reg [6:0] dat_q1_c, dat_q2_c;
reg [6:0] dat_q1_d, dat_q2_d;
reg [6:0] dat_q1_e, dat_q2_e;
reg [6:0] dat_q1_f, dat_q2_f;
reg [6:0] dat_q1_g, dat_q2_g;
reg [6:0] dat_q1_h, dat_q2_h;

reg [13:0] doutA;
reg [13:0] doutB;
reg [13:0] doutC;
reg [13:0] doutD;
reg [13:0] doutE;
reg [13:0] doutF;
reg [13:0] doutG;
reg [13:0] doutH;

reg [13:0] dout_a, dout_b;
reg [13:0] dout_c, dout_d;
reg [13:0] dout_e, dout_f;
reg [13:0] dout_g, dout_h;

reg [15:0] count;       
reg fco1,fco2;
reg fcostb;

wire dco;
wire dcoshifted;

IBUFGDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB1 (.O(dco_in), .I(dco_p), .IB(dco_n));
IBUFGDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB2 (.O(fco_in), .I(fco_p), .IB(fco_n));

IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB3 (.O(din_a), .I(din_ap), .IB(din_an)); 
IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB4 (.O(din_b), .I(din_bp), .IB(din_bn)); 
IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB5 (.O(din_c), .I(din_cp), .IB(din_cn));
IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB6 (.O(din_d), .I(din_dp), .IB(din_dn));
//IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB7 (.O(din_e), .I(din_ep), .IB(din_en)); 
//IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB8 (.O(din_f), .I(din_fp), .IB(din_fn)); 
//IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB9 (.O(din_g), .I(din_gp), .IB(din_gn));
//IBUFDS #(.DIFF_TERM("TRUE"), .IOSTANDARD("LVDS_25")) IB10 (.O(din_h), .I(din_hp), .IB(din_hn));





BUFG B1 (.I(dco_in), .O(dco));

		 
BUFG B2 (.I(fco_in), .O(fco));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I1 (
			.D(din_a), .C(dco), 
			.Q1(q1_a), .Q2(q2_a),
			.CE(1'b1), .S(1'b0), .R(1'b0));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I2 (
			.D(din_b), .C(dco), 
			.Q1(q1_b), .Q2(q2_b),
			.CE(1'b1), .S(1'b0), .R(1'b0));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I3 (
			.D(din_c), .C(dco), 
			.Q1(q1_c), .Q2(q2_c),
			.CE(1'b1), .S(1'b0), .R(1'b0));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I4 (
			.D(din_d), .C(dco), 
			.Q1(q1_d), .Q2(q2_d),
			.CE(1'b1), .S(1'b0), .R(1'b0));
/*
IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I5 (
			.D(din_e), .C(dco), 
			.Q1(q1_e), .Q2(q2_e),
			.CE(1'b1), .S(1'b0), .R(1'b0));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I6 (
			.D(din_f), .C(dco), 
			.Q1(q1_f), .Q2(q2_f),
			.CE(1'b1), .S(1'b0), .R(1'b0));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I7 (
			.D(din_g), .C(dco), 
			.Q1(q1_g), .Q2(q2_g),
			.CE(1'b1), .S(1'b0), .R(1'b0));

IDDR   #(.DDR_CLK_EDGE("SAME_EDGE_PIPELINED")) I8 (
			.D(din_h), .C(dco), 
			.Q1(q1_h), .Q2(q2_h),
			.CE(1'b1), .S(1'b0), .R(1'b0));
*/

always @(posedge dco)
	begin
		dat_q1_a[6:0] <= {dat_q1_a[5:0], q1_a}; 
		dat_q2_a[6:0] <= {dat_q2_a[5:0], q2_a}; 
		dat_q1_b[6:0] <= {dat_q1_b[5:0], q1_b}; 
		dat_q2_b[6:0] <= {dat_q2_b[5:0], q2_b}; 
		dat_q1_c[6:0] <= {dat_q1_c[5:0], q1_c}; 
		dat_q2_c[6:0] <= {dat_q2_c[5:0], q2_c}; 
		dat_q1_d[6:0] <= {dat_q1_d[5:0], q1_d}; 
		dat_q2_d[6:0] <= {dat_q2_d[5:0], q2_d}; 
		/*
		dat_q1_e[6:0] <= {dat_q1_e[5:0], q1_e}; 
		dat_q2_e[6:0] <= {dat_q2_e[5:0], q2_e}; 
		dat_q1_f[6:0] <= {dat_q1_f[5:0], q1_f}; 
		dat_q2_f[6:0] <= {dat_q2_f[5:0], q2_f}; 
		dat_q1_g[6:0] <= {dat_q1_g[5:0], q1_g}; 
		dat_q2_g[6:0] <= {dat_q2_g[5:0], q2_g}; 
		dat_q1_h[6:0] <= {dat_q1_h[5:0], q1_h}; 
		dat_q2_h[6:0] <= {dat_q2_h[5:0], q2_h};
		*/
	end
//start new fco stuff

//generate new FCO
always @ (posedge dco)
	begin
		fco1 <= fco;
		fco2 <= fco1;
		fcostb <= fco1 & ~fco2;
	end
	
always @(posedge dco)
	if (fcostb)
		begin
			dout_a <= {dat_q1_a[6], dat_q2_a[6],
						 dat_q1_a[5], dat_q2_a[5],
						 dat_q1_a[4], dat_q2_a[4],
						 dat_q1_a[3], dat_q2_a[3],
						 dat_q1_a[2], dat_q2_a[2],
						 dat_q1_a[1], dat_q2_a[1],
						 dat_q1_a[0], dat_q2_a[0]};
		end

always @(posedge dco)
	if (fcostb)
			begin
				dout_b <= {dat_q1_b[6], dat_q2_b[6],
							 dat_q1_b[5], dat_q2_b[5],
							 dat_q1_b[4], dat_q2_b[4],
							 dat_q1_b[3], dat_q2_b[3],
							 dat_q1_b[2], dat_q2_b[2],
							 dat_q1_b[1], dat_q2_b[1],
							 dat_q1_b[0], dat_q2_b[0]};
			end
		
always @(posedge dco)
	if (fcostb)
		begin
			dout_c <= {dat_q1_c[6], dat_q2_c[6],
						 dat_q1_c[5], dat_q2_c[5],
						 dat_q1_c[4], dat_q2_c[4],
						 dat_q1_c[3], dat_q2_c[3],
						 dat_q1_c[2], dat_q2_c[2],
						 dat_q1_c[1], dat_q2_c[1],
						 dat_q1_c[0], dat_q2_c[0]};
		end
	
always @(posedge dco)
	if (fcostb)
		begin
			dout_d <= {dat_q1_d[6], dat_q2_d[6],
						 dat_q1_d[5], dat_q2_d[5],
						 dat_q1_d[4], dat_q2_d[4],
						 dat_q1_d[3], dat_q2_d[3],
						 dat_q1_d[2], dat_q2_d[2],
						 dat_q1_d[1], dat_q2_d[1],
						 dat_q1_d[0], dat_q2_d[0]};
		end
/*
always @(posedge dco)
	if (fcostb)
		begin
			dout_e <= {dat_q1_e[6], dat_q2_e[6],
						 dat_q1_e[5], dat_q2_e[5],
						 dat_q1_e[4], dat_q2_e[4],
						 dat_q1_e[3], dat_q2_e[3],
						 dat_q1_e[2], dat_q2_e[2],
						 dat_q1_e[1], dat_q2_e[1],
						 dat_q1_e[0], dat_q2_e[0]};
		end
always @(posedge dco)
	if (fcostb)
		begin
			dout_f <= {dat_q1_f[6], dat_q2_f[6],
						 dat_q1_f[5], dat_q2_f[5],
						 dat_q1_f[4], dat_q2_f[4],
						 dat_q1_f[3], dat_q2_f[3],
						 dat_q1_f[2], dat_q2_f[2],
						 dat_q1_f[1], dat_q2_f[1],
						 dat_q1_f[0], dat_q2_f[0]};
		end
always @(posedge dco)
	if (fcostb)
		begin
			dout_g <= {dat_q1_g[6], dat_q2_g[6],
						 dat_q1_g[5], dat_q2_g[5],
						 dat_q1_g[4], dat_q2_g[4],
						 dat_q1_g[3], dat_q2_g[3],
						 dat_q1_g[2], dat_q2_g[2],
						 dat_q1_g[1], dat_q2_g[1],
						 dat_q1_g[0], dat_q2_g[0]};
		end
		
always @(posedge dco)
	if (fcostb)
		begin
			dout_h <= {dat_q1_h[6], dat_q2_h[6],
						 dat_q1_h[5], dat_q2_h[5],
						 dat_q1_h[4], dat_q2_h[4],
						 dat_q1_h[3], dat_q2_h[3],
						 dat_q1_h[2], dat_q2_h[2],
						 dat_q1_h[1], dat_q2_h[1],
						 dat_q1_h[0], dat_q2_h[0]};
		end
*/

always @(posedge dco)
	if (fcostb)
		begin
			doutA <= dout_a;
			doutB <= dout_b;
			doutC <= dout_c;
			doutD <= dout_d;
			//doutE <= dout_e;
			//doutF <= dout_f;
			//doutG <= dout_g;
			//doutH <= dout_h;
		end
		


assign clkout = fco;

always @(posedge dco)
begin
	if (rst)
		begin
			count <= 1'b0;
			gate <= 1'b0;
		end
	else if (fcostb)
		begin
			count <= count + 1;
			if (&count)
				gate <= 1;
		end
end
always @(posedge dco)
	 
	if (gate & fcostb)
		begin
			load <= wren;
		end

endmodule