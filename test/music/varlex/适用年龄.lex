export 适用年龄1=(${适用年龄})的?(${适用人群1})?=> request(适用年龄="$1",适用人群="$2",歌手名="") <0.2>;
export 适用年龄12=适合(${适用年龄})的?(${宝宝})?(爱听|能够听|能听|喜欢听|听)?的(${儿童歌曲}|${幼儿歌曲})=> request(适用年龄="$1",适用人群="$2",歌曲类型="$4") <0.5>;
export 适用年龄13=(${宝宝})(放|播|播放|找|要听|想听)(个|点|些|一些|一个)?(适合)?(${适用年龄})(爱听|能够听|能听|喜欢听|听)?的(${儿童歌曲}|${幼儿歌曲})=> request(适用人群="$1",适用年龄="$5",歌曲类型="$4") <0.5>;
export 适用年龄123=(${适用年龄})的?(${宝宝})?(爱听|能够听|能听|喜欢听|听)?的(${对象})(${播放}|${music_查找1})=> request(适用年龄="$1",适用人群="$2",对象="$4",操作="$5") <0.5>;
