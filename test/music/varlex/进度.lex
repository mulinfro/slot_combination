export zongkong_back=^(${快进})一点点?儿?$ => request(进度="$1") <0.6>;
export zongkong_back=^(${快退})一点点?儿?$ => request(进度="$1") <0.6>;
export zongkong_back=^(${快进mix})$ => request(进度="$1") <0.6>;
export zongkong_back=^(${快退mix})$ => request(进度="$1") <0.6>;
export zongkong_back=^(${快进to})$ => request(进度="$1") <0.6>;
export zongkong_back=^(${快退to})$ => request(进度="$1") <0.6>;
export zongkong_back=^(快进)$ =>  request(进度="+") <0.6>;
export zongkong_back=^(快退)$ =>  request(进度="-") <0.6>;

#####add for tx 2.0 by jk
##export zongkong_1=(${快进}|${快退})到?(${歌曲结构})=> request(歌曲结构="$3",对象="$2",进度="$1") <0.5>;
export zongkong_2 = ^(跳过)(${歌曲结构}) => request(歌曲结构="$2",操作="跳过") <0.61>;
export zongkong_3 = ^我?(不要|别|不想)(播|放|播放|听)(${歌曲结构})$ => request(歌曲结构="$3",操作="跳过",歌曲名="@") <0.61>;
export sc_1=(${播放})(${_片长值})的?(歌|音乐|歌曲)$ => request(操作="$1",时长="$2") <0.6>;
export sc_2=(${播放})(${_片长值})(${歌手名})的?(歌|音乐|歌曲)$ => request(操作="$1",时长="$2",歌手名="$3") <0.6>;
export sc_3=(${播放})(${_片长值})(${排行榜})的?(歌|音乐|歌曲)$ => request(操作="$1",时长="$2",排行榜="$3") <0.6>;
export sc_4=(来|听|${播放})(${_片长值})(.{2,10})的?(歌|音乐|歌曲)$ => request(时长="$2") <0.6>;
