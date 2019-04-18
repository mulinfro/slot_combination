# 规则生成数据

# USAGE

配置好配置文件， 配置文件是个python脚本(如果不方便后续可以考虑其他方式)


配置文件中主要是，1.词表名及其对应的文件地址; 2. "+*"的最大重复次数


# 运行run.py文件， 输入有三个参数:
* -i 输入的lex文件地址; 有两种方式
    1. 逗号分割的lex文件，可以有多个lex文件
    2. 文件目录， 会把目录中所有lex文件当作输入
* -o 生成数据的输出文件地址, 可忽略，默认打印到控制台
* -n 需要生成的样本数量
* -mn 每个规则生成的样本最少的数量
* -d 词表文件目录，目录下所有txt文件都会被载入，注意保持规则名与词表名一致



# config文件配置

### +和*的最大重复次数
DEAUFALT_MAX_REPEAT = 3

### 是否显示slot
show_slot = True

### 是否显示intent
show_intent = True

### 语法检查模式
syntax_check_mode = False

### 规则分布规则
1. uniform  =>  均匀分布，每个规则一样多
2. weight => 按照规则给定的权重大小分布，适用于人工设定
3. pattern_num =>  根据估算的每个规则的可生成数量确定


rule_select_strategy = "uniform"

### pattern_num模式下; 生成数量计算方法
1. sum =>  patterns + slots 
2. log =>  log(patterns + slots)


pattern_weight_func = "sum"

### DOT匹配
默认情况下，“.“ “.*” ，  dot会被空字符串替换
如果配置了__RE_DOT__.txt词表，会从中随机取一个生成


### 暂时不支持的语法
1. <m,n> 字数限制;不做检查
