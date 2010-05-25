////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995-2007 Xilinx, Inc.  All rights reserved.
////////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor: Xilinx
// \   \   \/     Version: J.40
//  \   \         Application: netgen
//  /   /         Filename: decimate.v
// /___/   /\     Timestamp: Fri Jun 05 21:05:08 2009
// \   \  /  \ 
//  \___\/\___\
//             
// Command	: -intstyle ise -w -sim -ofmt verilog "C:\Documents and Settings\bmhendri\Desktop\Low_Speed_Octal_synchronous_capture\tmp\_cg\decimate.ngc" "C:\Documents and Settings\bmhendri\Desktop\Low_Speed_Octal_synchronous_capture\tmp\_cg\decimate.v" 
// Device	: 4vfx20ff672-10
// Input file	: C:/Documents and Settings/bmhendri/Desktop/Low_Speed_Octal_synchronous_capture/tmp/_cg/decimate.ngc
// Output file	: C:/Documents and Settings/bmhendri/Desktop/Low_Speed_Octal_synchronous_capture/tmp/_cg/decimate.v
// # of Modules	: 1
// Design Name	: decimate
// Xilinx        : C:\Xilinx92i
//             
// Purpose:    
//     This verilog netlist is a verification model and uses simulation 
//     primitives which may not represent the true implementation of the 
//     device, however the netlist is functionally correct and should not 
//     be modified. This file cannot be synthesized and should only be used 
//     with supported simulation tools.
//             
// Reference:  
//     Development System Reference Guide, Chapter 23
//     Synthesis and Simulation Design Guide, Chapter 6
//             
////////////////////////////////////////////////////////////////////////////////

`timescale 1 ns/1 ps

module decimate (
  rfd, rdy, nd, clk, dout, din
);
  output rfd;
  output rdy;
  input nd;
  input clk;
  output [15 : 0] dout;
  input [11 : 0] din;
  
  // synopsys translate_off
  
  wire NlwRenamedSig_OI_rfd;
  wire \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/Mshreg_pipe_2_2 ;
  wire \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/Mshreg_pipe_3_3 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_1_4 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_2_5 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_0_6 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_3_7 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_4_8 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_6_9 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_7_10 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_5_11 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_8_12 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_9_13 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_11_14 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_12_15 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_10_16 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_14_17 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_15_18 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_13_19 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_17_20 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_18_21 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_16_22 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_19_23 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_0_24 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_2_25 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_3_26 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_1_27 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_4_28 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_5_29 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_7_30 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_8_31 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_6_32 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_9_33 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_10_34 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_12_35 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_13_36 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_11_37 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_15_38 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_16_39 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_14_40 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_18_41 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_19_42 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_17_43 ;
  wire \BU2/N66 ;
  wire \BU2/U0/decimator.decimation_filter/cnt_rst1_map4 ;
  wire \BU2/N63 ;
  wire \BU2/N62 ;
  wire \BU2/N61 ;
  wire \BU2/N60 ;
  wire \BU2/N59 ;
  wire \BU2/N58 ;
  wire \BU2/U0/decimator.decimation_filter/cnt_en ;
  wire \BU2/N57 ;
  wire \BU2/N64 ;
  wire \BU2/U0/decimator.decimation_filter/cnt_rst ;
  wire \BU2/U0/decimator.decimation_filter/cnt_rst1_map11 ;
  wire \BU2/N65 ;
  wire \BU2/N56 ;
  wire \BU2/N55 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0_44 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10_45 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11_46 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12_47 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13_48 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14_49 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15_50 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16_51 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17_52 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_18_53 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_19_54 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1_55 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2_56 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3_57 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4_58 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5_59 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6_60 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7_61 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8_62 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9_63 ;
  wire \BU2/U0/decimator.decimation_filter/en_delay_64 ;
  wire \BU2/U0/decimator.decimation_filter/down_sample_en_65 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>_rt_66 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>_rt_67 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>_rt_68 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>_rt_69 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>_rt_70 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>_rt_71 ;
  wire \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<7>_rt_72 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N88 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N87 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N86 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N85 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N84 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N83 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N82 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N81 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N80 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N79 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N78 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N77 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N76 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N75 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N74 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N73 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N72 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N71 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N65 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N51 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N29 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N16 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N15 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N14 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N13 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N12 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N11 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N10 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N9 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N8 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N7 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N6 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_32_73 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31_74 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30_75 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29_76 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28_77 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27_78 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26_79 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25_80 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_81 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_82 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_83 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_84 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_85 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_86 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_87 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_88 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_89 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_90 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_91 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_92 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_93 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_94 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_95 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_96 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_97 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_98 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_99 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_100 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_101 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_102 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_103 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_104 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_105 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 ;
  wire \BU2/U0/decimator.decimation_filter/en_tmp_106 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N23 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_19_107 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N22 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_18_108 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N21 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17_109 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N20 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16_110 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N19 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15_111 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N18 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14_112 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N17 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13_113 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N16 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12_114 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N15 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11_115 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N14 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10_116 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N13 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9_117 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N12 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8_118 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N11 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7_119 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N10 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6_120 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N9 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5_121 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N8 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4_122 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N7 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3_123 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N6 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2_124 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N5 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1_125 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N4 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0_126 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce ;
  wire NLW_VCC_P_UNCONNECTED;
  wire NLW_GND_G_UNCONNECTED;
  wire [11 : 0] din_127;
  wire [15 : 0] NlwRenamedSig_OI_dout;
  wire [2 : 2] \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe ;
  wire [7 : 0] \BU2/U0/decimator.decimation_filter/cnt_out ;
  wire [19 : 0] \BU2/U0/decimator.decimation_filter/comb_in ;
  wire [22 : 3] \BU2/U0/decimator.decimation_filter/int_out_reg ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe ;
  wire [3 : 3] \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe ;
  wire [7 : 0] \BU2/U0/decimator.decimation_filter/Result ;
  wire [6 : 0] \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy ;
  wire [21 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy ;
  wire [26 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy ;
  wire [31 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy ;
  wire [11 : 0] \BU2/U0/decimator.decimation_filter/din_reg ;
  wire [22 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> ;
  wire [22 : 1] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 ;
  wire [27 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> ;
  wire [27 : 1] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 ;
  wire [32 : 1] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 ;
  wire [18 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy ;
  wire [1 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt ;
  wire [1 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe ;
  wire [19 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 ;
  wire [3 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe ;
  wire [19 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in ;
  wire [19 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 ;
  wire [0 : 0] \BU2/chan_out ;
  assign
    rfd = NlwRenamedSig_OI_rfd,
    dout[15] = NlwRenamedSig_OI_dout[15],
    dout[14] = NlwRenamedSig_OI_dout[14],
    dout[13] = NlwRenamedSig_OI_dout[13],
    dout[12] = NlwRenamedSig_OI_dout[12],
    dout[11] = NlwRenamedSig_OI_dout[11],
    dout[10] = NlwRenamedSig_OI_dout[10],
    dout[9] = NlwRenamedSig_OI_dout[9],
    dout[8] = NlwRenamedSig_OI_dout[8],
    dout[7] = NlwRenamedSig_OI_dout[7],
    dout[6] = NlwRenamedSig_OI_dout[6],
    dout[5] = NlwRenamedSig_OI_dout[5],
    dout[4] = NlwRenamedSig_OI_dout[4],
    dout[3] = NlwRenamedSig_OI_dout[3],
    dout[2] = NlwRenamedSig_OI_dout[2],
    dout[1] = NlwRenamedSig_OI_dout[1],
    dout[0] = NlwRenamedSig_OI_dout[0],
    din_127[11] = din[11],
    din_127[10] = din[10],
    din_127[9] = din[9],
    din_127[8] = din[8],
    din_127[7] = din[7],
    din_127[6] = din[6],
    din_127[5] = din[5],
    din_127[4] = din[4],
    din_127[3] = din[3],
    din_127[2] = din[2],
    din_127[1] = din[1],
    din_127[0] = din[0];
  VCC VCC_0 (
    .P(NLW_VCC_P_UNCONNECTED)
  );
  GND GND_1 (
    .G(NLW_GND_G_UNCONNECTED)
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/Mshreg_pipe_2_2 ),
    .Q(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/Mshreg_pipe_2 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/Mshreg_pipe_2  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .Q(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/Mshreg_pipe_2_2 )
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/Mshreg_pipe_3_3 ),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/Mshreg_pipe_3 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/Mshreg_pipe_3  (
    .A0(\BU2/chan_out [0]),
    .A1(NlwRenamedSig_OI_rfd),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/Mshreg_pipe_3_3 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_1_4 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1_55 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_1 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_1  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [1]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_1_4 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_2_5 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2_56 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_2 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_2  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [2]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_2_5 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_0_6 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0_44 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_0 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_0  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_0_6 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_3_7 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3_57 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_3 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_3  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [3]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_3_7 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_4_8 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4_58 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_4 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_4  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_4_8 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_6_9 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6_60 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_6 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_6  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[2]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_6_9 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_7_10 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7_61 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_7 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_7  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[3]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_7_10 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_5_11 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5_59 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_5 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_5  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[1]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_5_11 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_8_12 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8_62 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_8 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_8  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[4]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_8_12 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_9_13 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9_63 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_9 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_9  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[5]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_9_13 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_11_14 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11_46 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_11 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_11  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[7]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_11_14 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_12_15 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12_47 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_12 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_12  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[8]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_12_15 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_10_16 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10_45 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_10 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_10  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[6]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_10_16 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_14_17 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14_49 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_14 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_14  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[10]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_14_17 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_15_18 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15_50 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_15 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_15  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[11]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_15_18 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_13_19 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13_48 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_13 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_13  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[9]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_13_19 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_17_20 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17_52 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_17 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_17  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[13]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_17_20 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_18 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_18_21 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_18_53 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_18 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_18  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[14]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_18_21 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_16_22 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16_51 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_16 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_16  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[12]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_16_22 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_19 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_19_23 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_19_54 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_19 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_19  (
    .A0(\BU2/chan_out [0]),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(NlwRenamedSig_OI_dout[15]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/Mshreg_pipe_1_19_23 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_0_24 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0_126 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_0 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_0  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_0_24 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_2_25 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2_124 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_2 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_2  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [2]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_2_25 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_3_26 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3_123 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_3 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_3  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [3]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_3_26 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_1_27 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1_125 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_1 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_1  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [1]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_1_27 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_4_28 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4_122 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_4 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_4  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [4]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_4_28 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_5_29 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5_121 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_5 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_5  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [5]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_5_29 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_7_30 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7_119 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_7 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_7  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [7]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_7_30 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_8_31 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8_118 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_8 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_8  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [8]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_8_31 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_6_32 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6_120 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_6 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_6  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [6]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_6_32 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_9_33 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9_117 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_9 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_9  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [9]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_9_33 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_10_34 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10_116 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_10 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_10  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [10]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_10_34 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_12_35 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12_114 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_12 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_12  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [12]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_12_35 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_13_36 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13_113 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_13 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_13  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [13]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_13_36 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_11_37 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11_115 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_11 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_11  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [11]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_11_37 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_15_38 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15_111 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_15 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_15  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [15]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_15_38 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_16_39 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16_110 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_16 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_16  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [16]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_16_39 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_14_40 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14_112 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_14 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_14  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [14]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_14_40 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_18 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_18_41 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_18_108 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_18 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_18  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [18]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_18_41 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_19 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_19_42 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_19_107 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_19 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_19  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [19]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_19_42 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_17_43 ),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17_109 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_17 .INIT = 16'h0000;
  SRL16E \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_17  (
    .A0(NlwRenamedSig_OI_rfd),
    .A1(\BU2/chan_out [0]),
    .A2(\BU2/chan_out [0]),
    .A3(\BU2/chan_out [0]),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .CLK(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [17]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/Mshreg_pipe_2_17_43 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_rst121 .INIT = 16'h0001;
  LUT4_D \BU2/U0/decimator.decimation_filter/cnt_rst121  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [6]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [5]),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .LO(\BU2/N66 ),
    .O(\BU2/U0/decimator.decimation_filter/cnt_rst1_map11 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_rst18 .INIT = 16'h0008;
  LUT4_D \BU2/U0/decimator.decimation_filter/cnt_rst18  (
    .I0(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2]),
    .I1(\BU2/U0/decimator.decimation_filter/en_delay_64 ),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .LO(\BU2/N65 ),
    .O(\BU2/U0/decimator.decimation_filter/cnt_rst1_map4 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_en1 .INIT = 4'h8;
  LUT2_D \BU2/U0/decimator.decimation_filter/cnt_en1  (
    .I0(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2]),
    .I1(\BU2/U0/decimator.decimation_filter/en_delay_64 ),
    .LO(\BU2/N64 ),
    .O(\BU2/U0/decimator.decimation_filter/cnt_en )
  );
  INV \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl1_INV_0  (
    .I(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [1]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl )
  );
  INV \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Mcount_ce_cnt_xor<0>11_INV_0  (
    .I(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [0]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result [0])
  );
  INV \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_lut<0>_INV_0  (
    .I(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .O(\BU2/U0/decimator.decimation_filter/Result [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_0_rstpot .INIT = 16'hFF78;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_0_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2]),
    .I1(\BU2/U0/decimator.decimation_filter/en_delay_64 ),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .O(\BU2/N56 )
  );
  defparam \BU2/U0/decimator.decimation_filter/down_sample_en_and000011 .INIT = 8'h80;
  LUT3 \BU2/U0/decimator.decimation_filter/down_sample_en_and000011  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_rst1_map4 ),
    .I2(\BU2/N66 ),
    .O(\BU2/N55 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_7 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_7  (
    .C(clk),
    .D(\BU2/N63 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_7_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_7_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_en ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [7]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [7]),
    .O(\BU2/N63 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_6 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_6  (
    .C(clk),
    .D(\BU2/N62 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_6_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_6_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_en ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [6]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [6]),
    .O(\BU2/N62 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_5 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_5  (
    .C(clk),
    .D(\BU2/N61 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_5_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_5_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_en ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [5]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [5]),
    .O(\BU2/N61 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_4 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_4  (
    .C(clk),
    .D(\BU2/N60 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_4_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_4_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_en ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [4]),
    .O(\BU2/N60 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_3 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_3  (
    .C(clk),
    .D(\BU2/N59 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_3_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_3_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_en ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [3]),
    .O(\BU2/N59 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_2 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_2  (
    .C(clk),
    .D(\BU2/N58 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_2_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_2_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_en ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [2]),
    .O(\BU2/N58 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_1 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_1  (
    .C(clk),
    .D(\BU2/N57 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_1_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_1_rstpot  (
    .I0(\BU2/N64 ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [1]),
    .O(\BU2/N57 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_rst2 .INIT = 16'h2000;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_rst2  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [7]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .I2(\BU2/N65 ),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_rst1_map11 ),
    .O(\BU2/U0/decimator.decimation_filter/cnt_rst )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_0 .INIT = 1'b1;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_0  (
    .C(clk),
    .D(\BU2/N56 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<7>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<7>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [7]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<7>_rt_72 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>_rt_66 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>_rt_67 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>_rt_68 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>_rt_69 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [5]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>_rt_70 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>_rt .INIT = 4'h2;
  LUT1 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>_rt  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [6]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>_rt_71 )
  );
  defparam \BU2/U0/decimator.decimation_filter/down_sample_en .INIT = 1'b0;
  FDR \BU2/U0/decimator.decimation_filter/down_sample_en  (
    .C(clk),
    .D(\BU2/N55 ),
    .R(\BU2/U0/decimator.decimation_filter/cnt_out [7]),
    .Q(\BU2/U0/decimator.decimation_filter/down_sample_en_65 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<0>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<0>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0_44 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [0]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<10>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<10>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10_45 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [10]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<11>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<11>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11_46 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [11]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<12>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<12>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12_47 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [12]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<13>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<13>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13_48 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [13]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<14>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<14>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14_49 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [14]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<15>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<15>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15_50 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [15]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<16>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<16>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16_51 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [16]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<17>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<17>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17_52 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [17]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<18>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<18>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_18_53 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [18]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<19>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<19>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_19_54 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [19]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<1>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<1>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1_55 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [1]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<2>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<2>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2_56 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [2]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<3>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<3>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3_57 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [3]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<4>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<4>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4_58 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [4]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<5>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<5>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5_59 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [5]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<6>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<6>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6_60 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [6]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<7>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<7>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7_61 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [7]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<8>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<8>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8_62 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [8]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<9>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<9>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9_63 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [9]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Mcount_ce_cnt_xor<1>11 .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Mcount_ce_cnt_xor<1>11  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [1]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [0]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce1 .INIT = 4'hD;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce1  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [1]),
    .I1(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce )
  );
  defparam \BU2/U0/decimator.decimation_filter/i_rdy1 .INIT = 4'h8;
  LUT2 \BU2/U0/decimator.decimation_filter/i_rdy1  (
    .I0(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe [0]),
    .O(rdy)
  );
  defparam \BU2/U0/decimator.decimation_filter/en_tmp .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/en_tmp  (
    .C(clk),
    .D(nd),
    .Q(\BU2/U0/decimator.decimation_filter/en_tmp_106 )
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_0 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_0  (
    .C(clk),
    .CE(nd),
    .D(din_127[0]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_1 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_1  (
    .C(clk),
    .CE(nd),
    .D(din_127[1]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_2  (
    .C(clk),
    .CE(nd),
    .D(din_127[2]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_3  (
    .C(clk),
    .CE(nd),
    .D(din_127[3]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_4 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_4  (
    .C(clk),
    .CE(nd),
    .D(din_127[4]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_5 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_5  (
    .C(clk),
    .CE(nd),
    .D(din_127[5]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_6 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_6  (
    .C(clk),
    .CE(nd),
    .D(din_127[6]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_7 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_7  (
    .C(clk),
    .CE(nd),
    .D(din_127[7]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_8 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_8  (
    .C(clk),
    .CE(nd),
    .D(din_127[8]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_9 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_9  (
    .C(clk),
    .CE(nd),
    .D(din_127[9]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_10 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_10  (
    .C(clk),
    .CE(nd),
    .D(din_127[10]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_11 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/din_reg_11  (
    .C(clk),
    .CE(nd),
    .D(din_127[11]),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/en_delay .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/en_delay  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .Q(\BU2/U0/decimator.decimation_filter/en_delay_64 )
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_3 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_3  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_4 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_4  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_5 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_5  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_6 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_6  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_7 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_7  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_8 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_8  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_9 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_9  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_10 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_10  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_11 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_11  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_12 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_12  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_13 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_13  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_14 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_14  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_15 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_15  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_16 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_16  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_17 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_17  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_18 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_18  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_19 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_19  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [19]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_20 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_20  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [20]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [20])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_21 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_21  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [21]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [21])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_22 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/int_out_reg_22  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [22]),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [22])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_0 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [3]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_1 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [4]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [5]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [6]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_4 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [7]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_5 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [8]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_6 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [9]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_7 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [10]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_8 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [11]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_9 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [12]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_10 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [13]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_11 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [14]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_12 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [15]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_13 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [16]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_14 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [17]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_15 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [18]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_16 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [19]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_17 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [20]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_18 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [21]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_19 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb_in_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [22]),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe_0  (
    .C(clk),
    .CE(NlwRenamedSig_OI_rfd),
    .D(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [3]),
    .R(\BU2/chan_out [0]),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe_0  (
    .C(clk),
    .CE(NlwRenamedSig_OI_rfd),
    .D(\BU2/U0/decimator.decimation_filter/down_sample_en_65 ),
    .R(\BU2/chan_out [0]),
    .Q(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(NlwRenamedSig_OI_rfd),
    .S(\BU2/U0/decimator.decimation_filter/Result [0]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [0])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [0]),
    .DI(\BU2/chan_out [0]),
    .S(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>_rt_66 ),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [1])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<1>_rt_66 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [1]),
    .DI(\BU2/chan_out [0]),
    .S(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>_rt_67 ),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [2])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>_rt_67 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [2]),
    .DI(\BU2/chan_out [0]),
    .S(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>_rt_68 ),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [3])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<3>_rt_68 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [3]),
    .DI(\BU2/chan_out [0]),
    .S(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>_rt_69 ),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [4])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<4>_rt_69 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [4]),
    .DI(\BU2/chan_out [0]),
    .S(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>_rt_70 ),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [5])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<5>_rt_70 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [5]),
    .DI(\BU2/chan_out [0]),
    .S(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>_rt_71 ),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [6])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<6>_rt_71 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [6])
  );
  XORCY \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<7>_rt_72 ),
    .O(\BU2/U0/decimator.decimation_filter/Result [7])
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [21]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N88 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [22])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<22> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<22>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [22]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [27]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N88 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [20]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N87 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [21])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [20]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [21]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N87 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [21])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<21> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<21>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [21]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [26]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N87 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [19]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N86 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [20])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [19]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [20]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N86 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [20])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<20> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<20>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [20]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [25]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N86 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [18]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N85 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [19])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [18]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [19]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N85 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<19> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<19>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [19]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [24]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N85 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N84 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [18])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [17]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N84 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<18> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [23]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N84 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N83 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N83 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<17> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [22]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N83 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N82 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N82 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<16> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N82 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N81 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N81 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<15> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N81 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N80 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N80 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<14> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N80 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N79 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N79 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<13> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N79 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N78 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N78 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<12> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N78 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N77 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N77 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<11> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N77 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [9]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N76 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [10])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [9]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N76 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<10> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N76 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [8]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N75 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [9])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [8]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N75 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<9> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N75 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [7]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N74 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [8])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [7]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N74 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<8> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N74 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N73 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [7])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [6]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N73 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<7> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N73 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N72 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [6])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [5]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N72 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<6> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N72 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N71 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [4]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N71 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<5> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N71 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [3]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<4> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [2]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<3> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [1]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<2> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<1> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 )
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [0]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<0> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [0]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<27>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [26]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N65 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [27])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<27> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<27>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [27]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_32_73 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N65 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<26>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [25]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [26])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<26>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [25]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [26]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [26])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<26> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<26>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [26]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31_74 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<25>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [24]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [25])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<25>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [24]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [25]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [25])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<25> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<25>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [25]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30_75 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<24>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [23]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [24])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<24>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [23]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [24]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [24])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<24> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<24>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [24]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29_76 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<23>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [22]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [23])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<23>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [22]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [23]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [23])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<23> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<23>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [23]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28_77 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [21]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [22])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [21]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [22]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [22])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<22> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<22>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [22]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27_78 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [20]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [21])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [20]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [21])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<21> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<21>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26_79 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [19]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [20])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [19]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [20])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<20> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<20>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25_80 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [18]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [19])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [18]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<19> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<19>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_81 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [18])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [17]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<18> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_82 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<17> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_83 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<16> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_84 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<15> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_85 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<14> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_86 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N51 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N51 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<13> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_87 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N51 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<12> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_88 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<11> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_89 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [9]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [10])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [9]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<10> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_90 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [8]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [9])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [8]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<9> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_91 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [7]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [8])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [7]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<8> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_92 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [7])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [6]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<7> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_93 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [6])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [5]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<6> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_94 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [4]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<5> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_95 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [3]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<4> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_96 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [2]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<3> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_97 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [1]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [2]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<2> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [2]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_98 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [1]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<1> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [1]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_99 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 )
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [0]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<0> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [0]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_100 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<32>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [31]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [32])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<32> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<32>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_32_73 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<31>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [30]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [31])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<31>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [30]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31_74 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [31])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<31> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<31>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31_74 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<30>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [29]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [30])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<30>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [29]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30_75 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [30])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<30> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<30>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30_75 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<29>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [28]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [29])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<29>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [28]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29_76 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [29])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<29> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<29>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29_76 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<28>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [27]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [28])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<28>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [27]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28_77 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [28])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<28> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<28>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28_77 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<27>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [26]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [27])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<27>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [26]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27_78 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [27])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<27> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<27>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27_78 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<26>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [25]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [26])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<26>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [25]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26_79 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [26])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<26> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<26>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26_79 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<25>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [24]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [25])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<25>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [24]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25_80 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [25])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<25> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<25>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25_80 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<24>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [23]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N29 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [24])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<24>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [23]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_81 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N29 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [24])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<24> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<24>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_81 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N29 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<23>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [22]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [23])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<23>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [22]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_82 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [23])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<23> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<23>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_82 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [21]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [22])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [21]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_83 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [22])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<22> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<22>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_83 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [20]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [21])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [20]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_84 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [21])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<21> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<21>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_84 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [19]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [20])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [19]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_85 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [20])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<20> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<20>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_85 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [18]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [19])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [18]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_86 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<19> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<19>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_86 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [18])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [17]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_87 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<18> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_87 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_88 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<17> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_88 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_89 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<16> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_89 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_90 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<15> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_90 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_91 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<14> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_91 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_92 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<13> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_92 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_93 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<12> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_93 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N16 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_94 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N16 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<11> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_94 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N16 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [9]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N15 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [10])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [9]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_95 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N15 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<10> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_95 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [10]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N15 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [8]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N14 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [9])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [8]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_96 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N14 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<9> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_96 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [9]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N14 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [7]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N13 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [8])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [7]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_97 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N13 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<8> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_97 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [8]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N13 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N12 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [7])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [6]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_98 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N12 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<7> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_98 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [7]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N12 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N11 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [6])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [5]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_99 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N11 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<6> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_99 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [6]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N11 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N10 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [4]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_100 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N10 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<5> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_100 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [5]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N10 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N9 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [3]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_101 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N9 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<4> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_101 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [4]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N9 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N8 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [2]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_102 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N8 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<3> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_102 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [3]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N8 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N7 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [1]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_103 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N7 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<2> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_103 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [2]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N7 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N6 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_104 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N6 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<1> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_104 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [1]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N6 )
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_105 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<0> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_105 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [0]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 )
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [11]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 ),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [0])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [10]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [9]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [19]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [19])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [8]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [18]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [7]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_22  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [22]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [22])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [6]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_21  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [21]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [21])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [17]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [16]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [5]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_20  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [20]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [20])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [15]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [4]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [14]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [3]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [13]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [2]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [12]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [1]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_23  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [23]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [23])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [18]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_22  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [22]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [22])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [9]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [17]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [8]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_21  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [21]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [16]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_20  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [20]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [15]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [7]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [6]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [14]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [5]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [13]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [4]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [12]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [3]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [11]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [2]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [2])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [10]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [1]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [1])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 ),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [0])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_27  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [27]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [27])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_26  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [26]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [26])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_25  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [25]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [25])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_24  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [24]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [24])
  );
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [19]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_32 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_32  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [32]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_32_73 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [31]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_31_74 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [30]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_30_75 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [29]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_29_76 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [28]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_28_77 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [27]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_27_78 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [26]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_26_79 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [25]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_25_80 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [24]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_81 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [23]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_82 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [22]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_83 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [21]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_84 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [20]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_85 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [19]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_86 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [18]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_87 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [17]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_88 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [16]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_89 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [15]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_90 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [14]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_91 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [13]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_92 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [12]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_93 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [11]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_94 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [10]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_95 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [9]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_96 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [8]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_97 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [7]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_98 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [6]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_99 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [5]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_100 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [4]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_101 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [3]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_102 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [2]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_103 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [1]),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_104 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/en_tmp_106 ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 ),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_105 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [18]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N23 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<19> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<19>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [19]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_19_107 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N23 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N22 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [18])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [17]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [18]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N22 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<18> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [18]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_18_108 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N22 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [17]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<17> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [17]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17_109 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N21 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N20 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [16]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N20 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<16> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [16]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16_110 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N20 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N19 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [15]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N19 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<15> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [15]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15_111 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N19 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N18 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [14]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N18 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<14> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [14]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14_112 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N18 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N17 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [13]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N17 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<13> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [13]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13_113 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N17 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N16 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [12]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N16 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<12> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [12]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12_114 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N16 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N15 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [11]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N15 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<11> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [11]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11_115 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N15 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [9]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N14 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [10])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [9]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [10]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N14 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<10> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [10]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10_116 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N14 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [8]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N13 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [9])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [8]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [9]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N13 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<9> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [9]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9_117 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N13 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [7]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N12 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [8])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [7]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [8]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N12 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<8> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [8]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8_118 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N12 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N11 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [7])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [6]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [7]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N11 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<7> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [7]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7_119 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N11 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N10 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [6])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [5]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [6]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N10 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<6> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [6]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6_120 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N10 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N9 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [4]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [5]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N9 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<5> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [5]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5_121 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N9 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N8 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [3]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [4]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N8 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<4> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [4]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4_122 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N8 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N7 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [2]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [3]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N7 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<3> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [3]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3_123 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N7 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N6 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [1]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [2]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N6 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<2> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [2]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2_124 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N6 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N5 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [0]),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [1]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N5 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<1> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [1]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1_125 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N5 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<0>  (
    .CI(NlwRenamedSig_OI_rfd),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N4 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [0])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy<0>  (
    .CI(NlwRenamedSig_OI_rfd),
    .DI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [0]),
    .S(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N4 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<0> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0_126 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N4 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl ),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result [1]),
    .R(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt_0 .INIT = 1'b1;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl ),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result [0]),
    .R(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe_0  (
    .C(clk),
    .CE(NlwRenamedSig_OI_rfd),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce ),
    .R(\BU2/chan_out [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe_0  (
    .C(clk),
    .CE(NlwRenamedSig_OI_rfd),
    .D(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .R(\BU2/chan_out [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_19 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [19]),
    .Q(NlwRenamedSig_OI_dout[15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_18 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [18]),
    .Q(NlwRenamedSig_OI_dout[14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_17 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [17]),
    .Q(NlwRenamedSig_OI_dout[13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_16 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [16]),
    .Q(NlwRenamedSig_OI_dout[12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_15 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [15]),
    .Q(NlwRenamedSig_OI_dout[11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_14 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [14]),
    .Q(NlwRenamedSig_OI_dout[10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_13 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [13]),
    .Q(NlwRenamedSig_OI_dout[9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_12 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [12]),
    .Q(NlwRenamedSig_OI_dout[8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_11 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [11]),
    .Q(NlwRenamedSig_OI_dout[7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_10 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [10]),
    .Q(NlwRenamedSig_OI_dout[6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_9 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [9]),
    .Q(NlwRenamedSig_OI_dout[5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_8 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [8]),
    .Q(NlwRenamedSig_OI_dout[4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_7 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [7]),
    .Q(NlwRenamedSig_OI_dout[3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_6 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [6]),
    .Q(NlwRenamedSig_OI_dout[2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_5 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [5]),
    .Q(NlwRenamedSig_OI_dout[1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_4 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [4]),
    .Q(NlwRenamedSig_OI_dout[0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_3 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [3]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_2 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [2]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_1 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [1]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_0 .INIT = 1'b0;
  FDE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_19 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_19  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [19]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_18 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_18  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [18]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_17 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_17  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [17]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_16 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_16  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [16]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_15 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_15  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [15]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_14 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_14  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [14]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_13 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_13  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [13]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_12 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_12  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [12]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_11 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_11  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [11]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_10 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_10  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [10]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_9 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_9  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [9]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_8 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_8  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [8]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_7 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_7  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [7]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_6 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_6  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [6]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_5 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_5  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [5]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_4 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_4  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [4]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_3 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_3  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [3]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_2 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_2  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [2]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_1 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_1  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [1]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_0 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_0  (
    .C(clk),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [0]),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [0])
  );
  VCC \BU2/XST_VCC  (
    .P(NlwRenamedSig_OI_rfd)
  );
  GND \BU2/XST_GND  (
    .G(\BU2/chan_out [0])
  );

// synopsys translate_on

endmodule

// synopsys translate_off

`timescale  1 ps / 1 ps

module glbl ();

    parameter ROC_WIDTH = 100000;
    parameter TOC_WIDTH = 0;

    wire GSR;
    wire GTS;
    wire PRLD;

    reg GSR_int;
    reg GTS_int;
    reg PRLD_int;

//--------   JTAG Globals --------------
    wire JTAG_TDO_GLBL;
    wire JTAG_TCK_GLBL;
    wire JTAG_TDI_GLBL;
    wire JTAG_TMS_GLBL;
    wire JTAG_TRST_GLBL;

    reg JTAG_CAPTURE_GLBL;
    reg JTAG_RESET_GLBL;
    reg JTAG_SHIFT_GLBL;
    reg JTAG_UPDATE_GLBL;

    reg JTAG_SEL1_GLBL = 0;
    reg JTAG_SEL2_GLBL = 0 ;
    reg JTAG_SEL3_GLBL = 0;
    reg JTAG_SEL4_GLBL = 0;

    reg JTAG_USER_TDO1_GLBL = 1'bz;
    reg JTAG_USER_TDO2_GLBL = 1'bz;
    reg JTAG_USER_TDO3_GLBL = 1'bz;
    reg JTAG_USER_TDO4_GLBL = 1'bz;

    assign (weak1, weak0) GSR = GSR_int;
    assign (weak1, weak0) GTS = GTS_int;
    assign (weak1, weak0) PRLD = PRLD_int;

    initial begin
	GSR_int = 1'b1;
	PRLD_int = 1'b1;
	#(ROC_WIDTH)
	GSR_int = 1'b0;
	PRLD_int = 1'b0;
    end

    initial begin
	GTS_int = 1'b1;
	#(TOC_WIDTH)
	GTS_int = 1'b0;
    end

endmodule

// synopsys translate_on
