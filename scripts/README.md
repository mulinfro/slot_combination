

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

# export一定是个list
export r1 = [{b1 <- W(2,5)} , {m1} ]    

## 
key_word_list
[beg_idx, end_idx, string, tag_list]

word_set
[beg_idx, end_idx, string, tag_list]
