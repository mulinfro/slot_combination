

## SYNTAX
atom = CONSTANT + CONSTANT ? |
atom_plus = atom+  贪心连续匹配

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

atom b1 = 播放
atom b2 = 播放|打开|听下？
atom_plus b1_p = ${b1}+

var m1 = ${.歌曲}|${.英文歌曲}
var m2 = [${atom}, ${m1} ]
var_plus m2_p = [${atom}, ${m1} ] +

rule r1 = [${b1}, ${m1} ]

## 
key_word_list
[beg_idx, end_idx, string, tag_list]

word_set
[beg_idx, end_idx, string, tag_list]