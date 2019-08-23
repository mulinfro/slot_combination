
#python3 run.py -i 故事_test.lex -n 20 -d /home/liangliu/expand_rules_git/expand_rules

ipath=/root/slot_combination

if [ $# -ge 1 ] ; then
    sss=${1}
else
    sss="一加一乘以二三减去根号三五三五"
fi


python3 run.py -i ${ipath}/test -s ${sss}
