
atom digit = 0|1|2|3|4|5|6|7|8|9
atom op = 加上?|减去?|乘以?|除去?

# 所有constant必须在atom中
atom 多少 = 多少|几
plus num = {digit}

export expr1 = [{num}, {op}, {num}, {多少}] => {intent="表达式1", opl = $1, op = $2, opr = $3 }

