
#python3 run.py -i 故事_test.lex -n 20 -d /home/liangliu/expand_rules_git/expand_rules

"""
ipath=/root/slot_combination

if [ $# -ge 1 ] ; then
    sss=${1}
    python3 run.py -i ${ipath}/test/poetry_test -d ${ipath}/test/poetry_test -s ${sss}
    #python3 run.py -i ${ipath}/test -s ${sss}
else
    sss="一加一乘以二减去根号三"
    python3 run.py -i ${ipath}/test/poetry_test -d ${ipath}/test/poetry_test -f ${ipath}/test/poetry.txt
fi
"""

ipath=/home/liangliu/github/slot_combination/sentence_semantic/

if [ $# -ge 1 ] ; then
    sss=${1}
    python3 run.py -i ${ipath}/test/poetry_test -d ${ipath}/test/poetry_test -s ${sss}
    #python3 run.py -i ${ipath}/test -s ${sss}
else
    sss="一加一乘以二减去根号三"
    python3 run.py -i ${ipath}/projects/古诗  -d ${ipath}/test/poetry_test -f ${ipath}/test/poetry.txt
fi
