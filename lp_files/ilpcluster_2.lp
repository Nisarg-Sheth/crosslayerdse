Maximize
problem: + 1 src_0 + 1 fft_1 + 1 matrix_0 + 1 ifft_0 + 1 fir_2 + 1 angle_4 + 1 road_1 + 1 table_2 + 1 sink_5 
Subject To
constraint_1 :   + 1 src_0  = 1
constraint_2 :   + 1 fft_0  + 1 fft_1  = 1
constraint_3 :   + 1 matrix_0  + 1 matrix_1  + 1 matrix_2  = 1
constraint_4 :   + 1 ifft_0  + 1 ifft_1  + 1 ifft_2  + 1 ifft_3  = 1
constraint_5 :   + 1 fir_0  + 1 fir_1  + 1 fir_2  + 1 fir_3  + 1 fir_4  = 1
constraint_6 :   + 1 angle_0  + 1 angle_1  + 1 angle_2  + 1 angle_3  + 1 angle_4  + 1 angle_5  = 1
constraint_7 :   + 1 road_0  + 1 road_1  + 1 road_2  + 1 road_3  + 1 road_4  + 1 road_5  + 1 road_6  = 1
constraint_8 :   + 1 table_0  + 1 table_1  + 1 table_2  + 1 table_3  + 1 table_4  + 1 table_5  + 1 table_6  + 1 table_7  = 1
constraint_9 :   + 1 sink_0  + 1 sink_1  + 1 sink_2  + 1 sink_3  + 1 sink_4  + 1 sink_5  + 1 sink_6  + 1 sink_7  + 1 sink_8  = 1
constraint_10 : - 1 src_iscluster + 1 src_0 + 1 fft_0 + 1 matrix_0 + 1 ifft_0 + 1 fir_0 + 1 angle_0 + 1 road_0 + 1 table_0 + 1 sink_0  >= 0
constraint_11 : - 1 fft_iscluster + 1 fft_1 + 1 matrix_1 + 1 ifft_1 + 1 fir_1 + 1 angle_1 + 1 road_1 + 1 table_1 + 1 sink_1  >= 0
constraint_12 : - 1 matrix_iscluster + 1 matrix_2 + 1 ifft_2 + 1 fir_2 + 1 angle_2 + 1 road_2 + 1 table_2 + 1 sink_2  >= 0
constraint_13 : - 1 ifft_iscluster + 1 ifft_3 + 1 fir_3 + 1 angle_3 + 1 road_3 + 1 table_3 + 1 sink_3  >= 0
constraint_14 : - 1 fir_iscluster + 1 fir_4 + 1 angle_4 + 1 road_4 + 1 table_4 + 1 sink_4  >= 0
constraint_15 : - 1 angle_iscluster + 1 angle_5 + 1 road_5 + 1 table_5 + 1 sink_5  >= 0
constraint_16 : - 1 road_iscluster + 1 road_6 + 1 table_6 + 1 sink_6  >= 0
constraint_17 : - 1 table_iscluster + 1 table_7 + 1 sink_7  >= 0
constraint_18 : - 1 sink_iscluster + 1 sink_8  >= 0

Binary

src_0
fft_0
fft_1
matrix_0
matrix_1
matrix_2
ifft_0
ifft_1
ifft_2
ifft_3
fir_0
fir_1
fir_2
fir_3
fir_4
angle_0
angle_1
angle_2
angle_3
angle_4
angle_5
road_0
road_1
road_2
road_3
road_4
road_5
road_6
table_0
table_1
table_2
table_3
table_4
table_5
table_6
table_7
sink_0
sink_1
sink_2
sink_3
sink_4
sink_5
sink_6
sink_7
sink_8
src_iscluster
fft_iscluster
matrix_iscluster
ifft_iscluster
fir_iscluster
angle_iscluster
road_iscluster
table_iscluster
sink_iscluster
