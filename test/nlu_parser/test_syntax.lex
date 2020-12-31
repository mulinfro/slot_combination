
atom xx = xx?
atom xxx = tx?t|yy
#
atom digit = 0|1|2|3|4|5|6|7|8|9 => {__OUT__ = @to_hans($0)}
atom op = 加上?|减去?|乘以?|除去?  

# 所有constant必须在atom中
#
atom 多少 = 多少|几 => {__OUT__ = "X"}
plus num = {digit}
# => {__OUT__ = @trans_digit(), __MATCH__ = @valid_digit() }
rule expr0 = [{num}, {op}, {num}]  

export expr1 = [{num}, {op}, {num}, {多少}] => {intent="表达式01", opl = $1, op = $2, opr = $3, joined=@join("-", $1, $2, $3)}
export expr2 = [{num}, {op}, {num}, {多少}] => {intent="表达式02", opl = $1, op = $2, opr = $3, joined=@join("-", $1, $2, $3), @delete("opl", "op", "opr")}

atom 知不知道 = 你?知道|你?知不知道

export calculator1=[{expr0}, {知不知道}?, {多少}? ] => {intent="表达式1", expr = $1, x = $3 }

rule any = __ANY__(1,9)
rule any2 = __ANY__(3,9)
#rule any = ${__ANY__}  => {@any_conf1}

atom 播放=播放?|放 
atom 歌手 = 刘德华|周杰伦|王菲
atom 歌曲 = 红豆|忘情水|双节棍
atom pre = 能不能|请|给我
export music = <{播放}?, {歌手}, {歌曲}>  => {intent="歌曲", act=$1, who=$2, targt=$3}
export music2 = [{pre}, <{播放}?, [{歌手}, {歌曲}]> ] => {intent="歌曲2", pre=$1, info=$2}

plus op_p = {op} => {@var_plus}
#export test_plus_conf = [{op_p}] => {intent="测试配置", val=$1}
export test_plus_conf2 = {op_p} => {intent="测试配置2", val=$0}

atom aaa = AAA
atom aa = AA
atom 导航= 导航去|导航到?
export test_any = [{aa}, {any}, {aaa}] => {intent="测试any", val=$2}
export test_any2 = [{导航}, {any2}] => {intent="测试any_end", val=$2}
export test_any3 = [{any2}, {导航}] => {intent="测试any_begin", val=$1}



#<bb, bbb>?
