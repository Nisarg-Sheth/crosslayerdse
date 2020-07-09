#! /usr/bin/env nix-shell
#! nix-shell
export CLASSPATH=.:~/tmp/Constraints/sat4j/opt4j-2.7.jar
COMPLETE_PATH=./sat_scenario.py
E3S_PATH=./e3s_reduced
TEST_PATH=./test1
echo "Start of run"
cd ..
pwd
mkdir ./results/test1
mkdir ./cons/test1
cd test1
python gen_config.py
echo "Generated config files"
cd ..
for config in $TEST_PATH/*.ini
do
  for file in $E3S_PATH/*.tgff
  do
    python $COMPLETE_PATH --tg=$file -c=$config >> run_time_data.txt &
  done
wait
done
echo "ITS ALL DONE :)"
