--------------------------------------------------------------------------------
--     This file is owned and controlled by Xilinx and must be used           --
--     solely for design, simulation, implementation and creation of          --
--     design files limited to Xilinx devices or technologies. Use            --
--     with non-Xilinx devices or technologies is expressly prohibited        --
--     and immediately terminates your license.                               --
--                                                                            --
--     XILINX IS PROVIDING THIS DESIGN, CODE, OR INFORMATION "AS IS"          --
--     SOLELY FOR USE IN DEVELOPING PROGRAMS AND SOLUTIONS FOR                --
--     XILINX DEVICES.  BY PROVIDING THIS DESIGN, CODE, OR INFORMATION        --
--     AS ONE POSSIBLE IMPLEMENTATION OF THIS FEATURE, APPLICATION            --
--     OR STANDARD, XILINX IS MAKING NO REPRESENTATION THAT THIS              --
--     IMPLEMENTATION IS FREE FROM ANY CLAIMS OF INFRINGEMENT,                --
--     AND YOU ARE RESPONSIBLE FOR OBTAINING ANY RIGHTS YOU MAY REQUIRE       --
--     FOR YOUR IMPLEMENTATION.  XILINX EXPRESSLY DISCLAIMS ANY               --
--     WARRANTY WHATSOEVER WITH RESPECT TO THE ADEQUACY OF THE                --
--     IMPLEMENTATION, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OR         --
--     REPRESENTATIONS THAT THIS IMPLEMENTATION IS FREE FROM CLAIMS OF        --
--     INFRINGEMENT, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS        --
--     FOR A PARTICULAR PURPOSE.                                              --
--                                                                            --
--     Xilinx products are not intended for use in life support               --
--     appliances, devices, or systems. Use in such applications are          --
--     expressly prohibited.                                                  --
--                                                                            --
--     (c) Copyright 1995-2007 Xilinx, Inc.                                   --
--     All rights reserved.                                                   --
--------------------------------------------------------------------------------
-- You must compile the wrapper file dec.vhd when simulating
-- the core, dec. When compiling the wrapper file, be sure to
-- reference the XilinxCoreLib VHDL simulation library. For detailed
-- instructions, please refer to the "CORE Generator Help".

-- The synthesis directives "translate_off/translate_on" specified
-- below are supported by Xilinx, Mentor Graphics and Synplicity
-- synthesis tools. Ensure they are correct for your synthesis tool(s).

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
-- synthesis translate_off
Library XilinxCoreLib;
-- synthesis translate_on
ENTITY dec IS
	port (
	din: IN std_logic_VECTOR(13 downto 0);
	nd: IN std_logic;
	ce: IN std_logic;
	sclr: IN std_logic;
	clk: IN std_logic;
	dout: OUT std_logic_VECTOR(13 downto 0);
	rdy: OUT std_logic;
	rfd: OUT std_logic);
END dec;

ARCHITECTURE dec_a OF dec IS
-- synthesis translate_off
component wrapped_dec
	port (
	din: IN std_logic_VECTOR(13 downto 0);
	nd: IN std_logic;
	ce: IN std_logic;
	sclr: IN std_logic;
	clk: IN std_logic;
	dout: OUT std_logic_VECTOR(13 downto 0);
	rdy: OUT std_logic;
	rfd: OUT std_logic);
end component;

-- Configuration specification 
	for all : wrapped_dec use entity XilinxCoreLib.cic_compiler_v1_0(behavioral)
		generic map(
			c_num_stages => 3,
			c_list_rates => "4,5",
			c_num_channels => 1,
			c_has_rounding => 0,
			c_diff_delay => 1,
			c_input_width => 14,
			c_use_dsp => 0,
			c_filter_type => 1,
			c_sample_freq => 65000000,
			c_overclock => 1,
			c_has_sclr => 1,
			c_rate_type => 0,
			c_min_rate => 16,
			c_has_ce => 1,
			c_family => "virtex4",
			c_clk_freq => 65000000,
			c_rate => 16,
			c_max_rate => 16,
			c_num_rates => 2,
			c_component_name => "dec",
			c_xdevicefamily => "virtex4",
			c_output_width => 14);
-- synthesis translate_on
BEGIN
-- synthesis translate_off
U0 : wrapped_dec
		port map (
			din => din,
			nd => nd,
			ce => ce,
			sclr => sclr,
			clk => clk,
			dout => dout,
			rdy => rdy,
			rfd => rfd);
-- synthesis translate_on

END dec_a;

