
#python3 run.py -i 故事_test.lex -n 20 -d /home/liangliu/expand_rules_git/expand_rules

run_path=/home/liangliu/github/slot_combination/scripts/engine
ipath=/home/liangliu/github/slot_combination/sentence_semantic

#/home/liangliu/github/slot_combination/test/poetry_test

#sss=${1}
#python3 run.py -i ${ipath}/test/poetry_test -s ${sss} -d ${ipath}/test/poetry_test 
#exit 0

if [ $# -ge 1 ] ; then
    sss=${1}
    #python3 run.py -i ${ipath}/test/poetry_test -d ${ipath}/test/poetry_test -s ${sss}
    python3 $run_path/run.py -i ${ipath}/projects -d ${ipath}/lexicon/domain,${ipath}/lexicon/general -s ${sss}
else
    sss="一加一乘以二减去根号三"
    python3 $run_path/run.py -i ${ipath}/projects -d ${ipath}/lexicon/domain,${ipath}/lexicon/general -f ${ipath}/test/test.txt
fi


