#! /usr/bin/env nix-shell
#! nix-shell

COMPLETE_PATH=./sat_scenario.py
E3S_PATH=./e3s_reduced
TEST_PATH=./test1
echo "Start of run"
cd ..
pwd
mkdir ./results/artificial
mkdir ./cons/artificial
cd artificial_configs
python gen_config.py
echo "Generated config files"
cd ..
for config in $TEST_PATH/*.ini
do
  for file in $E3S_PATH/*.tgff
  do
    python $COMPLETE_PATH --tg=$file -c=$config >> run_time_data.txt &
  done
done
echo "ITS ALL DONE :)"
