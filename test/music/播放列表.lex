播放列表1=(频道|列表|播放列表)(.+) => ("$2");
播放列表2=(.+)(频道|列表|播放列表) => ("$1");
export 列表1=(${播放列表1})(里的|里面的|内的|中的) => request(播放列表="$1") <0.31>;#,crfflag="0"
export 列表2=(${播放列表1})(里的|里面的|内的|中的)? => request(播放列表="$1") <0.31>;#,crfflag="0"


#export 列表2=(${整数}) => request(列表="$1") <0.18>;

#播放列表3=(频道|列表|播放列表)(${整数}) => ("$2");
#播放列表4=(${整数})(频道|列表|播放列表) => ("$1");
#export 列表4=(${播放列表3})(里的|里面的|内的|中的) => request(播放列表="$1") <0.31>;
#export 列表4=(${播放列表3})(里的|里面的|内的|中的)?$ => request(播放列表="$1") <0.31>;
export 列表3=(我要|我想|给我)?(播放|听|播|放|切换)(一下)?(${播放列表2})=> request(播放列表="$4") <0.3>;#,crfflag="0"


#export 列表3=(我要|我想|给我)?(播放|听|播|放|切换)(一下)?(${播放列表4})=> request(播放列表="$4") <0.3>;
export 列表3=^(${播放列表2})$=> request(播放列表="$1") <0.2>;#,crfflag="0"
#export 列表3=^(${播放列表4})$=> request(播放列表="$1") <0.2>;
export 操作1=^(${操作})$=> request(播放列表="") <0.4>;

export 列表3=^(帮我|给我|替我|我要|请|我想)?(换|切|切一下|换|换个|切换)(频道)$=> request(播放列表="") <0.3>;
听一首=听(${整数}|几)?(首|曲|些|点|支)?;

export 操作1=(${操作}|${听一首})(${歌手名})(的|唱的|演唱的)(${歌单})=> request(播放列表="") <0.5>;
export 操作1=(${歌手名})(的|唱的|演唱的)(${歌单})$=> request(播放列表="") <0.4>;
export 操作1=(${操作}|${听一首})(${歌单})(${歌手名})(的|唱的|演唱的)=> request(播放列表="") <0.4>;

