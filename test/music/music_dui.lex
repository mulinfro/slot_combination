#include "${pwd}/../../misc/num.lex"
#include "${pwd}/../../post/进度.lex"
#include "${pwd}/../../misc/time.3part.lex"
#include "${pwd}/../../post/片长.3part.lex"
#include "${pwd}/../../misc/date_pastaddnearby.lex"
句首修饰词=我想|我要|我想要|我需要|我希望|帮忙|帮我|替我|给我|为我|请|请给我|请帮我|请为我|请替我|麻烦|麻烦给我|麻烦帮我|麻烦为我|麻烦替我|请你|你帮我|你替我|你给我|你为我|麻烦你|我们想|我们要|我们想要|我们需要|我们希望|帮我们|替我们|给我们|为我们|请给我们|请帮我们|请为我们|请替我们|麻烦给我们|麻烦帮我们|麻烦为我们|麻烦替我们|你帮我们|你替我们|你给我们|你为我们|帮忙|请帮忙|麻烦请|请麻烦|我想我要|我要帮我|帮我替我|我想要给我;
##%merge=声音类型;
歌曲名other=.+;
当前歌曲=(这个|这首|这|当前)(歌|歌儿|曲子|音乐|歌曲)=>("current");
歌曲名=${.music_歌曲名}|${.music_歌曲名_xiqu}|挺好|看我的|${.music_英文歌曲}|${当前歌曲}|${.music_歌曲名_del的}|${.music_儿歌};


hot歌曲名=${.hot_歌曲名}|${.music_儿歌};


歌手名=${.music_歌手名}|林侑嘉|${.music_英文歌手};
单字歌名=${.music_单字歌名}|${.music_单字儿歌名};
女歌手=女声|女生|女歌手|女人 =>("女生");
男歌手=男生|男声|男歌手|男人 =>("男生");
歌手性别=${女歌手}|${男歌手};
#歌手性别=${.music_歌手性别};
语气词=(呢|吗|呀|啊|吧|哟|好吗|可以吗|行吗|行不|谢谢|呜|哇|咯|噢|么|呜|唉|唔|呗|呵呵|哈哈|嗯|呃|嘛|哦|呐|哎|啦|了|诶|好了)+;
######场景
场景=${.music_场景};
#场景=游戏|${场景_健身}|${场景_阅读}|胎教|${场景_工作}|瑜伽|广场舞|跳舞|${场景_睡觉};
######适用人群
music_适用人群1=(小婴儿|婴儿) => ("婴儿");
music_适用人群2=(幼儿|儿子|女儿);
music_适用人群3=(小孩子|小孩儿|小朋友|小孩|孩子|儿童) => ("小孩");
music_适用人群4=(宝宝|小宝贝|宝贝|比比|BABY|小BABY) => ("宝宝");
宝宝=(幼儿园|小班|中班|大班)?(${music_适用人群1}|${music_适用人群2}|${music_适用人群3}|${music_适用人群4});
适用人群1=${宝宝};
######适用年龄
适用年龄1=(${整数})(岁半?|个?月) =>(_join,prefix="$1",mid="$2");
适用年龄2=(${适用年龄1})(${整数})(个?月)=>(_join,prefix="$1",mid="$2",suffix="$3");
适用年龄3=(${整数})(个?周|个?星期|个?礼拜|天)=>(_join,prefix="$1",mid="$2");
适用年龄=${适用年龄1}|${适用年龄2}|${适用年龄3};
######
#适用年龄1=(${整数}|半)(岁|月);
#适用年龄2=(${整数})岁(半|零?${整数}个?月);
#适用年龄3=${整数}(个)?(周|星期|礼拜|天);
lx_乡村=(乡村|乡村的|乡村类型|乡村类型的|乡村风格|乡村风格的|COUNTRYMUSIC) =>("乡村");
lx_beatbox=(BEATBOX|BBOX) => ("BEATBOX");
lx_SOUL=(灵魂乐|SOUL乐|SOUL音乐) => ("SOUL");
lx_dj=(喊麦|喊麦的|MC喊麦|MC喊麦的) => ("喊麦");
lx_交响乐=(交响乐|交响曲|管弦乐|交响音乐) => ("交响乐");
lx_草原=(草原|草原的|草原风|草原风的|草原类型的) => ("草原");
#lx_说唱=(中文说唱|中文说唱的|中文RAP|中文RAP的|中文饶舌|中文饶舌的|说唱|说唱的|RAP|RAP的|饶舌|饶舌的) => ("说唱");
lx_说唱=(说唱|说唱的|RAP|RAP的|饶舌|饶舌的) => ("说唱");
lx_圆舞曲= (圆舞曲|华尔兹|圆舞曲音乐|华尔兹音乐) => ("圆舞曲");
lx_朋克=(朋克|PUNK|朋克乐|朋克音乐|PUNK音乐|PUNK乐) => ("朋克");
lx_黑人=(黑人音乐|黑人歌曲|黑人的歌|黑人的音乐|黑人的歌曲|黑人唱的歌|黑人唱的歌曲|黑人唱的音乐|黑人) =>("黑人");
lx_基督=(基督教音乐|基督教歌曲|基督教的音乐|基督教的歌|基督教的歌曲|唱诗班音乐|唱诗班歌曲|基督) => ("基督教音乐");
#zt_女生民谣=(女生唱的民谣|女生的民谣|女声唱的民谣|女声的民谣|女生民谣) => ("女生民谣");
lx_和声=(纯人声|和声|和声版本) => ("和声");
######音乐类型
音乐类型1=(串烧|乡村|原声带|原声带摇滚|另类|合唱|嘻哈|婚礼|弹唱|朋克|清唱|爵士|经典|世界经典|翻唱|蓝调|说唱|中国风|中华风|古典|草原|现代|流行|电音|电子|新世纪|古风)(歌曲|歌|音乐|乐|曲)? => ("$1");
音乐类型2=(HIPHOP|MTV|RANDB|RAP|RB|R&B|RPA|SOLO|R AND B流行|陕西民歌|音乐剧|老歌|舞曲|美声|红歌|秦腔|苏格兰小调|男双对唱|男女合唱|男女对唱|男男合唱|男男对唱|祝酒歌|求爱歌|斗牛士舞曲|校园民谣|摇篮曲|摇篮歌|快歌|慢歌|情歌|客家山歌|山歌|山西民歌|大合唱|奏鸣曲|女女合唱|女女对唱|东北民歌|K歌经典|K歌经曲|K歌金曲|交响乐|三重奏|伴奏|圣经|水声|混音|热恋慢歌|独奏|布鲁斯|舞台|黄梅戏|昆曲|歌剧|豫剧|越剧|粤剧|戏曲|京剧|电子|恐怖灵异|民谣|二次元|JAZZ|POP|经典老歌|${lx_乡村}|情歌对唱|${lx_朋克}|ACG|雷鬼|${lx_beatbox}|${lx_SOUL}|${lx_dj}|${lx_交响乐}|${lx_草原}|${lx_说唱}|${lx_圆舞曲}|${lx_朋克}|${lx_黑人}|${lx_基督}|${lx_和声}) => ("$1");
HIGH歌=嗨|HIGH|喊麦|DJ =>("DJ");
神曲=神曲|奇葩|魔性 =>("神曲");
佛教歌曲=佛教音乐|佛歌|佛教歌曲|佛教|佛乐 =>("佛教");
儿童歌曲1=(儿童|小朋友|小孩|小孩子|小孩儿)的歌(曲)?;
儿童歌曲=儿歌|儿童歌|儿童歌曲|儿童音乐|童谣|儿童童谣|儿童歌谣|${儿童歌曲1} =>("儿歌");
军旅歌曲=军旅|军旅歌曲|军歌  =>("军旅");
民族歌曲=民族|民族歌曲|民族风  =>("民族");
爱情歌曲=爱情歌曲|爱情民谣|爱情老歌 =>("爱情");
网络歌曲=网络神曲|网络神曲|网络音乐 =>("网络歌曲");
##胎教歌曲=胎教|胎教歌|胎教音乐|胎教歌曲 =>("胎教");
轻声歌曲=轻声歌曲|轻声音乐|轻音乐 =>("轻音乐");
金属歌曲=重金属乐|重金属|重金属音乐|重金属歌曲|重音乐|金属|金属乐|金属歌曲|金属音乐 =>("金属乐");
摇滚歌曲=摇滚歌曲|摇滚音乐|摇滚|摇滚曲|摇滚乐 =>("摇滚");
摇篮歌曲=摇篮曲|摇篮歌|摇篮歌曲 =>("摇篮曲");
慢摇歌曲=慢摇|慢摇曲|慢摇歌曲|慢音乐 =>("慢摇");
藏族歌曲=藏族歌曲|藏族音乐|藏乐|藏歌  =>("藏族");
影视歌曲=影视歌曲|影视金曲|电影中?的?歌曲|电视剧的?歌曲|影视剧中?的?歌曲 =>("影视歌曲");
幼儿歌曲=幼儿音乐|幼儿歌曲|宝宝歌谣 =>("幼儿歌曲");
催眠歌曲=宝宝催眠曲|安眠曲|睡眠曲|催眠曲|催眠曲儿 =>("催眠曲");
纯音乐=没歌词的歌|纯音乐|没歌词的 =>("纯音乐");
收藏music=收藏的?(音乐|歌曲|歌|曲子|歌曲)  => ("收藏列表");
电子舞曲=EDM|电子舞曲 => ("电子舞曲");
音乐类型3=${佛教歌曲}|${军旅歌曲}|${民族歌曲}|${爱情歌曲}|${网络歌曲}|${轻声歌曲}|${金属歌曲}|${摇滚歌曲}|${摇篮歌曲}|${慢摇歌曲}|${藏族歌曲}|${影视歌曲}|${催眠歌曲}|${纯音乐}|${HIGH歌}|${神曲}|文艺|${电子舞曲};
zy快 = (快|快速) => ("快歌");
zy慢 = (慢|慢速) => ("慢歌");
音乐类型_快慢歌 = (${zy快}|${zy慢})(节奏)(的)?(歌|歌曲|音乐|曲子) => ("$1");
儿歌类型=${.music_儿歌类型};
音乐类型=${儿歌类型}|${音乐类型1}|${音乐类型2}|${音乐类型3}|${音乐类型_快慢歌}|胎教DJ|DJ儿歌|后摇;
##########语种
英文=(英语|英文|外文|外语|国外|英国|外国|不列颠|英格兰) =>("英文");
日文=(日语|日本|日文) =>("日文");
泰文=(泰语|泰文|泰国) =>("泰文");
法文=(法语|法文|法国) =>("法文");
粤语=(白话|粤语|粵语|广东话) =>("粤语");
华语=(中文|华语|中国|国语|汉语) =>("华语");
韩文=韩国|韩文|韩语 =>("韩文");
闽南语=闽南|闽南语 =>("闽南语");
拉丁=(拉丁|拉丁语|拉丁文|拉丁文的|拉丁语的) => ("拉丁");
德文=(德语|德文|德国|德语的|德文的|德国的) => ("德文");
俄语=(俄语|俄文|俄罗斯|俄语的|俄文的|俄罗斯的|俄国|俄国的) => ("俄语");
藏语=(藏语|西藏|藏语的|西藏的) => ("藏语");
西班牙语=(西班牙|西班牙语) => ("西班牙语");
意大利语=(意大利|意大利语) => ("意大利语");
印度语=印度语|印度 => ("印度语");
语种=${英文}|${日文}|${泰文}|${法文}|${粤语}|${华语}|${韩文}|丹麦语|俄语|克罗地亚语|匈牙利|台湾|台语|土耳其语|巴西葡萄牙语|希腊语|${意大利语}|挪威语|捷克语|斯洛伐克语|斯洛文尼亚语|日韩|欧美|波兰语|济南话|瑞典语|美国|芬兰语|荷兰语|藏族|${西班牙语}|越南|重庆|${闽南语}|阿拉伯语|香港|港台|内地|大陆|${拉丁}|${德文}|${俄语}|${藏语}|小语种|${印度语};
影视语种=(${语种})(歌舞里|影视剧|歌舞剧|电影里) => ("$1");
##############
#音乐类型=${.music_音乐类型}|布鲁斯|舞台;
#语种=${.music_语种};
m中文整数=${中文数1}|${中文数2}|${中文数字}|${中文十};
韩剧=(韩剧|韩剧的|韩剧里的|韩剧里面的)=>("韩剧");
#ms_哔哩哔哩=(BILIBILI|BILIBILI的配乐|BILIBILI的音乐|BILIBILI的BGM|BILIBILI的歌|BILIBILI的歌曲|BILIBILI最火的歌|BILIBILI最火的歌曲|BILIBILI最火的音乐)=>("哔哩哔哩");
ms_哔哩哔哩=(BILIBILI)=>("哔哩哔哩");
ms_背景音乐=(BGM|背景音乐|BGM音乐) => ("背景音乐");
zt_电影原声=(电影原声|电影里?) => ("电影原声");
zt_歌舞剧音乐=歌舞剧?里?(歌曲)?=>("歌舞剧音乐");
zt_影视歌曲=影视原声|影视歌曲|电视剧歌曲|电影歌曲|电影里的歌曲|影视剧歌曲|影视剧的歌曲|电影音乐|影视剧音乐|电视剧音乐|影视|影视剧|${zt_电影原声} => ("影视歌曲");
zt_格莱美=格莱美|格莱美获奖 => ("格莱美");
zt_基督=(基督教音乐|基督教歌曲|基督教的音乐|基督教的歌|基督教的歌曲|唱诗班音乐|唱诗班歌曲|基督) => ("基督教音乐");
zt_早晨=(清晨|清晨听的|早晨听的|早上听的|适合清晨听的|适合早晨听的|适合早上听的) => ("早晨");
zt_美剧=(美剧的|美剧里的|美剧里面的) => ("美剧");
zt_试音=(试音|煲机) => ("试音");
#zt_早晨=(清晨|清晨听的|早晨听的|早上听的|适合清晨听的|适合早晨听的|适合早上听的) => ("早晨");
#zt_基督=(基督教音乐|基督教歌曲|基督教的音乐|基督教的歌|基督教的歌曲|唱诗班音乐|唱诗班歌曲|基督) => ("基督教音乐");
#zt_黑人=(黑人音乐|黑人歌曲|黑人的歌|黑人的音乐|黑人的歌曲|黑人唱的歌|黑人唱的歌曲|黑人唱的音乐|黑人) =>("黑人");
#zt_女生民谣=(女生唱的民谣|女生的民谣|女声唱的民谣|女声的民谣|女生民谣) => ("女生民谣");
#zt_和声=(纯人声|和声|和声版本) => ("和声");
主题_部=(${.music_主题_del的}|${.music_影视名称}|${.music_主题})(第${m中文整数}部)?;
主题=(${.music_主题_del的}|${.music_影视名称}|${.music_主题})(第${m中文整数}季)?(第${m中文整数}期)?(第${m中文整数}集)?(第${m中文整数}场)?(第${m中文整数}节)?|${主题_部}|韩剧|纯人声|${ms_哔哩哔哩}|英剧|${zt_美剧}|${zt_试音}|${zt_影视歌曲}|${zt_格莱美}|${zt_歌舞剧音乐}|广告|中国新歌声|中国有嘻哈|明日之子|跨界歌王|中国情歌汇|金曲捞|歌手|我是歌手|中国好歌曲|中国好声音|天籁之战|梦想的声音|蒙面歌王|蒙面唱将猜猜猜|围炉音乐会;
主题类型=${.music_主题类型}|配乐|插曲|${ms_背景音乐};
乐器=${.music_乐器};
专辑名=${.music_专辑名}|${.music_儿歌专辑名};
清新风格=小清新|清新=>("小清新");
伤心=伤心|失恋=>("伤心");
fg_节奏感=(有节奏感的|节奏感强的|节奏感好的|节奏感强) =>("节奏感强");
武侠=(武侠|武侠剧的|武侠剧里的|武侠剧里面的|武侠风格的) =>("武侠");
fg_舒缓=(放松|舒缓|放松些|放松一些|舒缓些|舒缓一些) =>("舒缓");
fg_寂寞=(一个人听的|适合一个人听的|一个人的时候听的|适合一个人的时候听的|寂寞的|孤独的|孤单的) =>("寂寞");
fg_抒情=(抒情的|抒情些的|抒情一些的)=>("抒情");
fg_冷门=(小众|冷门) =>("冷门");
#fg_冷门=(冷门华语|冷门的华语|华语冷门|华语的冷门|小众华语|小众的华语|冷门国语|冷门的国语|国语冷门|国语的冷门|冷门) =>("冷门");
fg_治愈=治愈|治愈系 => ("治愈");
fg_性感=性感|SEXY|sexy => ("性感");
风格=(${.music_风格}|世界|亲热|生日|动漫|校园|温暖|郁闷|治愈系?|疲惫|青春|休闲|小清新|清新|伤心|失恋|${武侠}|${fg_舒缓}|${fg_寂寞}|${fg_节奏感}|${fg_抒情}|${fg_冷门}|${fg_治愈}|温馨|活泼|疗伤|${fg_性感}|调情)(一点|点|些|一些)? => ("$1");

##排行榜=${.music_排行榜};
######排行榜
排行_内地=(内地排行榜|内地音乐排行榜)=>("内地");
排行_港台=(港台排行榜|港台音乐排行榜|港台最火的|港台最热门的|港台最火的|港台最流行的|香港最火的|香港最热门的|香港最热的|香港最流行的|台湾最火的|台湾最热门的|台湾最热的|台湾最流行的)=>("港台");
排行_欧美=(欧美排行榜|欧美音乐排行榜)=>("欧美");
排行_公告牌=(美国公告牌|美国公告牌的|美国公告牌上的|公告牌|公告牌的|公告牌上的|BILLBOARDS|BILLBOARDS的|BILLBOARDS上的|美国BILLBOARDS|美国BILLBOARDS的|美国BILLBOARDS上的) =>("美国公告牌");
排行_最新=新|新出的|最近出的|刚出的|新发行的|最新|最近|新出的|最近新出的|最近出来的|最新的排行榜|刚出来|刚发行|刚刚出来|刚刚发行 =>("最新");
排行_最热=(最近|最近比较|比较|最)?(最热|最热门|最近流行|热门|最火|最近比较火|最近比较热门|最近比较热|排行榜最热|最热排行榜|排行榜最火|最热的排行榜|最火的排行榜|大家听得多|比较热|比较火|比较流行|听的最多|大家听的最多|最流行|热歌|热|热度最高) =>("最热");
####add by xuyang
排行_好听=(最近|最近比较|比较|最)?(好听|好听的|最好听|最好听的|好听点的) => ("好听");
排行_不好听=(最近|最近比较|比较|最)?(不好听|不好听的) => ("");
####add by xuyang
排行榜=${排行_最新}|${排行_最热}|${.music_排行榜}|${排行_内地}|${排行_港台}|${排行_欧美}|${排行_公告牌}|${排行_好听}|${排行_不好听};

#######年代
年代5=(五十年代|五零年代|五几年|五几年代) => ("五十年代");
年代6=(六十年代|六零年代|六几年|六几年代) => ("六十年代");
年代7=(七十年代|七零年代|七几年|七几年代) => ("七十年代");
年代8=(八十年代|八零年代|八几年|八几年代) => ("八十年代");
年代9=(九十年代|九零年代|九几年|九几年代) => ("九十年代");
年代0=(零零年代|零几年|零几年代) => ("零零年代");
年代10=(一零年代|幺零年代|一几年|一几年代|幺几年|幺几年代) => ("一零年代");
年代=零零后|七零后|八零后|九零后|${年代5}|${年代6}|${年代7}|${年代8}|${年代9}|${年代10}|${年代0};
遍数=(${整数})(遍|次) => ("$1");
音乐_APP=(QQ音乐|百度音乐|网易云音乐|酷我音乐|酷狗音乐|虾米音乐);
应用名=${.music_应用名};
音乐=歌曲|歌|音乐|MUSIC|曲子|虾米音乐|曲儿|歌谣|歌儿|乐曲 => ("音乐");
歌曲_这个=这首歌|这个歌|这歌|这支歌=>("音乐");
歌单=歌单|歌曲列表=> ("歌单");
代表作=成名作|代表作品|成名曲|成名作品|代表作|成名歌曲 =>("代表作");

## by zhangyu, 2019-04-03, aidui.0.3.0
## 新方案，配合“儿歌”领域，将“儿歌”、“幼儿歌曲”，从音乐类型搬迁到音乐对象里面去
对象=${音乐}|专辑|单曲|歌单|歌曲列表|${代表作}|CD|${儿童歌曲}|${幼儿歌曲};

###########操作
music_查找1=(找|搜|搜索|搜寻|查找)(一|几|两|${整数})?(个|点|首|曲|支|些|找|下|搜|段)? => ("查找");
##music_查找2=(找|搜|搜索|搜寻|查找) => ("查找");
music_查看 = 查看 => ("查找");
music_查=查一下|找|查看|查询|查询下|查询一下|查找|查|查下找找|查查|查一查 => ("查找");
music_听=听些|我想听|听听|听一下|听一听|听一个|听一些|听些|听个|听一点|听(一|几|两|${整数})?首 => ("收听");
musci_看看=(看|看一下|看下|我想知道|我想看|显示|知不知道|看一看|推荐|介绍) => ("");
music_查找=${musci_看看}|${music_查}|${music_听}|${music_查找1};
music_查找2=看|看一下|看下|我想知道|我想看|显示|查看|查询|查询下|查询一下|查找|找|找下|找一下|搜搜|查|查下|搜|搜下|搜一下|找找|查查|搜|找|知不知道|搜索|找几个|找一找|查一查|搜一搜|看一看|推荐|介绍|搜寻一下|查一下|搜寻|寻找;
music_发送=发送|发下|发一下|发送下|发送一下=>("发送");
来首=(听|来|放|播放|找|唱|点|播)(一|几)?(首|曲|支|些);
来首2=(听|来|放|播放|找|唱|点|播)(一|几|${整数})?(首|曲|支|些);
上一首1=(播放|重新播放|换成|换|切到|切|播|放|再|切换到|切换)?(上|前|上面|前面)一(曲|首|个|种|支) => ("上一首");
上一首2=上首|再上首|上个歌|上首歌|刚才那一?首|前边那一?首|刚刚那一?首 => ("上一首");
上一首=${上一首1}|${上一首2};
下一首=(播放|重新播放|换成|换|切到|切|播|放|再|切换|切换到)?(下|后|下面|后面)一(曲|首|个|种|支) => ("下一首");
下一首5=下一个|后一个|后面那个|后面一个|之后的|之后那个|之后一个|不是这首 => ("下一首");
下一首1=(换成|换|切到|切|切换)(一曲|一首|一个|个|曲|支|首|乐曲) => ("切换");
播放1=(放|播放|播|来|点)(一|几|两|${整数})?(个|点|首|曲|支|些) => ("播放");
播放2=(播放|放|播|放一下|放一个|播一个|播下|放下|播一下|播放一下|帮我放|给我放|替我放|播个)=>("播放");
播放_1=听点|听 => ("收听");
#播放_2=(给我|替我|帮我)?(${播放1}|插播|播|播报|播放|放|点播|开始播放|点) => ("播放");
播放_2=(${播放1}|插播|播|播报|播放|放|点播|开始播放|点) => ("播放");
#播放=(给我|替我|帮我)?(${播放1}|插播|播|播报|播放|放|点播|开始播放|点) => ("播放");
播放_3=(弄|整|来)(一个|一点|一些|一下|个|首|一首) => ("播放");
播放_4=整|弄 => ("");
播放5=(放|播|播放)(个|点|些|一些|一个|段|一段)=>("播放");
播放=${播放_1}|${播放_2}|${播放_3}|${播放_4}|${播放5}|${music_查找};
bug下一首=(${播放}|听|来|点)(一|两|几)?(个|点|首|曲|支|些)?(其它|别的|其他)的?;
下一首2=(切歌|换歌|换首歌|下首|再下首|再来首|再来一首|下一个|下个|再下一个|下个歌|跳过|放别的|别放这首了|换别的|别再重复了|不要放这首歌了|${bug下一首}) => ("下一首");
下一首3=(不要|别)再?(循环|重复)(播放|放|播)? => ("下一首");
下一首4=换成|切换成|(切)?换(一)?(首|个|曲|种)?=>("切换");

上一列表=(播放|重新播放|换成|换|切到|切|播|放)?(上一频道|上一列表|上一个列表|上一个频道|上一个播放列表|上一播放列表) => ("上一列表");
下一列表=(播放|重新播放|换成|换|切到|切|播|放)?(下一频道|下一列表|下一个列表|下一个频道|下一个播放列表|下一播放列表) => ("下一列表");
下一列表1=(换成|换)(一)?(频道|列表|播放列表) => ("下一列表");

m来些2=来些|来一些|来点|来一点|来首|来一首|来两首|来几首|点|点些|点一些|点首|点一首|点两首|点几首|听些|听一些|听点|听一点|听首|听一首|听两首|听几首|我想听|我要听|来个|来一个;
打开=(打开|开|开启|启动|进入|运行) => ("打开");
下一首6=(我要|我想)?(${播放}|听|来|点)(一|两|几)?(个|点|首|曲|支|些)?(其它|别的|其他)(歌|歌曲|音乐|曲子) =>("下一首");

演唱=(给我|替我|帮我)?(唱|演唱) =>("演唱");

不想=我?不(想|要)?;
停止=(停|停止|停下来|停吧|停播|停下|中止|中断)(播放|播|放|听)?|(别)(播放|播|放|听) => ("停止");
暂停=暂停|暂停播放|别放了|别吵了|不要放歌了|别播了|不要唱了|暂时停一下 => ("暂停");
单曲循环=一直播这一?首|一直播放这一?首|一直听这一?首|一直唱这一?首|一直放这一?首|就放这一?首|只放这一?首|只听这一?个|单曲循环|单个循环|只放这一?个|只听这一?首|只播这一?个|只播这一?首 => ("单曲循环");
ms_重复播放3=(把这个|把这条|把这一条)?(给我|替我)?再(给我|替我)?(放|播放|播|读|说|听|唱)一(遍|次);
ms_重新播放2=从头播放|重新播放|从开始播放|从开头播放|再放一次|多听一遍|再来一遍|再听一次|再听一遍|再放一遍|再唱一次|再播一遍|再唱一遍|再播一次|再读一次|重读这条|重读这一条|重播|${ms_重复播放3} => ("重新播放");
ms_重复播放1=重复播放|重复|重复放|重复播|重复这首=>("重复播放");
ms_重新播放4=(从新|重新|从头)(开始)?(放|播放|播)  => ("重新播放");
ms_重新播放5= 回到开始(放|播放|播)? => ("重新播放");

重复播放=${ms_重复播放1}|${ms_重新播放2}|${ms_重新播放4}|${ms_重新播放5};
重复播放2=一直(播放|放|播|听|唱)=>("重复播放");
循环播放=循环播放|循环放|循环播 => ("循环播放");

关闭=(关闭|关|关了|关掉|结束|你关闭吧) => ("关闭");
退出1=退出播放|退出|退下|退了|你退下吧|你退出吧 => ("退出");
#####退出2=我?(不听了|不想听了|不听歌了|不要听了|不听音乐了) => ("退出");
退出2=(我|我们)?(不|不想|不要|不想要|不愿|不愿意)(听|收听)(歌|音乐)?(了)? => ("暂停");
退出=${退出1}|${退出2};
返回=回到|返回 => ("返回");
显示=显示|${music_查看};
查询=(查询|查看|查|看)(下|一下)? =>("查询");
继续=(继续|接着|接着上次|解除暂停)(放|播放|唱)?(${语气词})? => ("继续");
休眠=(休眠|睡眠|你去睡吧|你休息吧|睡觉去吧|那你睡觉吧|你去休息吧|休息一下|休息吧|你该休息了|你休眠吧|赶紧休眠|休息一会儿) =>("休眠");
显示歌词=显示歌词|歌词显示 =>("显示歌词");
操作_new=(切换|切|调节|调) => ("打开");
单曲循环1=(一直播放|只听|只放|只播|循环播放)(这首|这支|这一首|这一个|这一|这个) => ("单曲循环");
单曲循环new=单曲循环|${单曲循环1};
随机播放=随机播放|乱序播放 => ("随机播放");
随机播放模式=随机播放模式  => ("随机播放模式");
顺序播放1=(不要|别)再?(重复|循环)(放|播|播放)?了?;
顺序播放=顺序播放|${顺序播放1} => ("顺序播放");
music_收藏=(帮我|给我)?(加|加一下)?收藏 => ("收藏");
操作1=推荐|${返回}|${显示}|下载|取消|${播放}|${停止}|${暂停}|${退出}|${打开}|${关闭}|${继续}|${休眠}|${演唱};
操作=${操作1}|${上一首}|${下一首}|${下一首1}|${下一首2}|${下一首3}|${下一首4}|${下一首6}|${上一列表}|${下一列表}|${下一列表1}|${顺序播放}|${循环播放}|${随机播放}|随机循环|顺序循环|${单曲循环}|列表循环|暂停下载|${重复播放}|${music_收藏}|${显示歌词};
操作up=(再|给我|帮我|替我)?(顺序播放|循环播放|${随机播放}|${随机播放模式}|随机循环|顺序循环|${单曲循环new}|列表循环|暂停下载|重复播放|全部循环) => ("$2");
##########音量
最高=最高|最大|最响|最强 => ("max");
最低=最低|最小|最暗|最弱 => ("min");
调高1=(调高|调大|升高|增大|增加|提高|变大|大|高|加|开大|加大|开大|增强|强|上升|升)(一点|一些|点|些)? => ("+");
调低1=(调低|调小|降低|减小|变小|小|低|减少|减|关小|下降|关小|减弱|弱|降)(一点|一些|点|些)? => ("-");
调高2=(大|高)(一点|一些|点|点儿|一点儿|些)? => ("+");
调低2=(小|低)(一点|一些|点|点儿|一点儿|些)? => ("-");
调高=${调高1}|${调高2};
调低=${调低1}|${调低2};
_大声=(声音)?(响|大声|大点声|响点声)(一点|一些|点|点儿|一点儿|些)? => ("+");
_小声=(声音)?(小声|小点声|太吵)(一点|一些|点|点儿|一点儿|些)? => ("-");
_静音=(静音|关闭声音|关闭音量) => ("0");
音量加减=${调高}|${调低};
相对音量=${_大声}|${_小声}|${_静音};
音量1=(${整数}) => ("$1");
音量2=(百分之)(${整数}) => (_join,prefix="$2",mid="%");
音量=${音量1}|${音量2}|${最高}|${最低};

USB=USB|U盘|优盘 =>("USB");
网络=网络|网上  => ("网络");
LIVE=LIVE|live => ("LIVE");
音源=${USB}|CD|IPOD|本地|${网络}|SD卡|蓝牙|MP4;

####add by cx
mu_版=(版|版本|版版本|版的版本) => ("版本");
music_版本=现场|演唱会|${LIVE}|录制|录音棚|原唱;

spec切换=(不|不想|不要|不想要|不愿|不愿意)(听|收听)这(一)?(个|首)|不(是|要)这(一)?(个|首)? => ("切换");
mu不喜欢=不(喜欢|爱听|爱)|讨厌 => ("不喜欢");
mu喜好=${mu不喜欢};

mu音乐类型2=(的)?(${音乐类型}) => (_and,item="$2");
mu音乐类型and=(经典)(的)?(${mu音乐类型2}) => (_logical,item1="$1",item2="$3");
####
#############
伴奏=伴奏|K歌版本=>("伴奏");

副歌=副歌|副歌部分=>("副歌");
高潮=高潮|高潮部分=>("高潮");
前奏=前奏|前奏部分=>("前奏");
歌曲结构=${副歌}|${高潮}|${前奏};
歌手_当前=他|这个人|这个歌手=>("current");


序列号1=(第)(${整数})(个|首|曲|首歌曲) => ("$2");
序列号2=最后一个|最后那个|最后这个|倒数第一首|最后一首|最后那首|最后这首|倒数第一首 =>("#1");
序列号3=(倒数|最后)(第|后|那)?(${整数})(个|首|曲) => (_join,prefix="#",mid="$3");
序列号4=(中间)(一|那|这|那一|这一)(个|首|曲) => ("mid");
序列号5=(选)(第)?(${整数}) => ("$3");
## by zhangyu, 2019-04-17, 添加序列号说法
mu序列号_最前1=最(先|前|前面|前边|靠前|靠前边|靠前面|上面|上端)的?(那|那一|一|这|这一|第一)(个|首|曲) => ("1");
mu序列号_最后1=最(后|后面|后边|靠后|靠后边|靠后面|下面|下端)的?(那|那一|一|这|这一|倒数第一)(个|首|曲) => ("#1");
mu序列号_最前2=(顶部|头部)的?(那|那一|一|这|这一|第一)(个|首|曲) => ("1");
mu序列号_最后2=(底部|脚部)的?(那|那一|一|这|这一|倒数第一)(个|首|曲) => ("#1");

序列号=${序列号1}|${序列号2}|${序列号3}|${序列号4}|${序列号5}|${mu序列号_最前1}|${mu序列号_最后1}|${mu序列号_最前2}|${mu序列号_最后2};

上一页=上一页|前一页|往上翻|往上翻页|往前翻|往前翻页 => ("-1");
下一页=下一页|后一页|往下翻|往下翻页|往后翻|往后翻页|翻页|翻一页 => ("+1");
上N页=(上|前|前面|上翻|前翻|往前翻|往上翻)(${整数})页 => (_join,prefix="-",mid="$2");
下N页=(下|后|后面|下翻|后翻|往后翻|往下翻)(${整数})页 => (_join,prefix="+",mid="$2");
页码3=(倒数|最后)(第|后|那)?(${整数})(页) => (_join,prefix="#",mid="$3");
页码4=(中间)(一|那|这|那一|这一)(页) => ("mid");
页码2=第(${整数})页 => ("$1");
## by zhangyu, 2019-04-17, 添加页码说法
mu页码_最前1 = 最(先|前|前面|前边|靠前|靠前边|靠前面)的?(那|那一|一|这|这一|第一)页 => ("1");
mu页码_最后1 = 最(后|后面|后边|靠后|靠后边|靠后面)的?(那|那一|一|这|这一|倒数第一)页 => ("#1");

页码1=${页码3}|${页码2}|${页码4}|${mu页码_最前1}|${mu页码_最后1};

_再见=再见|拜拜|闭嘴|BYE|我?不想说了?|不说了|明天见|下次见|滚吧|滚犊子|滚蛋|给我滚|滚球|GOODBYE|滚一边去|明天见|滚蛋吧|滚开|快滚|晚安|你给我滚蛋|你可以滚了|谢谢再见|你滚蛋|我要睡觉了晚安|你退出吧|你给我闭嘴|滚你妈的|再见亲爱的|睡觉了晚安|我叫你滚|退出来|滚远一点|滚出去|快点滚|不用了再见 => ("退出");

快进=(前进|向前|快进|往前) => ("+") ;
快退=(后退|倒退|向后|往后|快退) =>("-");
快进mix=(${快进})(${_进度值}) => (_join,prefix="$1",mid="$2");
快退mix=(${快退})(${_进度值}) => (_join,prefix="$1",mid="$2");
快进to=(${快进})到(${_进度值}) => ("$2");
快退to=(${快退})到(${_进度值}) => ("$2");
## add new parameter 20170325
##music_搜索=搜搜|搜|搜下|搜一下|搜索|搜寻一下|查一下|搜寻|搜索些|搜一些|找|搜索|搜下|找下|搜索下|搜索一下|搜些|找些|搜索一些|搜个|搜一个|搜索个|搜索一个;
##music_查找=看|看一下|看下|我想知道|我想看|显示|查看|查询|查询下|查询一下|查找|找|找下|找一下|查|查下找找|查查|找|知不知道|找几个|找一找|查一查|搜一搜|看一看|推荐|介绍|${music_搜索};
##music_发送=发送|发下|发一下|发送下|发送一下=>("发送");
#include "${pwd}/actsentence.lex"

music_相对时间=(${_相对时间})(后|之后|以后|过后)? => ("$1");


请求语气词结尾1=(可以|行|好)(吗|不|啵);
请求语气词结尾2=行不行|好不好;
请求语气词结尾=${请求语气词结尾1}|${请求语气词结尾2};
删除=(删除|删掉|去掉|删了|不喜欢)(这一首|这首|这个)? => ("删除");
收藏1=(收藏|保存)(一下|下)?(这一首|这首|这个|这曲|这支)? => ("收藏");
收藏2=(加入到|添加到|加入|放入|放到|加到)(收藏) => ("收藏");
收藏=${收藏1}|${收藏2};
关闭2=(关闭|关|关了|关掉|结束) => ("关闭");
操作2=${返回}|${显示}|下载|取消|${播放}|${停止}|${暂停}|${退出}|${打开}|${关闭2}|${继续}|${删除}|${收藏};
操作3=(再|给我|帮我|替我)?(${操作2}|${上一首}|${下一首}|${下一首1}|${下一首2}|${上一列表}|${下一列表}|${下一列表1}|顺序播放|循环播放|${随机播放}|${随机播放模式}|随机循环|顺序循环|${单曲循环}|列表循环|暂停下载|重复播放|全部循环) => ("$2");
播放_xt=(放|播放|播|点|来)=> ("播放");

export b1=^你好小乐|小乐你好|小乐继续|小乐来首歌|小乐我要听歌|我要听那个叫叫那个呃|我要听那个叫叫什么|小乐我想听|小乐我想听歌$ => request(crfflag="0") <0.8>;
切换_xt=换|切换|切|换成|切换成|切成|换下|切换下|切下|换一下|切换一下|切一下=> ("切换");
句末听听类动词_xt=听听|来听|来听听|来听一下;
音乐_61 = 歌曲|歌|音乐|MUSIC|曲子|乐曲|曲儿|歌谣|歌儿|曲|乐 => ("音乐");


#export opt17=(${操作})(一)?(点|首|曲)?(音乐|歌曲|歌|专辑|MUSIC) => request(操作="$1") <0.22>;

if not actflag then

#include "${pwd}/varlex/歌手性别.lex"
#include "${pwd}/varlex/歌手名.lex"
#include "${pwd}/varlex/语种.lex"
#include "${pwd}/varlex/排行榜.lex"
#include "${pwd}/varlex/乐器.lex"
#include "${pwd}/varlex/主题类型.lex"
#include "${pwd}/varlex/音乐类型.lex"
#include "${pwd}/varlex/专辑名.lex"
#include "${pwd}/varlex/主题.lex"
#include "${pwd}/varlex/版本.lex"


###删除音量 xn-dui
####include "${pwd}/varlex/音量.lex"
####删除声音类型 xn-dui
######include "${pwd}/varlex/声音类型.lex"

#include "${pwd}/varlex/操作.lex"
#include "${pwd}/varlex/歌曲名.lex"
#include "${pwd}/varlex/风格.lex"
#include "${pwd}/varlex/序列号.lex"
##include "${pwd}/varlex/场景.lex"
##include "${pwd}/varlex/心情.lex"
#include "${pwd}/varlex/action.lex"
#include "${pwd}/varlex/年代.lex"
#include "${pwd}/varlex/重复次数.lex"
#include "${pwd}/varlex/节奏.lex"
#include "${pwd}/varlex/歌曲数量.lex"
#include "${pwd}/varlex/音乐场景.lex"
#include "${pwd}/varlex/进度.lex"
#include "${pwd}/varlex/适用人群.lex"
#include "${pwd}/varlex/适用年龄.lex"
###删除歌词  xn-dui
####include "${pwd}/varlex/歌词.lex"
#include "${pwd}/varlex/相对时间.lex"
#include "${pwd}/varlex/多领域.lex"
end


#include "${pwd}/播放列表.lex"

export yinyuan1=(${音源})(上|里)?的?(音乐|歌曲)? => request(音源="$1") <0.2>;
export opt2=(${对象}) => request(对象="$1") <0.201>;
export opt01=(${操作}|听|来)(一|几|${整数})?(些|首|点)?(${对象}) => request(对象="$4",播放列表="") <0.4>;


歌曲随便=(随便|随机|随意) => ("dontcare");
export singer =^(给我|替我)?(${歌曲随便})(给我|替我)?(来|听|放|播|播放|听听)一?(首|点|曲)?(歌|音乐) => request(歌曲名="$2") <0.81>;
export singer =^(给我|替我)?(${歌曲随便})(给我|替我)?(来|听|放|播|播放|听听)一?(首|点|曲)?(${歌手名}|${风格})的(歌|音乐) => request(歌曲名="$2") <0.81>;
export singer =^(给我|替我)?(${歌曲随便})(给我|替我)?(听|放|播|播放|听听|来)(一)?(首|曲|个)$ => request(歌曲名="$2") <0.81>;
export singer =(${歌手名})的(歌|音乐|歌曲)(给我|替我)?(${歌曲随便})(给我|替我)?(来|听|放|播|播放|听听)一?(首|点|曲|个) => request(歌曲名="$5") <0.81>;
export singer =(${歌曲随便})(给我|替我)?(来|听|放|播|播放|听听)(首|点|曲)?(歌|音乐) => request(歌曲名="$1") <0.3>;
export singer =(${歌曲随便})(给我|替我)?(听|放|播|播放|听听) => request(歌曲名="$1") <0.13>;
export singer =(${歌曲随便})(给我|替我)?(听|放|播|播放|听听|来)(一)?(首|曲|个) => request(歌曲名="$1") <0.13>;
export singer =^(${歌曲随便})(${语气词})?$ => request(歌曲名="$1") <0.13>;
export music序列号=(播放|放|来)(第)(${整数})(首|支)(歌|歌曲|曲) $=> request(序列号="$3")<0.65>;

ss给我 = (给|替|为)(我|我们|爷);
ss推荐首 = (推荐)(几|${整数})(首|支|曲);
export singer2 = ^(${ss给我})?(${歌曲随便})(${ss给我})?(${来首2}|${ss推荐首})(${歌手名}|${排行榜}|${年代}|${乐器}|${语种}) => request(歌曲名="$2") <0.1>;

###删除适用人名，keyword  xn-dui
####if not 适用人群 then 
####    #include "${pwd}/varlex/适用人名.lex"
####end

####include "${pwd}/varlex/keyword.lex"

#if not 对象 and not 歌曲名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别 and not 乐器 and not 排行榜 and not 语种 and not 主题 and not 主题类型 and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__ and not actflag  and not 音乐场景 then
#    export default1 = (我想听|我要听|播放)(首|一首|一下)?(${歌手名})的(.{2,10})(${语气词})?$ => request(歌曲名="$4") <0.06>;
#    export default2 = (来|放)(首|一首|一下)(${歌手名})的(.{2,10})(${语气词})?$ => request(歌曲名="$4") <0.06>;
#end

#if not 对象 and not 歌曲名 and not 歌手名 and not 专辑名 and not 风格 and not 音乐类型  and not 音源  and not 播放列表 and not 性别  and not 乐器  and not 排行榜  and not 语种 and not 主题 and not 主题类型 and not 音量 and not 序列号 and not 页码 and not 年代 and not 重复次数 and not 节奏 and not __tgt__  and not actflag and not 音乐场景 then
#    export default3 = (我想听|我要听|播放)(首|一首|一下)?(.{2,10})(${语气词})?$ => request(歌曲名="$3") <0.06>;
#end



#if not 歌曲名 and not 歌手名 and not 风格 and not 音乐类型  and not 操作 and not 音源  and not 播放列表 and not actflag then
#    #include "${pwd}/housekeeping.lex"
#end

if not __act__ then 
    export affirm100 = ^啊|阿|世道|似的|吃的$ => request(__act__="affirm") <0.1>;
    export inform100 = .+ => request(__act__="inform") <0.1>;
end





#### add by xuhua 过滤音乐的集数,lua见
export dom_filer_music1=(放|播放|播)(一下|个|一个)?(${歌曲名}|${歌曲名}|故事|节目|栏目|小说|有声书)的?(最后)?(第)(${整数})(集|章|章节)=>request(domainnot="1")<0.6>;
export dom_filer_music2=(放|播放|播)(一下|个|一个)?(${歌曲名}|故事|节目|栏目|小说|有声书)的?(最后|最新|最近)(${整数})(集|章|章节)=>request(domainnot="1")<0.6>;
export dom_filer_music3=(${歌曲名}|故事|节目|栏目|小说|有声书)的?(最后|最新|最近)(${整数})(集|章|章节)=>request(domainnot="1")<0.6>;

## by zhangyu, 2019-08-07, 抖音流行音乐特殊处理
export douyinmusic = (抖音)(上面?|里面?|中)?的?(流行|火热|热门|到?最火|到?最热|最红)的?(音乐|歌曲|曲子) => (主题="$1") <0.2>;

