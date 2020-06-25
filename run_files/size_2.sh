#nix-shell -p [python27]++(with python.pkgs;[matplotlib]);
export CLASSPATH=.:~/tmp/Constraints/sat4j/opt4j-2.7.jar
COMPLETE_PATH=~/tmp/Constraints/sat_scenario.py
E3S_PATH=~/tmp/Constraints/e3s_reduced
echo "Start of run"
cd ~/tmp/Constraints/
for file in $E3S_PATH/*.tgff
do
    echo "Test started for $file"
    python $COMPLETE_PATH --tg=$file -c=./configuration_files/size_2_2.ini
    echo "Test completed for $file"
done
echo "ITS ALL DONE :)"
