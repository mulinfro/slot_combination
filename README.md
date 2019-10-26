
# slot_combination
### 主要特点：
    1. 运行速度非常快
	2. 支持正则语法
	3. 支持规则模糊匹配，句式归一化，带泛化能力
	4. 支持简单的规则自动生成功能
	5. 基于词库的方式，便于复用，逻辑上更清晰
	
####  例子：
   
规则语法：
1. 语法上主要还是正则，形式上做了点变化；最主要的是做了约束，所有的词必须属于某些类型， 即下面的atom或者词库，这两个本质上一样的。
这种约束的好处是隐式规范了规则编写过程中的必要语义抽象
2. 增加更强大的规则，比如模板匹配: `<A?, B?, C?, D>`, `A, B, C, D`任意顺序出现, ABC可有可无，D必有
3. 因为每个词都有类型，可以对规则做二阶抽象，比如指定实体及其修饰词，以及动作词库，可以自动生成相关的规则组合

     atom 听 = 听|播放
     atom 量词 = 一首?|一个
     atom 歌曲对象 = 歌曲|歌
     export r1 = [{听},  <{量词}？, {.歌手名}？>,  {.歌曲名}|{歌曲对象} ]  :: {MAX_GAP=3 } => {}
     
     MAX_GAP限制了槽位之间跳过字数最多不能超过3个字
	一条规则能覆盖如下的:   听下刘德华的歌
	                     听下刘德华的忘情水
						 听一首刘德华的歌曲
						 听一首刘德华的流行歌曲
						 听一首热门歌曲
						 听下刘德华的一首歌曲
						 听一下忘情水
						 ...
	
	 
 -  词表展现的是槽位值的差异，槽位的词表可以在不同项目复用，方便整理
 -  规则实现的是句式结构，句式结构有一定规律及抽象意义，可以做自动扩展
	
	
### 实验 (python实现)： 
  
 - 测试了dui的两个线上领域： 1. 计算器领域， 2. 古诗领域， （重写覆盖了计算器领域的大部分规则， 古诗领域全部规则）   
  - dui的测试数据， 解析结果中解析正确性没有问题， 两个领域每条平均耗时都**小于0.5ms**， 最长不超过1ms   
  - 其中计算器的测试集合包含了之前超时的测试集
  - 古诗领域dui上不到200条规则，几千条规模的领域还没有实验过， 几百条内的领域应该不会有问题

   
### 实现思路：
1. 所有的关键词都有类型， 或者说所有词都属于词表（一个词可以属于多个类型）
2. 把规则编译成一个前缀树**T**的结构，便于检索 （预处理过程）
3. 用AC状态机找出所有的词的列表**L**
4. 列表**L**上搜索所有词的不交叉组合，选出所有满足规则的可能集合，从所有集合中选出最大匹配，*注: 用第2步的数据结构能让单步搜索时间复杂度为O(1)*

#### 索引结构构造：
`[{听}, <{量词}？, {歌手名}？>, {歌曲名}|{歌曲对象} ]`  将会扩展为 

    听_量词_歌手名_歌曲名 ，
    听_歌手名_歌曲名，
    听_量词_歌曲名，
    听_量词_歌曲对象，
    听_歌手名_量词_歌曲名，
     ， ...

 
这些扩展的规则可以build成一个前缀树的结构， **特别的树中的节点可以设定逻辑条件**， 比如限定某个槽位长度不大于K， 只要在匹配的时候检查下这个条件是否满足即可;
正则语法中只有 `+,*`比较难放入这个树的结构中去，这两个做了特殊预处理

#### 搜索过程：
比如 **听一首刘德华的歌曲**， *听：听， （一首， 一），量词， 刘德华： 歌手名， （歌，歌曲）： 对象*
搜索过程遍历所有可能性  
  step1： 听， 在树结构中，继续
  step2： 听_量词, 在树结构中，继续
  ...

检索过程中只在词的列表L上进行，不相关的字会被跳过， 以及不符合语法的会被剪枝， 解析时间复杂度正比于搜索步数


#### 时间复杂性分析：
 *假设query长度为L， 解析出的候选词集合大小为N*
- 步骤1,2, 预处理过程，不消耗预测时间
- 步骤3的近似复杂度是L， 最差复杂度是L^2, 考虑大部分到L<=30， 这个时间可以忽略不计
- 步骤4的时间正比于搜索次数， 搜索的最坏时间复杂度为： 2^N, 当N为20时，最多需要搜索1048576次， 保守的估计C++也能控制在200ms以内
- 时间与规则数量没有直接线性关系，因为不需要对规则遍历
- **事实上需要的搜索次数要远远小于2^N**
   1. 对于30个字以内的句子，大部分领域不会有这么多候选词； 20个字，每个词平均2个字，那只有10个词， 当N <= 10时， 最多1024次搜索，非常快; 当然这里需要考虑领域内词之间的重叠度，大部分领域重叠度不会太大
   2. 规则会对搜索过程中做剪枝，非法的组合会停止;  比如计算器领域内词很多， 一加一加一加一加一... , 虽然词多完全不影响速度
   3. 搜索过程中会限定词之间不能有重叠， 词之间的最大间隔不超过一定距离， 相差太远的词的组合错误不会出现，这个会大大减小搜索空间

