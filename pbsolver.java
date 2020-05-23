import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;
import java.io.BufferedReader;
import java.util.*;

import org.opt4j.core.problem.Creator;
import org.opt4j.genotype.SelectGenotype;
import org.opt4j.sat.*;
import org.opt4j.core.Genotype;
import org.opt4j.common.random.Rand;

import com.google.inject.Inject;

public class pbsolver{

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		FileReader fr=null;
		FileReader file_reader=null;
		BufferedReader cons;
		BufferedReader decision_strat;

		//  Defining the solver to use.
		DefaultSolver constraints= new DefaultSolver();

		// Opening the constraints file
		try
    {
        fr = new FileReader(args[0]);
    }
    catch (FileNotFoundException fe)
    {
        System.out.println("File not found");
        return;
    }
		cons = new BufferedReader(fr);

		// Reading the constraints file
		String line = cons.readLine();
		while(line != null)
		{
			// System.out.println(line);
			// Map <String,String> var_sign = new HashMap<String,String>();
			Map <Object,Integer> var_coeff = new HashMap<Object,Integer>();

			// getting the clauses out
			String[] w=line.split("\\s");
			int i=0;
			while(w.length>(i+4))
			{
				int temp=Integer.parseInt(w[i+2]);
				if(w[i+1].equals("-"))
				{
					temp=(-1)*(temp);
				}
				var_coeff.put(w[i+3],temp);
				// System.out.println(w[i+3]);
				i=i+3;
			}
			// System.out.println(w[i+2]);

			Constraint clause = new Constraint (w[i+1],Integer.parseInt(w[i+2])) ;
			// adding the clauses
			for (Map.Entry<Object, Integer> entry : var_coeff.entrySet()) {
				clause.add(entry.getValue(),new Literal(entry.getKey(),true));
				// System.out.println(entry.getValue());
			}
			constraints.addConstraint(clause);
			line =cons.readLine();
		}
		cons.close();


		MixedSATManager pbmanager=new MixedSATManager(constraints);
		file_reader=new FileReader(args[1]);
		decision_strat = new BufferedReader(file_reader);


		// Initiate the Decision strategy
		List<Object> vars = new ArrayList<Object>();
		Map <Object,Double> lowerBounds = new HashMap<Object,Double>();
		Map <Object,Double> upperBounds = new HashMap<Object,Double>();
		Map <Object,Double> priorities = new HashMap<Object,Double>();
		Map <Object,Boolean> phases = new HashMap<Object,Boolean>();
		// String line = cons.readLine();
		line= decision_strat.readLine();
		while(line != null)
		{
			Boolean temp_phase=new Boolean(false);
			String[] w=line.split("\\s");
			if(w[1].equals("True"))
			{
				temp_phase=new Boolean(true);
			}
			Double temp_priority=new Double(w[2]);
			vars.add(w[0]);
			lowerBounds.put(w[0],new Double(0.0));
			upperBounds.put(w[0],new Double(1.1));
			priorities.put(w[0],temp_priority);
			phases.put(w[0],temp_phase);
			line =decision_strat.readLine();
		}

		// Calling the actual solver on the variables.
		Genotype gene=pbmanager.createSATGenotype(vars,lowerBounds,upperBounds,priorities,phases);
		Model ans=pbmanager.decodeSATGenotype(vars,gene);

		PrintWriter filewriter=new PrintWriter(new FileWriter(args[2]));
		for(Map.Entry<Object, Boolean> entry : ans.pairs()){
			filewriter.write(String.valueOf(entry.getKey()));
			filewriter.write(" ");
			filewriter.write(String.valueOf(entry.getValue()));
			filewriter.write("\n");
			// System.out.println(entry.getKey());
			// System.out.println(entry.getValue());
		}
		filewriter.close();
		System.out.println("Sucessful Assignment");


	}

}
