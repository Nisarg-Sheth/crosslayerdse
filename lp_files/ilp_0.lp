Maximize
problem: can1_master + fp_master + can2_master
Subject To
constraint_1 :  +  1 src_master +  1 src_slave = 1
constraint_2 :  + 0 src_master <= 0
constraint_3 :  + 5 src_slave +  1 C_can1_src +  1 C_fp_src +  1 C_can2_src +  1 C_pulse_src +  1 C_sink_src <= 5
constraint_4 :  -  1 src_slave = 0
constraint_5 :  -  1 src_master +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 = 0
constraint_6 :  -  1 src_master +  1 dvfs_0_src +  1 dvfs_1_src +  1 dvfs_2_src +  1 dvfs_3_src +  1 dvfs_4_src = 0
constraint_7 :  -  1 C_src_can1 +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_8 :  -  1 C_src_fp +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_9 :  -  1 C_src_can2 +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_10 :  -  1 C_src_pulse +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_11 :  -  1 C_src_sink +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_12 :  +  1 can1_master +  1 can1_slave = 1
constraint_13 :  + 1 can1_master +  1 C_can1_src <= 1
constraint_14 :  + 4 can1_slave +  1 C_fp_can1 +  1 C_can2_can1 +  1 C_pulse_can1 +  1 C_sink_can1 <= 4
constraint_15 :  -  1 can1_slave +  1 C_can1_src = 0
constraint_16 :  -  1 can1_master +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 = 0
constraint_17 :  -  1 can1_master +  1 dvfs_0_can1 +  1 dvfs_1_can1 +  1 dvfs_2_can1 +  1 dvfs_3_can1 +  1 dvfs_4_can1 = 0
constraint_18 :  -  1 C_can1_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_19 :  -  1 C_can1_fp +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_20 :  -  1 C_can1_can2 +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_21 :  -  1 C_can1_pulse +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_22 :  -  1 C_can1_sink +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_23 :  +  1 fp_master +  1 fp_slave = 1
constraint_24 :  + 2 fp_master +  1 C_fp_src +  1 C_fp_can1 <= 2
constraint_25 :  + 3 fp_slave +  1 C_can2_fp +  1 C_pulse_fp +  1 C_sink_fp <= 3
constraint_26 :  -  1 fp_slave +  1 C_fp_src +  1 C_fp_can1 = 0
constraint_27 :  -  1 fp_master +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 = 0
constraint_28 :  -  1 fp_master +  1 dvfs_0_fp +  1 dvfs_1_fp +  1 dvfs_2_fp +  1 dvfs_3_fp +  1 dvfs_4_fp = 0
constraint_29 :  -  1 C_fp_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_30 :  -  1 C_fp_can1 +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_31 :  -  1 C_fp_can2 +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 >= 0
constraint_32 :  -  1 C_fp_pulse +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 >= 0
constraint_33 :  -  1 C_fp_sink +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 >= 0
constraint_34 :  +  1 can2_master +  1 can2_slave = 1
constraint_35 :  + 3 can2_master +  1 C_can2_src +  1 C_can2_can1 +  1 C_can2_fp <= 3
constraint_36 :  + 2 can2_slave +  1 C_pulse_can2 +  1 C_sink_can2 <= 2
constraint_37 :  -  1 can2_slave +  1 C_can2_src +  1 C_can2_can1 +  1 C_can2_fp = 0
constraint_38 :  -  1 can2_master +  1 map_can2_CLIENT_PE0 +  1 map_can2_CLIENT_PE2 +  1 map_can2_CLIENT_PE3 +  1 map_can2_CLIENT_PE4 +  1 map_can2_CLIENT_PE6 +  1 map_can2_CLIENT_PE7 +  1 map_can2_CLIENT_PE13 +  1 map_can2_CLIENT_PE14 = 0
constraint_39 :  -  1 can2_master +  1 dvfs_0_can2 +  1 dvfs_1_can2 +  1 dvfs_2_can2 +  1 dvfs_3_can2 +  1 dvfs_4_can2 = 0
constraint_40 :  -  1 C_can2_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_41 :  -  1 C_can2_can1 +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_42 :  -  1 C_can2_fp +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 >= 0
constraint_43 :  -  1 C_can2_pulse +  1 map_can2_CLIENT_PE0 +  1 map_can2_CLIENT_PE2 +  1 map_can2_CLIENT_PE3 +  1 map_can2_CLIENT_PE4 +  1 map_can2_CLIENT_PE6 +  1 map_can2_CLIENT_PE7 +  1 map_can2_CLIENT_PE13 +  1 map_can2_CLIENT_PE14 >= 0
constraint_44 :  -  1 C_can2_sink +  1 map_can2_CLIENT_PE0 +  1 map_can2_CLIENT_PE2 +  1 map_can2_CLIENT_PE3 +  1 map_can2_CLIENT_PE4 +  1 map_can2_CLIENT_PE6 +  1 map_can2_CLIENT_PE7 +  1 map_can2_CLIENT_PE13 +  1 map_can2_CLIENT_PE14 >= 0
constraint_45 :  +  1 pulse_master +  1 pulse_slave = 1
constraint_46 :  + 4 pulse_master +  1 C_pulse_src +  1 C_pulse_can1 +  1 C_pulse_fp +  1 C_pulse_can2 <= 4
constraint_47 :  + 1 pulse_slave +  1 C_sink_pulse <= 1
constraint_48 :  -  1 pulse_slave +  1 C_pulse_src +  1 C_pulse_can1 +  1 C_pulse_fp +  1 C_pulse_can2 = 0
constraint_49 :  -  1 pulse_master +  1 map_pulse_CLIENT_PE0 +  1 map_pulse_CLIENT_PE2 +  1 map_pulse_CLIENT_PE3 +  1 map_pulse_CLIENT_PE4 +  1 map_pulse_CLIENT_PE6 +  1 map_pulse_CLIENT_PE7 +  1 map_pulse_CLIENT_PE13 +  1 map_pulse_CLIENT_PE14 = 0
constraint_50 :  -  1 pulse_master +  1 dvfs_0_pulse +  1 dvfs_1_pulse +  1 dvfs_2_pulse +  1 dvfs_3_pulse +  1 dvfs_4_pulse = 0
constraint_51 :  -  1 C_pulse_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_52 :  -  1 C_pulse_can1 +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_53 :  -  1 C_pulse_fp +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 >= 0
constraint_54 :  -  1 C_pulse_can2 +  1 map_can2_CLIENT_PE0 +  1 map_can2_CLIENT_PE2 +  1 map_can2_CLIENT_PE3 +  1 map_can2_CLIENT_PE4 +  1 map_can2_CLIENT_PE6 +  1 map_can2_CLIENT_PE7 +  1 map_can2_CLIENT_PE13 +  1 map_can2_CLIENT_PE14 >= 0
constraint_55 :  -  1 C_pulse_sink +  1 map_pulse_CLIENT_PE0 +  1 map_pulse_CLIENT_PE2 +  1 map_pulse_CLIENT_PE3 +  1 map_pulse_CLIENT_PE4 +  1 map_pulse_CLIENT_PE6 +  1 map_pulse_CLIENT_PE7 +  1 map_pulse_CLIENT_PE13 +  1 map_pulse_CLIENT_PE14 >= 0
constraint_56 :  +  1 sink_master +  1 sink_slave = 1
constraint_57 :  + 5 sink_master +  1 C_sink_src +  1 C_sink_can1 +  1 C_sink_fp +  1 C_sink_can2 +  1 C_sink_pulse <= 5
constraint_58 :  + 0 sink_slave <= 0
constraint_59 :  -  1 sink_slave +  1 C_sink_src +  1 C_sink_can1 +  1 C_sink_fp +  1 C_sink_can2 +  1 C_sink_pulse = 0
constraint_60 :  -  1 sink_master +  1 map_sink_CLIENT_PE0 +  1 map_sink_CLIENT_PE1 +  1 map_sink_CLIENT_PE2 +  1 map_sink_CLIENT_PE3 +  1 map_sink_CLIENT_PE4 +  1 map_sink_CLIENT_PE5 +  1 map_sink_CLIENT_PE6 +  1 map_sink_CLIENT_PE7 +  1 map_sink_CLIENT_PE8 +  1 map_sink_CLIENT_PE9 +  1 map_sink_CLIENT_PE10 +  1 map_sink_CLIENT_PE11 +  1 map_sink_CLIENT_PE12 +  1 map_sink_CLIENT_PE13 +  1 map_sink_CLIENT_PE14 +  1 map_sink_CLIENT_PE15 +  1 map_sink_CLIENT_PE16 = 0
constraint_61 :  -  1 sink_master +  1 dvfs_0_sink +  1 dvfs_1_sink +  1 dvfs_2_sink +  1 dvfs_3_sink +  1 dvfs_4_sink = 0
constraint_62 :  -  1 C_sink_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_63 :  -  1 C_sink_can1 +  1 map_can1_CLIENT_PE0 +  1 map_can1_CLIENT_PE2 +  1 map_can1_CLIENT_PE3 +  1 map_can1_CLIENT_PE4 +  1 map_can1_CLIENT_PE6 +  1 map_can1_CLIENT_PE7 +  1 map_can1_CLIENT_PE13 +  1 map_can1_CLIENT_PE14 >= 0
constraint_64 :  -  1 C_sink_fp +  1 map_fp_CLIENT_PE0 +  1 map_fp_CLIENT_PE2 +  1 map_fp_CLIENT_PE3 +  1 map_fp_CLIENT_PE4 +  1 map_fp_CLIENT_PE6 +  1 map_fp_CLIENT_PE7 +  1 map_fp_CLIENT_PE13 +  1 map_fp_CLIENT_PE14 >= 0
constraint_65 :  -  1 C_sink_can2 +  1 map_can2_CLIENT_PE0 +  1 map_can2_CLIENT_PE2 +  1 map_can2_CLIENT_PE3 +  1 map_can2_CLIENT_PE4 +  1 map_can2_CLIENT_PE6 +  1 map_can2_CLIENT_PE7 +  1 map_can2_CLIENT_PE13 +  1 map_can2_CLIENT_PE14 >= 0
constraint_66 :  -  1 C_sink_pulse +  1 map_pulse_CLIENT_PE0 +  1 map_pulse_CLIENT_PE2 +  1 map_pulse_CLIENT_PE3 +  1 map_pulse_CLIENT_PE4 +  1 map_pulse_CLIENT_PE6 +  1 map_pulse_CLIENT_PE7 +  1 map_pulse_CLIENT_PE13 +  1 map_pulse_CLIENT_PE14 >= 0
constraint_67 :  +  1 sl_0_a0_01 +  1 sl_1_a0_01 +  1 sl_2_a0_01 +  1 sl_3_a0_01 +  1 sl_4_a0_01 +  1 sl_5_a0_01 +  1 sl_6_a0_01 +  1 sl_7_a0_01 +  1 sl_8_a0_01 +  1 sl_9_a0_01 = 1
constraint_68 :  +  1 hop_1_a0_01 +  1 hop_2_a0_01 +  1 hop_3_a0_01 +  1 hop_4_a0_01 +  1 hop_5_a0_01 +  1 hop_6_a0_01 +  1 hop_7_a0_01 +  1 hop_8_a0_01 +  1 hop_9_a0_01 +  1 hop_10_a0_01 +  1 hop_11_a0_01 +  1 hop_12_a0_01 +  1 hop_13_a0_01 +  1 hop_14_a0_01 = 1
constraint_69 :  +  1 sl_0_a0_12 +  1 sl_1_a0_12 +  1 sl_2_a0_12 +  1 sl_3_a0_12 +  1 sl_4_a0_12 +  1 sl_5_a0_12 +  1 sl_6_a0_12 +  1 sl_7_a0_12 +  1 sl_8_a0_12 +  1 sl_9_a0_12 = 1
constraint_70 :  +  1 hop_1_a0_12 +  1 hop_2_a0_12 +  1 hop_3_a0_12 +  1 hop_4_a0_12 +  1 hop_5_a0_12 +  1 hop_6_a0_12 +  1 hop_7_a0_12 +  1 hop_8_a0_12 +  1 hop_9_a0_12 +  1 hop_10_a0_12 +  1 hop_11_a0_12 +  1 hop_12_a0_12 +  1 hop_13_a0_12 +  1 hop_14_a0_12 = 1
constraint_71 :  +  1 sl_0_a0_13 +  1 sl_1_a0_13 +  1 sl_2_a0_13 +  1 sl_3_a0_13 +  1 sl_4_a0_13 +  1 sl_5_a0_13 +  1 sl_6_a0_13 +  1 sl_7_a0_13 +  1 sl_8_a0_13 +  1 sl_9_a0_13 = 1
constraint_72 :  +  1 hop_1_a0_13 +  1 hop_2_a0_13 +  1 hop_3_a0_13 +  1 hop_4_a0_13 +  1 hop_5_a0_13 +  1 hop_6_a0_13 +  1 hop_7_a0_13 +  1 hop_8_a0_13 +  1 hop_9_a0_13 +  1 hop_10_a0_13 +  1 hop_11_a0_13 +  1 hop_12_a0_13 +  1 hop_13_a0_13 +  1 hop_14_a0_13 = 1
constraint_73 :  +  1 sl_0_a0_24 +  1 sl_1_a0_24 +  1 sl_2_a0_24 +  1 sl_3_a0_24 +  1 sl_4_a0_24 +  1 sl_5_a0_24 +  1 sl_6_a0_24 +  1 sl_7_a0_24 +  1 sl_8_a0_24 +  1 sl_9_a0_24 = 1
constraint_74 :  +  1 hop_1_a0_24 +  1 hop_2_a0_24 +  1 hop_3_a0_24 +  1 hop_4_a0_24 +  1 hop_5_a0_24 +  1 hop_6_a0_24 +  1 hop_7_a0_24 +  1 hop_8_a0_24 +  1 hop_9_a0_24 +  1 hop_10_a0_24 +  1 hop_11_a0_24 +  1 hop_12_a0_24 +  1 hop_13_a0_24 +  1 hop_14_a0_24 = 1
constraint_75 :  +  1 sl_0_a0_35 +  1 sl_1_a0_35 +  1 sl_2_a0_35 +  1 sl_3_a0_35 +  1 sl_4_a0_35 +  1 sl_5_a0_35 +  1 sl_6_a0_35 +  1 sl_7_a0_35 +  1 sl_8_a0_35 +  1 sl_9_a0_35 = 1
constraint_76 :  +  1 hop_1_a0_35 +  1 hop_2_a0_35 +  1 hop_3_a0_35 +  1 hop_4_a0_35 +  1 hop_5_a0_35 +  1 hop_6_a0_35 +  1 hop_7_a0_35 +  1 hop_8_a0_35 +  1 hop_9_a0_35 +  1 hop_10_a0_35 +  1 hop_11_a0_35 +  1 hop_12_a0_35 +  1 hop_13_a0_35 +  1 hop_14_a0_35 = 1

Binary

src_master
src_slave
C_src_can1
C_src_fp
C_src_can2
C_src_pulse
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
dvfs_0_src
dvfs_1_src
dvfs_2_src
dvfs_3_src
dvfs_4_src
can1_master
can1_slave
C_can1_src
C_can1_fp
C_can1_can2
C_can1_pulse
C_can1_sink
map_can1_CLIENT_PE0
map_can1_CLIENT_PE2
map_can1_CLIENT_PE3
map_can1_CLIENT_PE4
map_can1_CLIENT_PE6
map_can1_CLIENT_PE7
map_can1_CLIENT_PE13
map_can1_CLIENT_PE14
dvfs_0_can1
dvfs_1_can1
dvfs_2_can1
dvfs_3_can1
dvfs_4_can1
fp_master
fp_slave
C_fp_src
C_fp_can1
C_fp_can2
C_fp_pulse
C_fp_sink
map_fp_CLIENT_PE0
map_fp_CLIENT_PE2
map_fp_CLIENT_PE3
map_fp_CLIENT_PE4
map_fp_CLIENT_PE6
map_fp_CLIENT_PE7
map_fp_CLIENT_PE13
map_fp_CLIENT_PE14
dvfs_0_fp
dvfs_1_fp
dvfs_2_fp
dvfs_3_fp
dvfs_4_fp
can2_master
can2_slave
C_can2_src
C_can2_can1
C_can2_fp
C_can2_pulse
C_can2_sink
map_can2_CLIENT_PE0
map_can2_CLIENT_PE2
map_can2_CLIENT_PE3
map_can2_CLIENT_PE4
map_can2_CLIENT_PE6
map_can2_CLIENT_PE7
map_can2_CLIENT_PE13
map_can2_CLIENT_PE14
dvfs_0_can2
dvfs_1_can2
dvfs_2_can2
dvfs_3_can2
dvfs_4_can2
pulse_master
pulse_slave
C_pulse_src
C_pulse_can1
C_pulse_fp
C_pulse_can2
C_pulse_sink
map_pulse_CLIENT_PE0
map_pulse_CLIENT_PE2
map_pulse_CLIENT_PE3
map_pulse_CLIENT_PE4
map_pulse_CLIENT_PE6
map_pulse_CLIENT_PE7
map_pulse_CLIENT_PE13
map_pulse_CLIENT_PE14
dvfs_0_pulse
dvfs_1_pulse
dvfs_2_pulse
dvfs_3_pulse
dvfs_4_pulse
sink_master
sink_slave
C_sink_src
C_sink_can1
C_sink_fp
C_sink_can2
C_sink_pulse
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
dvfs_0_sink
dvfs_1_sink
dvfs_2_sink
dvfs_3_sink
dvfs_4_sink
sl_0_a0_01
sl_1_a0_01
sl_2_a0_01
sl_3_a0_01
sl_4_a0_01
sl_5_a0_01
sl_6_a0_01
sl_7_a0_01
sl_8_a0_01
sl_9_a0_01
hop_1_a0_01
hop_2_a0_01
hop_3_a0_01
hop_4_a0_01
hop_5_a0_01
hop_6_a0_01
hop_7_a0_01
hop_8_a0_01
hop_9_a0_01
hop_10_a0_01
hop_11_a0_01
hop_12_a0_01
hop_13_a0_01
hop_14_a0_01
sl_0_a0_12
sl_1_a0_12
sl_2_a0_12
sl_3_a0_12
sl_4_a0_12
sl_5_a0_12
sl_6_a0_12
sl_7_a0_12
sl_8_a0_12
sl_9_a0_12
hop_1_a0_12
hop_2_a0_12
hop_3_a0_12
hop_4_a0_12
hop_5_a0_12
hop_6_a0_12
hop_7_a0_12
hop_8_a0_12
hop_9_a0_12
hop_10_a0_12
hop_11_a0_12
hop_12_a0_12
hop_13_a0_12
hop_14_a0_12
sl_0_a0_13
sl_1_a0_13
sl_2_a0_13
sl_3_a0_13
sl_4_a0_13
sl_5_a0_13
sl_6_a0_13
sl_7_a0_13
sl_8_a0_13
sl_9_a0_13
hop_1_a0_13
hop_2_a0_13
hop_3_a0_13
hop_4_a0_13
hop_5_a0_13
hop_6_a0_13
hop_7_a0_13
hop_8_a0_13
hop_9_a0_13
hop_10_a0_13
hop_11_a0_13
hop_12_a0_13
hop_13_a0_13
hop_14_a0_13
sl_0_a0_24
sl_1_a0_24
sl_2_a0_24
sl_3_a0_24
sl_4_a0_24
sl_5_a0_24
sl_6_a0_24
sl_7_a0_24
sl_8_a0_24
sl_9_a0_24
hop_1_a0_24
hop_2_a0_24
hop_3_a0_24
hop_4_a0_24
hop_5_a0_24
hop_6_a0_24
hop_7_a0_24
hop_8_a0_24
hop_9_a0_24
hop_10_a0_24
hop_11_a0_24
hop_12_a0_24
hop_13_a0_24
hop_14_a0_24
sl_0_a0_35
sl_1_a0_35
sl_2_a0_35
sl_3_a0_35
sl_4_a0_35
sl_5_a0_35
sl_6_a0_35
sl_7_a0_35
sl_8_a0_35
sl_9_a0_35
hop_1_a0_35
hop_2_a0_35
hop_3_a0_35
hop_4_a0_35
hop_5_a0_35
hop_6_a0_35
hop_7_a0_35
hop_8_a0_35
hop_9_a0_35
hop_10_a0_35
hop_11_a0_35
hop_12_a0_35
hop_13_a0_35
hop_14_a0_35
End
