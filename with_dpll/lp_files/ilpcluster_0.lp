Maximize
problem: + 1 src_0 + 1 can1_1 + 1 fp_2 + 1 can2_2 + 1 pulse_0 + 1 sink_1 
Subject To
constraint_1 :   + 1 src_0  = 1
constraint_2 :   + 1 can1_0  + 1 can1_1  = 1
constraint_3 :   + 1 fp_0  + 1 fp_1  + 1 fp_2  = 1
constraint_4 :   + 1 can2_0  + 1 can2_1  + 1 can2_2  + 1 can2_3  = 1
constraint_5 :   + 1 pulse_0  + 1 pulse_1  + 1 pulse_2  + 1 pulse_3  + 1 pulse_4  = 1
constraint_6 :   + 1 sink_0  + 1 sink_1  + 1 sink_2  + 1 sink_3  + 1 sink_4  + 1 sink_5  = 1
constraint_7 : - 1 src_iscluster + 1 src_0 + 1 can1_0 + 1 fp_0 + 1 can2_0 + 1 pulse_0 + 1 sink_0  >= 0
constraint_8 : - 1 can1_iscluster + 1 can1_1 + 1 fp_1 + 1 can2_1 + 1 pulse_1 + 1 sink_1  >= 0
constraint_9 : - 1 fp_iscluster + 1 fp_2 + 1 can2_2 + 1 pulse_2 + 1 sink_2  >= 0
constraint_10 : - 1 can2_iscluster + 1 can2_3 + 1 pulse_3 + 1 sink_3  >= 0
constraint_11 : - 1 pulse_iscluster + 1 pulse_4 + 1 sink_4  >= 0
constraint_12 : - 1 sink_iscluster + 1 sink_5  >= 0

Binary

src_0
can1_0
can1_1
fp_0
fp_1
fp_2
can2_0
can2_1
can2_2
can2_3
pulse_0
pulse_1
pulse_2
pulse_3
pulse_4
sink_0
sink_1
sink_2
sink_3
sink_4
sink_5
src_iscluster
can1_iscluster
fp_iscluster
can2_iscluster
pulse_iscluster
sink_iscluster
