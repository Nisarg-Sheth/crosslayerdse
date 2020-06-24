#nix-shell -p [python27]++(with python.pkgs;[matplotlib]);
COMPLETE_PATH=~/tmp/Constraints/scenario_run.py
E3S_PATH=~/tmp/Constraints/e3s
echo "Start of run"
for file in $E3S_PATH/*.tgff
do
    echo "Test started for $file"
    python $COMPLETE_PATH --tg=$file
    echo "Test completed for $file"
done
echo "ITS ALL DONE :)"
