export musictengxun1=(这首|这个|重复播放|循环播放)(歌|歌曲)?(播|放|播放|重复|听)(${遍数})  => request(重复次数="$4") <0.5>;
export musictengxun1=^(重复|循环)?(播|放|播放|重复|听)(${遍数})  => request(重复次数="$3") <0.2>;
