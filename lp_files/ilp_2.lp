Maximize
problem: fft_master + matrix_master + ifft_master
Subject To
constraint_1 :  +  1 src_master +  1 src_slave = 1
constraint_2 :  + 0 src_master <= 0
constraint_3 :  + 8 src_slave +  1 C_fft_src +  1 C_matrix_src +  1 C_ifft_src +  1 C_fir_src +  1 C_angle_src +  1 C_road_src +  1 C_table_src +  1 C_sink_src <= 8
constraint_4 :  -  1 src_slave = 0
constraint_5 :  -  1 src_master +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 = 0
constraint_6 :  -  1 src_master +  1 dvfs_0_src +  1 dvfs_1_src +  1 dvfs_2_src +  1 dvfs_3_src +  1 dvfs_4_src = 0
constraint_7 :  -  1 C_src_fft +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_8 :  -  1 C_src_matrix +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_9 :  -  1 C_src_ifft +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_10 :  -  1 C_src_fir +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_11 :  -  1 C_src_angle +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_12 :  -  1 C_src_road +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_13 :  -  1 C_src_table +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_14 :  -  1 C_src_sink +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_15 :  +  1 fft_master +  1 fft_slave = 1
constraint_16 :  + 1 fft_master +  1 C_fft_src <= 1
constraint_17 :  + 7 fft_slave +  1 C_matrix_fft +  1 C_ifft_fft +  1 C_fir_fft +  1 C_angle_fft +  1 C_road_fft +  1 C_table_fft +  1 C_sink_fft <= 7
constraint_18 :  -  1 fft_slave +  1 C_fft_src = 0
constraint_19 :  -  1 fft_master +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 = 0
constraint_20 :  -  1 fft_master +  1 dvfs_0_fft +  1 dvfs_1_fft +  1 dvfs_2_fft +  1 dvfs_3_fft +  1 dvfs_4_fft = 0
constraint_21 :  -  1 C_fft_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_22 :  -  1 C_fft_matrix +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_23 :  -  1 C_fft_ifft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_24 :  -  1 C_fft_fir +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_25 :  -  1 C_fft_angle +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_26 :  -  1 C_fft_road +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_27 :  -  1 C_fft_table +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_28 :  -  1 C_fft_sink +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_29 :  +  1 matrix_master +  1 matrix_slave = 1
constraint_30 :  + 2 matrix_master +  1 C_matrix_src +  1 C_matrix_fft <= 2
constraint_31 :  + 6 matrix_slave +  1 C_ifft_matrix +  1 C_fir_matrix +  1 C_angle_matrix +  1 C_road_matrix +  1 C_table_matrix +  1 C_sink_matrix <= 6
constraint_32 :  -  1 matrix_slave +  1 C_matrix_src +  1 C_matrix_fft = 0
constraint_33 :  -  1 matrix_master +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 = 0
constraint_34 :  -  1 matrix_master +  1 dvfs_0_matrix +  1 dvfs_1_matrix +  1 dvfs_2_matrix +  1 dvfs_3_matrix +  1 dvfs_4_matrix = 0
constraint_35 :  -  1 C_matrix_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_36 :  -  1 C_matrix_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_37 :  -  1 C_matrix_ifft +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_38 :  -  1 C_matrix_fir +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_39 :  -  1 C_matrix_angle +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_40 :  -  1 C_matrix_road +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_41 :  -  1 C_matrix_table +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_42 :  -  1 C_matrix_sink +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_43 :  +  1 ifft_master +  1 ifft_slave = 1
constraint_44 :  + 3 ifft_master +  1 C_ifft_src +  1 C_ifft_fft +  1 C_ifft_matrix <= 3
constraint_45 :  + 5 ifft_slave +  1 C_fir_ifft +  1 C_angle_ifft +  1 C_road_ifft +  1 C_table_ifft +  1 C_sink_ifft <= 5
constraint_46 :  -  1 ifft_slave +  1 C_ifft_src +  1 C_ifft_fft +  1 C_ifft_matrix = 0
constraint_47 :  -  1 ifft_master +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 = 0
constraint_48 :  -  1 ifft_master +  1 dvfs_0_ifft +  1 dvfs_1_ifft +  1 dvfs_2_ifft +  1 dvfs_3_ifft +  1 dvfs_4_ifft = 0
constraint_49 :  -  1 C_ifft_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_50 :  -  1 C_ifft_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_51 :  -  1 C_ifft_matrix +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_52 :  -  1 C_ifft_fir +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_53 :  -  1 C_ifft_angle +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_54 :  -  1 C_ifft_road +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_55 :  -  1 C_ifft_table +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_56 :  -  1 C_ifft_sink +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_57 :  +  1 fir_master +  1 fir_slave = 1
constraint_58 :  + 4 fir_master +  1 C_fir_src +  1 C_fir_fft +  1 C_fir_matrix +  1 C_fir_ifft <= 4
constraint_59 :  + 4 fir_slave +  1 C_angle_fir +  1 C_road_fir +  1 C_table_fir +  1 C_sink_fir <= 4
constraint_60 :  -  1 fir_slave +  1 C_fir_src +  1 C_fir_fft +  1 C_fir_matrix +  1 C_fir_ifft = 0
constraint_61 :  -  1 fir_master +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 = 0
constraint_62 :  -  1 fir_master +  1 dvfs_0_fir +  1 dvfs_1_fir +  1 dvfs_2_fir +  1 dvfs_3_fir +  1 dvfs_4_fir = 0
constraint_63 :  -  1 C_fir_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_64 :  -  1 C_fir_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_65 :  -  1 C_fir_matrix +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_66 :  -  1 C_fir_ifft +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_67 :  -  1 C_fir_angle +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_68 :  -  1 C_fir_road +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_69 :  -  1 C_fir_table +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_70 :  -  1 C_fir_sink +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_71 :  +  1 angle_master +  1 angle_slave = 1
constraint_72 :  + 5 angle_master +  1 C_angle_src +  1 C_angle_fft +  1 C_angle_matrix +  1 C_angle_ifft +  1 C_angle_fir <= 5
constraint_73 :  + 3 angle_slave +  1 C_road_angle +  1 C_table_angle +  1 C_sink_angle <= 3
constraint_74 :  -  1 angle_slave +  1 C_angle_src +  1 C_angle_fft +  1 C_angle_matrix +  1 C_angle_ifft +  1 C_angle_fir = 0
constraint_75 :  -  1 angle_master +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 = 0
constraint_76 :  -  1 angle_master +  1 dvfs_0_angle +  1 dvfs_1_angle +  1 dvfs_2_angle +  1 dvfs_3_angle +  1 dvfs_4_angle = 0
constraint_77 :  -  1 C_angle_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_78 :  -  1 C_angle_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_79 :  -  1 C_angle_matrix +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_80 :  -  1 C_angle_ifft +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_81 :  -  1 C_angle_fir +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_82 :  -  1 C_angle_road +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 >= 0
constraint_83 :  -  1 C_angle_table +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 >= 0
constraint_84 :  -  1 C_angle_sink +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 >= 0
constraint_85 :  +  1 road_master +  1 road_slave = 1
constraint_86 :  + 6 road_master +  1 C_road_src +  1 C_road_fft +  1 C_road_matrix +  1 C_road_ifft +  1 C_road_fir +  1 C_road_angle <= 6
constraint_87 :  + 2 road_slave +  1 C_table_road +  1 C_sink_road <= 2
constraint_88 :  -  1 road_slave +  1 C_road_src +  1 C_road_fft +  1 C_road_matrix +  1 C_road_ifft +  1 C_road_fir +  1 C_road_angle = 0
constraint_89 :  -  1 road_master +  1 map_road_CLIENT_PE0 +  1 map_road_CLIENT_PE2 +  1 map_road_CLIENT_PE3 +  1 map_road_CLIENT_PE4 +  1 map_road_CLIENT_PE6 +  1 map_road_CLIENT_PE7 +  1 map_road_CLIENT_PE13 +  1 map_road_CLIENT_PE14 = 0
constraint_90 :  -  1 road_master +  1 dvfs_0_road +  1 dvfs_1_road +  1 dvfs_2_road +  1 dvfs_3_road +  1 dvfs_4_road = 0
constraint_91 :  -  1 C_road_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_92 :  -  1 C_road_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_93 :  -  1 C_road_matrix +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_94 :  -  1 C_road_ifft +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_95 :  -  1 C_road_fir +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_96 :  -  1 C_road_angle +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 >= 0
constraint_97 :  -  1 C_road_table +  1 map_road_CLIENT_PE0 +  1 map_road_CLIENT_PE2 +  1 map_road_CLIENT_PE3 +  1 map_road_CLIENT_PE4 +  1 map_road_CLIENT_PE6 +  1 map_road_CLIENT_PE7 +  1 map_road_CLIENT_PE13 +  1 map_road_CLIENT_PE14 >= 0
constraint_98 :  -  1 C_road_sink +  1 map_road_CLIENT_PE0 +  1 map_road_CLIENT_PE2 +  1 map_road_CLIENT_PE3 +  1 map_road_CLIENT_PE4 +  1 map_road_CLIENT_PE6 +  1 map_road_CLIENT_PE7 +  1 map_road_CLIENT_PE13 +  1 map_road_CLIENT_PE14 >= 0
constraint_99 :  +  1 table_master +  1 table_slave = 1
constraint_100 :  + 7 table_master +  1 C_table_src +  1 C_table_fft +  1 C_table_matrix +  1 C_table_ifft +  1 C_table_fir +  1 C_table_angle +  1 C_table_road <= 7
constraint_101 :  + 1 table_slave +  1 C_sink_table <= 1
constraint_102 :  -  1 table_slave +  1 C_table_src +  1 C_table_fft +  1 C_table_matrix +  1 C_table_ifft +  1 C_table_fir +  1 C_table_angle +  1 C_table_road = 0
constraint_103 :  -  1 table_master +  1 map_table_CLIENT_PE0 +  1 map_table_CLIENT_PE2 +  1 map_table_CLIENT_PE3 +  1 map_table_CLIENT_PE4 +  1 map_table_CLIENT_PE6 +  1 map_table_CLIENT_PE7 +  1 map_table_CLIENT_PE13 +  1 map_table_CLIENT_PE14 = 0
constraint_104 :  -  1 table_master +  1 dvfs_0_table +  1 dvfs_1_table +  1 dvfs_2_table +  1 dvfs_3_table +  1 dvfs_4_table = 0
constraint_105 :  -  1 C_table_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 >= 0
constraint_106 :  -  1 C_table_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_107 :  -  1 C_table_matrix +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_108 :  -  1 C_table_ifft +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_109 :  -  1 C_table_fir +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_110 :  -  1 C_table_angle +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 >= 0
constraint_111 :  -  1 C_table_road +  1 map_road_CLIENT_PE0 +  1 map_road_CLIENT_PE2 +  1 map_road_CLIENT_PE3 +  1 map_road_CLIENT_PE4 +  1 map_road_CLIENT_PE6 +  1 map_road_CLIENT_PE7 +  1 map_road_CLIENT_PE13 +  1 map_road_CLIENT_PE14 >= 0
constraint_112 :  -  1 C_table_sink +  1 map_table_CLIENT_PE0 +  1 map_table_CLIENT_PE2 +  1 map_table_CLIENT_PE3 +  1 map_table_CLIENT_PE4 +  1 map_table_CLIENT_PE6 +  1 map_table_CLIENT_PE7 +  1 map_table_CLIENT_PE13 +  1 map_table_CLIENT_PE14 >= 0
constraint_113 :  +  1 sink_master +  1 sink_slave = 1
constraint_114 :  + 8 sink_master +  1 C_sink_src +  1 C_sink_fft +  1 C_sink_matrix +  1 C_sink_ifft +  1 C_sink_fir +  1 C_sink_angle +  1 C_sink_road +  1 C_sink_table <= 8
constraint_115 :  + 0 sink_slave <= 0
constraint_116 :  -  1 sink_slave +  1 C_sink_src +  1 C_sink_fft +  1 C_sink_matrix +  1 C_sink_ifft +  1 C_sink_fir +  1 C_sink_angle +  1 C_sink_road +  1 C_sink_table = 0
constraint_117 :  -  1 sink_master +  1 map_sink_CLIENT_PE0 +  1 map_sink_CLIENT_PE1 +  1 map_sink_CLIENT_PE2 +  1 map_sink_CLIENT_PE3 +  1 map_sink_CLIENT_PE4 +  1 map_sink_CLIENT_PE5 +  1 map_sink_CLIENT_PE6 +  1 map_sink_CLIENT_PE7 +  1 map_sink_CLIENT_PE8 +  1 map_sink_CLIENT_PE9 +  1 map_sink_CLIENT_PE10 +  1 map_sink_CLIENT_PE11 +  1 map_sink_CLIENT_PE12 +  1 map_sink_CLIENT_PE13 +  1 map_sink_CLIENT_PE14 +  1 map_sink_CLIENT_PE15 +  1 map_sink_CLIENT_PE16 = 0
constraint_118 :  -  1 sink_master +  1 dvfs_0_sink +  1 dvfs_1_sink +  1 dvfs_2_sink +  1 dvfs_3_sink +  1 dvfs_4_sink = 0
constraint_119 :  -  1 C_sink_src +  1 map_src_CLIENT_PE0 +  1 map_src_CLIENT_PE1 +  1 map_src_CLIENT_PE2 +  1 map_src_CLIENT_PE3 +  1 map_src_CLIENT_PE4 +  1 map_src_CLIENT_PE5 +  1 map_src_CLIENT_PE6 +  1 map_src_CLIENT_PE7 +  1 map_src_CLIENT_PE8 +  1 map_src_CLIENT_PE9 +  1 map_src_CLIENT_PE10 +  1 map_src_CLIENT_PE11 +  1 map_src_CLIENT_PE12 +  1 map_src_CLIENT_PE13 +  1 map_src_CLIENT_PE14 +  1 map_src_CLIENT_PE15 +  1 map_src_CLIENT_PE16 >= 0
constraint_120 :  -  1 C_sink_fft +  1 map_fft_CLIENT_PE0 +  1 map_fft_CLIENT_PE2 +  1 map_fft_CLIENT_PE3 +  1 map_fft_CLIENT_PE4 +  1 map_fft_CLIENT_PE6 +  1 map_fft_CLIENT_PE7 +  1 map_fft_CLIENT_PE13 +  1 map_fft_CLIENT_PE14 >= 0
constraint_121 :  -  1 C_sink_matrix +  1 map_matrix_CLIENT_PE0 +  1 map_matrix_CLIENT_PE2 +  1 map_matrix_CLIENT_PE3 +  1 map_matrix_CLIENT_PE4 +  1 map_matrix_CLIENT_PE6 +  1 map_matrix_CLIENT_PE7 +  1 map_matrix_CLIENT_PE13 +  1 map_matrix_CLIENT_PE14 >= 0
constraint_122 :  -  1 C_sink_ifft +  1 map_ifft_CLIENT_PE0 +  1 map_ifft_CLIENT_PE2 +  1 map_ifft_CLIENT_PE3 +  1 map_ifft_CLIENT_PE4 +  1 map_ifft_CLIENT_PE6 +  1 map_ifft_CLIENT_PE7 +  1 map_ifft_CLIENT_PE13 +  1 map_ifft_CLIENT_PE14 >= 0
constraint_123 :  -  1 C_sink_fir +  1 map_fir_CLIENT_PE0 +  1 map_fir_CLIENT_PE2 +  1 map_fir_CLIENT_PE3 +  1 map_fir_CLIENT_PE4 +  1 map_fir_CLIENT_PE6 +  1 map_fir_CLIENT_PE7 +  1 map_fir_CLIENT_PE13 +  1 map_fir_CLIENT_PE14 >= 0
constraint_124 :  -  1 C_sink_angle +  1 map_angle_CLIENT_PE0 +  1 map_angle_CLIENT_PE2 +  1 map_angle_CLIENT_PE3 +  1 map_angle_CLIENT_PE4 +  1 map_angle_CLIENT_PE6 +  1 map_angle_CLIENT_PE7 +  1 map_angle_CLIENT_PE13 +  1 map_angle_CLIENT_PE14 >= 0
constraint_125 :  -  1 C_sink_road +  1 map_road_CLIENT_PE0 +  1 map_road_CLIENT_PE2 +  1 map_road_CLIENT_PE3 +  1 map_road_CLIENT_PE4 +  1 map_road_CLIENT_PE6 +  1 map_road_CLIENT_PE7 +  1 map_road_CLIENT_PE13 +  1 map_road_CLIENT_PE14 >= 0
constraint_126 :  -  1 C_sink_table +  1 map_table_CLIENT_PE0 +  1 map_table_CLIENT_PE2 +  1 map_table_CLIENT_PE3 +  1 map_table_CLIENT_PE4 +  1 map_table_CLIENT_PE6 +  1 map_table_CLIENT_PE7 +  1 map_table_CLIENT_PE13 +  1 map_table_CLIENT_PE14 >= 0
constraint_127 :  +  1 sl_0_a2_01 +  1 sl_1_a2_01 +  1 sl_2_a2_01 +  1 sl_3_a2_01 +  1 sl_4_a2_01 +  1 sl_5_a2_01 +  1 sl_6_a2_01 +  1 sl_7_a2_01 +  1 sl_8_a2_01 +  1 sl_9_a2_01 = 1
constraint_128 :  +  1 hop_1_a2_01 +  1 hop_2_a2_01 +  1 hop_3_a2_01 +  1 hop_4_a2_01 +  1 hop_5_a2_01 +  1 hop_6_a2_01 +  1 hop_7_a2_01 +  1 hop_8_a2_01 +  1 hop_9_a2_01 +  1 hop_10_a2_01 +  1 hop_11_a2_01 +  1 hop_12_a2_01 +  1 hop_13_a2_01 +  1 hop_14_a2_01 = 1
constraint_129 :  +  1 sl_0_a2_12 +  1 sl_1_a2_12 +  1 sl_2_a2_12 +  1 sl_3_a2_12 +  1 sl_4_a2_12 +  1 sl_5_a2_12 +  1 sl_6_a2_12 +  1 sl_7_a2_12 +  1 sl_8_a2_12 +  1 sl_9_a2_12 = 1
constraint_130 :  +  1 hop_1_a2_12 +  1 hop_2_a2_12 +  1 hop_3_a2_12 +  1 hop_4_a2_12 +  1 hop_5_a2_12 +  1 hop_6_a2_12 +  1 hop_7_a2_12 +  1 hop_8_a2_12 +  1 hop_9_a2_12 +  1 hop_10_a2_12 +  1 hop_11_a2_12 +  1 hop_12_a2_12 +  1 hop_13_a2_12 +  1 hop_14_a2_12 = 1
constraint_131 :  +  1 sl_0_a2_23 +  1 sl_1_a2_23 +  1 sl_2_a2_23 +  1 sl_3_a2_23 +  1 sl_4_a2_23 +  1 sl_5_a2_23 +  1 sl_6_a2_23 +  1 sl_7_a2_23 +  1 sl_8_a2_23 +  1 sl_9_a2_23 = 1
constraint_132 :  +  1 hop_1_a2_23 +  1 hop_2_a2_23 +  1 hop_3_a2_23 +  1 hop_4_a2_23 +  1 hop_5_a2_23 +  1 hop_6_a2_23 +  1 hop_7_a2_23 +  1 hop_8_a2_23 +  1 hop_9_a2_23 +  1 hop_10_a2_23 +  1 hop_11_a2_23 +  1 hop_12_a2_23 +  1 hop_13_a2_23 +  1 hop_14_a2_23 = 1
constraint_133 :  +  1 sl_0_a2_34 +  1 sl_1_a2_34 +  1 sl_2_a2_34 +  1 sl_3_a2_34 +  1 sl_4_a2_34 +  1 sl_5_a2_34 +  1 sl_6_a2_34 +  1 sl_7_a2_34 +  1 sl_8_a2_34 +  1 sl_9_a2_34 = 1
constraint_134 :  +  1 hop_1_a2_34 +  1 hop_2_a2_34 +  1 hop_3_a2_34 +  1 hop_4_a2_34 +  1 hop_5_a2_34 +  1 hop_6_a2_34 +  1 hop_7_a2_34 +  1 hop_8_a2_34 +  1 hop_9_a2_34 +  1 hop_10_a2_34 +  1 hop_11_a2_34 +  1 hop_12_a2_34 +  1 hop_13_a2_34 +  1 hop_14_a2_34 = 1
constraint_135 :  +  1 sl_0_a2_45 +  1 sl_1_a2_45 +  1 sl_2_a2_45 +  1 sl_3_a2_45 +  1 sl_4_a2_45 +  1 sl_5_a2_45 +  1 sl_6_a2_45 +  1 sl_7_a2_45 +  1 sl_8_a2_45 +  1 sl_9_a2_45 = 1
constraint_136 :  +  1 hop_1_a2_45 +  1 hop_2_a2_45 +  1 hop_3_a2_45 +  1 hop_4_a2_45 +  1 hop_5_a2_45 +  1 hop_6_a2_45 +  1 hop_7_a2_45 +  1 hop_8_a2_45 +  1 hop_9_a2_45 +  1 hop_10_a2_45 +  1 hop_11_a2_45 +  1 hop_12_a2_45 +  1 hop_13_a2_45 +  1 hop_14_a2_45 = 1
constraint_137 :  +  1 sl_0_a2_56 +  1 sl_1_a2_56 +  1 sl_2_a2_56 +  1 sl_3_a2_56 +  1 sl_4_a2_56 +  1 sl_5_a2_56 +  1 sl_6_a2_56 +  1 sl_7_a2_56 +  1 sl_8_a2_56 +  1 sl_9_a2_56 = 1
constraint_138 :  +  1 hop_1_a2_56 +  1 hop_2_a2_56 +  1 hop_3_a2_56 +  1 hop_4_a2_56 +  1 hop_5_a2_56 +  1 hop_6_a2_56 +  1 hop_7_a2_56 +  1 hop_8_a2_56 +  1 hop_9_a2_56 +  1 hop_10_a2_56 +  1 hop_11_a2_56 +  1 hop_12_a2_56 +  1 hop_13_a2_56 +  1 hop_14_a2_56 = 1
constraint_139 :  +  1 sl_0_a2_67 +  1 sl_1_a2_67 +  1 sl_2_a2_67 +  1 sl_3_a2_67 +  1 sl_4_a2_67 +  1 sl_5_a2_67 +  1 sl_6_a2_67 +  1 sl_7_a2_67 +  1 sl_8_a2_67 +  1 sl_9_a2_67 = 1
constraint_140 :  +  1 hop_1_a2_67 +  1 hop_2_a2_67 +  1 hop_3_a2_67 +  1 hop_4_a2_67 +  1 hop_5_a2_67 +  1 hop_6_a2_67 +  1 hop_7_a2_67 +  1 hop_8_a2_67 +  1 hop_9_a2_67 +  1 hop_10_a2_67 +  1 hop_11_a2_67 +  1 hop_12_a2_67 +  1 hop_13_a2_67 +  1 hop_14_a2_67 = 1
constraint_141 :  +  1 sl_0_a2_78 +  1 sl_1_a2_78 +  1 sl_2_a2_78 +  1 sl_3_a2_78 +  1 sl_4_a2_78 +  1 sl_5_a2_78 +  1 sl_6_a2_78 +  1 sl_7_a2_78 +  1 sl_8_a2_78 +  1 sl_9_a2_78 = 1
constraint_142 :  +  1 hop_1_a2_78 +  1 hop_2_a2_78 +  1 hop_3_a2_78 +  1 hop_4_a2_78 +  1 hop_5_a2_78 +  1 hop_6_a2_78 +  1 hop_7_a2_78 +  1 hop_8_a2_78 +  1 hop_9_a2_78 +  1 hop_10_a2_78 +  1 hop_11_a2_78 +  1 hop_12_a2_78 +  1 hop_13_a2_78 +  1 hop_14_a2_78 = 1
constraint_143 :  +  1 sl_0_a2_89 +  1 sl_1_a2_89 +  1 sl_2_a2_89 +  1 sl_3_a2_89 +  1 sl_4_a2_89 +  1 sl_5_a2_89 +  1 sl_6_a2_89 +  1 sl_7_a2_89 +  1 sl_8_a2_89 +  1 sl_9_a2_89 = 1
constraint_144 :  +  1 hop_1_a2_89 +  1 hop_2_a2_89 +  1 hop_3_a2_89 +  1 hop_4_a2_89 +  1 hop_5_a2_89 +  1 hop_6_a2_89 +  1 hop_7_a2_89 +  1 hop_8_a2_89 +  1 hop_9_a2_89 +  1 hop_10_a2_89 +  1 hop_11_a2_89 +  1 hop_12_a2_89 +  1 hop_13_a2_89 +  1 hop_14_a2_89 = 1

Binary

src_master
src_slave
C_src_fft
C_src_matrix
C_src_ifft
C_src_fir
C_src_angle
C_src_road
C_src_table
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
fft_master
fft_slave
C_fft_src
C_fft_matrix
C_fft_ifft
C_fft_fir
C_fft_angle
C_fft_road
C_fft_table
C_fft_sink
map_fft_CLIENT_PE0
map_fft_CLIENT_PE2
map_fft_CLIENT_PE3
map_fft_CLIENT_PE4
map_fft_CLIENT_PE6
map_fft_CLIENT_PE7
map_fft_CLIENT_PE13
map_fft_CLIENT_PE14
dvfs_0_fft
dvfs_1_fft
dvfs_2_fft
dvfs_3_fft
dvfs_4_fft
matrix_master
matrix_slave
C_matrix_src
C_matrix_fft
C_matrix_ifft
C_matrix_fir
C_matrix_angle
C_matrix_road
C_matrix_table
C_matrix_sink
map_matrix_CLIENT_PE0
map_matrix_CLIENT_PE2
map_matrix_CLIENT_PE3
map_matrix_CLIENT_PE4
map_matrix_CLIENT_PE6
map_matrix_CLIENT_PE7
map_matrix_CLIENT_PE13
map_matrix_CLIENT_PE14
dvfs_0_matrix
dvfs_1_matrix
dvfs_2_matrix
dvfs_3_matrix
dvfs_4_matrix
ifft_master
ifft_slave
C_ifft_src
C_ifft_fft
C_ifft_matrix
C_ifft_fir
C_ifft_angle
C_ifft_road
C_ifft_table
C_ifft_sink
map_ifft_CLIENT_PE0
map_ifft_CLIENT_PE2
map_ifft_CLIENT_PE3
map_ifft_CLIENT_PE4
map_ifft_CLIENT_PE6
map_ifft_CLIENT_PE7
map_ifft_CLIENT_PE13
map_ifft_CLIENT_PE14
dvfs_0_ifft
dvfs_1_ifft
dvfs_2_ifft
dvfs_3_ifft
dvfs_4_ifft
fir_master
fir_slave
C_fir_src
C_fir_fft
C_fir_matrix
C_fir_ifft
C_fir_angle
C_fir_road
C_fir_table
C_fir_sink
map_fir_CLIENT_PE0
map_fir_CLIENT_PE2
map_fir_CLIENT_PE3
map_fir_CLIENT_PE4
map_fir_CLIENT_PE6
map_fir_CLIENT_PE7
map_fir_CLIENT_PE13
map_fir_CLIENT_PE14
dvfs_0_fir
dvfs_1_fir
dvfs_2_fir
dvfs_3_fir
dvfs_4_fir
angle_master
angle_slave
C_angle_src
C_angle_fft
C_angle_matrix
C_angle_ifft
C_angle_fir
C_angle_road
C_angle_table
C_angle_sink
map_angle_CLIENT_PE0
map_angle_CLIENT_PE2
map_angle_CLIENT_PE3
map_angle_CLIENT_PE4
map_angle_CLIENT_PE6
map_angle_CLIENT_PE7
map_angle_CLIENT_PE13
map_angle_CLIENT_PE14
dvfs_0_angle
dvfs_1_angle
dvfs_2_angle
dvfs_3_angle
dvfs_4_angle
road_master
road_slave
C_road_src
C_road_fft
C_road_matrix
C_road_ifft
C_road_fir
C_road_angle
C_road_table
C_road_sink
map_road_CLIENT_PE0
map_road_CLIENT_PE2
map_road_CLIENT_PE3
map_road_CLIENT_PE4
map_road_CLIENT_PE6
map_road_CLIENT_PE7
map_road_CLIENT_PE13
map_road_CLIENT_PE14
dvfs_0_road
dvfs_1_road
dvfs_2_road
dvfs_3_road
dvfs_4_road
table_master
table_slave
C_table_src
C_table_fft
C_table_matrix
C_table_ifft
C_table_fir
C_table_angle
C_table_road
C_table_sink
map_table_CLIENT_PE0
map_table_CLIENT_PE2
map_table_CLIENT_PE3
map_table_CLIENT_PE4
map_table_CLIENT_PE6
map_table_CLIENT_PE7
map_table_CLIENT_PE13
map_table_CLIENT_PE14
dvfs_0_table
dvfs_1_table
dvfs_2_table
dvfs_3_table
dvfs_4_table
sink_master
sink_slave
C_sink_src
C_sink_fft
C_sink_matrix
C_sink_ifft
C_sink_fir
C_sink_angle
C_sink_road
C_sink_table
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
sl_0_a2_01
sl_1_a2_01
sl_2_a2_01
sl_3_a2_01
sl_4_a2_01
sl_5_a2_01
sl_6_a2_01
sl_7_a2_01
sl_8_a2_01
sl_9_a2_01
hop_1_a2_01
hop_2_a2_01
hop_3_a2_01
hop_4_a2_01
hop_5_a2_01
hop_6_a2_01
hop_7_a2_01
hop_8_a2_01
hop_9_a2_01
hop_10_a2_01
hop_11_a2_01
hop_12_a2_01
hop_13_a2_01
hop_14_a2_01
sl_0_a2_12
sl_1_a2_12
sl_2_a2_12
sl_3_a2_12
sl_4_a2_12
sl_5_a2_12
sl_6_a2_12
sl_7_a2_12
sl_8_a2_12
sl_9_a2_12
hop_1_a2_12
hop_2_a2_12
hop_3_a2_12
hop_4_a2_12
hop_5_a2_12
hop_6_a2_12
hop_7_a2_12
hop_8_a2_12
hop_9_a2_12
hop_10_a2_12
hop_11_a2_12
hop_12_a2_12
hop_13_a2_12
hop_14_a2_12
sl_0_a2_23
sl_1_a2_23
sl_2_a2_23
sl_3_a2_23
sl_4_a2_23
sl_5_a2_23
sl_6_a2_23
sl_7_a2_23
sl_8_a2_23
sl_9_a2_23
hop_1_a2_23
hop_2_a2_23
hop_3_a2_23
hop_4_a2_23
hop_5_a2_23
hop_6_a2_23
hop_7_a2_23
hop_8_a2_23
hop_9_a2_23
hop_10_a2_23
hop_11_a2_23
hop_12_a2_23
hop_13_a2_23
hop_14_a2_23
sl_0_a2_34
sl_1_a2_34
sl_2_a2_34
sl_3_a2_34
sl_4_a2_34
sl_5_a2_34
sl_6_a2_34
sl_7_a2_34
sl_8_a2_34
sl_9_a2_34
hop_1_a2_34
hop_2_a2_34
hop_3_a2_34
hop_4_a2_34
hop_5_a2_34
hop_6_a2_34
hop_7_a2_34
hop_8_a2_34
hop_9_a2_34
hop_10_a2_34
hop_11_a2_34
hop_12_a2_34
hop_13_a2_34
hop_14_a2_34
sl_0_a2_45
sl_1_a2_45
sl_2_a2_45
sl_3_a2_45
sl_4_a2_45
sl_5_a2_45
sl_6_a2_45
sl_7_a2_45
sl_8_a2_45
sl_9_a2_45
hop_1_a2_45
hop_2_a2_45
hop_3_a2_45
hop_4_a2_45
hop_5_a2_45
hop_6_a2_45
hop_7_a2_45
hop_8_a2_45
hop_9_a2_45
hop_10_a2_45
hop_11_a2_45
hop_12_a2_45
hop_13_a2_45
hop_14_a2_45
sl_0_a2_56
sl_1_a2_56
sl_2_a2_56
sl_3_a2_56
sl_4_a2_56
sl_5_a2_56
sl_6_a2_56
sl_7_a2_56
sl_8_a2_56
sl_9_a2_56
hop_1_a2_56
hop_2_a2_56
hop_3_a2_56
hop_4_a2_56
hop_5_a2_56
hop_6_a2_56
hop_7_a2_56
hop_8_a2_56
hop_9_a2_56
hop_10_a2_56
hop_11_a2_56
hop_12_a2_56
hop_13_a2_56
hop_14_a2_56
sl_0_a2_67
sl_1_a2_67
sl_2_a2_67
sl_3_a2_67
sl_4_a2_67
sl_5_a2_67
sl_6_a2_67
sl_7_a2_67
sl_8_a2_67
sl_9_a2_67
hop_1_a2_67
hop_2_a2_67
hop_3_a2_67
hop_4_a2_67
hop_5_a2_67
hop_6_a2_67
hop_7_a2_67
hop_8_a2_67
hop_9_a2_67
hop_10_a2_67
hop_11_a2_67
hop_12_a2_67
hop_13_a2_67
hop_14_a2_67
sl_0_a2_78
sl_1_a2_78
sl_2_a2_78
sl_3_a2_78
sl_4_a2_78
sl_5_a2_78
sl_6_a2_78
sl_7_a2_78
sl_8_a2_78
sl_9_a2_78
hop_1_a2_78
hop_2_a2_78
hop_3_a2_78
hop_4_a2_78
hop_5_a2_78
hop_6_a2_78
hop_7_a2_78
hop_8_a2_78
hop_9_a2_78
hop_10_a2_78
hop_11_a2_78
hop_12_a2_78
hop_13_a2_78
hop_14_a2_78
sl_0_a2_89
sl_1_a2_89
sl_2_a2_89
sl_3_a2_89
sl_4_a2_89
sl_5_a2_89
sl_6_a2_89
sl_7_a2_89
sl_8_a2_89
sl_9_a2_89
hop_1_a2_89
hop_2_a2_89
hop_3_a2_89
hop_4_a2_89
hop_5_a2_89
hop_6_a2_89
hop_7_a2_89
hop_8_a2_89
hop_9_a2_89
hop_10_a2_89
hop_11_a2_89
hop_12_a2_89
hop_13_a2_89
hop_14_a2_89
End
