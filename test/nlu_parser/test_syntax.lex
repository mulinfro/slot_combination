
atom digit = 0|1|2|3|4|5|6|7|8|9
atom op = 加上?|减去?|乘以?|除去?

# 所有constant必须在atom中
atom 多少 = 多少|几
plus num = {digit}

rule expr0 = [{num}, {op}, {num}]

export expr1 = [{num}, {op}, {num}, {多少}] => {intent="表达式0", opl = $1, op = $2, opr = $3, joined=@join("-", $1, $2, $3)}
export expr2 = [{num}, {op}, {num}, {多少}] => {intent="表达式02", opl = $1, op = $2, opr = $3, joined=@join("-", $1, $2, $3), @delete("opl", "op", "opr")}

atom 知不知道 = 你?知道|你?知不知道

export calculator1=[{expr0}, {知不知道}?, {多少}? ] => {intent="表达式1", expr = $1, x = $3 }

atom 播放=播放?|放 
atom 歌手 = 刘德华|周杰伦|王菲
atom 歌曲 = 红豆|忘情水|双节棍
atom pre = 能不能|请|给我
export music = <{播放}?, {歌手}, {歌曲}>  => {intent="歌曲", act=$1, who=$2, targt=$3}
export music2 = [{pre}, <{播放}?, [{歌手}, {歌曲}]> ] => {intent="歌曲2", pre=$1, info=$2}

plus op_p = {op} => {@var_plus}
export test_plus_conf = [{op_p}] => {intent="测试配置", val=$1}


atom aaa = AAA
atom aa = AA

<bb, bbb>?