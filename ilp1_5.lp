Maximize
problem: iir_master + idct_master + sink_master
Subject To
constraint_1 :  +  1 src_master +  1 src_slave = 1
constraint_2 :  + 0 src_master <= 0
constraint_3 :  + 3 src_slave +  1 C_iir_src +  1 C_idct_src +  1 C_sink_src <= 3
constraint_4 :  -  1 src_slave = 0
constraint_5 :  -  1 src_master +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 = 0
constraint_6 :  -  1 C_src_iir +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_7 :  -  1 C_src_idct +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_8 :  -  1 C_src_sink +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_9 :  +  1 iir_master +  1 iir_slave = 1
constraint_10 :  + 1 iir_master +  1 C_iir_src <= 1
constraint_11 :  + 2 iir_slave +  1 C_idct_iir +  1 C_sink_iir <= 2
constraint_12 :  -  1 iir_slave +  1 C_iir_src = 0
constraint_13 :  -  1 iir_master +  1 map_iir_CLIENT_PE0 +  1 map_iir_CLIENT_PE2 +  1 map_iir_CLIENT_PE3 +  1 map_iir_CLIENT_PE4 +  1 map_iir_CLIENT_PE6 +  1 map_iir_CLIENT_PE7 +  1 map_iir_CLIENT_PE13 +  1 map_iir_CLIENT_PE14 = 0
constraint_14 :  -  1 C_iir_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_15 :  -  1 C_iir_idct +  1 map_iir_CLIENT_PE0 +  1 map_iir_CLIENT_PE2 +  1 map_iir_CLIENT_PE3 +  1 map_iir_CLIENT_PE4 +  1 map_iir_CLIENT_PE6 +  1 map_iir_CLIENT_PE7 +  1 map_iir_CLIENT_PE13 +  1 map_iir_CLIENT_PE14 >= 0
constraint_16 :  -  1 C_iir_sink +  1 map_iir_CLIENT_PE0 +  1 map_iir_CLIENT_PE2 +  1 map_iir_CLIENT_PE3 +  1 map_iir_CLIENT_PE4 +  1 map_iir_CLIENT_PE6 +  1 map_iir_CLIENT_PE7 +  1 map_iir_CLIENT_PE13 +  1 map_iir_CLIENT_PE14 >= 0
constraint_17 :  +  1 idct_master +  1 idct_slave = 1
constraint_18 :  + 2 idct_master +  1 C_idct_src +  1 C_idct_iir <= 2
constraint_19 :  + 1 idct_slave +  1 C_sink_idct <= 1
constraint_20 :  -  1 idct_slave +  1 C_idct_src +  1 C_idct_iir = 0
constraint_21 :  -  1 idct_master +  1 map_idct_CLIENT_PE0 +  1 map_idct_CLIENT_PE2 +  1 map_idct_CLIENT_PE3 +  1 map_idct_CLIENT_PE4 +  1 map_idct_CLIENT_PE6 +  1 map_idct_CLIENT_PE7 +  1 map_idct_CLIENT_PE13 +  1 map_idct_CLIENT_PE14 = 0
constraint_22 :  -  1 C_idct_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_23 :  -  1 C_idct_iir +  1 map_iir_CLIENT_PE0 +  1 map_iir_CLIENT_PE2 +  1 map_iir_CLIENT_PE3 +  1 map_iir_CLIENT_PE4 +  1 map_iir_CLIENT_PE6 +  1 map_iir_CLIENT_PE7 +  1 map_iir_CLIENT_PE13 +  1 map_iir_CLIENT_PE14 >= 0
constraint_24 :  -  1 C_idct_sink +  1 map_idct_CLIENT_PE0 +  1 map_idct_CLIENT_PE2 +  1 map_idct_CLIENT_PE3 +  1 map_idct_CLIENT_PE4 +  1 map_idct_CLIENT_PE6 +  1 map_idct_CLIENT_PE7 +  1 map_idct_CLIENT_PE13 +  1 map_idct_CLIENT_PE14 >= 0
constraint_25 :  +  1 sink_master +  1 sink_slave = 1
constraint_26 :  + 3 sink_master +  1 C_sink_src +  1 C_sink_iir +  1 C_sink_idct <= 3
constraint_27 :  + 0 sink_slave <= 0
constraint_28 :  -  1 sink_slave +  1 C_sink_src +  1 C_sink_iir +  1 C_sink_idct = 0
constraint_29 :  -  1 sink_master +  1 map_sink_CLIENT_PE0 +  1 map_sink_CLIENT_PE1 +  1 map_sink_CLIENT_PE2 +  1 map_sink_CLIENT_PE3 +  1 map_sink_CLIENT_PE4 +  1 map_sink_CLIENT_PE5 +  1 map_sink_CLIENT_PE6 +  1 map_sink_CLIENT_PE7 +  1 map_sink_CLIENT_PE8 +  1 map_sink_CLIENT_PE9 +  1 map_sink_CLIENT_PE10 +  1 map_sink_CLIENT_PE11 +  1 map_sink_CLIENT_PE12 +  1 map_sink_CLIENT_PE13 +  1 map_sink_CLIENT_PE14 +  1 map_sink_CLIENT_PE15 +  1 map_sink_CLIENT_PE16 = 0
constraint_30 :  -  1 C_sink_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_31 :  -  1 C_sink_iir +  1 map_iir_CLIENT_PE0 +  1 map_iir_CLIENT_PE2 +  1 map_iir_CLIENT_PE3 +  1 map_iir_CLIENT_PE4 +  1 map_iir_CLIENT_PE6 +  1 map_iir_CLIENT_PE7 +  1 map_iir_CLIENT_PE13 +  1 map_iir_CLIENT_PE14 >= 0
constraint_32 :  -  1 C_sink_idct +  1 map_idct_CLIENT_PE0 +  1 map_idct_CLIENT_PE2 +  1 map_idct_CLIENT_PE3 +  1 map_idct_CLIENT_PE4 +  1 map_idct_CLIENT_PE6 +  1 map_idct_CLIENT_PE7 +  1 map_idct_CLIENT_PE13 +  1 map_idct_CLIENT_PE14 >= 0
constraint_33 :  +  1 sl_0_a1_01 +  1 sl_1_a1_01 +  1 sl_2_a1_01 +  1 sl_3_a1_01 +  1 sl_4_a1_01 +  1 sl_5_a1_01 +  1 sl_6_a1_01 +  1 sl_7_a1_01 +  1 sl_8_a1_01 +  1 sl_9_a1_01 = 1
constraint_34 :  +  1 hop_1_a1_01 +  1 hop_2_a1_01 +  1 hop_3_a1_01 +  1 hop_4_a1_01 +  1 hop_5_a1_01 +  1 hop_6_a1_01 +  1 hop_7_a1_01 +  1 hop_8_a1_01 +  1 hop_9_a1_01 +  1 hop_10_a1_01 +  1 hop_11_a1_01 +  1 hop_12_a1_01 +  1 hop_13_a1_01 +  1 hop_14_a1_01 = 1
constraint_35 :  +  1 sl_0_a1_12 +  1 sl_1_a1_12 +  1 sl_2_a1_12 +  1 sl_3_a1_12 +  1 sl_4_a1_12 +  1 sl_5_a1_12 +  1 sl_6_a1_12 +  1 sl_7_a1_12 +  1 sl_8_a1_12 +  1 sl_9_a1_12 = 1
constraint_36 :  +  1 hop_1_a1_12 +  1 hop_2_a1_12 +  1 hop_3_a1_12 +  1 hop_4_a1_12 +  1 hop_5_a1_12 +  1 hop_6_a1_12 +  1 hop_7_a1_12 +  1 hop_8_a1_12 +  1 hop_9_a1_12 +  1 hop_10_a1_12 +  1 hop_11_a1_12 +  1 hop_12_a1_12 +  1 hop_13_a1_12 +  1 hop_14_a1_12 = 1
constraint_37 :  +  1 sl_0_a1_23 +  1 sl_1_a1_23 +  1 sl_2_a1_23 +  1 sl_3_a1_23 +  1 sl_4_a1_23 +  1 sl_5_a1_23 +  1 sl_6_a1_23 +  1 sl_7_a1_23 +  1 sl_8_a1_23 +  1 sl_9_a1_23 = 1
constraint_38 :  +  1 hop_1_a1_23 +  1 hop_2_a1_23 +  1 hop_3_a1_23 +  1 hop_4_a1_23 +  1 hop_5_a1_23 +  1 hop_6_a1_23 +  1 hop_7_a1_23 +  1 hop_8_a1_23 +  1 hop_9_a1_23 +  1 hop_10_a1_23 +  1 hop_11_a1_23 +  1 hop_12_a1_23 +  1 hop_13_a1_23 +  1 hop_14_a1_23 = 1

Binary

src_master
src_slave
C_src_iir
C_src_idct
C_src_sink
map_src_CLIENT_PE0
map_src_CLIENT_PE1
map_src_CLIENT_PE2
map_src_CLIENT_PE3
map_src_CLIENT_PE4
map_src_CLIENT_PE5
map_src_CLIENT_PE6
map_src_CLIENT_PE7
map_src_CLIENT_PE8
map_src_CLIENT_PE9
map_src_CLIENT_PE10
map_src_CLIENT_PE11
map_src_CLIENT_PE12
map_src_CLIENT_PE13
map_src_CLIENT_PE14
map_src_CLIENT_PE15
map_src_CLIENT_PE16
iir_master
iir_slave
C_iir_src
C_iir_idct
C_iir_sink
map_iir_CLIENT_PE0
map_iir_CLIENT_PE2
map_iir_CLIENT_PE3
map_iir_CLIENT_PE4
map_iir_CLIENT_PE6
map_iir_CLIENT_PE7
map_iir_CLIENT_PE13
map_iir_CLIENT_PE14
idct_master
idct_slave
C_idct_src
C_idct_iir
C_idct_sink
map_idct_CLIENT_PE0
map_idct_CLIENT_PE2
map_idct_CLIENT_PE3
map_idct_CLIENT_PE4
map_idct_CLIENT_PE6
map_idct_CLIENT_PE7
map_idct_CLIENT_PE13
map_idct_CLIENT_PE14
sink_master
sink_slave
C_sink_src
C_sink_iir
C_sink_idct
map_sink_CLIENT_PE0
map_sink_CLIENT_PE1
map_sink_CLIENT_PE2
map_sink_CLIENT_PE3
map_sink_CLIENT_PE4
map_sink_CLIENT_PE5
map_sink_CLIENT_PE6
map_sink_CLIENT_PE7
map_sink_CLIENT_PE8
map_sink_CLIENT_PE9
map_sink_CLIENT_PE10
map_sink_CLIENT_PE11
map_sink_CLIENT_PE12
map_sink_CLIENT_PE13
map_sink_CLIENT_PE14
map_sink_CLIENT_PE15
map_sink_CLIENT_PE16
sl_0_a1_01
sl_1_a1_01
sl_2_a1_01
sl_3_a1_01
sl_4_a1_01
sl_5_a1_01
sl_6_a1_01
sl_7_a1_01
sl_8_a1_01
sl_9_a1_01
hop_1_a1_01
hop_2_a1_01
hop_3_a1_01
hop_4_a1_01
hop_5_a1_01
hop_6_a1_01
hop_7_a1_01
hop_8_a1_01
hop_9_a1_01
hop_10_a1_01
hop_11_a1_01
hop_12_a1_01
hop_13_a1_01
hop_14_a1_01
sl_0_a1_12
sl_1_a1_12
sl_2_a1_12
sl_3_a1_12
sl_4_a1_12
sl_5_a1_12
sl_6_a1_12
sl_7_a1_12
sl_8_a1_12
sl_9_a1_12
hop_1_a1_12
hop_2_a1_12
hop_3_a1_12
hop_4_a1_12
hop_5_a1_12
hop_6_a1_12
hop_7_a1_12
hop_8_a1_12
hop_9_a1_12
hop_10_a1_12
hop_11_a1_12
hop_12_a1_12
hop_13_a1_12
hop_14_a1_12
sl_0_a1_23
sl_1_a1_23
sl_2_a1_23
sl_3_a1_23
sl_4_a1_23
sl_5_a1_23
sl_6_a1_23
sl_7_a1_23
sl_8_a1_23
sl_9_a1_23
hop_1_a1_23
hop_2_a1_23
hop_3_a1_23
hop_4_a1_23
hop_5_a1_23
hop_6_a1_23
hop_7_a1_23
hop_8_a1_23
hop_9_a1_23
hop_10_a1_23
hop_11_a1_23
hop_12_a1_23
hop_13_a1_23
hop_14_a1_23
End
