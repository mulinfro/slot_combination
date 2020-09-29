
atom 数字派 =派|PI|圆周率
atom dig = 零|一|二|三|四|五|六|七|八|九|十|百|千|万|亿
plus num0 = {dig}
atom frac_sym = 分之
rule 分数 = [{num0}, {frac_sym}, {num0} ]
rule num = {num0}|{数字派}|{分数}

atom 再操作 = 再|然后|之后|然后再|之后再
atom 前缀运算符 = 正|负|平方根|根号|根号下|开根号|立方根
atom 二元运算符 = 加上?|减去?|减掉|乘上|乘以|乘|除以?|与|和
atom 后缀运算符 = 倒数|绝对值|相反数|阶乘|平方|立方|平方根|立方根|负一次方|负二次方|负三次方

plus prefix = {前缀运算符}
plus suffix = {后缀运算符}

rule unary = [{prefix}?, {num}, {suffix}?]

plus bin_part = [{二元运算符}, {unary}]

rule bin = [{unary}, {bin_part}]

atom parn = 括号|括弧 
atom left_parn = 左括号
atom right_parn = 右括号
rule parn_bin0 = [{left_parn}|{parn}, {bin}, {right_parn}|{parn}]
plus parn_bin_helper = [{unary}, {二元运算符}]
rule parn_bin1 = [ {parn_bin_helper}, {parn_bin0}, {bin_part} ]

atom 和差积商 = 和|差|积|商|相乘|相加|相除|相减
rule expr0 = {unary}|{bin}|{parn_bin1}|{parn_bin0}

atom 知不知道 = 你?知道|你?知不知道
atom 等于 = 是|等于|得
atom 多少 = 多少|几
atom 算算 = 算一下|算一算|算算

export more_c = [{expr0}, {再操作}, {后缀运算符} ]       
export hcjs = [{expr0}, {二元运算符}, {expr0}, {和差积商}]  =>   {domain = "计算器", type="和差积商", bin_func, expr_left = "$1", right_op = "$3" }
export calculator0= {expr0}
export calculator1=[{expr0}, {知不知道}?, {等于}, {多少}? ]
export calculator3 = [{算算}, {expr0}]





#export calculator12=^(${语气词})?(${表达式})(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;

#export calculator12=^(${语气词})?(${表达式2})(等于|是|得)?(多少|得几|是几|等于几)(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;
#export calculator2=[{表达式2}, {知不知道}?, {等于}, {多少}? ]

#export calculator13=(算一下|算一算|算算)(${表达式}) => request(domain="计算器", domainflag1="计算器") <0.8>;
#export calculator14=(算一下|算一算|算算)(${表达式2})(等于|是|得)?(多少|得几|是几|等于几)(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;
## 特殊说法
#export calculator1_1=(${表达式})(的|得)(多少|几)(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;

## 绝对值
#####绝对值 by hcx
#_绝对值=${数字1}的?绝对值;
#export calcultor001=^(${_绝对值})(是|等于)?(多少|几)?$ => request(domain="计算器", domainflag1="计算器") <0.8>;
#export calculator1=(${表达式})(知不知道)?(是|等于|得)(多少|几) 

# bugfix
#export calculator1 = (${表达式})(是|等于|得)$ => request(domain="计算器", domainflag1="计算器") <0.78>;
#export calculator003 = ^(${语气词})?(你好|您好)?(我|我们|咱|咱们|你|你们|小?朋友)?(想|要|想要)?(知道|了解|学习|搜索|查看|查查|查)?(一下|下|次|一次)?(${表达式})(是|等于|得)(多少|多些|几|什么)?(呀|啊|呢)?(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.78>;
