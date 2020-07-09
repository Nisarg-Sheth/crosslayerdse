#! /usr/bin/env nix-shell
#! nix-shell
export CLASSPATH=.:~/tmp/Constraints/sat4j/opt4j-2.7.jar
COMPLETE_PATH=./sat_scenario.py
E3S_PATH=./
TEST_PATH=./artificial_configs
echo "Start of run"
cd ..
pwd
rm -r ./results/artificial
rm -r ./results/artificial
mkdir ./results/artificial
mkdir ./cons/artificial
cd tgff-3.6
make
cd ..
cd artificial_configs
python gen_config.py
echo "Generated config files"
cd ..
i=0
for config in $TEST_PATH/*.ini
do
   ((i=i+1))
   if [ $i -ge 4 ];
then
	 i=0;
	wait
fi
    python $COMPLETE_PATH  -c=$config >> run_time_data.txt &
done
echo "ITS ALL DONE :)"
