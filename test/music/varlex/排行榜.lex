#export ranking1=(${排行榜}) => request(排行榜="$1") <0.21>;
export ranking2=(${歌手名})(的|唱的|演唱的)?(${排行榜}) => request(排行榜="$3") <0.1>;
export ranking30=(${排行榜})的?(排行榜)?(里|中)?的(${对象}) => request(排行榜="$1") <0.1>;
export ranking3=(${歌手名})的新的?(${对象}) => request(排行榜="最新",对象="$2") <0.8>;
export ranking3=(有哪些|有什么|有啥|想听|要听|播放|${来首}|听下|听听|听一下|放点|放一点|放些|放一些)新的?歌 => request(排行榜="最新") <0.8>;
export ranking3=(有哪些|有什么|有啥)新的?(${对象}) => request(排行榜="最新") <0.8>;
export ranking3=(${语种})的?新的?(${对象})(${语气词})?$ => request(排行榜="最新",对象="$2") <0.8>;
export songname39=(听|${来首}|播|放)(一下|下)?(目前|现在|最近)?(${排行榜})的(歌|歌曲|音乐|${对象})$ => request(排行榜="$4",歌曲名="") <0.8>;
export ranking3=[^(清)]新的(歌|单曲) => request(排行榜="最新") <0.1>;
export ranking3=^新的(歌|单曲) => request(排行榜="最新") <0.1>;
export ranking3=(${排行_最热})的(歌|单曲) => request(排行榜="$1") <0.1>;
export ranking3=(歌|歌曲|音乐)(最近)(新|刚)出来的 => request(排行榜="最新") <0.1>;
export ranking3=[^(清)](新|新出)的?(歌|歌曲|曲子|单曲)$ => request(排行榜="最新") <0.1>;
export ranking3=^(新|新出)的?(歌|歌曲|曲子|单曲)$ => request(排行榜="最新") <0.1>;
#export ranking3=(歌|歌曲|曲子|单曲)(刚出来的|最新|最近|新出的|最近新出的|最近出来的|最新的排行榜|刚出来的|刚发行的) => request(排行榜="最新") <0.1>;
export ranking3=热歌$ => request(排行榜="最热") <0.1>;
export ranking31=(${操作})(${对象})(排行榜)?(里|中)?(${排行榜})的$ => request(排行榜="$5") <0.1>;

##### by zhangyu #####
export paihangbang1_1 = (放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲)(${排行榜})(里|里面|中)?的?(排|排行|排名)?(第)(${整数})(名|个|位)?(的)(歌|歌曲|音乐|曲子|曲儿|${对象}) => request(排行榜="$4", 序列号="$8") <0.5>;
export paihangbang2_1 = (放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲)(${排行榜})(里|里面|中)?(的)(歌|歌曲|音乐|曲子|曲儿|${对象}) => request(排行榜="$4") <0.35>;

export paihangbang3_1 = (${排行榜})(里|里面|其中|中)?(的)?(${歌手名})(的)(歌|歌曲|音乐|乐曲|曲子|曲儿|${对象}) => request(排行榜="$1", 歌手名="$4") <0.4>;

export paihangbang4_1 = (${排行榜})(里|里面|其中|中)(的)?(${乐器}|${语种}|${年代})?(的)?(歌|歌曲|音乐|曲子|曲儿|曲|新歌|老歌|${对象}) => request(排行榜="$1") <0.3>;

export paihangbang5_1 = (放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲|些)(${排行榜})的$ => request(排行榜="$4") <0.5>;
export paihangbang5_122 = (放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐|${来首})(${对象})?(${排行榜})的$ => request(排行榜="$3") <0.5>;
export paihangbang5_1333=(放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲|些)?(${排行榜})的(歌|歌曲|音乐|曲子|曲儿|${对象})? => request(排行榜="$4") <0.3>;
export paihangbang5_1444=(放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲|些)?(歌|歌曲|音乐|曲子|曲儿|${对象})(${排行榜})的?=> request(排行榜="$5") <0.3>;
export paihangbang5_1555=(最近|近期|近来)?有?(什么|哪些|啥)(歌|歌曲|音乐|曲子|曲儿|${对象})(${排行榜})的? => request(排行榜="$5") <0.3>;
热门2=(放|听|播|播放|点|唱)(的|得);
热门1=(${热门2})?(比较|最|超级|很)?(多|火|热|热门|流行)=>("最热");
export paihangbang5_2=(最近|近期|近来|现在)?有?(什么|哪些|啥)(歌|歌曲|音乐|曲子|曲儿|${对象})(大家)?(${热门1}) => request(排行榜="$5") <0.3>;
export  paihangbang5_3=(最近|近期|近来|现在)?(大家)?(${热门1})的(歌|歌曲|音乐|曲子|曲儿|${对象})(是什么|是啥|有啥|有什么|有哪些|是哪些)=> request(排行榜="$3",音乐类型="") <0.3>;
export paihangbang5_4=(最近|近期|近来|现在)?有?(什么|哪些|啥)(歌|歌曲|音乐|曲子|曲儿|${对象})(最近|近期|近来)?(${热门1})=> request(排行榜="最热",音乐类型="") <0.3>;
export paihangbang5_5=(${操作})(热歌)?排行榜(的|得)?(歌|歌曲|音乐|曲子|曲儿|${对象})? => request(排行榜="最热") <0.3>;
export paihangbang5_5=(大家|全国)?(${热门2})(次数)?(比较|最|超级)(多|火|热|热门)(的|得)?(歌|歌曲|音乐|曲子|曲儿|${对象})?=> request(排行榜="最热") <0.3>;
export paihangbang5_5=(放|播放|播|演唱|听)(${.music_排行榜})$ => request(排行榜="$2") <0.01>;
export paihangbang5_61=(放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲|些)?(热歌排行榜) => request(排行榜="最热") <0.31>;
export paihangbang5_62=(放|播放|播|来|唱|演唱|歌唱|听|点|找|推荐)(几|${整数}|两|一)?(首|支|个|曲|些)?(${排行榜}) => request(排行榜="$4") <0.31>;
export paihangbang5_7=(${播放}|${m来些2})(热歌)?排行榜(的|得)?(歌|歌曲|音乐|曲子|曲儿|${对象})? => request(排行榜="最热") <0.3>;

##by jk
export paihangbang6_1=^(${排行榜})(的|得)?(歌|歌曲|音乐|曲子|曲儿|${对象})?$ => request(排行榜="$1") <0.3>;
export paihangbang6_2=(${排行榜})(的|得)?(歌|歌曲|音乐|曲子|曲儿|${对象}) => request(排行榜="$1") <0.3>;
export paihangbang6_3=(歌|歌曲|音乐|曲子|曲儿|${对象})(${排行榜})(的|得)? => request(排行榜="$2") <0.3>;
export paihangbang6_4=(${语种})(歌|歌曲|音乐|曲子|曲儿|${对象})(${语气词})?(${排行榜})(的|得)?(${语气词})?$ => request(排行榜="$4") <0.1>;
export paihangbang6_4=(${排行榜})(的|得)?(${语种})(歌|歌曲|音乐|曲子|曲儿|${对象})(${语气词})?$ => request(排行榜="$1") <0.1>;

## by zhangyu, 2019-08-12
export paihangbang7_1 = (${排行榜})(的|得)?(${音乐类型})版?的?(${音乐}) => request(排行榜="$1") <0.1>;


