#nix-shell -p [python27]++(with python.pkgs;[matplotlib]);
export CLASSPATH=.:~/tmp/Constraints/sat4j/opt4j-2.7.jar
COMPLETE_PATH=~/tmp/Constraints/sat_with_meta.py
E3S_PATH=~/tmp/Constraints/e3s
echo "Start of run"
for file in $E3S_PATH/*.tgff
do
    echo "Test started for $file"
    python $COMPLETE_PATH --tg=$file -c=config_time.ini
    echo "Test completed for $file"
done
echo "ITS ALL DONE :)"
