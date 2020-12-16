

## SYNTAX
atom = CONSTANT + CONSTANT ? |
plus = atom+  贪心连续匹配

var = REF, atom_plus, |  [var, var]
var_plus = var +  贪心连续匹配，允许一定间隔

rule = var list


## 如果没有 + 
取出所有词性， 做一个动态规划
前向最大匹配（贪心）



## 有 + 
没有规则嵌套

规则嵌套 前向最大匹配（贪心）


## EXAMPLE

# atom只能常量, 带?的扩展
atom b1 = 播放
atom b2 = 播放|打开|听下？

# rule list or 或,  不允许直接嵌套， 约束灵活性为了最大化公用
rule m1 = {.歌曲}|{.英文歌曲}
rule m2 = [{atom}, {m1} ]

# plus atom 字典 or 变量
plus b1_p = {b1}

# export一定是个list, @代表配置
export r1 = [{b1 :: W(2,5)} , {m1} ]  => { intent=$1, @G1 = 3, @G2 }

## 
key_word_list
[beg_idx, end_idx, string, tag_list]

word_set
[beg_idx, end_idx, string, tag_list]


## 

搜索：严格; 不大于距离;  中间没有其他有效keyword; 
     减枝： 如果匹配到长的, 后面不搜索


三种模式:严格; 不大于距离;  中间没有其他有效keyword; 一次算不算
只在export支持 | ;

atom | 拼接？

先动态规划 去掉覆盖的问题再贪心匹配
search

检查名称是否冲突  atom  ref

生成规则


半搜索， 存在冲突点  播放下


分歧点
ABC  [A "BC.."] [AB "C.."]
ABC  ["A" BCD..] ["AB" CD..]
ABC  [AB CD..] [A BCD..]

## DONE
删除export不存在的tag


记录计算搜索， 达到一定步数自动跳出，采用贪心, 兼顾效果和效率
先贪心最大不重叠覆盖， 在这个覆盖上寻找解
限制搜索时不超过N个slot, 即不中间跨过N个
