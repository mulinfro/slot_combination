#default_opt=(放|播放|播|放些|放一些|放点|放一点|放首|放一首|放两首|放几首|播些|播一些|播点|播一点|播首|播一首|播一首|播两首|播几首|来些|来一些|来点|来一点|来首|来一首|来两首|来几首|点|点些|点一些|点首|点一首|点两首|点几首|听些|听一些|听点|听一点|听首|听一首|听两首|听几首|我想听|我要听|帮我放|给我放|替我放|听一听)(首|一首|一下|个|一个|下)?(那个)?;
dis_word=放|播放|播|放些|放一些|放点|放一点|放首|放一首|放两首|放几首|播些|播一些|播点|播一点|播首|播一首|播一首|播两首|播几首|来些|来一些|来点|来一点|来首|来一首|来两首|来几首|点|点些|点一些|点首|点一首|点两首|点几首|听些|听一些|听点|听一点|听首|听一首|听两首|听几首|我想听|我要听|帮我放|给我放|替我放|给我搜|找|搜索|搜下|找下|搜索下|搜一下|找一下|搜索一下|搜些|找些|搜索些|搜一些|找一些|搜索一些|来个|来一个|放个|放一个|播个|播一个|播放个|播放一个|点个|点一个|听个|听一个|有没有|有|你有没有|请问有没有|请问有没|请问你有没有|请帮我|请给我|请替我|请|麻烦|烦请|麻烦帮我|麻烦给我|麻烦替我|烦请帮我|烦请替我|烦请给我|我需要|我想|我想要;
default_opt=(放|播放|播|来些|来一些|来点|来一点|来首|来一首|来两首|来几首|点|听|听一听)(首|一首|一下|个|一个|下|些|一些|两首|几首|点|一点|搜)?(那个)?;
default_optall=(放|播放|播|放些|放一些|放点|放一点|放首|放一首|放两首|放几首|播些|播一些|播点|播一点|播首|播一首|播一首|播两首|播几首|来些|来一些|来点|来一点|来首|来一首|来两首|来几首|点些|点一些|点首|点一首|点两首|点几首|听些|听一些|听点|听一点|听首|听一首|听两首|听几首|我想听|我要听|帮我放|给我放|替我放|听一听)(首|一首|一下|个|一个|下|点|一点)?(那个)?;
default_obj=(所有|全部)?(歌|音乐|歌曲|主题曲|插曲|片头曲|片尾曲|配乐|曲子|专辑|单曲|小曲);
default_objall=(所有|全部)?(歌|音乐|歌曲|主题曲|插曲|片头曲|片尾曲|配乐|曲子|专辑|单曲|小曲);

export default0 = (${default_optall})(${歌手名})?的?(好听|超级好听|超好听)?(点|一点)?的(${default_obj})(${语气词})?$ => request(keyword="") <0.8>;
####add 歌手们+声音白噪声结尾的keyword捞出有问题
export default2 = (${default_opt})(${歌手名})(唱|演唱)?的(声音|白噪声|白噪音)(${语气词})?$ => request(keyword="") <0.4>;

if not 歌曲名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别 and not 乐器 and not 排行榜 and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__ and not actflag  and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 适用人名 then
    export default1 = (${default_opt})(${歌手名})(唱|演唱)?的.(${default_obj})(${语气词})?$ => request(keyword="") <0.41>;
    export default1 = (${default_opt})(${歌手名})(唱|演唱)?的(.{2,10})(${default_obj})(${语气词})?$ => request(keyword="$4") <0.4>;
end

if not 对象 and not 歌曲名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别 and not 乐器 and not 排行榜 and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__ and not actflag  and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 适用人名 then
    export default2 = (${default_opt})(${歌手名})(唱|演唱)?的.(${语气词})?$ => request(keyword="") <0.31>;
    export default2 = (${default_opt})(${歌手名})(唱|演唱)?的(.{2,10})(${语气词})?$ => request(keyword="$4") <0.3>;
end

if not 歌手名 and not 歌曲名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别  and not 乐器  and not 排行榜  and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__  and not actflag and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 适用人名 then
    export default3 = (${default_opt})(.{1,10})(唱|演唱)?的(${default_obj})(${语气词})?$ => request(keyword="$2") <0.2>;
    export gedan0=(${default_optall})(我的)(的|这个)?歌单(${语气词})?$ => request(keyword="") <0.211>;
    export gedan1=(${default_optall})(名字是|歌单名是)?(.{2,10})(的|这个)?歌单 => request(keyword="$3") <0.3>;
    export gedan2=(${default_optall})(.{2,10})的?歌单里的(歌|音乐)? => request(keyword="$2") <0.3>;
    export gedan3=(${default_optall})歌单(名字是|歌单是|歌单名是)(.{2,10}) => request(keyword="$3") <0.31>;
    export default3_1 = (${music_查找}|${播放1})(.{2,10})(唱|演唱)?的(${default_obj})(${语气词})?$ => request(keyword="$2") <0.22>;
    export default3_2 = (${default_opt})(${_片长值})(.{2,10})(唱|演唱)?的(${default_obj})(${语气词})?$ => request(keyword="$3") <0.2>;
    ##export default3 = (${default_optall}).(唱|演唱)?的(${default_obj})(${语气词})?$ => request(keyword="") <0.21>;

end

if not 对象 and not 歌曲名 and not 歌手名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别  and not 乐器  and not 排行榜  and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__  and not actflag and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 声音类型 and not 适用人名 then
    export default4 = (我想听|我要听|播放|我想听一听)(首|一首|一下|个|一个|下|些|一些|点|一点)?(来听|来听下|来听一下)(${语气词})?$ => request(keyword="") <0.3>;
    export default4 = (我想听|我要听|播放|我想听一听)(首|一首|一下|个|一个|下|些|一些|点|一点)?(${主题类型})(${语气词})?$ => request(keyword="") <0.3>;
    export default4 = (我想听|我要听|播放|我想听一听)(首|一首|一下|个|一个|下|些|一些|点|一点)?(.{2,10})(${语气词})?$ => request(keyword="$3") <0.1>;
    ##export default5 = (${句首修饰词})?(${播放})?(电影|电视剧|电视)?(.{2,10})(的|里的|里面的|里头的|节目的|节目里的|节目里面的|节目里头的)?(主题歌|主题曲|插曲|配乐|片头曲|片尾曲|歌|歌曲|音乐)(${语气词})? => request(keyword="$4") <0.2>;
    ##export default6 = (${句首修饰词})?(${播放})(我的|QQ音乐|我的QQ音乐)?歌单(名字是|歌单是|歌单名是|歌单名字是)?(.{1,10})(${语气词})? => request(keyword="$5") <0.2>;
    ##export default7 = (${句首修饰词})?(${播放})(名字是|歌单名是|歌单名字是|我的|QQ音乐|我的QQ音乐)?(.{2,10})(的|这个|那个)?歌单(${语气词})? => request(keyword="$4") <0.1>;
end

if not 歌曲名 and not 歌手名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别  and not 乐器  and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__  and not actflag and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 声音类型 and not 适用人名 and not 排行榜 then
    export default5_1 = ^(${句首修饰词})?(${播放})(电影|电视剧|电视)?(.{1,10})(的|里的|里面的|里头的|节目的|节目里的|节目里面的|节目里头的)?(主题歌|主题曲|插曲|配乐|片头曲|片尾曲|歌|歌曲|音乐)(${语气词})?$ => request(keyword="$4") <0.2>;
    export default5_2 = ^(${句首修饰词})?(${播放})?(电影|电视剧|电视)(.{1,10})(的|里的|里面的|里头的|节目的|节目里的|节目里面的|节目里头的)?(主题歌|主题曲|插曲|配乐|片头曲|片尾曲|歌|歌曲|音乐)(${语气词})?$ => request(keyword="$4") <0.2>;
    export default6 = ^(${句首修饰词})?(${播放})(我的|QQ音乐|我的QQ音乐)?歌单(名字是|歌单是|歌单名是|歌单名字是|名是)?(.{1,10})(${语气词})?$ => request(tailkeyword="$5") <0.2>;
end
if not 歌曲名 and not 歌手名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别  and not 乐器  and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__  and not actflag and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 声音类型 and not 适用人名 then
    export default7 = ^(${句首修饰词})?(${播放})(名字是|歌单名是|歌单名字是|我的|QQ音乐|我的QQ音乐)?(.{1,10})(的|这个|那个)?歌单(${语气词})?$ => request(keyword="$4") <0.1>;
end
if not keyword and not 歌曲名 and not 歌手名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别  and not 乐器  and not 语种 and not 主题  and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__  and not actflag and not 音乐场景 and not keywordflag and not 歌曲结构 and not 适用人群 and not 应用名 and not 声音类型 and not 适用人名 and not 排行榜 and not 歌曲数量 then
    export default9 = ^(${句首修饰词})?(${播放})(我的|QQ音乐|我的QQ音乐)?歌单(名字是|歌单是|歌单名是|歌单名字是|名是)?(.{1,10})(${语气词})? => request(tailkeyword="$5") <0.01>;
    export default8 = (${句首修饰词})?(${播放}|切换)?(电影|电视剧|电视)?(.{1,10})(的|里的|里面的|里头的|节目的|节目里的|节目里面的|节目里头的)?(主题歌|主题曲|插曲|配乐|片头曲|片尾曲|歌|歌曲|音乐)(${语气词})?$ => request(headkeyword="$4") <0.01>;
end
