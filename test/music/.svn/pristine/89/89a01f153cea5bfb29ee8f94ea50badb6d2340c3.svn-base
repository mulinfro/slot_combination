
#------chat------#
#----问名字(who)
export chat1=(你|您)是(谁|什么)|介绍一?下你?自己呗? => request(__act__="chat",聊天类型="who") <0.2>;
export chat2=(你|您)叫(什么|啥)(名字|名)?|(你|您)?的?(名字|闺名|芳名) => request(__act__="chat",聊天类型="who") <0.2>;
#----问功能(function)
export chat3=(我不知道|我不知道你|你)?有(啥|哪些|什么)$ =>request(__act__="chat",聊天类型="function") <0.2>;
export chat4=你(还|都)?(能做|有|能干|会干|会)(点|些)?(嘛|啥|什么|哪些) => request(__act__="chat",聊天类型="function") <0.2>;
export chat5=(你|您)?有什么用 => request(__act__="chat",聊天类型="function") <0.2>;
#----问好(hello)
你好=hello|Hello|HELLO|你好|您好|你好么|您好么|hi美女|早上好|上午好|下午好|晚上好|早啊;
export hello1=^(${语气词})?(${你好})(${语气词})?$ => request(__act__="chat",聊天类型="hello") <0.3>;
export hello1=(${你好}) => request(__act__="chat",聊天类型="hello") <0.2>;
#----表扬（praise）
export ack1=^(${语气词})?(${夸奖}) => request(__act__="chat",聊天类型="praise") <0.4>;
export ack2=(不错有点意思|挺有意思的|好开心|好高兴|心情好好) => request(__act__="chat",聊天类型="praise") <0.4>;
#----感谢（thanks）
export thanks1=(${感谢}) => request(__act__="chat",聊天类型="thanks") <0.4>;
#----骂脏话(abuse)
export abuse1=快点?去死|去死吧|可以去死了|可以死了|怎么不去死|还不去死 => request(__act__="chat",聊天类型="abuse") <0.4>;
export abuse2=傻叉|傻逼|傻B|sb|SB|Sb|sB|二货|傻冒|傻缺|二比 => request(__act__="chat",聊天类型="abuse") <0.8>;
export abuse3=说?你妹(阿|啊)? => request(__act__="chat",聊天类型="abuse") <0.4>;
export abuse4=(操|去)(你|他)(妈|妈妈|老母|妹|大爷)? => request(__act__="chat",聊天类型="abuse") <0.4>;
export abuse5=我操|我靠|他妈的|狗屎|一坨屎 => request(__act__="chat",聊天类型="abuse") <0.4>;
export abuse6=^(${语气词})?操(${语气词})?$ => request(__act__="chat",聊天类型="abuse") <0.4>;
#----抱怨(complain)
_烂=烂|差劲;
export complain1=这是?什么(啊|阿|呀)?$ => request(__act__="chat",聊天类型="complain") <0.4>;
export complain2=(啥|什么|总|这)(也|都)(找|搜)不到 => request(__act__="chat",聊天类型="complain") <0.4>;
export complain3=(啥|什么|这|这个).*(也|都)没有 => request(__act__="chat",聊天类型="complain") <0.4>;
export complain4=怎么可能 => request(__act__="chat",聊天类型="complain" <0.4>);
export complain5=你?(太|好)(${_烂})|什么(破|烂)(玩意|东西) => request(__act__="chat",聊天类型="complain") <0.8>; 
export complain6=^(${语气词})?(又来|又来了|我去|我哭|我哭了|我晕)(${语气词})?$ => request(__act__="chat",聊天类型="complain") <0.4>;
export complain6=被你打败了|闭嘴 => request(__act__="chat",聊天类型="complain") <0.4>;
export complain7=你搞得我都没|垃圾(东西|玩意|玩意儿|货) => request(__act__="chat",聊天类型="complain") <0.4>;
export complain8=(你是)?(傻瓜|笨蛋|傻子)|你傻啊?|(笨|傻)(死了)? => request(__act__="chat",聊天类型="complain") <0.3>;
export complain9= 你?(真|太|好|真是|这么|那么|这个)(笨|傻|二|蠢|蠢货|笨蛋)了? => request(__act__="chat",聊天类型="complain") <0.7>;
export complain10=什么垃圾(东西|玩意|玩意儿|货)? => request(__act__="chat",聊天类型="complain") <0.8>;
export complain11=对你真?无语|你?真垃圾|烦死了|你真烦|真讨厌 => request(__act__="chat",聊天类型="complain") <0.8>;
export complain12=^什么呀$ => request(__act__="chat",聊天类型="complain") <0.8>;

#------askrepeat------#
export askrepeat1=我?没有?听清|你说啥|再说一遍|听不清|再说一下|你说什么|再说一次|重复一次|重复一遍|重说一次|重说一遍 => request(__act__="askrepeat") <0.1>;
export askrepeat1=^(${语气词})?我?(没听清|你说啥|再说一遍|听不清|没听见)$ => request(__act__="askrepeat") <0.8>;

#------restart------#

#export restart1=重新(再)?(找|开始|搜|查)|重启|重新启动 => request(__act__="restart") <0.1>;
export restart2=^(${语气词})?(重启|重新启动|重启对话|对话重启|重新开始|重新开始对话|对话重新开始)(一下)?(${语气词})?$ => request(__act__="restart") <0.8>;
#export restart3=^(${语气词})?重新(再)?(找|开始|搜|查) => request(__act__="restart") <0.4>;


#------help------#
export help1=扯淡|帮助|help|求助|(如何|怎么)(使用|操作|用) => request(__act__="help");


#------cancel------#
#export cancel1=取消|取消拨打|放弃|不要拨了|不要打了|我不拨了|我不打了|不打了|不打啦|不拨了|不拨啦|别打了|别打|不拨打|不打 => request(__act__="cancel") <0.6>;

#------hangup------#
export hangup1=稍等|我想想|等会|等一会|等一下|等下|等我一会|等我一下 => request(__act__="hangup") <0.1>;


#------dontcare------#
_随便=随便|随你的便|随便你|听你的|无所谓|哪个都行|哪个都可以|都行|都可以|你帮我(选|挑)一?个;
export dontcare1=^(${语气词})?(${_随便})(${语气词})?$ => request(value="dontcare") <0.1>;
export dontcare2=(${_随便}) => request(value="dontcare") <0.03>;


