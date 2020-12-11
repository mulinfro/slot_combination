## by zhangyu ##
## 计算器领域时间优化 ##

export calculator1=(${表达式}) => request(domain="计算器") <0.021>;
export calculator1=(${表达式2})(等于|是|得)?(多少|得几|是几|等于几) => request(domain="计算器") <0.021>;
export calculator1=(${数字3}) => request(domain="计算器") <0.021>;

export calculator004 = (${数字})(是|等于|得)(多少|多些|几|什么)?(呀|啊|呢)?(${语气词})?$ => request(domain="计算器", domainflag1="计算器") <0.1>;
export calculator005 = (${数字})(是多少|等于多少|得多少|等于几|等于什么) => request(domain="计算器", domainflag1="计算器") <0.1>;
