#nix-shell -p [python27]++(with python.pkgs;[matplotlib]);
COMPLETE_PATH=~/tmp/Constraints/with_dpll/complete.py
E3S_PATH=~/tmp/Constraints/e3s/
echo "Start of run"
for file in $E3S_PATH/*.tgff
do
    echo "Test started for $file"
    python $COMPLETE_PATH $file --dvfs=5 >> $file.txt
    echo "Test completed for $file"
done
echo "ITS ALL DONE :)"
