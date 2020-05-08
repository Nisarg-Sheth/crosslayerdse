echo "Test for 5"
python gen_tg.py -o=tg5 -n=5
python with_dpll/both.py tg_generated/tg5.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout5.txt
echo "Test for 8"
python gen_tg.py -o=tg8 -n=8
python with_dpll/both.py tg_generated/tg8.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout8.txt
echo "Test for 10"
python gen_tg.py -o=tg10 -n=10
python with_dpll/both.py tg_generated/tg10.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout10.txt
echo "Test for 12"
python gen_tg.py -o=tg12 -n=12
python with_dpll/both.py tg_generated/tg12.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout12.txt
echo "Test for 14"
python gen_tg.py -o=tg14 -n=14
python with_dpll/both.py tg_generated/tg14.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout14.txt
echo "Test for 16"
python gen_tg.py -o=tg16 -n=16
python with_dpll/both.py tg_generated/tg16.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout16.txt
echo "Test for 18"
python gen_tg.py -o=tg18 -n=18
python with_dpll/both.py tg_generated/tg18.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout18.txt
echo "Test for 20"
python gen_tg.py -o=tg20 -n=20
python with_dpll/both.py tg_generated/tg20.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout20.txt
echo "Test for 25"
python gen_tg.py -o=tg25 -n=25
python with_dpll/both.py tg_generated/tg25.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout25.txt
echo "Test for 30"
python gen_tg.py -o=tg30 -n=30
python with_dpll/both.py tg_generated/tg30.tgff --dvfs=5 --dir=./run_both >> ./text_output/tgout30.txt
