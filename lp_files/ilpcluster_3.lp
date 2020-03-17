Maximize
problem: + 1 src_0 + 1 ptr_0 + 1 cache_2 + 1 tooth_2 + 1 sink_1 
Subject To
constraint_1 :   + 1 src_0  = 1
constraint_2 :   + 1 ptr_0  + 1 ptr_1  = 1
constraint_3 :   + 1 cache_0  + 1 cache_1  + 1 cache_2  = 1
constraint_4 :   + 1 tooth_0  + 1 tooth_1  + 1 tooth_2  + 1 tooth_3  = 1
constraint_5 :   + 1 sink_0  + 1 sink_1  + 1 sink_2  + 1 sink_3  + 1 sink_4  = 1
constraint_6 : - 1 src_iscluster + 1 src_0 + 1 ptr_0 + 1 cache_0 + 1 tooth_0 + 1 sink_0  >= 0
constraint_7 : - 1 ptr_iscluster + 1 ptr_1 + 1 cache_1 + 1 tooth_1 + 1 sink_1  >= 0
constraint_8 : - 1 cache_iscluster + 1 cache_2 + 1 tooth_2 + 1 sink_2  >= 0
constraint_9 : - 1 tooth_iscluster + 1 tooth_3 + 1 sink_3  >= 0
constraint_10 : - 1 sink_iscluster + 1 sink_4  >= 0

Binary

src_0
ptr_0
ptr_1
cache_0
cache_1
cache_2
tooth_0
tooth_1
tooth_2
tooth_3
sink_0
sink_1
sink_2
sink_3
sink_4
src_iscluster
ptr_iscluster
cache_iscluster
tooth_iscluster
sink_iscluster
