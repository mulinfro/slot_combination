## 备忘
搜索：严格; 不大于距离;  中间没有其他有效keyword; 
     减枝： 如果匹配到长的, 后面不搜索

三种模式:严格; 不大于距离;  中间没有其他有效keyword; 一次算不算

先动态规划 去掉覆盖的问题再贪心匹配

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
