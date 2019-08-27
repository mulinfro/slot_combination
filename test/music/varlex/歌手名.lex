export singer1=(${操作})(${歌手名})的?(${歌曲名}) => request(歌手名="$2",歌曲名="$3",适用年龄="") <0.4>;
export singer111111111=(${操作}|想听|要听)(${歌手名})(唱?的|演唱的)(歌|歌曲|音乐|歌谣|曲子|小曲|儿歌|童谣)(${语气词}|好吗|行吗|可以吗|可不可以|行不行)?$ => request(歌手名="$2"适用年龄="") <0.4>;
export singer12=(想听|要听|${来首}|播放)(${歌手名})的(歌|歌曲|音乐)(${语气词})$ => request(歌手名="$2",歌曲名="",__act__="inform",__tgt__="") <0.6511>;
export singer121=^(我|我们|给我|给我们|帮我|帮我们)?(想听|要听|${来首}|播放|放|播)(${歌手名})(唱|演唱)?的(歌|歌曲|音乐)$ => request(歌手名="$3",歌曲名="@",__act__="inform",__tgt__="") <0.90>;

## by zhangyu, 2018-07-02, 全量说法的支持
export singer122=^(${语气词}|那个|就是|就是那个|是|那)?(${歌手名})的(歌|歌曲|音乐|曲子)(给|给我|给我们|帮我|帮我们)?(来|播|放|播放)(一|几|两|俩)?(个|首)(${语气词})?$ => request(歌手名="$2",歌曲名="@",__act__="inform",__tgt__="") <0.7>;
export singer122_1=^(${语气词}|那个|就是|就是那个|是|那)?(我|我们|给我|给我们|帮我|帮我们)?(想听|要听|${来首}|播放|放|播)(${歌手名})(唱|演唱)?的(${音乐类型})(${语气词})?$ => request(歌手名="$4", 歌曲名="@", __act__="inform", __tgt__="", 音乐类型="$6") <0.7>;

## by zhangyu, 2018-07-02, 丰富歌手名说法
export singer12_1 = (${歌手名})的(${音乐类型}) => request(歌手名="$1", 音乐类型="$2") <0.15>;
export singer12_2 = (${歌手名})的(${对象})(${歌曲名}) => request(歌手名="$1", 对象="$2", 歌曲名="$3") <0.31>;

export singer10=(${歌手名})的(单曲|歌曲) => request(歌手名="$1") <0.1>;
export singer12=(${歌手名})(唱的|的歌|的音乐) => request(歌手名="$1") <0.1>;

export singer13=(${歌手名})的?(${歌曲名}) => request(歌手名="$1",歌曲名="$2") <0.39>;
export singer14=(${歌曲名})(${歌手名}) => request(歌手名="$2",歌曲名="$1") <0.3>;
export singer15=(${歌手名})的 => request(歌手名="$1") <0.1>;
export singer16=(${歌手名})(${语气词})?$ => request(歌手名="$1") <0.07>;
export singer17=(${歌手名}) => request(歌手名="$1") <0.05>;



singerlabel_or1=(或|或者)(${歌手名}) => (_or,item="$2");
singerlabel_or2=(${歌手名})(唱的|的歌|的歌曲)?(${singerlabel_or1}+) => (_logical,item1="$1",item2="$3");
export 歌手名10=(${singerlabel_or2}) => request(歌手名="$1") <0.4> ;

singerlabel_and1=(和|与|跟)(${歌手名}) => (_and,item="$2");
singerlabel_and2=(${歌手名})(${singerlabel_and1}+)(唱的|合唱的|一起合?唱|的合唱|合作|一起合作)? => (_logical,item1="$1",item2="$2");
export 歌手名11=(${singerlabel_and2}) => request(歌手名="$1") <0.4> ;

###add by xuyang 调低没有连接词的两个歌手的概率
singerlabel_and11=(${歌手名}) => (_and,item="$1");
singerlabel_and22=(${歌手名})(${singerlabel_and11}+)(唱的|合唱|一起合?唱|的合唱|合作|一起合作|唱)? => (_logical,item1="$1",item2="$2");
export 歌手名111=(${singerlabel_and22}) => request(歌手名="$1") <0.1> ;
export 歌手名111=(${singerlabel_and22})的(${歌曲名}) => request(歌手名="$1") <0.4> ;
export 歌手名111=(${singerlabel_and22})的(${对象}) => request(歌手名="$1") <0.4> ;
###add by xuyang 调低没有连接词的两个歌手的概率


singerlabel_not1=(不是|不要|不是要|不想要|别听|不听|不想听)听?(${歌手名})的?(歌|歌曲)? => (_not,item="$2");
singerlabel_not2=我?是?(是|要|听|想听|有没有)听?(${歌手名}).*(${singerlabel_not1}) => (_logical,item1="$2",item2="$3");
singerlabel_not3=我?(${singerlabel_not1}).*(是|要|听|想听|有没有)听?(${歌手名}) => (_logical,item1="$3",item2="$1");
export 歌手名12=(${singerlabel_not2}) => request(歌手名="$1",__act__="inform",__tgt__="") <0.4>;
export 歌手名13=(${singerlabel_not3}) => request(歌手名="$1",__act__="inform",__tgt__="") <0.4> ;

singerlabel_not4=(有没有)(不是)(${歌手名}) => (_not,item="$3");
singerlabel_not5=(有)(不是)(${歌手名})的吗 => (_not,item="$3");
export 歌手名14=(${singerlabel_not4}|${singerlabel_not5}) => request(歌手名="$1",__act__="inform",__tgt__="") <0.4> ;
##add by hcx
export singer16=(${下一首4})(${歌手名})(的|唱的|演唱的)(${音乐}) => request(操作="$1",歌手名="$2",对象="$4") <0.5> ;
###add by jk for bug
export singer17=^(${播放})(歌手)?(${歌手名})(唱的|的歌|的歌曲|唱的歌)?(${歌曲名})?(${语气词})?$ => request(操作="$1",歌手名="$3",主题="@") <0.5> ;

### by zhangyu, 2019-08-12
export singer_bug_zy1 = ^(${句首修饰词})?(${播放})(歌手)?(${歌手名})(唱|演唱)?的?(这一?个|这一?首|这一?曲|这)(${音乐})(${语气词})?$ => request(歌手名="$4", 歌曲名="@") <0.41>;
export songname_bug_zy1 = ^(${句首修饰词})?(${播放})(${歌曲名})的?(这一?个|这一?首|这一?曲|这)(${音乐})(${语气词})?$ => request(歌曲名="$3") <0.51>;


## "SHE" 特殊处理
export singer_bug_zy3 = ^(${句首修饰词})?听(下|一下|一首|一曲)?(SHE|she|S H E)的?(${音乐})?(${语气词})?$ => request(操作="收听",歌曲名="@",歌手名="SHE") <0.811>;

