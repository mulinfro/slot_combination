
#python3 run.py -i 故事_test.lex -n 20 -d /home/liangliu/expand_rules_git/expand_rules

#ipath=/mnt/c/Users/liuliang/Documents/GitHub/slot_combination/
#/home/liangliu/github/slot_combination/test/poetry_test

ipath="../.."

python3 ${ipath}/engine/app.py -i test_syntax.lex -f test_text.txt

#sss=${1}
#python3 run.py -i ${ipath}/test/poetry_test -s ${sss} -d ${ipath}/test/poetry_test 
#exit 0

#if [ $# -ge 1 ] ; then
#    sss=${1}
#    #python3 run.py -i ${ipath}/test/poetry_test -d ${ipath}/test/poetry_test -s ${sss}
#    python3 run.py -i ${ipath}/test/worst_test.lex -d ${ipath}/test/poetry_test -s ${sss}
#    #python3 run.py -i ${ipath}/test -s ${sss}
#else
#    sss="一加一乘以二减去根号三"
#    python3 run.py -i ${ipath}/test/poetry_test -d ${ipath}/test/poetry_test -f ${ipath}/test/poetry.txt
#fi
