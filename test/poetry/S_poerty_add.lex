##### update by zhangyu #####
##### 给古诗领域添加slot操作="背诵"|"说"|"收听" #####

export poetry4=(poe古诗_类别)(${古诗名}) => request(古诗名="$2") <0.9>;
export poetry4=(${古诗名})<2,-1> => request(古诗名="$1") <0.2>;

## 操作 & 古诗名 ##
export poetry4_1 = (${poe操作})(一)?(个|段|首|下)?(poe古诗_类别)?(${古诗名}) => request(古诗名="$5", 操作="$1") <0.3>;

##### update by zhangyu & peilu.wang #####
##### 支持新说法 & 新的搜索条件 #####
## 作者名 ##
export poetry6_5=(${古诗_作者})(的)?(${poe古诗_类别}) => request(对象="$3", 作者="$1") <0.2>;
export poetry6_6=(${古诗_作者})(的)?(作品|大作|诗歌) => request(作者="$1") <0.1>;
## 作者名&古诗名 ##
export poetry7_5=(${古诗_作者})(的)?(${poe古诗_类别}|作品|大作|诗歌)(${古诗名}) => request(作者="$1", 古诗名="$4") <0.3>;
export poetry7_7=(${古诗_作者})(的)?(${古诗名}) => request(作者="$1", 古诗名="$3") <0.1>;
## 单句诗句 ##
export poetry8=(${古诗_诗句}) => request(诗句="$1") <0.1>;
##
export poetry_and1=(${_合成诗句1}) => request(诗句="$1") <0.2>;
export poetry_and2=(${_合成国学句子1}) => request(诗句="$1") <0.2>;
##
##### by zhangyu #####
## 单字古诗名 ##
export poetry_sp1 = (想|要|想要)(看|听)(一)?(个|段|首|下)?(${古诗_作者})?(的)?(唐诗|古诗)(${单字古诗名}) => request(作者="$6", 古诗名="$8") <0.3>;
export poetry_sp2 = ^(给我|为我)?(来|说|讲|背|背诵|读|朗读|念)(一)?(个|段|首|下)?(${古诗_作者})?(的)?(唐诗|古诗)(${单字古诗名}) => request(作者="$5", 古诗名="$8") <0.3>;

##add by jiangkun
export poetry1_1=(${poe操作})(个|一个|一段|段|首|一首|一些|一?下)?(${古诗_作者})?(的|写的)?(${poe古诗_类别})?(${古诗名}) => request(古诗名="$6", 操作="$1", 对象="$5", 作者="$3") <0.6>;
export poetry7_4=(${poe操作})(一)?(个|段|首|下|点|两首|两个|几首|些|几个|会)?(${古诗_作者})?(的)?(${poe古诗_类别}) => request(作者="$4", 对象="$6", 操作="$1") <0.6>;

#add by jy 20170919
export poetry9_1=(${古诗名})(${古诗_作者}) => request(作者="$2", 古诗名="$1") <0.2>;

#古诗名和诗句重复的bug
export poetry1_2=(${poe操作})(个|一个|一段|段|首|一首|一些|一?下)?(${古诗_作者})?(的|写的)?(${poe古诗_类别})?(${古诗名})(${语气词})?$ => request(古诗名="$6",诗句="",操作="$1", 对象="$5", 作者="$3") <0.61>;

# for 酷旗_线上分析 20180102 JY
export poetry01021=(${poe操作})(一)?(个|段|首|下)?(${古诗_诗句}) => request(操作="$1") <0.2>;

# kuqi 线上数据 lyf
export poetry0115 = (${古诗名})怎么(${poe背诵}|${poe说})(${语气词})?$ => request(古诗名="$1",操作="$2") <0.3>;

##### by zhangyu & peilu.w #####
##### 古诗句子定位搜索 #####
#句子定位
#上下句   
export gushi3=(${古诗_诗句})(的?)(${操作_上下句}) => request(操作="$3", 诗句="$1" ) <0.5>;
#句子次序
export gushi3=(${古诗名})(的?)(${句子次序}) => request(古诗名="$1",位置="$3") <0.5>;
#第N句
第N句=第(${整数})句 => ("$1");
export gushi3=(${古诗名})(的?)(${第N句}) => request(古诗名="$1",位置="$3") <0.4>;
#倒数第N句
倒数第N句=倒数第(${整数})句 => (_join, prefix="#", mid="$1");
export gushi3=(${古诗名})(的?)(${倒数第N句}) => request(古诗名="$1",位置="$3") <0.4>;

##### update by zhangyu #####
##### 给故事领域添加slot操作="收听"|"说"|"背诵" #####

export poetry1=(我想听|我要听)(个|一个|首|一首)?(${poe古诗_类别}) => request(对象="$3", 操作="收听") <0.2>;
export poetry1=(我想看|我要看)(个|一个|首|一首)?(${poe古诗_类别}) => request(对象="$3", 操作="观看") <0.2>;

export poetry2_1=(${poe说}|${poe背诵})(一)?(个|段|首|下)?(${poe古诗_类别}) => request(对象="$4", 操作="$1") <0.2>;

export poetry6=(${poe古诗_类别}) => request(对象="$1") <0.1>;

##### update by zhangyu & peilu.wang #####
##### 支持新说法 #####
## 朗读(操作归一到"说") ##
export poetry7_1=(${poe说})(一)?(个|首|下|段|点|两首|两个|几首|一些|几个)?(${poe古诗_类别}) => request(对象="$4", 操作="说") <0.2>;
export poetry8_1 = (播|放|播放)(一)?(个|首|下|段|点|两首|两个|几首|一些|几个)?(${poe古诗_类别}) => request(对象="$4", 操作="播放") <0.2>;
##### by zhangyu & peilu.wang #####
##### 给定搜索条件, 搜索特定的内容 #####
#查询对象
#给古诗名问作者
export gushi4=(${古诗名})(的?)(作者) => request(查询对象="作者",古诗名="$1") <0.5>;
export gushi4=(${古诗名})(是?)(谁)(的?)(大作|写的|作品|所作|所写|所创作|创作|提出|发表|写出|诗|词|古诗) => request(查询对象="作者",古诗名="$1") <0.5>;
#给句子问作者
export gushi4=(${古诗_诗句})(的?)(作者)=> request(查询对象="作者",诗句="$1") <0.5>;
export gushi4=(${古诗_诗句})(是|来自|出自)?(谁)(的?)(大作|写的|作品|所作|所写|所创作|创作|提出|发表|写出|诗|词|古诗) => request(查询对象="作者",诗句="$1") <0.5>;

#给句子问古诗名
export gushi4=(${古诗_诗句})(是|来自|出自)?(哪|那)(首|个)(诗|词|古诗|唐诗)(里的|里面的|的)?(句子)? => request(查询对象="古诗名",诗句="$1") <0.5>;
export gushi5 = (哪|什么)(一)?(首|段|个)?(诗|古诗|唐诗)(里|里面|中|中间|其中)(有|含|含有|包含)(那个|那句|那一句)?(${古诗_诗句}) => request(查询对象="古诗名", 诗句="$8") <0.5>;

## by zhangyu ##
## 添加查询句式 ##
export gushi5 = (哪一?个)(诗人|作者)(写|作|提)(的|了)?(唐诗|古诗|诗)?(${古诗名}) => request(查询对象="作者", 古诗名="$6") <0.2>;
export gushi6 = (哪一?个)(诗人|作者)(写|作|提)(的|了)?(诗句|名句)?(${古诗_诗句}) => request(查询对象="作者", 诗句="$6") <0.2>;

##kuqi 线上资源 lyf
export gushi7=(${古诗名})(那首诗|这首诗)(是?)(谁)(的?)(大作|写的|作品|所作|所写|所创作|创作|提出|发表|写出|诗|词|古诗) => request(查询对象="作者",古诗名="$1",对象="") <0.5>;# wjz 20190702

export poetry100=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})应?该?是?(怎么|咋|如何|的)(翻译|解释|释义|意思|含义|译文) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;
export poetry101=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})的?(${poe古诗_类别})的?(翻译|解释|释义|意思|含义|译文) => request(intent="查询诗词释义", 作者="$1", 诗句="$3", 对象="$4", 古诗名="") <0.6>;
export poetry102=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})的?(古诗|诗词|现代文|普通话|白话|白话文)的?(翻译|解释|释义|意思|含义|译文) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;
export poetry103=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})${句首修饰词}?(翻译|解释|释义|意思|含义|译文) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;

export poetry104=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})你?(会|能|可以|会不会|能不能|可不可以|可以不可以)(翻译|解释|释义) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;
export poetry105=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})你?(知道|晓得)应?该?是?(怎么|咋|如何)(翻译|解释|释义) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;
export poetry106=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})你?${句首修饰词}?(查|找|搜|查询|查找|解释|看)(一?下)?应?该?(怎么|咋|如何|的)(翻译|解释|释义) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;

export poetry107=(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})应?该?是?(什么|啥|怎么|咋)(翻译|解释|释义|意思|含义|译文) => request(intent="查询诗词释义", 作者="$1", 诗句="$3") <0.6>;

export poetry108=(怎么|咋)(翻译|解释|释义)(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句}) => request(intent="查询诗词释义", 作者="$3", 诗句="$5") <0.6>;
export poetry109=(翻译|解释|释义)(一?下)?(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句}) => request(intent="查询诗词释义", 作者="$3", 诗句="$5") <0.6>;
export poetry110=(把|将)(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})给?(翻译|解释|释义) => request(intent="查询诗词释义", 作者="$2", 诗句="$4") <0.6>;

export poetry111=(把|将)(${古诗_作者})?(的|写的|创作的)?(${古诗_诗句})给?(翻译|解释|释义|译)(成|为) => request(intent="查询诗词释义", 作者="$2", 诗句="$4") <0.6>;

