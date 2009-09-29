////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995-2007 Xilinx, Inc.  All rights reserved.
////////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor: Xilinx
// \   \   \/     Version: J.40
//  \   \         Application: netgen
//  /   /         Filename: dec.v
// /___/   /\     Timestamp: Wed Apr 29 23:29:26 2009
// \   \  /  \ 
//  \___\/\___\
//             
// Command	: -intstyle ise -w -sim -ofmt verilog /afs/unity.ncsu.edu/users/b/bmhendri/w00t/woosha/High_Speed_Octal_synchronous_capture/tmp/_cg/dec.ngc /afs/unity.ncsu.edu/users/b/bmhendri/w00t/woosha/High_Speed_Octal_synchronous_capture/tmp/_cg/dec.v 
// Device	: 4vfx20ff672-10
// Input file	: /afs/unity.ncsu.edu/users/b/bmhendri/w00t/woosha/High_Speed_Octal_synchronous_capture/tmp/_cg/dec.ngc
// Output file	: /afs/unity.ncsu.edu/users/b/bmhendri/w00t/woosha/High_Speed_Octal_synchronous_capture/tmp/_cg/dec.v
// # of Modules	: 1
// Design Name	: dec
// Xilinx        : /afs/eos.ncsu.edu/dist/xilinx92i/ise
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

module dec (
  sclr, ce, rfd, rdy, nd, clk, dout, din
);
  input sclr;
  input ce;
  output rfd;
  output rdy;
  input nd;
  input clk;
  output [13 : 0] dout;
  input [13 : 0] din;
  
  // synopsys translate_off
  
  wire NlwRenamedSig_OI_rfd;
  wire \BU2/N68 ;
  wire \BU2/N67 ;
  wire \BU2/N66 ;
  wire \BU2/N65 ;
  wire \BU2/N69 ;
  wire \BU2/N64 ;
  wire \BU2/U0/decimator.decimation_filter/cnt_out_not0001 ;
  wire \BU2/U0/decimator.decimation_filter/cnt_rst ;
  wire \BU2/U0/decimator.decimation_filter/cnt_rst_map9 ;
  wire \BU2/N62 ;
  wire \BU2/N28 ;
  wire \BU2/U0/decimator.decimation_filter/down_sample_en_and0000_2 ;
  wire \BU2/U0/decimator.decimation_filter/din_reg_not0002 ;
  wire \BU2/U0/decimator.decimation_filter/en_delay_3 ;
  wire \BU2/U0/decimator.decimation_filter/en_tmp_4 ;
  wire \BU2/U0/decimator.decimation_filter/down_sample_en_5 ;
  wire \BU2/U0/decimator.decimation_filter/comb_en_in1 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 ;
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
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 ;
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
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_6 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_7 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_8 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_9 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_10 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_11 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_12 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_13 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_14 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_15 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_16 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_17 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_18 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_19 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_20 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_21 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_22 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_23 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_24 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_25 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_26 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_27 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_28 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_29 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_30 ;
  wire \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 ;
  wire \BU2/U0/decimator.decimation_filter/int_en ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0_31 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_0_32 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1_33 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_1_34 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2_35 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_2_36 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3_37 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_3_38 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4_39 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_4_40 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5_41 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_5_42 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6_43 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_6_44 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7_45 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_7_46 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8_47 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_8_48 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9_49 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_9_50 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10_51 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_10_52 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11_53 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_11_54 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12_55 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_12_56 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13_57 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_13_58 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14_59 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_14_60 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15_61 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_15_62 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16_63 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_16_64 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17_65 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_17_66 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_0_67 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_1_68 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_2_69 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_3_70 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_4_71 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_5_72 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_6_73 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_7_74 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_8_75 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_9_76 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_10_77 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_11_78 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_12_79 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_13_80 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_14_81 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_15_82 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_16_83 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_17_84 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_0_85 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_1_86 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_2_87 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_3_88 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_4_89 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_5_90 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_6_91 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_7_92 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_8_93 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_9_94 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_10_95 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_11_96 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_12_97 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_13_98 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_14_99 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_15_100 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_16_101 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_17_102 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N21 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17_103 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N20 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16_104 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N19 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15_105 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N18 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14_106 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N17 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13_107 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N16 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12_108 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N15 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11_109 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N14 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10_110 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N13 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9_111 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N12 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8_112 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N11 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7_113 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N10 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6_114 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N9 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5_115 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N8 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4_116 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N7 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3_117 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N6 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2_118 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N5 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1_119 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N4 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0_120 ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl ;
  wire \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce ;
  wire NLW_VCC_P_UNCONNECTED;
  wire NLW_GND_G_UNCONNECTED;
  wire [13 : 0] din_121;
  wire [13 : 0] NlwRenamedSig_OI_dout;
  wire [4 : 0] \BU2/U0/decimator.decimation_filter/Result ;
  wire [2 : 2] \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy ;
  wire [4 : 0] \BU2/U0/decimator.decimation_filter/cnt_out ;
  wire [17 : 0] \BU2/U0/decimator.decimation_filter/comb_in ;
  wire [18 : 1] \BU2/U0/decimator.decimation_filter/int_out_reg ;
  wire [2 : 0] \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe ;
  wire [3 : 0] \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe ;
  wire [17 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy ;
  wire [20 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy ;
  wire [23 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy ;
  wire [12 : 0] \BU2/U0/decimator.decimation_filter/din_reg ;
  wire [18 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> ;
  wire [18 : 1] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 ;
  wire [21 : 0] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> ;
  wire [21 : 1] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 ;
  wire [24 : 1] \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 ;
  wire [16 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy ;
  wire [1 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt ;
  wire [1 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe ;
  wire [17 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 ;
  wire [3 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum ;
  wire [0 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe ;
  wire [17 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in ;
  wire [17 : 0] \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 ;
  wire [0 : 0] \BU2/chan_out ;
  assign
    rfd = NlwRenamedSig_OI_rfd,
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
    din_121[13] = din[13],
    din_121[12] = din[12],
    din_121[11] = din[11],
    din_121[10] = din[10],
    din_121[9] = din[9],
    din_121[8] = din[8],
    din_121[7] = din[7],
    din_121[6] = din[6],
    din_121[5] = din[5],
    din_121[4] = din[4],
    din_121[3] = din[3],
    din_121[2] = din[2],
    din_121[1] = din[1],
    din_121[0] = din[0];
  VCC VCC_0 (
    .P(NLW_VCC_P_UNCONNECTED)
  );
  GND GND_1 (
    .G(NLW_GND_G_UNCONNECTED)
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_rst17 .INIT = 16'h0008;
  LUT4_L \BU2/U0/decimator.decimation_filter/cnt_rst17  (
    .I0(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2]),
    .I1(\BU2/U0/decimator.decimation_filter/en_delay_3 ),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .LO(\BU2/U0/decimator.decimation_filter/cnt_rst_map9 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<4>11 .INIT = 8'h6A;
  LUT3_L \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<4>11  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .I2(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [2]),
    .LO(\BU2/U0/decimator.decimation_filter/Result [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_not00011 .INIT = 8'h80;
  LUT3_D \BU2/U0/decimator.decimation_filter/cnt_out_not00011  (
    .I0(ce),
    .I1(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2]),
    .I2(\BU2/U0/decimator.decimation_filter/en_delay_3 ),
    .LO(\BU2/N69 ),
    .O(\BU2/U0/decimator.decimation_filter/cnt_out_not0001 )
  );
  defparam \BU2/U0/decimator.decimation_filter/down_sample_en_and0000_SW0 .INIT = 16'hFFBF;
  LUT4_L \BU2/U0/decimator.decimation_filter/down_sample_en_and0000_SW0  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I1(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2]),
    .I2(\BU2/U0/decimator.decimation_filter/en_delay_3 ),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .LO(\BU2/N28 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<2>11 .INIT = 8'h6A;
  LUT3_L \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<2>11  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .LO(\BU2/U0/decimator.decimation_filter/Result [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<1>11 .INIT = 4'h6;
  LUT2_L \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<1>11  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .LO(\BU2/U0/decimator.decimation_filter/Result [1])
  );
  INV \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl1_INV_0  (
    .I(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [1]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_ctl )
  );
  INV \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<0>11_INV_0  (
    .I(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .O(\BU2/U0/decimator.decimation_filter/Result [0])
  );
  INV \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Mcount_ce_cnt_xor<0>11_INV_0  (
    .I(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/ce_cnt [0]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Result [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_0 .INIT = 1'b1;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_0  (
    .C(clk),
    .D(\BU2/N68 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_0_rstpot .INIT = 16'hFEF4;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_0_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out_not0001 ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [0]),
    .O(\BU2/N68 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_1 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_1  (
    .C(clk),
    .D(\BU2/N67 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_1_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_1_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out_not0001 ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [1]),
    .O(\BU2/N67 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_2 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_2  (
    .C(clk),
    .D(\BU2/N66 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_2_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_2_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out_not0001 ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [2]),
    .O(\BU2/N66 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_3 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_3  (
    .C(clk),
    .D(\BU2/N65 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_3_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_3_rstpot  (
    .I0(\BU2/N69 ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [3]),
    .O(\BU2/N65 )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_4 .INIT = 1'b0;
  FD \BU2/U0/decimator.decimation_filter/cnt_out_4  (
    .C(clk),
    .D(\BU2/N64 ),
    .Q(\BU2/U0/decimator.decimation_filter/cnt_out [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_out_4_rstpot .INIT = 16'h0E04;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_out_4_rstpot  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out_not0001 ),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_rst ),
    .I3(\BU2/U0/decimator.decimation_filter/Result [4]),
    .O(\BU2/N64 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<3>11 .INIT = 16'h6AAA;
  LUT4 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_xor<3>11  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .O(\BU2/U0/decimator.decimation_filter/Result [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_rst29 .INIT = 16'hEAAA;
  LUT4 \BU2/U0/decimator.decimation_filter/cnt_rst29  (
    .I0(sclr),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .I2(\BU2/N62 ),
    .I3(\BU2/U0/decimator.decimation_filter/cnt_rst_map9 ),
    .O(\BU2/U0/decimator.decimation_filter/cnt_rst )
  );
  defparam \BU2/U0/decimator.decimation_filter/cnt_rst29_SW0 .INIT = 8'h02;
  LUT3 \BU2/U0/decimator.decimation_filter/cnt_rst29_SW0  (
    .I0(ce),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .O(\BU2/N62 )
  );
  defparam \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>11 .INIT = 8'h80;
  LUT3 \BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy<2>11  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [2]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [1]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .O(\BU2/U0/decimator.decimation_filter/Mcount_cnt_out_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_en_in11 .INIT = 4'h8;
  LUT2 \BU2/U0/decimator.decimation_filter/comb_en_in11  (
    .I0(\BU2/U0/decimator.decimation_filter/down_sample_en_5 ),
    .I1(ce),
    .O(\BU2/U0/decimator.decimation_filter/comb_en_in1 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_19_not00001 .INIT = 4'h8;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_19_not00001  (
    .I0(\BU2/U0/decimator.decimation_filter/en_tmp_4 ),
    .I1(ce),
    .O(\BU2/U0/decimator.decimation_filter/int_en )
  );
  defparam \BU2/U0/decimator.decimation_filter/down_sample_en_and0000 .INIT = 16'h0002;
  LUT4 \BU2/U0/decimator.decimation_filter/down_sample_en_and0000  (
    .I0(\BU2/U0/decimator.decimation_filter/cnt_out [0]),
    .I1(\BU2/U0/decimator.decimation_filter/cnt_out [4]),
    .I2(\BU2/U0/decimator.decimation_filter/cnt_out [3]),
    .I3(\BU2/N28 ),
    .O(\BU2/U0/decimator.decimation_filter/down_sample_en_and0000_2 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<0>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<0>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0_31 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [0]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<10>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<10>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10_51 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [10]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<11>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<11>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11_53 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [11]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<12>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<12>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12_55 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [12]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<13>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<13>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13_57 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [13]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<14>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<14>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14_59 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [14]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<15>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<15>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15_61 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [15]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<16>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<16>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16_63 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [16]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<17>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<17>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17_65 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [17]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<1>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<1>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1_33 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [1]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<2>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<2>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2_35 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [2]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<3>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<3>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3_37 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [3]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<4>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<4>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4_39 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [4]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<5>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<5>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5_41 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [5]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<6>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<6>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6_43 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [6]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<7>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<7>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7_45 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [7]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<8>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<8>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8_47 ),
    .I2(\BU2/U0/decimator.decimation_filter/comb_in [8]),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001 [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<9>1 .INIT = 8'hE4;
  LUT3 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in_mux0001<9>1  (
    .I0(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9_49 ),
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
  defparam \BU2/U0/decimator.decimation_filter/din_reg_not00021 .INIT = 4'h8;
  LUT2 \BU2/U0/decimator.decimation_filter/din_reg_not00021  (
    .I0(nd),
    .I1(ce),
    .O(\BU2/U0/decimator.decimation_filter/din_reg_not0002 )
  );
  defparam \BU2/U0/decimator.decimation_filter/i_rdy1 .INIT = 4'h8;
  LUT2 \BU2/U0/decimator.decimation_filter/i_rdy1  (
    .I0(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe [0]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe [0]),
    .O(rdy)
  );
  defparam \BU2/U0/decimator.decimation_filter/down_sample_en .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/down_sample_en  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/down_sample_en_and0000_2 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/down_sample_en_5 )
  );
  defparam \BU2/U0/decimator.decimation_filter/en_tmp .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/en_tmp  (
    .C(clk),
    .CE(ce),
    .D(nd),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/en_tmp_4 )
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/din_reg_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/din_reg_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/din_reg_not0002 ),
    .D(din_121[13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/din_reg [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/en_delay .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/en_delay  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/en_tmp_4 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/en_delay_3 )
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_1  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_2  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_3  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_4  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_5  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_6  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_7  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_8  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_9  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_10  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_11  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_12  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_13  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_14  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_15  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_16  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_17  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/int_out_reg_18 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/int_out_reg_18  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/int_out_reg [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [14]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [15]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [16]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [17]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb_in_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb_in_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/int_out_reg [18]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb_in [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/en_tmp_4 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_en_pipe_delay/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe_0  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delaya/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe_0  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/down_sample_en_5 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb_en_in1 ),
    .D(\BU2/U0/decimator.decimation_filter/down_sample_en_5 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/gen_comb_en_pipe_delay/pipe [0])
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<18> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N70 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<17> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N69 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<16> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N68 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<15> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N67 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<14> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N66 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N65 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N65 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<13> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N65 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<12> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N64 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<11> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N63 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [9]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [10])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [9]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<10> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N62 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [8]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [9])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [8]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<9> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N61 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [7]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [8])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [7]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<8> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N60 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [7])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [6]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<7> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N59 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [6])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [5]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<6> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N58 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [4]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<5> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N57 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [3]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<4> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N56 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [2]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<3> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N55 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [1]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<2> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N54 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<1> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N53 )
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [0]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<0> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0001_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [0]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [20]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N51 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [21])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<21> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<21>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_6 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N51 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [19]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [20])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [19]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [20])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<20> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<20>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_7 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N50 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [18]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [19])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [18]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<19> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<19>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_8 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N49 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [18])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [17]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<18> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_9 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N48 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<17> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_10 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N47 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<16> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_11 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N46 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<15> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_12 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N45 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<14> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_13 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N44 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<13> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_14 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N43 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<12> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_15 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N42 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<11> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_16 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N41 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [9]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [10])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<10>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [9]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<10> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_17 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N40 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [8]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [9])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<9>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [8]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<9> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_18 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N39 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [7]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [8])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<8>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [7]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<8> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_19 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N38 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [6]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [7])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<7>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [6]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<7> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_20 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N37 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [5]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [6])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<6>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [5]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<6> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_21 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N36 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [4]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [5])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<5>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [4]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<5> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_22 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N35 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [3]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [4])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<4>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [3]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<4> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_23 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N34 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [2]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [3])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<3>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [2]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<3> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_24 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N33 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [1]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [2])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<2>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [1]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [2]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<2> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [2]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_25 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N32 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_xor<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [0]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [1])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<1>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [1]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<1> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [1]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_26 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N31 )
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [0]),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<0> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd__add0000_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [0]),
    .I1(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_27 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<24>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [23]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N29 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [24])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<24> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<24>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_6 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N29 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<23>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [22]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [23])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<23>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [22]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_7 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [23])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<23> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<23>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_7 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N28 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [21]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [22])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<22>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [21]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_8 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [22])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<22> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<22>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_8 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N27 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [20]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [21])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<21>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [20]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_9 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [21])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<21> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<21>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_9 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N26 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [19]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [20])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<20>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [19]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_10 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [20])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<20> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<20>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_10 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N25 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [18]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [19])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<19>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [18]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_11 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<19> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<19>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_11 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N24 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [17]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [18])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<18>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [17]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_12 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [18])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<18> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<18>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_12 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N23 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [17])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [16]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_13 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<17> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_13 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N22 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [15]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [16])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<16>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [15]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_14 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [16])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<16> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<16>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_14 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N21 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [14]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [15])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<15>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [14]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_15 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [15])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<15> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<15>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_15 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N20 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [13]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [14])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<14>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [13]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_16 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [14])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<14> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<14>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_16 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N19 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [12]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [13])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<13>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [12]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_17 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [13])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<13> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<13>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_17 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N18 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [11]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [12])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<12>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [11]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_18 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [12])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<12> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<12>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_18 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [12]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N17 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_xor<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [10]),
    .LI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N16 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [11])
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<11>  (
    .CI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [10]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_19 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N16 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [11])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<11> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<11>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_19 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_20 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N15 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [10])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<10> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<10>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_20 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_21 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N14 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [9])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<9> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<9>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_21 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_22 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N13 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [8])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<8> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<8>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_22 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_23 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N12 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [7])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<7> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<7>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_23 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_24 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N11 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [6])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<6> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<6>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_24 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_25 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N10 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [5])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<5> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<5>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_25 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_26 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N9 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [4])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<4> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<4>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_26 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_27 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N8 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<3> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<3>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_27 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_28 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N7 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<2> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<2>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_28 ),
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
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_29 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N6 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<1> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<1>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_29 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [1]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N6 )
  );
  MUXCY \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy<0>  (
    .CI(\BU2/chan_out [0]),
    .DI(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_30 ),
    .S(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 ),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_cy [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<0> .INIT = 4'h6;
  LUT2 \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/Madd_sum_0_add0000_lut<0>  (
    .I0(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_30 ),
    .I1(\BU2/U0/decimator.decimation_filter/din_reg [0]),
    .O(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 )
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [11])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N52 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [0])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [10])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [9])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [8])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [7])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [17]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [17])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [18]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [18])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [16]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [16])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [5])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [6])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [4])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [14]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [14])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [15]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [15])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [13])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [2])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [3])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [12])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2>_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0001 [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<2> [1])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [18]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [18])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [17]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [17])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [9])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_21  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [21]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [21])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [16]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [16])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [8])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_20  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [20]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [20])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [15]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [15])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [7])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [14]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [14])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [6])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [13])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [4])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [5])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [3])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [11])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [12])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [10])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [1])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [2])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N30 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [0])
  );
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1>_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/_add0000 [19]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum<1> [19])
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [24]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_24_6 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [23]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_23_7 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [22]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_22_8 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [21]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_21_9 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [20]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_20_10 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [19]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_19_11 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [18]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_18_12 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [17]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_17_13 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [16]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_16_14 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [15]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_15_15 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [14]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_14_16 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_13_17 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_12_18 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_11_19 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_10_20 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_9_21 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_8_22 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_7_23 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_6_24 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_5_25 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_4_26 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_3_27 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_2_28 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_add0000 [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_1_29 )
  );
  defparam \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/int_en ),
    .D(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/N5 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/integrator/gen_int_fab_unfold.integrator/sum_0_0_30 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_0_32 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_1_34 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_2_36 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_3_38 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_4_40 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_5_42 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_6_44 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_7_46 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_8_48 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_9_50 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_10_52 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_11_54 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_12_56 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_13_58 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_14_60 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_15_62 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_16_64 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(NlwRenamedSig_OI_dout[13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_17_66 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_0_32 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_0_31 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_1_34 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_1_33 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_2_36 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_2_35 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_3_38 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_3_37 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_4_40 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_4_39 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_5_42 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_5_41 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_6_44 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_6_43 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_7_46 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_7_45 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_8_48 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_8_47 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_9_50 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_9_49 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_10_52 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_10_51 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_11_54 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_11_53 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_12_56 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_12_55 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_13_58 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_13_57 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_14_60 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_14_59 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_15_62 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_15_61 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_16_64 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_16_63 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_0_17_66 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_sum/pipe_1_17_65 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_0_67 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_1_68 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_2_69 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_3_70 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [4]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_4_71 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [5]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_5_72 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [6]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_6_73 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [7]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_7_74 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [8]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_8_75 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [9]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_9_76 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [10]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_10_77 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [11]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_11_78 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [12]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_12_79 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [13]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_13_80 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [14]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_14_81 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [15]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_15_82 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [16]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_16_83 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [17]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_17_84 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_0_67 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_0_85 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_1_68 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_1_86 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_2_69 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_2_87 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_3_70 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_3_88 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_4_71 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_4_89 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_5_72 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_5_90 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_6_73 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_6_91 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_7_74 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_7_92 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_8_75 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_8_93 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_9_76 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_9_94 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_10_77 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_10_95 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_11_78 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_11_96 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_12_79 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_12_97 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_13_80 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_13_98 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_14_81 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_14_99 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_15_82 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_15_100 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_16_83 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_16_101 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_0_17_84 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_17_102 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_0_85 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0_120 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_1_86 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1_119 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_2_87 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2_118 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_3_88 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3_117 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_4_89 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4_116 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_5_90 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5_115 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_6_91 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6_114 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_7_92 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7_113 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_8_93 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8_112 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_9_94 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9_111 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_10_95 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10_110 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_11_96 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11_109 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_12_97 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12_108 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_13_98 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13_107 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_14_99 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14_106 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_15_100 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15_105 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_16_101 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16_104 )
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_1_17_102 ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17_103 )
  );
  XORCY \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_xor<17>  (
    .CI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_cy [16]),
    .LI(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/N21 ),
    .O(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [17])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<17> .INIT = 4'h9;
  LUT2 \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/Msub_sum_sub0000_lut<17>  (
    .I0(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/stage_in [17]),
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_17_103 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_16_104 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_15_105 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_14_106 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_13_107 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_12_108 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_11_109 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_10_110 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_9_111 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_8_112 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_7_113 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_6_114 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_5_115 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_4_116 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_3_117 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_2_118 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_1_119 ),
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
    .I1(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.delay_in/pipe_2_0_120 ),
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
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/comb_ce ),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe_0  (
    .C(clk),
    .CE(ce),
    .D(\BU2/U0/decimator.decimation_filter/delay_comb_en_by_1/pipe [0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.en_delay/pipe [0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_17 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_17  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [17]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[13])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_16 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_16  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [16]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[12])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_15 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_15  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [15]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[11])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_14 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_14  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [14]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[10])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_13 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_13  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [13]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[9])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_12 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_12  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [12]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[8])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_11 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_11  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [11]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[7])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_10 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_10  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [10]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[6])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_9 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_9  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [9]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[5])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_8 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_8  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [8]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[4])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_7 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_7  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [7]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_6 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_6  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [6]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_5 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_5  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [5]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_4 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_4  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [4]),
    .R(sclr),
    .Q(NlwRenamedSig_OI_dout[0])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_3 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_3  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [3]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [3])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_2 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_2  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [2]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [2])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_1 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_1  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [1]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [1])
  );
  defparam \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_0 .INIT = 1'b0;
  FDRE \BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_0  (
    .C(clk),
    .CE(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/non_pipelined_fabric.comb_en_delay/pipe [0]),
    .D(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum_sub0000 [0]),
    .R(sclr),
    .Q(\BU2/U0/decimator.decimation_filter/comb/gen_comb_fab_fold.comb/sum [0])
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
