###为解决多领域冲突 add by cx for tx2.0
music_multi_第一=最开始|最开头|最头 => ("1");
music_multi_序列号1=(第|头)(${整数})(个|的) => ("$2");
music_multi_最后=(倒数|最后)(第|后|那|这)?(${整数})(个|的) => (_join,prefix="#",mid="$3");
music_multi_最后1=最尾 => ("#1");

music_multi_实体=音乐|电台|故事;
music_multi_删除=删除|删掉 => ("删除");

music_multi_序列号=${music_multi_序列号1}|${music_multi_第一}|${music_multi_最后}|${music_multi_最后1};

music_multi_都不要1=(全|全部|所有)(都)?不(要)? => ("all");
music_multi_都不要2=(都)不(要)? => ("all");

music_multi_都要1=(全|全部|所有)(都)?(要)? => ("all");
music_multi_都要2=(都)(要)? => ("all");

export mutli_domain1=(${music_multi_序列号}) => request(序列号="$1")<0.05>;
export multi_domain2=(不要)(${music_multi_序列号}) => request(__act__="deny",序列号="$2")<0.06>;
export multi_domain3=^(${music_multi_都不要1})$ => request(__act__="deny",序列号="$1")<0.05>;
export multi_domain3=(${music_multi_都不要1})(播|播放) => request(操作="播放",__act__="deny",序列号="$1")<0.05>;
export multi_domain30=^(${music_multi_都不要2})$ => request(__act__="deny",序列号="$1")<0.05>;
export multi_domain31=(${music_multi_都不要2})(播|播放) => request(操作="播放",__act__="deny",序列号="$1")<0.05>;
export multi_domain4=^(${music_multi_都要1})$ => request(序列号="$1")<0.05>;
export multi_domain4=(${music_multi_都要1})(播|播放) => request(操作="播放",序列号="$1")<0.05>;
export multi_domain40=^(${music_multi_都要2})$ => request(序列号="$1")<0.05>;
export multi_domain40=(${music_multi_都要2})(播|播放) => request(操作="播放",序列号="$1")<0.05>;

export multi_domain50=除了(${music_multi_实体})(其他|其他的|别的|剩下的)(都)?(不要)$ => request(序列号="")<0.06>;
export multi_domain50=除了(${music_multi_实体})(其他|其他的|别的|剩下的)(都)?(不播|不要播) => request(操作="播放",序列号="")<0.06>;

export multi_domain_60=(${music_multi_删除})(${music_multi_实体}) => request(操作="$1") <0.05>;
export multi_domain_60=(不要)(${music_multi_实体}) => request(__act__="deny",__tgt__="对象",对象="$2") <0.05>;
export multi_domain_60=(不播)(${music_multi_实体}) => request(操作="播放",__act__="deny",__tgt__="对象",对象="$2") <0.05>;
