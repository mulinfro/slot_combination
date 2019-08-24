

atom dig = 零|一|二|三|四|五|六|七|八|九|十|百|千|万|亿
plus num = {dig}

atom 再操作 = 再|然后|之后|然后再|之后再
atom 前缀运算符 = 正|负| 平方根|根号|根号下|开根号|立方根
atom 二元运算符 = 加上|加|减去|减|减掉|乘上|乘以|乘|除以|除
atom 后缀运算符 = 倒数|绝对值|相反数|平方|立方|平方根|立方根|负一次方|负二次方|负三次方|阶乘

plus prefix = {前缀运算符}
plus suffix = {后缀运算符}

rule unary = [{prefix}?, {num}, {suffix}?]

rule bin_part = [{二元运算符}, {unary}]

plus bin = [{二元运算符}, {unary}]

export expr0 = [ {unary}]
export expr1 = [ {unary}, {bin} ] => { @G1, @G2="www", intent=$1, slot=join($2, $3, 0)  }
export expr2 = [ {num}, {bin} ]
export expr3 = [ {dig}, {bin} ]
