## by zhangyu ##
## 计算器领域时间优化 ##
## 添加的复杂运算 ##

## 专门为了复杂计算进行的时间优化，其他领域优先级大于复杂计算 ##
_表达式new = (${表达式}|${数字});
 

_倍数扩大1_1 = (${_表达式new})的(${_正数})倍(要|能|就|会|可能)?(是|得|等于|是等于)(几|多少|几个);
_倍数扩大1_2 = (将|把|让)(${_表达式new})(扩|变|扩大|变成|变大)(${_正数})倍(要|能|就|会|可能)?(是|得|等于|是等于)(几|多少|几个);

export complex_caculator_3_1 = (${_倍数扩大1_1}) => request(domain="计算器", calculator_flag3="计算器", domainflag2="计算器") <0.7>;
export complex_caculator_3_2 = (${_倍数扩大1_2}) => request(domain="计算器", calculator_flag3="计算器", domainflag2="计算器") <0.7>;
## kuqi lyf
export complex_caculator_3_3 = ^(${_表达式new})的(${_正数})倍$ => request(domain="计算器", calculator_flag3="计算器", domainflag2="计算器") <0.4>;
##

_倍数计算2_1 = (${_表达式new})(要|能|就|会|可能)?(是|等于)(${_表达式new})的(几|多少)倍;
_倍数计算2_2 = (${_表达式new})(的|扩|扩大)(几|多少)倍(是|等于)(${_表达式new});

export complex_caculator_4_1 = (${_倍数计算2_1}) => request(domain="计算器", calculator_flag3="计算器", domainflag2="计算器") <0.7>;
export complex_caculator_4_2 = (${_倍数计算2_2}) => request(domain="计算器", calculator_flag3="计算器", domainflag2="计算器") <0.7>;

 

ca同 = (跟|与|和|同);
ca比大 = (大|多);
ca比小 = (小|少);

_大小比较1_1 = (${_表达式new})(${ca比较})(${_表达式new})(要|会|能|可能|能会|可能会|是|会是)?(${ca比大}|${ca比小})(几|多少|几个);
_大小比较1_2 = (${_表达式new})(${ca同})(${_表达式new})(${ca比较})(来说|来看|来|看来|说来)?(要|会|能|可能|能会|可能会|是|会是)?(${ca比大}|${ca比小})(几|多少|几个);
_大小比较1_3 = (${ca同})(${_表达式new})(${ca比较})(来说|来看|来|看来|说来)?(${_表达式new})(要|会|能|可能|能会|可能会|是|会是)?(${ca比大}|${ca比小})(几|多少|几个);

export complex_caculator_1_1 = (${_大小比较1_1}) => request(domain="计算器", calculator_flag3="计算器", domainflag3="计算器") <0.7>;
export complex_caculator_1_2 = (${_大小比较1_2}) => request(domain="计算器", calculator_flag3="计算器", domainflag3="计算器") <0.7>;
export complex_caculator_1_3 = (${_大小比较1_3}) => request(domain="计算器", calculator_flag3="计算器", domainflag3="计算器") <0.7>;

## by zhangyu, 2017-12-29 ##
## 酷奇紧急需求, 比A多B的数字是多少 ##
_大小比较1_4 = (${ca比较})(${_表达式new})(要|会|能|可能|能会|可能会)?(${ca比大}|${ca比小}|超|超过)(${_表达式new})(的|数|数字|的数|的数字)?(是|会是|可能是|能是|可能会是|能会是)(几|多少|什么);
export complex_caculator_1_4 = (${_大小比较1_4}) => request(domain="计算器", calculator_flag3="计算器", domainflag2="计算器") <0.7>;



ca比较表达式后缀 = (和|与|跟|同|及|以及|还有)(${_表达式new});
ca比较表达式 = (${_表达式new})(${ca比较表达式后缀}+);
_大小比较2_1 = (${ca比较表达式})(谁|哪个|哪一个)(比较|最|更)?(${ca比大}|${ca比小});

export complex_caculator_2_1 = (${_大小比较2_1}) => request(domain="计算器", calculator_flag3="计算器", domainflag3="计算器") <0.7>;