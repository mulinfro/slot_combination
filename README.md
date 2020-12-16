
# slot_combination
slot_combination是一个快速的, 支持模糊匹配的, 多模正则语义解析引擎; 尤其适合中文解析。

### 主要特点：
  1. 解析速度非常快(ms级)
	2. 支持正则语法 + 一些更强大的语法
	3. 支持模糊匹配，带泛化能力, 大大减少开发工作量
	4. 基于词库的组织方式，便于复用
	5. 拥有模板功能, 语义快速领域迁移; 大大加快开发速度

### 例子介绍
```python
  atom 播放 = 听|播放|放
  atom 量词 = 一首?|一个
  atom 歌曲 = 歌曲|歌
  atom 播放方式 = 随机|重复|循环
  atom 的 = 的|地
  rule 类型 = <{.作者}?, {.专辑}?, {.风格}?>
  export r1 = [{播放方式}?, {播放}, {量词}?, {类型}, {的}?, {歌曲}|{.歌曲名}] => {intent="播放歌曲", 量词=$3, 类型=$4, 歌曲=$6}
 
  "{}"是变量，表示引用
  这里{.作者}, {.专辑}, {.风格}, {.歌曲名}, "."点开始的变量表明是词典文件, 没有定义在规则中

	   听下刘德华的歌
	                     听下刘德华的忘情水
						 听一首刘德华的歌曲
						 听一首刘德华的流行歌曲
						 听一首热门歌曲
						 听下刘德华的一首歌曲
						 听一下忘情水
```

一条规则能覆盖如下的:
 循环 播放 一首 周杰伦 七里香 里的 止战之殇
 随机 播放 一首 周杰伦 七里香 里的 歌曲
 随机 播放 周杰伦 七里香 里的 歌
 随机 播放 周杰伦 里的 歌
 给我放下 七里香 里的 止战之殇
 给我放下 七里香专辑 周杰伦 的 歌曲
 听 一下 稻香
 ...

从例子中可以看出，表达能力主要来源于以下几点：
1. 词汇的替换
2. "?", 表示可有可无; "|" 表示"或"
3. <ele1?, ele2?, ele3?> 三个元素可有可无，且顺序随机
4. [ele1, ele2, ele3, ..] 元素之间可以跳过一定长度的文字（可以通过配置文件调整；默认为3，若为0就是严格匹配） 

### requirements
* python3.7+
* ahocorasick (pip3 install ahocorasick)

### 使用方式
命令行方式:
```sh
python3 engine/app.py -i ${lexFiles} -d ${dictDirPathes} -f ${queryFile} -s ${query}
```
lexFiles: 规则文件, 可以是逗号分割的文件列表; 或者是个目录，自动找到目录中所有lex后缀文件作为输入
dictDirPathes: 词典目录文件， 逗号分割的目录列表， 所有目录中的txt后缀的文件都会被加载; 文件名作为加载的词典名
query:  query字符串
queryFile: query文件，用作批量调用

调用engine/app.py里的Engine类
```python
    engine = Engine(lexFiles, dictDirPathes)
    ans = engine.apply(query)
    print(ans)
```
### 其他说明
程序结构见engine/IMPL.md文件
规则语法说明见syntax.md
测试例子见test目录

### 与常见引擎的差异
语法上与常见的正则语义解析引擎类似, 主要有两点差异:
1. 强制按照词表方式组织语料

2. 默认支持随机跳过字数

3. 对正则做了限制，同时理论上可以比正则语法更强

### 模板化

### 适用场景
    * 短句多模模式匹配
    * 任务式对话

### LICENSE
