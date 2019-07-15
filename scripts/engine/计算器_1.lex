## by zhangyu ##
## 计算器领域时间优化 ##
数字PI=派|PI|圆周率 => ("PI");
_正负数=(负|正)?的?(${数值}|${数字PI});
_正数=正?(${数值}) =>("$1");
## by zhangyu, 2017-12-29 ##
## 酷奇紧急需求, 支持分数运算, 暂只支持简单分数 ##
_ca分数内部 = (${整数})(分之)(${整数}) => (_join,prefix="$3",mid="@",suffix="$1");
_分数 = (正|负)?的?(${_ca分数内部});

数字1=(${_正负数}|${_分数}) =>("$1");

再操作=(再|然后|之后|然后再|之后再) => (")");
_加减乘除=(${再操作})?(加上|加|减去|减|减掉|乘上|乘以|乘|除以|除);

_平方=平方|二次方 =>("^2");
_立方=立方|三次方 =>("^3");
_N次方=(${数字1})次(方|幂) =>(_join2,prefix="^",mid="$1");

_平方根=开根号|根号|根号下|开方|开平方|开二次方|开平方根|开二次方根|平方根|二次方根 =>("^(1/2)");
_平方根1=根号|根号下 =>("^(1/2)");
_立方根=开立方|开三次方|开立方根|开三次方根|立方根|三次方根|三次方根下 =>("^(1/3)");
_立方根1=三次方根|三次方根下 =>("^(1@3)");
_N次方根1=(${数字1})次方根号? => (_join2,prefix="(1/",mid="$1",suffix=")");
_N次方根2=开(${数字1})次方根? => (_join2,prefix="(1/",mid="$1",suffix=")");
_N次方根=(${_N次方根1}|${_N次方根2}) => (_join2,prefix="^",mid="$1");

运算符=${_加减乘除};

数字2=(${数字1})的?(${_平方}|${_立方}|${_N次方}|${_平方根}|${_立方根}|${_N次方根}|倒数|阶乘|绝对值|相反数);
数字3=(${_平方根1}|${_立方根1})(${数字1}) =>(_join2,prefix="$2",mid="$1");
和差积商=(${数字1})(与|和|加上?|减去?|乘以?|除以)(${数字1})的?(和|差|积|商|相乘|相加|相除|相减) => (_join,prefix="$1",mid="$4",suffix="$4");

数字=${数字1}|${数字2}|${数字3}|${和差积商};


_一般括号=括号|括弧 => ("?");
_左括号=左括号 => ("(");
_右括号=右括号 => (")");
括号=${_一般括号}|${_左括号}|${_右括号};

左数字=(${_一般括号}|${_左括号})(${数字}) => (_join2,prefix="$1",mid="$2");
右数字=(${数字})(${_一般括号}|${_右括号}) => (_join2,prefix="$1",mid="$2");

_表达式=(${运算符})(${左数字}|${右数字}|${数字}) => (_join2,prefix="$1",mid="$2");
_表达式1=(${左数字}|${数字})(${_表达式}+) => (_join2,prefix="$1",mid="$2");
_表达式2=(${_表达式1})(的|再)(${_平方}|${_立方}|${_N次方}|${_平方根}|${_立方根}|${_N次方根}) =>(_join2,prefix="$1",mid="$3");

表达式=${_表达式1}|${数字2}|${_表达式2}|${和差积商};

## 乘法口诀
ca基础数字=${1}|${2}|${3}|${4}|${5}|${6}|${7}|${8}|${9};
表达式2=(${ca基础数字})(${ca基础数字}) => (_join,prefix="$1",mid="*",suffix="$2");

ca比较 = (比|比较|相比|相比较|相较);
## 高频率规则 ##
export calculator1=(${表达式})(你?知道|你?知不知道)?(是|等于|得)(多少|几) => request(domain="计算器", domainflag1="计算器") <0.8>;
export calculator12=^(${语气词})?(${表达式})(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;
export calculator12=^(${语气词})?(${表达式2})(等于|是|得)?(多少|得几|是几|等于几)(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;
export calculator13=(算一下|算一算|算算)(${表达式}) => request(domain="计算器", domainflag1="计算器") <0.8>;
export calculator14=(算一下|算一算|算算)(${表达式2})(等于|是|得)?(多少|得几|是几|等于几)(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;
## 特殊说法
export calculator1_1=(${表达式})(的|得)(多少|几)(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.8>;

## 绝对值
#####绝对值 by hcx
_绝对值=${数字1}的?绝对值;
export calcultor001=^(${_绝对值})(是|等于)?(多少|几)?$ => request(domain="计算器", domainflag1="计算器") <0.8>;

# bugfix
export calculator1 = (${表达式})(是|等于|得)$ => request(domain="计算器", domainflag1="计算器") <0.78>;
export calculator003 = ^(${语气词})?(你好|您好)?(我|我们|咱|咱们|你|你们|小?朋友)?(想|要|想要)?(知道|了解|学习|搜索|查看|查查|查)?(一下|下|次|一次)?(${表达式})(是|等于|得)(多少|多些|几|什么)?(呀|啊|呢)?(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.78>;
