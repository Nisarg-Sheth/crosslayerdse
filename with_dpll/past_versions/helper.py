num_var=0
  for i in range(len(graph.tasks)):
      #f.write(master_list[i]+"\n")
      locals()[master_list[i]]=gb_model.addVar(vtype=GRB.BINARY, name=master_list[i])
      num_var+=1
      #f.write(slave_list[i]+"\n")
      locals()[slave_list[i]]=gb_model.addVar(vtype=GRB.BINARY, name=slave_list[i])
      num_var+=1
      for j in range(i):
          #f.write(c_list[(i*graph.num_of_tasks)+j]+"\n")
          locals()[c_list[(i*graph.num_of_tasks)+j]]=gb_model.addVar(vtype=GRB.BINARY, name=c_list[(i*graph.num_of_tasks)+j])
          num_var+=1
      for j in range((i+1),graph.num_of_tasks):
          #f.write(c_list[(i*graph.num_of_tasks)+j]+"\n")
          locals()[c_list[(i*graph.num_of_tasks)+j]]=gb_model.addVar(vtype=GRB.BINARY, name=c_list[(i*graph.num_of_tasks)+j])
          num_var+=1
      for j in map_list[i]:
          #f.write("map_t"+str(i)+j+"\n")
          locals()["map_t"+str(i)+j]=gb_model.addVar(vtype=GRB.BINARY, name=("map_t"+str(i)+j))
          num_var+=1

  for m in graph.arcs:
      for j in range(service_level):
          #f.write("sl_"+str(j)+m+"\n")
          locals()[("sl_"+str(j)+m)]=gb_model.addVar(vtype=GRB.BINARY, name=("sl_"+str(j)+m))
          num_var+=1
      for j in range(hop_level):
          #f.write("hop_"+str(j+1)+m+"\n")
          locals()[("hop_"+str(j+1)+m)]=gb_model.addVar(vtype=GRB.BINARY, name=("hop_"+str(j+1)+m))
          num_var+=1
  print("The number of variables: "+str(num_var))
