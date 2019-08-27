夸奖=(你|哇塞)?你?(太|真|还|好|还真|这么|可真|还蛮|蛮)?挺?(牛|牛逼|牛叉|牛X|牛B|聪明|好棒|太棒|很好|不错|太好了|太好啦|回答的很好|厉害);
感谢=谢谢(你|了|啦)?|谢啦|太感谢了|THANKYOU;
#------bye------#
export bye11=^(${_再见})(应用)$ => request(操作="$1",actflag="1") <0.8>;
export bye21=^(${_再见})(${_再见})$ => request(操作="$1",actflag="1") <0.8>;
export bye41=^(${感谢}|${夸奖})(${_再见})(${_再见})?(${语气词})?$ => request(操作="$2",聊天类型="",actflag="1") <0.81>;
export bye51=^(${语气词})?(滚)(${语气词})?$ => request(操作="退出",actflag="1") <0.8>;
export bye61=^(${_再见})(${语气词})?$ => request(操作="$1",actflag="1") <0.1>;

#------askrepeat------#
没听清=(我?没有?听清楚?|我?听不清楚?) => ("askrepeat");
askrepeat=(${没听清})?(你说啥|再说一遍|再说一下|你说什么|再说一次|重复一次|重复一遍|重说一次|重说一遍) => ("askrepeat");
export askrepeat1=(${askrepeat}) => request(__act__="$1") <0.15>;
export askrepeat1=^(${没听清}|${askrepeat})$ => request(__act__="$1",actflag="1") <0.55>;
export askrepeat1=^(${语气词})?我?(没听清|你说啥|再说一遍|听不清|没听见)$ => request(__act__="askrepeat",actflag="1") <0.8>;



