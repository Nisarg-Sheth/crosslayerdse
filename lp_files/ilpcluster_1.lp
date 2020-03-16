Maximize
problem: src_iscluster
Subject To
constraint_1 :   + 1 src_0  = 1
constraint_2 :   + 1 iir_0  + 1 iir_1  = 1
constraint_3 :   + 1 idct_0  + 1 idct_1  + 1 idct_2  = 1
constraint_4 :   + 1 sink_0  + 1 sink_1  + 1 sink_2  + 1 sink_3  = 1
constraint_5 : - 1 src_iscluster + 1 src_0 + 1 iir_0 + 1 idct_0 + 1 sink_0  >= 0
constraint_6 : - 1 iir_iscluster + 1 iir_1 + 1 idct_1 + 1 sink_1  >= 0
constraint_7 : - 1 idct_iscluster + 1 idct_2 + 1 sink_2  >= 0
constraint_8 : - 1 sink_iscluster + 1 sink_3  >= 0

Binary

src_0
iir_0
iir_1
idct_0
idct_1
idct_2
sink_0
sink_1
sink_2
sink_3
src_iscluster
iir_iscluster
idct_iscluster
sink_iscluster
