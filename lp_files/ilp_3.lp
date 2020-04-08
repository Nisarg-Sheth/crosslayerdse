Maximize
problem: ptr_master + cache_master + tooth_master
Subject To
constraint_1 :  +  1 src_master +  1 src_slave = 1
constraint_2 :  + 0 src_master <= 0
constraint_3 :  + 4 src_slave +  1 C_ptr_src +  1 C_cache_src +  1 C_tooth_src +  1 C_sink_src <= 4
constraint_4 :  -  1 src_slave = 0
constraint_5 :  -  1 src_master +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 = 0
constraint_6 :  -  1 src_master +  1 dvfs_0_src +  1 dvfs_1_src +  1 dvfs_2_src +  1 dvfs_3_src +  1 dvfs_4_src = 0
constraint_7 :  -  1 C_src_ptr +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_8 :  -  1 C_src_cache +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_9 :  -  1 C_src_tooth +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_10 :  -  1 C_src_sink +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_11 :  +  1 ptr_master +  1 ptr_slave = 1
constraint_12 :  + 1 ptr_master +  1 C_ptr_src <= 1
constraint_13 :  + 3 ptr_slave +  1 C_cache_ptr +  1 C_tooth_ptr +  1 C_sink_ptr <= 3
constraint_14 :  -  1 ptr_slave +  1 C_ptr_src = 0
constraint_15 :  -  1 ptr_master +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 = 0
constraint_16 :  -  1 ptr_master +  1 dvfs_0_ptr +  1 dvfs_1_ptr +  1 dvfs_2_ptr +  1 dvfs_3_ptr +  1 dvfs_4_ptr = 0
constraint_17 :  -  1 C_ptr_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_18 :  -  1 C_ptr_cache +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 >= 0
constraint_19 :  -  1 C_ptr_tooth +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 >= 0
constraint_20 :  -  1 C_ptr_sink +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 >= 0
constraint_21 :  +  1 cache_master +  1 cache_slave = 1
constraint_22 :  + 2 cache_master +  1 C_cache_src +  1 C_cache_ptr <= 2
constraint_23 :  + 2 cache_slave +  1 C_tooth_cache +  1 C_sink_cache <= 2
constraint_24 :  -  1 cache_slave +  1 C_cache_src +  1 C_cache_ptr = 0
constraint_25 :  -  1 cache_master +  1 map_cache_CLIENT_PE0 +  1 map_cache_CLIENT_PE2 +  1 map_cache_CLIENT_PE3 +  1 map_cache_CLIENT_PE4 +  1 map_cache_CLIENT_PE6 +  1 map_cache_CLIENT_PE7 +  1 map_cache_CLIENT_PE13 +  1 map_cache_CLIENT_PE14 = 0
constraint_26 :  -  1 cache_master +  1 dvfs_0_cache +  1 dvfs_1_cache +  1 dvfs_2_cache +  1 dvfs_3_cache +  1 dvfs_4_cache = 0
constraint_27 :  -  1 C_cache_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_28 :  -  1 C_cache_ptr +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 >= 0
constraint_29 :  -  1 C_cache_tooth +  1 map_cache_CLIENT_PE0 +  1 map_cache_CLIENT_PE2 +  1 map_cache_CLIENT_PE3 +  1 map_cache_CLIENT_PE4 +  1 map_cache_CLIENT_PE6 +  1 map_cache_CLIENT_PE7 +  1 map_cache_CLIENT_PE13 +  1 map_cache_CLIENT_PE14 >= 0
constraint_30 :  -  1 C_cache_sink +  1 map_cache_CLIENT_PE0 +  1 map_cache_CLIENT_PE2 +  1 map_cache_CLIENT_PE3 +  1 map_cache_CLIENT_PE4 +  1 map_cache_CLIENT_PE6 +  1 map_cache_CLIENT_PE7 +  1 map_cache_CLIENT_PE13 +  1 map_cache_CLIENT_PE14 >= 0
constraint_31 :  +  1 tooth_master +  1 tooth_slave = 1
constraint_32 :  + 3 tooth_master +  1 C_tooth_src +  1 C_tooth_ptr +  1 C_tooth_cache <= 3
constraint_33 :  + 1 tooth_slave +  1 C_sink_tooth <= 1
constraint_34 :  -  1 tooth_slave +  1 C_tooth_src +  1 C_tooth_ptr +  1 C_tooth_cache = 0
constraint_35 :  -  1 tooth_master +  1 map_tooth_CLIENT_PE0 +  1 map_tooth_CLIENT_PE2 +  1 map_tooth_CLIENT_PE3 +  1 map_tooth_CLIENT_PE4 +  1 map_tooth_CLIENT_PE6 +  1 map_tooth_CLIENT_PE7 +  1 map_tooth_CLIENT_PE13 +  1 map_tooth_CLIENT_PE14 = 0
constraint_36 :  -  1 tooth_master +  1 dvfs_0_tooth +  1 dvfs_1_tooth +  1 dvfs_2_tooth +  1 dvfs_3_tooth +  1 dvfs_4_tooth = 0
constraint_37 :  -  1 C_tooth_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_38 :  -  1 C_tooth_ptr +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 >= 0
constraint_39 :  -  1 C_tooth_cache +  1 map_cache_CLIENT_PE0 +  1 map_cache_CLIENT_PE2 +  1 map_cache_CLIENT_PE3 +  1 map_cache_CLIENT_PE4 +  1 map_cache_CLIENT_PE6 +  1 map_cache_CLIENT_PE7 +  1 map_cache_CLIENT_PE13 +  1 map_cache_CLIENT_PE14 >= 0
constraint_40 :  -  1 C_tooth_sink +  1 map_tooth_CLIENT_PE0 +  1 map_tooth_CLIENT_PE2 +  1 map_tooth_CLIENT_PE3 +  1 map_tooth_CLIENT_PE4 +  1 map_tooth_CLIENT_PE6 +  1 map_tooth_CLIENT_PE7 +  1 map_tooth_CLIENT_PE13 +  1 map_tooth_CLIENT_PE14 >= 0
constraint_41 :  +  1 sink_master +  1 sink_slave = 1
constraint_42 :  + 4 sink_master +  1 C_sink_src +  1 C_sink_ptr +  1 C_sink_cache +  1 C_sink_tooth <= 4
constraint_43 :  + 0 sink_slave <= 0
constraint_44 :  -  1 sink_slave +  1 C_sink_src +  1 C_sink_ptr +  1 C_sink_cache +  1 C_sink_tooth = 0
constraint_45 :  -  1 sink_master +  1 map_sink_CLIENT_PE0 +  1 map_sink_CLIENT_PE1 +  1 map_sink_CLIENT_PE2 +  1 map_sink_CLIENT_PE3 +  1 map_sink_CLIENT_PE4 +  1 map_sink_CLIENT_PE5 +  1 map_sink_CLIENT_PE6 +  1 map_sink_CLIENT_PE7 +  1 map_sink_CLIENT_PE8 +  1 map_sink_CLIENT_PE9 +  1 map_sink_CLIENT_PE10 +  1 map_sink_CLIENT_PE11 +  1 map_sink_CLIENT_PE12 +  1 map_sink_CLIENT_PE13 +  1 map_sink_CLIENT_PE14 +  1 map_sink_CLIENT_PE15 +  1 map_sink_CLIENT_PE16 = 0
constraint_46 :  -  1 sink_master +  1 dvfs_0_sink +  1 dvfs_1_sink +  1 dvfs_2_sink +  1 dvfs_3_sink +  1 dvfs_4_sink = 0
constraint_47 :  -  1 C_sink_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_48 :  -  1 C_sink_ptr +  1 map_ptr_CLIENT_PE0 +  1 map_ptr_CLIENT_PE2 +  1 map_ptr_CLIENT_PE3 +  1 map_ptr_CLIENT_PE4 +  1 map_ptr_CLIENT_PE6 +  1 map_ptr_CLIENT_PE7 +  1 map_ptr_CLIENT_PE13 +  1 map_ptr_CLIENT_PE14 >= 0
constraint_49 :  -  1 C_sink_cache +  1 map_cache_CLIENT_PE0 +  1 map_cache_CLIENT_PE2 +  1 map_cache_CLIENT_PE3 +  1 map_cache_CLIENT_PE4 +  1 map_cache_CLIENT_PE6 +  1 map_cache_CLIENT_PE7 +  1 map_cache_CLIENT_PE13 +  1 map_cache_CLIENT_PE14 >= 0
constraint_50 :  -  1 C_sink_tooth +  1 map_tooth_CLIENT_PE0 +  1 map_tooth_CLIENT_PE2 +  1 map_tooth_CLIENT_PE3 +  1 map_tooth_CLIENT_PE4 +  1 map_tooth_CLIENT_PE6 +  1 map_tooth_CLIENT_PE7 +  1 map_tooth_CLIENT_PE13 +  1 map_tooth_CLIENT_PE14 >= 0
constraint_51 :  +  1 sl_0_a3_01 +  1 sl_1_a3_01 +  1 sl_2_a3_01 +  1 sl_3_a3_01 +  1 sl_4_a3_01 +  1 sl_5_a3_01 +  1 sl_6_a3_01 +  1 sl_7_a3_01 +  1 sl_8_a3_01 +  1 sl_9_a3_01 = 1
constraint_52 :  +  1 hop_1_a3_01 +  1 hop_2_a3_01 +  1 hop_3_a3_01 +  1 hop_4_a3_01 +  1 hop_5_a3_01 +  1 hop_6_a3_01 +  1 hop_7_a3_01 +  1 hop_8_a3_01 +  1 hop_9_a3_01 +  1 hop_10_a3_01 +  1 hop_11_a3_01 +  1 hop_12_a3_01 +  1 hop_13_a3_01 +  1 hop_14_a3_01 = 1
constraint_53 :  +  1 sl_0_a3_12 +  1 sl_1_a3_12 +  1 sl_2_a3_12 +  1 sl_3_a3_12 +  1 sl_4_a3_12 +  1 sl_5_a3_12 +  1 sl_6_a3_12 +  1 sl_7_a3_12 +  1 sl_8_a3_12 +  1 sl_9_a3_12 = 1
constraint_54 :  +  1 hop_1_a3_12 +  1 hop_2_a3_12 +  1 hop_3_a3_12 +  1 hop_4_a3_12 +  1 hop_5_a3_12 +  1 hop_6_a3_12 +  1 hop_7_a3_12 +  1 hop_8_a3_12 +  1 hop_9_a3_12 +  1 hop_10_a3_12 +  1 hop_11_a3_12 +  1 hop_12_a3_12 +  1 hop_13_a3_12 +  1 hop_14_a3_12 = 1
constraint_55 :  +  1 sl_0_a3_23 +  1 sl_1_a3_23 +  1 sl_2_a3_23 +  1 sl_3_a3_23 +  1 sl_4_a3_23 +  1 sl_5_a3_23 +  1 sl_6_a3_23 +  1 sl_7_a3_23 +  1 sl_8_a3_23 +  1 sl_9_a3_23 = 1
constraint_56 :  +  1 hop_1_a3_23 +  1 hop_2_a3_23 +  1 hop_3_a3_23 +  1 hop_4_a3_23 +  1 hop_5_a3_23 +  1 hop_6_a3_23 +  1 hop_7_a3_23 +  1 hop_8_a3_23 +  1 hop_9_a3_23 +  1 hop_10_a3_23 +  1 hop_11_a3_23 +  1 hop_12_a3_23 +  1 hop_13_a3_23 +  1 hop_14_a3_23 = 1
constraint_57 :  +  1 sl_0_a3_34 +  1 sl_1_a3_34 +  1 sl_2_a3_34 +  1 sl_3_a3_34 +  1 sl_4_a3_34 +  1 sl_5_a3_34 +  1 sl_6_a3_34 +  1 sl_7_a3_34 +  1 sl_8_a3_34 +  1 sl_9_a3_34 = 1
constraint_58 :  +  1 hop_1_a3_34 +  1 hop_2_a3_34 +  1 hop_3_a3_34 +  1 hop_4_a3_34 +  1 hop_5_a3_34 +  1 hop_6_a3_34 +  1 hop_7_a3_34 +  1 hop_8_a3_34 +  1 hop_9_a3_34 +  1 hop_10_a3_34 +  1 hop_11_a3_34 +  1 hop_12_a3_34 +  1 hop_13_a3_34 +  1 hop_14_a3_34 = 1

Binary

src_master
src_slave
C_src_ptr
C_src_cache
C_src_tooth
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
ptr_master
ptr_slave
C_ptr_src
C_ptr_cache
C_ptr_tooth
C_ptr_sink
map_ptr_CLIENT_PE0
map_ptr_CLIENT_PE2
map_ptr_CLIENT_PE3
map_ptr_CLIENT_PE4
map_ptr_CLIENT_PE6
map_ptr_CLIENT_PE7
map_ptr_CLIENT_PE13
map_ptr_CLIENT_PE14
dvfs_0_ptr
dvfs_1_ptr
dvfs_2_ptr
dvfs_3_ptr
dvfs_4_ptr
cache_master
cache_slave
C_cache_src
C_cache_ptr
C_cache_tooth
C_cache_sink
map_cache_CLIENT_PE0
map_cache_CLIENT_PE2
map_cache_CLIENT_PE3
map_cache_CLIENT_PE4
map_cache_CLIENT_PE6
map_cache_CLIENT_PE7
map_cache_CLIENT_PE13
map_cache_CLIENT_PE14
dvfs_0_cache
dvfs_1_cache
dvfs_2_cache
dvfs_3_cache
dvfs_4_cache
tooth_master
tooth_slave
C_tooth_src
C_tooth_ptr
C_tooth_cache
C_tooth_sink
map_tooth_CLIENT_PE0
map_tooth_CLIENT_PE2
map_tooth_CLIENT_PE3
map_tooth_CLIENT_PE4
map_tooth_CLIENT_PE6
map_tooth_CLIENT_PE7
map_tooth_CLIENT_PE13
map_tooth_CLIENT_PE14
dvfs_0_tooth
dvfs_1_tooth
dvfs_2_tooth
dvfs_3_tooth
dvfs_4_tooth
sink_master
sink_slave
C_sink_src
C_sink_ptr
C_sink_cache
C_sink_tooth
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
sl_0_a3_01
sl_1_a3_01
sl_2_a3_01
sl_3_a3_01
sl_4_a3_01
sl_5_a3_01
sl_6_a3_01
sl_7_a3_01
sl_8_a3_01
sl_9_a3_01
hop_1_a3_01
hop_2_a3_01
hop_3_a3_01
hop_4_a3_01
hop_5_a3_01
hop_6_a3_01
hop_7_a3_01
hop_8_a3_01
hop_9_a3_01
hop_10_a3_01
hop_11_a3_01
hop_12_a3_01
hop_13_a3_01
hop_14_a3_01
sl_0_a3_12
sl_1_a3_12
sl_2_a3_12
sl_3_a3_12
sl_4_a3_12
sl_5_a3_12
sl_6_a3_12
sl_7_a3_12
sl_8_a3_12
sl_9_a3_12
hop_1_a3_12
hop_2_a3_12
hop_3_a3_12
hop_4_a3_12
hop_5_a3_12
hop_6_a3_12
hop_7_a3_12
hop_8_a3_12
hop_9_a3_12
hop_10_a3_12
hop_11_a3_12
hop_12_a3_12
hop_13_a3_12
hop_14_a3_12
sl_0_a3_23
sl_1_a3_23
sl_2_a3_23
sl_3_a3_23
sl_4_a3_23
sl_5_a3_23
sl_6_a3_23
sl_7_a3_23
sl_8_a3_23
sl_9_a3_23
hop_1_a3_23
hop_2_a3_23
hop_3_a3_23
hop_4_a3_23
hop_5_a3_23
hop_6_a3_23
hop_7_a3_23
hop_8_a3_23
hop_9_a3_23
hop_10_a3_23
hop_11_a3_23
hop_12_a3_23
hop_13_a3_23
hop_14_a3_23
sl_0_a3_34
sl_1_a3_34
sl_2_a3_34
sl_3_a3_34
sl_4_a3_34
sl_5_a3_34
sl_6_a3_34
sl_7_a3_34
sl_8_a3_34
sl_9_a3_34
hop_1_a3_34
hop_2_a3_34
hop_3_a3_34
hop_4_a3_34
hop_5_a3_34
hop_6_a3_34
hop_7_a3_34
hop_8_a3_34
hop_9_a3_34
hop_10_a3_34
hop_11_a3_34
hop_12_a3_34
hop_13_a3_34
hop_14_a3_34
End
