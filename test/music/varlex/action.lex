#negate
export negate1=^(不好|不是|不对|不确定|不确认|不要|不要了|不行|不需要|不了)(的|吧)?.*(我要|想找|要找|我想|要听|想听) => request(__act__="deny") <0.4>;
export negate2=^(${语气词})?不(好|是|对|可以|确定|确认|要|要了|行|需要|用了?|想听|要听)(的|${语气词})?$ => request(__act__="deny") <0.2>;
#export negate3=no|NO|算了|错了|不用了|不用啦|不是谢谢|不要这个 => request(__act__="deny") <0.2>;
#export negate4=都不(是|想|要|好|行|喜欢) => request(__act__="deny") <0.2>;
export negate5=^(不是|不是的|不对|不要|不要了|不行|不需要|不了|算了|错了|不用了|不用啦|不是谢谢|不要这个|不是这个)$ => request(__act__="deny") <0.2>;
export negate5=^不$ => request(__act__="deny") <0.2>;
#deny
_deny1=(不是|不是要|不要|不想要);#|不想
_deny2=(不|别)(要|是|想)?(找|听);
_deny=${_deny1}|${_deny2};

#否定一个tgt
export deny1_1=^我?(${_deny})(${歌手名})的?(那个|那首)?(歌|歌曲|曲子|音乐)?了?$ => request(__act__="deny",__tgt__="歌手名") <0.8>;
export deny1_2=^我?(${_deny})(${歌曲名})的?(那个|那首|这首)?(歌|歌曲|曲子|音乐)?了?$ => request(__act__="deny",__tgt__="歌曲名") <0.8>;
export deny1_2=^我?(${_deny})(${风格})的?(歌|歌曲|曲子|音乐)?$ => request(__act__="deny",__tgt__="音乐风格") <0.8>;
export deny1_2=^我?(${_deny})(${音乐类型})的?(歌|歌曲|曲子|音乐)?$ => request(__act__="deny",__tgt__="音乐类型") <0.8>;

#否定一个tgt并给出另一个inform
export deny2_1=^我?(${_deny})(${歌手名})的?.*我?(要|找|是|想|听|有没有).+ => request(__act__="deny",__tgt__="歌手名") <0.81>;
export deny2_2=^我?(${_deny})(${歌曲名})的?.*我?(要|找|是|想|听|有没有).+=> request(__act__="deny",__tgt__="歌曲名") <0.81>;
export deny2_2=^我?(${_deny})(${风格})的?.*我?(要|找|是|想|听|有没有).+=> request(__act__="deny",__tgt__="音乐风格") <0.81>;
export deny2_2=^我?(${_deny})(${音乐类型})的?.*我?(要|找|是|想|听|有没有).+=> request(__act__="deny",__tgt__="音乐类型") <0.81>;


#同时否定两个tgt
export deny3_1=(${_deny})(${歌手名})的(${歌曲名}) => request(__act__="deny",__tgt__="歌曲名&歌手名") <0.82>;

# affirm
export affirm1=^(${语气词})?(好|是|对|行|可以|嗯|有|喜欢|确定|确认|确信|ok|OK|YES|yes|要|对了)(的|吧|得|地|滴)?$ => request(__act__="affirm",歌曲名="@") <0.8>;
export affirm2=没错 => request(__act__="affirm") <0.3>;
export affirm3=^(${语气词})?(要|听|是|就|就是|就要|就听)这(个|首|一首)$ => request(__act__="affirm") <0.3>;
export affirm4=^(${语气词})?(好|是|对)(的|得|地|滴) => request(__act__="affirm") <0.2>;
export affirm2=^我?(要|就要|就|就是)(听|放)?这(个|首|一首)吧?$ => request(__act__="affirm") <0.3>;
export affirm5=^(需要)吧?$ => request(__act__="affirm") <0.3>;
export affirm6=^(请|能不能|可不可以|可以|能|能够)?(再试一次|再试试|再来一次)(${语气词})?$ => request(操作="重试",歌曲名="@",主题="@") <0.78>;
# confirm
##确认单个tgt
export confirm1_1=是(不|否)是(${歌手名})(唱|演唱)?的?(歌|歌曲|曲子|音乐)?(吗|呀|么|不)? => request(__act__="confirm",__tgt__="歌手名") <0.6>;
export confirm1_2=是(不|否)是(${歌曲名})的?(这首|那首)?(歌|歌曲|曲子|音乐)?(吗|呀|么|不)? => request(__act__="confirm",__tgt__="歌曲名") <0.6>;

export confirm1_7=是(否|否是)?(${歌手名})(唱|演唱)?的?(歌|歌曲|曲子|音乐)?(吗|呀|么|不) => request(__act__="confirm",__tgt__="歌手名") <0.6>;
export confirm1_8=是(否|否是)?(${歌曲名})的?(这首|那首)?(歌|歌曲|曲子|音乐)?(吗|呀|么|不) => request(__act__="confirm",__tgt__="歌曲名") <0.6>;

##------------确认两个tgt----------------##
#歌手名+歌曲名
export confirm2_1=是(不|否)是(${歌手名})(唱|演唱)?的(这首|那首)?(${歌曲名})的?(歌|歌曲|曲子|音乐)?(吗|呀|么)?$ => request(__act__="confirm",__tgt__="歌手名&歌曲名") <0.85>;
export confirm2_2=是(否|否是)?(${歌手名})(唱|演唱)?的(这首|那首)?(${歌曲名})的?(歌|歌曲|曲子|音乐)?(吗|呀|么)$ => request(__act__="confirm",__tgt__="歌手名&歌曲名") <0.6>;


# findalts
export findalts1=^(${语气词})?(他|${歌手名})?还(有没)?有(别|其他|其它|哪些)?的?(歌|歌曲|曲子|音乐)?(吗) => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts1=^(${语气词})?(他|${歌手名})?还(有没)?有(别|其他|其它|哪些)?的?(歌|歌曲|曲子|音乐) => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts2=^(${语气词})?(他|${歌手名})?只有这(个|两个|一首|这首|首|两首|几首)(歌|歌曲|曲子|音乐)?吗 => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts3=^(${语气词})?(他|${歌手名})?还?有没有(其他|其它)的了 => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts4=^(${语气词})?(他|${歌手名})?有(没有)?(别|其他|其它)的?(歌|歌曲|曲子|音乐)?吗 => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts4=^(${语气词})?(他|${歌手名}|你)?(只有)(一个|这个|一首|这首)(歌|歌曲|曲子|音乐)吗 => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts4=^(${语气词})?(他|${歌手名}|你)?还?有(没有)(别|其他|其它|哪些)的?(歌|歌曲|曲子|音乐) => request(__act__="findalts",__tgt__="歌曲名") <0.6>;
export findalts4=(他|${歌手名}|你)的?(另外)(一个|这个|一首|这首)(歌|歌曲|曲子|音乐) => request(__act__="findalts",__tgt__="歌曲名") <0.6>;

# querymore
export querymore1=能(提供|给|给点|给出)(更多)的(信息)吗 => request(__act__="querymore") <0.6>;
export querymore2=能不能(提供|给|给点|给出)(更多)的(信息) => request(__act__="querymore") <0.6>;

#inform
export inform2=(不喜欢|不太喜欢|不是很喜欢|不是特别喜欢).*(但是|可是|还是) => request(__act__="inform") <0.6>;

#request
查找=搜|找|查|搜搜|找找|查查|搜一搜|找一找|查一查|查下|搜下|找下|看下|查一下|搜一下|找一下|看一下|查询|查找|搜索|说一下|讲一下|说下|讲下|报一下|报下|说一遍|讲一遍|报一遍|想知道|告诉我;

#歌手名
export request1_10=(${歌曲名})?(的)?(歌手|演唱|演唱者)是(谁|哪位)   => request(__act__="request",__tgt__="歌手名") <0.6>;
export request1_3=(${查找})(${歌曲名})?(这首歌)?(是谁唱的)  => request(__act__="request",__tgt__="歌手名") <0.6>;
export request1_3=(${歌曲名})(这首歌)?(是谁唱的)  => request(__act__="request",__tgt__="歌手名") <0.6>;
export request1_3=(是谁唱的|是谁的歌|谁唱的)  => request(__act__="request",__tgt__="歌手名",操作="@") <0.3>;
singer=(唱)(这首|这个)? ;
export request1_11=(歌手|演唱|演唱者)是(谁|哪位)   => request(__act__="request",__tgt__="歌手名") <0.3>;
export request1_12=(${singer})(歌|歌曲|音乐|曲子)的(是谁|是哪位)   => request(__act__="request",__tgt__="歌手名") <0.3>;
export request1_13=(这|那|在播|在放|电台|收音机)?(歌手是谁|谁唱的|谁唱的歌) => request(__act__="request",__tgt__="歌手名") <0.3>;
export request1_14=^(是)?(谁唱的)(${语气词})?$ => request(__act__="request",__tgt__="歌手名") <0.3>;

#歌曲名
##export request1_21=(什么|哪些|啥)(歌|歌曲|音乐|曲子|曲儿|${对象})(大家)?(放|听|播|播放|点|唱)(的|得)(比较|最|超级)(多|火|热|热门) => request(__act__="request",__tgt__="歌曲名") <0.3>;
##export request1_3=(放|听|播|播放|点|唱)(的|得)?(比较|最|超级)?(多|火|热|热门)的(歌|歌曲|音乐|曲子|曲儿|${对象})(是什么|是啥|有啥|有什么|有哪些|是哪些)=> request(__act__="request",__tgt__="歌曲名") <0.3>;
##export request1_4=(什么|哪些|啥)(歌|歌曲|音乐|曲子|曲儿|${对象})(最近|近期|近来)?(比较|最|超级)?(火|热|流行|火热|热门)=> request(__act__="request",__tgt__="歌曲名") <0.3>;
export request1_15=(这首歌|这歌|歌曲|音乐|曲子|歌)(叫什么|叫啥|什么名|叫什么名|叫啥名|是什么|是啥)   => request(__act__="request",__tgt__="歌曲名") <0.3>;
export request1_16=(这首歌|这歌|歌|歌曲|音乐|曲子)(的)?(名|名字)(叫什么|叫啥|什么名|叫什么名|是什么|是啥)   => request(__act__="request",__tgt__="歌曲名") <0.3>;
export request1_221=(名|名字)叫做?(${歌曲名})=> request(__act__="inform",__tgt__="") <0.18>;
export request1_22=(这首歌|这歌|歌|歌曲|音乐|曲子)(的)?(名|名字)=> request(__act__="request",__tgt__="歌曲名") <0.15>;

###export request1_17=(有哪些|有什么|有啥)(${排行榜}|新|比较热|比较火|比较热门|比较流行)的?(${对象})   => request(__act__="request",__tgt__="歌曲名",对象="$3") <0.3>;
####export request1_18=(${排行榜}|比较热|比较火|比较热门|比较流行)的(${对象})(是什么|是啥|有哪些)   => request(__act__="request",__tgt__="歌曲名",对象="$2") <0.3>;
export request1_19=(叫什么|叫啥|什么名|什么名字)(这首歌|歌名|这歌)   => request(__act__="request",__tgt__="歌曲名") <0.3>;
##### modified by caixiang
export request1_111=(这|那|这首|那首|在播|在放|电台|收音机|在播放|我在听)(的|是|的是|叫)?(什么|啥|哪首|是什么|哪一首|哪个)(歌|音乐|啥|歌曲|什么)?$ => request(__act__="request",__tgt__="歌曲名",操作="@") <0.3>;
export request1_111_1=(这|那|这首|那首|在播|在放|电台|收音机|在播放|我在听)(的|是|的是|叫)?(歌|音乐|啥|歌曲|什么)?(是)?(什么|啥|哪首|是什么|哪一首|哪个)$ => request(__act__="request",__tgt__="歌曲名",操作="@") <0.3>;
export request1_111_2=^你在唱什么(歌|音乐|啥|歌曲)?$ => request(__act__="request",__tgt__="歌曲名",操作="@") <0.3>;
#####
export request1_112=(放|播|播放|我听|我在听|这)(的)?(是|叫)?(什么歌|啥歌|什么音乐|啥音乐)=> request(__act__="request",__tgt__="歌曲名") <0.3>;
export request1_113=(放|播|播放|我听|我在听|这|唱)(的)?(叫什么|叫啥|是什么|是啥)=> request(__act__="request",__tgt__="歌曲名",操作="@") <0.1>;
export musictengxun33_1=^(请)?(给我)?(听听|听下|听一下|听听看|猜猜看|猜猜|猜下|猜一下)(这是什么歌|这是啥歌|这首歌叫什么|这首歌叫啥|这首歌的名字叫什么|这首歌的名字是什么)(${语气词})?$=> request(歌曲名="@") <0.4>;
export request1_114=^(是)?(什么歌|啥歌|什么音乐|啥音乐)(${语气词})?$ => request(__act__="request",__tgt__="歌曲名") <0.3>;
export request1_116=(电台|收音机|车上|后视镜|车机|手机)?(放|播放|播|这是)(的是)?叫?(什么歌|啥歌|什么音乐|啥音乐) => request(__act__="request",__tgt__="歌曲名") <0.3>;
export request1_115=(电台|收音机|车上|后视镜|车机|手机)?(放的|播放的|播的)(歌|音乐)(是什么|是啥|叫什么) => request(__act__="request",__tgt__="歌曲名") <0.3>;
#专辑名
export request1_117=(有哪些|有什么|有啥)(${排行榜}|新|比较热|比较火|比较热门|比较流行)的?(专辑)   => request(__act__="request",__tgt__="专辑名") <0.3>;
export request1_118=(${排行榜}|比较热|比较火|比较热门|比较流行)的(专辑)(有哪些|有什么|有啥|是什么|是啥)   => request(__act__="request",__tgt__="专辑名") <0.3>;
export request1_119=(哪张|啥|什么|哪个|哪一个|哪一张)(专辑)   => request(__act__="request",__tgt__="专辑名") <0.3>;
#export request1_119_bug=(哪张|啥|什么|哪个|哪一个|哪一张)(专辑)(里的|中的)?(${语气词})?$  => request(__act__="request",__tgt__="专辑名") <0.301>;
export request1_120=(专辑)(有哪些|有什么|有啥|是什么|是啥|叫什么)   => request(__act__="request",__tgt__="专辑名") <0.2>;
export request1_1201=(${当前歌曲})的专辑(有哪些|有什么|有啥|是什么|是啥|叫什么)(${语气词})?$   => request(__act__="request",__tgt__="专辑名",歌曲名="$1") <0.2>;
export request1_1203=(${当前歌曲})(属于|是|在|收录在|发表在|发布在)(哪张|哪一张|哪个|哪一个)专辑(里|里面|里头)?(的)?(${语气词})?$   => request(__act__="request",__tgt__="专辑名",歌曲名="$1") <0.6>;
export request1_1204=^(属于|是|在|收录在|发表在|发布在)(哪张|哪一张|哪个|哪一个)专辑(里|里面|里头)?(的)?(${语气词})?$   => request(__act__="request",__tgt__="专辑名",歌曲名="@") <0.65>;
#播放列表

#作词
export request1_121=(这首歌)(是谁)(作词|写的|作的词)   => request(__act__="request",__tgt__="作词") <0.6>;
export request1_122=(作词是谁|这是谁写的|作词者是谁)   => request(__act__="request",__tgt__="作词") <0.3>;
export request1_123=(歌词|词)(是谁)(写的|作的)   => request(__act__="request",__tgt__="作词") <0.3>;
export request1_124=(谁)(写的|作的)(歌词|词|这首歌|这首曲)   => request(__act__="request",__tgt__="作词") <0.3>;
export request1_125=写(这首歌)的(是谁)   => request(__act__="request",__tgt__="作词") <0.3>;
export request1_126=(是谁)(作词|写的词|作的词)   => request(__act__="request",__tgt__="作词") <0.3>;

#作曲
export request1_127_0=(${歌曲名})(这首歌)(是谁)(编曲|作曲|编的曲|作的曲)   => request(__act__="request",__tgt__="作曲",歌曲名="$1") <0.6>;
export request1_127=(这首歌)(是谁)(编曲|作曲|编的曲|作的曲)   => request(__act__="request",__tgt__="作曲") <0.6>;
export request1_127_0=(${歌曲名})(这首歌)的?(编曲|作曲|编的曲|作的曲)(是谁)   => request(__act__="request",__tgt__="作曲",歌曲名="$1") <0.6>;
export request1_128=(谁)(编曲|作曲|编的曲|作的曲|谱曲|谱的曲|做的曲)   => request(__act__="request",__tgt__="作曲") <0.3>;
export request1_129=(编曲|作曲)者?的?(是谁)   => request(__act__="request",__tgt__="作曲") <0.3>;
export request1_130=(曲子)(是谁)(写的|作的|谱写|谱的)   => request(__act__="request",__tgt__="作曲") <0.3>;

#年代
export request1_131_0=(${歌曲名})(这首歌)(是|在|是在)?(什么|哪个)(时候|年代)   => request(__act__="request",__tgt__="年代",歌曲名="$1") <0.6>;
export request1_131=(这首歌)(是|在|是在)?(什么|哪个)(时候|年代)   => request(__act__="request",__tgt__="年代") <0.6>;
export request1_132=(这首歌)(是|在|是在)(哪一年|哪年)   => request(__act__="request",__tgt__="年代") <0.6>;
export request1_133=(这)(是|在|是在)(什么|哪个)(时候|年代)(的)(歌|歌曲|音乐|曲子)   => request(__act__="request",__tgt__="年代") <0.6>;
export request1_134=(这)(是|在|是在)(哪一年|哪年)(的)?(歌|歌曲|音乐|曲子)   => request(__act__="request",__tgt__="年代") <0.6>;
export request1_135=(哪一年|哪年)(唱|写)(的)?(这首)?(歌|歌曲|音乐|曲子)   => request(__act__="request",__tgt__="年代") <0.6>;
export request1_136=(什么|哪个)(时候|年代)(的)   => request(__act__="request",__tgt__="年代") <0.1>;

##----request两个tgt----######

#request--是**还是**
export request10_1=是(${歌手名})(唱|演唱)?的(歌|歌曲|曲子|音乐)?(还是)(${歌手名})(唱|演唱)?的(歌|歌曲|曲子|音乐)?  => request(__act__="request",__tgt__="歌手名",歌手名="") <0.7>;
###for tengxun
export request1_2=这个(歌|曲子|音乐|歌曲)?(叫|是)(啥|什么)=> request(__act__="request",__tgt__="歌曲名",歌曲名="") <0.3>;


###add by caixiang for tx2.1
export request_tx21_00=(${播放})(和|同|与|跟)?(${当前歌曲})(风格|曲风|类型)?(类似的|相似的)(${对象})(${语气词})?$ => request(操作="$1",__act__="request",__tgt__="相似歌曲",歌曲名="$3",主题="")<0.71>;
export request_tx21_00=(${播放})(和|同|与|跟)?(这个)(风格|曲风|类型)?(类似的|相似的)(${对象})(${语气词})?$ => request(操作="$1",__act__="request",__tgt__="相似歌曲",歌曲名="current",主题="")<0.71>;
export request_tx21_01=(${播放})(风格|曲风|类型)?(类似的|相似的)(${对象})(${语气词})?$ => request(操作="$1",__act__="request",__tgt__="相似歌曲",主题="")<0.71>;
export request_tx21_02=(${播放})(和|同|与|跟)?(${歌曲名})(风格|曲风|类型)?(类似的|相似的)(${对象})(${语气词})?$ => request(操作="$1",__act__="request",__tgt__="相似歌曲",歌曲名="$3",主题="")<0.71>;
export request_tx21_03=(${播放})(的)?(${当前歌曲})(不是)(${music_版本})(的)?(${mu_版})?(${语气词})?$ => request(操作="$1",__act__="deny",歌曲名="$3",版本="$5")<0.71>;
export request_tx21_03=(${播放})(的)?(这个)(不是)(${music_版本})(的)?(${mu_版})?(${语气词})?$ => request(操作="$1",__act__="deny",歌曲名="current",版本="$5")<0.71>;
export request_tx21_04=(${播放})(的)(不是)(${music_版本})(的)?(${mu_版})?(${语气词})?$ => request(操作="$1",__act__="deny",版本="$4")<0.71>;
export request_tx21_05=^(${当前歌曲})?(不是)(${music_版本})(的)?(${mu_版})?(${语气词})?$ => request(__act__="deny",版本="$3",歌曲名="$1")<0.71>;
export request_tx21_05=^(这个)?(不是)(${music_版本})(的)?(${mu_版})?(${语气词})?$ => request(__act__="deny",版本="$3",歌曲名="current")<0.71>;
export request_tx21_05=^(${当前歌曲})?(不是)(原唱)(的)?(${mu_版})?(${语气词})?$ => request(__act__="deny",版本="原唱",歌曲名="$1")<0.712>;
export request_tx21_05=^(这个)?(不是)(原唱)(的)?(${mu_版})?(${语气词})?$ => request(__act__="deny",版本="原唱",歌曲名="current")<0.712>;
export request_tx21_06=^(你)?(${播放})错了$ => request(__act__="deny",操作="$2",歌曲名="@")<0.71>;
####

# inform_bug
#export inform_bug1=^(${播放})(${整数}|几)?(首|曲|支|个)(${歌曲名})$=> request(__act__="inform",__tgt__="") <0.61>;


