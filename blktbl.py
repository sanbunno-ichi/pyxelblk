#-----------------------------------------------------------------
#最初の高さ、ブロックの並び（色番号）320x240(横18縦最大20)、240x240(横13縦最大20)、終端0xff

#終端テーブル
stageend_tbl = [0 for tbl in range(1)]
stageend_tbl = [ 0xff ]

#-------
#0x0:無し	
#0x1:ROCK	0x2:WHITE	0x3:RED		0x4:GREEN	#0x5:BLUE
#0x6:YELLOW	0x7:MIZU	0x8:PURPLE	0x9:ORANGE	0xa PINK	0x0b GRAY
#-------
#[0]320x240 Original Stage
stage001_tbl = [
	1,
	3,3,3,3,6,0,6,8,0,0,0,8,7,7,7,4,0,0,
	3,0,0,3,6,0,6,8,0,0,0,8,7,0,0,4,0,0,
	3,0,0,3,6,0,6,0,8,0,8,0,7,0,0,4,0,0,
	3,3,3,3,0,6,0,0,0,8,0,0,7,7,0,4,0,0,
	3,0,0,0,0,6,0,0,0,8,0,0,7,0,0,4,0,0,
	3,0,0,0,0,6,0,0,8,0,8,0,7,0,0,4,0,0,
	3,0,0,0,0,6,0,8,0,0,0,8,7,0,0,4,0,0,
	3,0,0,0,0,6,0,8,0,0,0,8,7,7,7,4,4,4,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	5,5,5,0,7,0,0,0,2,2,2,0,0,9,0,10,0,10,
	5,0,0,5,7,0,0,2,11,11,11,2,9,0,9,10,0,10,
	5,0,0,5,7,0,0,2,11,0,11,2,9,0,9,10,0,10,
	5,5,5,0,7,0,0,2,11,0,11,2,9,0,0,10,10,0,
	5,0,0,5,7,0,0,2,11,0,11,2,9,0,0,10,0,10,
	5,0,0,5,7,0,0,2,11,0,11,2,9,0,9,10,0,10,
	5,0,0,5,7,0,0,2,11,11,11,2,9,0,9,10,0,10,
	5,5,5,5,7,7,7,0,2,2,2,0,0,9,0,10,0,10,
	0xff]

#インベーダー
stage002_tbl = [
	0,
	0,0,0,2,2,0,0,0,0,0,0,0,0,2,2,0,0,0,
	0,0,2,2,2,2,0,0,0,0,0,0,2,2,2,2,0,0,
	0,2,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,0,
	2,2,11,2,2,11,2,2,0,0,2,2,11,2,2,11,2,2,
	2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,
	0,2,0,2,2,0,2,0,0,0,0,0,2,0,0,2,0,0,
	2,0,0,0,0,0,0,2,0,0,0,2,0,2,2,0,2,0,
	0,2,0,0,0,0,2,0,0,0,2,0,2,0,0,2,0,2,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,
	0,0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0,0,
	0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,
	0,0,0,2,2,2,11,11,2,2,11,11,2,2,2,0,0,0,
	0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,
	0,0,0,0,0,2,2,2,0,0,2,2,2,0,0,0,0,0,
	0,0,0,0,2,2,0,0,2,2,0,0,2,2,0,0,0,0,
	0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,
	0xff]

#富士山
stage003_tbl = [
	5,
	0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,
	0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,
	0,0,0,0,0,0,2,5,2,2,5,2,0,0,0,0,0,0,
	0,0,0,0,0,2,5,5,2,2,5,5,2,0,0,0,0,0,
	0,0,0,0,0,2,5,2,5,5,2,5,2,0,0,0,0,0,
	0,0,0,0,5,5,5,5,5,5,5,5,5,5,0,0,0,0,
	0,0,0,5,5,5,5,5,5,5,5,5,5,5,5,0,0,0,
	0,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,0,0,
	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
	0xff]

stage004_tbl = [
	2,
	0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,
	0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,
	0,0,2,0,3,3,3,3,3,3,3,3,3,3,0,2,0,0,
	0,0,2,0,3,0,0,0,0,0,0,0,0,3,0,2,0,0,
	0,0,2,0,3,0,4,4,4,4,4,4,0,3,0,2,0,0,
	0,0,2,0,3,0,4,0,0,0,0,4,0,3,0,2,0,0,
	0,0,2,0,3,0,4,0,1,1,0,4,0,3,0,2,0,0,
	0,0,2,0,3,0,4,0,1,1,0,4,0,3,0,2,0,0,
	0,0,2,0,3,0,4,0,0,0,0,4,0,3,0,2,0,0,
	0,0,2,0,3,0,4,4,4,4,4,4,0,3,0,2,0,0,
	0,0,2,0,3,0,0,0,0,0,0,0,0,3,0,2,0,0,
	0,0,2,0,3,3,3,3,3,3,3,3,3,3,0,2,0,0,
	0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,
	0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,
	0xff]

stage005_tbl = [
	1,
	1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
	2,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,2,
	0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
	0,2,0,4,4,4,4,4,4,4,4,4,4,4,4,0,2,0,
	0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,
	0,0,2,0,5,5,5,5,5,5,5,5,5,5,0,2,0,0,
	0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,
	0,0,0,2,0,6,6,6,6,6,6,6,6,0,2,0,0,0,
	0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,
	0,0,0,0,2,0,7,7,7,7,7,7,0,2,0,0,0,0,
	0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,
	0,0,0,0,0,2,0,8,8,8,8,0,2,0,0,0,0,0,
	0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,
	0,0,0,0,0,0,2,0,9,9,0,2,0,0,0,0,0,0,
	0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,
	0xff]

stage006_tbl = [
	5,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,
	0,0,1,0,0,1,0,0,0,0,0,0,1,5,5,1,0,0,
	0,0,1,7,7,1,8,8,8,8,8,8,1,6,6,1,0,0,
	0,0,1,6,6,1,8,8,8,8,8,8,1,7,7,1,0,0,
	0,0,1,5,5,1,8,8,8,8,8,8,1,0,0,1,0,0,
	0,0,1,1,1,1,8,8,8,8,8,8,1,0,0,1,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,
	0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,
	0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0xff]

#Lemmings
stage007_tbl = [
	2,
	0,0,4,0,4,0,0,0,4,0,0,0,0,0,0,0,0,0,
	0,4,4,4,0,0,4,0,4,4,4,0,0,4,4,4,4,0,
	0,4,4,2,0,0,0,4,4,2,0,0,0,4,4,2,0,0,
	0,0,2,2,2,0,4,0,2,2,2,0,0,0,2,2,2,0,
	0,0,2,5,0,0,0,0,2,5,0,0,0,0,2,5,0,0,
	0,2,5,5,0,0,0,2,5,5,0,0,0,2,5,5,0,0,
	0,2,5,5,0,2,0,2,5,5,0,0,0,2,5,5,0,0,
	0,0,5,5,0,2,0,0,5,5,0,0,0,0,5,5,0,0,
	0,5,5,0,2,0,0,2,2,5,5,0,2,2,0,5,5,0,
	0,2,2,0,0,0,0,0,0,2,2,0,2,0,0,2,2,0,
	0xff]

stage008_tbl = [
	4,
	0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 1, 11, 11, 1, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 1, 11, 11, 1, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 11, 11, 11, 11, 11, 11, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 11, 6, 6, 6, 6, 11, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 11, 11, 11, 0, 0, 0, 0, 11, 11, 11, 0, 0, 0, 0,
	0, 0, 0, 0, 11, 3, 3, 0, 0, 0, 0, 3, 3, 11, 0, 0, 0, 0,
	0, 0, 11, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11, 11, 0, 0,
	0, 0, 11, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 11, 0, 0,
	11, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11, 11,
	0xff]

#花火
stage009_tbl = [
	0,
	0,0,0,0,0,0,0,6,6,6,6,0,0,0,0,0,0,0,
	0,2,0,0,0,6,6,0,0,0,0,6,6,0,0,0,2,0,
	0,0,2,0,6,0,0,0,0,0,0,0,0,6,0,2,0,0,
	0,0,0,6,0,0,0,9,9,9,9,0,0,0,6,0,0,0,
	0,0,6,0,1,0,9,0,0,0,0,9,0,1,0,6,0,0,
	0,0,6,0,0,9,0,0,0,0,0,0,9,0,0,6,0,0,
	0,6,0,0,9,0,0,0,8,8,0,0,0,9,0,0,6,0,
	0,6,0,9,0,0,11,1,0,0,1,11,0,0,9,0,6,0,
	0,6,0,9,0,11,8,0,3,3,0,8,11,0,9,0,6,0,
	0,6,0,9,0,11,8,0,3,3,0,8,11,0,9,0,6,0,
	0,6,0,9,0,0,11,1,0,0,1,11,0,0,9,0,6,0,
	0,6,0,0,9,0,0,0,8,8,0,0,0,9,0,0,6,0,
	0,0,6,0,0,9,0,0,0,0,0,0,9,0,0,6,0,0,
	0,0,6,0,1,0,9,0,0,0,0,9,0,1,0,6,0,0,
	0,0,0,6,0,0,0,9,9,9,9,0,0,0,6,0,0,0,
	0,0,2,0,6,0,0,0,0,0,0,0,0,6,0,2,0,0,
	0,2,0,0,0,6,6,0,0,0,0,6,6,0,0,0,2,0,
	0,0,0,0,0,0,0,6,6,6,6,0,0,0,0,0,0,0,
	0xff]

#囲まれたブロック
stage010_tbl = [
	0,
	0,1,0,0,0,5,5,5,5,5,5,5,5,5,5,5,1,0,
	0,1,0,0,0,0,5,5,5,5,5,5,5,5,5,5,1,0,
	0,1,0,0,0,0,0,5,5,5,5,5,5,5,5,5,1,0,
	0,0,0,0,0,0,0,0,5,5,5,5,5,5,5,5,1,0,
	0,1,0,0,0,0,0,0,0,5,5,5,5,5,5,5,1,0,
	0,1,3,0,0,0,0,0,0,0,5,5,5,5,5,5,1,0,
	0,1,3,3,0,0,0,0,0,0,0,5,5,5,5,5,1,0,
	0,1,3,3,3,0,0,0,0,0,0,0,5,5,5,5,1,0,
	0,1,3,3,3,3,0,0,0,0,0,0,0,5,5,5,1,0,
	0,1,3,3,3,3,3,0,0,0,0,0,0,0,5,5,1,0,
	0,1,3,3,3,3,3,3,0,0,0,0,0,0,0,5,1,0,
	0,1,3,3,3,3,3,3,3,0,0,0,0,0,0,0,1,0,
	0,1,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,
	0,1,3,3,3,3,3,3,3,3,3,0,0,0,0,0,1,0,
	0,1,3,3,3,3,3,3,3,3,3,3,0,0,0,0,1,0,
	0,0,1,3,3,3,3,3,3,3,3,3,3,0,0,0,1,0,
	0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,
	0xff]

#Pyxelマーク
stage011_tbl = [
	0,
	0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,5,5,9,1,5,5,0,0,0,0,0,0,
	0,0,0,0,5,5,9,9,5,5,9,9,5,5,0,0,0,0,
	0,0,5,5,9,9,5,5,5,5,5,5,9,9,5,5,0,0,
	0,5,1,10,5,5,5,5,5,5,5,5,5,5,7,1,5,0,
	0,5,10,5,10,10,5,5,5,5,5,5,7,7,5,7,5,0,
	0,5,10,5,5,5,10,10,5,5,7,7,5,5,5,7,5,0,
	0,5,10,5,5,5,5,5,10,1,5,5,5,5,5,7,5,0,
	0,5,10,5,5,5,5,5,5,7,5,5,5,5,5,7,5,0,
	0,5,10,5,5,5,5,5,5,7,5,5,5,5,5,7,5,0,
	0,5,10,5,5,5,5,5,5,7,5,5,5,5,5,7,5,0,
	0,5,10,5,5,5,5,5,5,7,5,5,5,5,5,7,5,0,
	0,5,10,5,5,5,5,5,5,7,5,5,5,5,5,7,5,0,
	0,5,1,10,5,5,5,5,5,7,5,5,5,5,7,1,5,0,
	0,0,5,5,10,10,5,5,5,7,5,5,7,7,5,5,0,0,
	0,0,0,0,5,5,10,10,5,7,7,7,5,5,0,0,0,0,
	0,0,0,0,0,0,5,5,10,1,5,5,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,
	0xff]

#トイレマーク
stage012_tbl = [
	1,
	0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
	0,0,5,5,5,0,0,0,1,1,0,0,0,3,3,3,0,0,
	0,5,5,5,5,5,0,0,1,1,0,0,3,3,3,3,3,0,
	0,5,5,5,5,5,0,0,1,1,0,0,3,3,3,3,3,0,
	0,5,5,5,5,5,0,0,1,1,0,0,3,3,3,3,3,0,
	0,0,5,5,5,0,0,0,1,1,0,0,0,3,3,3,0,0,
	0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
	0,5,5,5,5,5,0,0,1,1,0,0,0,0,3,0,0,0,
	0,5,5,5,5,5,0,0,1,1,0,0,0,0,3,0,0,0,
	0,5,5,5,5,5,0,0,1,1,0,0,0,3,3,3,0,0,
	0,0,5,5,5,0,0,0,1,1,0,0,0,3,3,3,0,0,
	0,0,5,5,5,0,0,0,1,1,0,0,0,3,3,3,0,0,
	0,0,5,5,5,0,0,0,1,1,0,0,3,3,3,3,3,0,
	0,0,0,5,0,0,0,0,1,1,0,0,3,3,3,3,3,0,
	0,0,0,5,0,0,0,0,1,1,0,0,3,3,3,3,3,0,
	0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
	0xff]

#ブドウ
stage013_tbl = [
	0,
	0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,
	0,0,0,0,0,0,0,0,0,0,0,0,11,11,11,4,4,0,
	0,0,0,0,0,0,0,0,0,11,11,11,11,3,8,11,0,0,
	0,0,0,0,0,0,0,0,11,3,10,8,11,10,8,11,0,0,
	0,0,0,0,0,0,0,0,11,10,10,8,11,8,8,11,0,0,
	0,0,0,0,0,0,0,0,11,8,8,8,11,11,11,0,0,0,
	0,0,0,0,0,0,0,0,0,11,11,11,11,3,10,11,0,0,
	0,0,0,11,11,11,0,0,0,11,3,10,11,10,11,11,0,0,
	0,0,11,3,10,8,11,11,11,11,10,10,8,11,10,8,11,0,
	0,0,11,10,10,8,11,3,10,11,8,8,8,11,10,8,11,0,
	0,0,11,8,11,11,11,10,10,8,11,11,11,11,8,8,11,0,
	0,0,0,11,3,10,11,8,8,8,11,3,10,8,11,11,0,0,
	0,11,11,11,10,10,8,11,11,11,11,10,10,8,11,0,0,0,
	11,3,10,11,8,8,8,11,3,10,11,8,8,8,11,0,0,0,
	11,10,10,8,11,11,11,11,10,10,8,11,11,11,0,0,0,0,
	11,8,8,8,11,0,0,11,8,8,8,11,0,0,0,0,0,0,
	0,11,11,11,0,0,0,0,11,11,11,0,0,0,0,0,0,0,
	0xff]

#リンゴ
stage014_tbl = [
	0,
	0,0,0,0,0,0,0,0,0,0,0,0,11,11,9,11,4,4,
	0,0,0,0,0,0,0,0,0,0,11,11,3,3,9,3,3,11,
	0,0,0,0,0,0,0,0,0,11,3,3,3,11,11,11,3,3,
	0,0,0,0,0,0,9,9,11,4,4,4,3,3,3,3,3,3,
	0,0,0,0,0,0,0,9,4,4,4,4,4,3,3,3,3,3,
	0,0,0,0,0,11,11,9,11,4,4,4,3,3,3,3,3,3,
	0,0,0,11,11,3,3,9,3,3,11,11,3,3,3,3,3,3,
	0,0,11,3,3,3,11,11,11,3,3,3,11,3,3,3,3,3,
	0,11,3,1,3,3,3,3,3,3,3,3,3,11,3,3,3,3,
	0,11,3,1,3,3,3,3,3,3,3,3,3,11,6,6,6,11,
	0,11,3,3,3,3,3,3,3,3,3,3,3,11,11,11,11,0,
	0,11,3,1,3,3,3,3,3,3,3,3,3,11,0,0,0,0,
	0,11,3,3,1,3,3,3,3,3,3,3,3,11,0,0,0,0,
	0,0,11,3,3,3,3,3,3,3,3,3,11,0,0,0,0,0,
	0,0,0,11,11,6,6,6,6,6,11,11,0,0,0,0,0,0,
	0,0,0,0,0,11,11,11,11,11,0,0,0,0,0,0,0,0,
	0xff]

stage015_tbl = [
	0,
	0,5,5,5,0,0,0,2,0,0,2,0,0,0,5,5,5,0,
	0,2,2,2,0,0,0,0,2,2,0,0,0,0,2,2,2,0,
	0,2,5,2,0,0,0,2,0,0,2,0,0,0,2,5,2,0,
	0,0,2,0,0,0,1,1,1,1,1,1,0,0,0,2,0,0,
	0,0,5,0,0,1,1,1,1,1,1,1,1,0,0,5,0,0,
	0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,
	0,0,1,0,0,1,0,0,4,4,0,0,1,0,0,1,0,0,
	0,0,1,0,0,1,0,8,1,1,8,0,1,0,0,1,0,0,
	0,0,1,0,0,1,3,0,1,1,0,3,1,0,0,1,0,0,
	0,6,1,7,7,1,0,8,1,1,8,0,1,7,7,1,6,0,
	0,0,1,0,0,1,3,0,1,1,0,3,1,0,0,1,0,0,
	0,6,1,7,7,1,0,8,1,1,8,0,1,7,7,1,6,0,
	0,0,1,0,0,1,3,0,1,1,0,3,1,0,0,1,0,0,
	0,6,1,7,7,1,0,8,1,1,8,0,1,7,7,1,6,0,
	0,0,1,0,0,1,3,0,1,1,0,3,1,0,0,1,0,0,
	0,6,1,0,9,9,9,8,1,1,8,9,9,9,0,1,6,0,
	0,0,1,9,9,9,9,0,1,1,0,9,9,9,9,1,0,0,
	0,6,1,0,9,9,0,0,0,0,0,0,9,9,0,1,6,0,
	0xff]

stage016_tbl = [
	5,
	3,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,
	0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,4,
	1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,
	6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,
	0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	3,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,
	0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,4,
	1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,
	6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,
	0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
	0xff]

stage017_tbl = [
	1,
	0,0,0,0,0,1,3,1,0,0,1,3,1,0,0,0,0,0,
	0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,
	0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,1,4,1,0,0,0,1,8,1,0,0,0,0,1,4,1,0,
	0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,1,0,
	0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,1,5,1,0,0,0,0,1,5,1,0,0,0,0,
	0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,
	0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,6,1,0,0,0,0,0,0,0,0,0,0,0,0,1,6,1,
	1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,
	0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
	0xff]

stage018_tbl = [
	3,
	1,4,1,5,1,6,1,7,1,8,1,9,1,0,1,0,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,3,1,4,1,5,1,6,1,7,1,8,1,9,1,0,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,0,1,3,1,4,1,5,1,6,1,7,1,8,1,9,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,0,1,0,1,3,1,4,1,5,1,6,1,7,1,8,1,9,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,0,1,0,1,0,1,3,1,4,1,5,1,6,1,7,1,8,
	0xff]

stage019_tbl = [
	2,
	0,1,3,3,3,1,0,0,0,0,0,0,1,3,3,3,1,0,
	1,0,0,4,0,0,1,0,0,0,0,1,0,0,4,0,0,1,
	1,0,4,4,4,0,1,0,0,0,0,1,0,4,4,4,0,1,
	1,4,4,8,4,4,1,0,0,0,0,1,4,4,8,4,4,1,
	0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,1,3,3,3,1,0,0,0,0,0,0,
	0,0,0,0,0,0,1,0,0,4,0,0,1,0,0,0,0,0,
	0,0,0,0,0,0,1,0,4,4,4,0,1,0,0,0,0,0,
	0,0,0,0,0,0,1,4,4,6,4,4,1,0,0,0,0,0,
	0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,
	0xff]

stage020_tbl = [
	5,
	1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,5,
	9,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,
	1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,4,
	8,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,
	1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,3,
	7,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,
	1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,
	6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,
	1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0xff]

stage021_tbl = [
	0,
	0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
	0,3,0,0,0,3,0,0,0,3,0,0,0,3,0,0,0,3,
	0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
	0,0,0,4,0,0,0,4,0,0,0,4,0,0,0,4,0,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
	0,5,0,0,0,5,0,0,0,5,0,0,0,5,0,0,0,5,
	0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
	0,0,0,6,0,0,0,6,0,0,0,6,0,0,0,6,0,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
	0,7,0,0,0,7,0,0,0,7,0,0,0,7,0,0,0,7,
	0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
	0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,0,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
	0,9,0,0,0,9,0,0,0,9,0,0,0,9,0,0,0,9,
	0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
	0,0,0,10,0,0,0,10,0,0,0,10,0,0,0,10,0,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,
	0xff]

stage022_tbl = [
	0,
	1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
	1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
	1,0,6,6,6,6,6,6,6,6,6,6,6,6,6,6,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	7,0,7,0,0,0,0,7,1,1,7,0,0,0,0,7,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	4,0,4,0,0,0,0,4,1,1,4,0,0,0,0,4,0,4,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	9,0,9,0,0,0,0,9,1,1,9,0,0,0,0,9,0,9,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	3,0,3,0,0,0,0,3,1,1,3,0,0,0,0,3,0,3,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	8,0,8,0,0,0,0,8,1,1,8,0,0,0,0,8,0,8,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,
	0xff]


stage023_tbl = [
	0,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3,
	0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3,
	0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3,
	0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
	0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
	0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
	0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
	0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	0xff]

#The End
stage024_tbl = [
	1,
	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
	5,1,1,1,5,1,5,1,5,1,1,1,5,5,5,5,5,5,
	5,5,1,5,5,1,5,1,5,1,5,5,5,5,5,5,5,5,
	5,5,1,5,5,1,1,1,5,1,1,5,5,5,5,5,5,5,
	5,5,1,5,5,1,5,1,5,1,5,5,5,5,5,5,5,5,
	5,5,1,5,5,1,5,1,5,1,1,1,5,5,5,5,5,5,
	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
	5,5,5,5,5,1,1,1,5,1,5,5,1,5,1,1,5,5,
	5,5,5,5,5,1,5,5,5,1,1,5,1,5,1,5,1,5,
	5,5,5,5,5,1,1,5,5,1,1,5,1,5,1,5,1,5,
	5,5,5,5,5,1,5,5,5,1,5,1,1,5,1,5,1,5,
	5,5,5,5,5,1,1,1,5,1,5,5,1,5,1,5,1,5,
	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
	0xff]

stage0_tbl = [
	stage001_tbl, stage002_tbl, stage003_tbl, stage004_tbl, stage005_tbl, 
	stage006_tbl, stage007_tbl, stage008_tbl, stage009_tbl, stage010_tbl, 
	stage011_tbl, stage012_tbl, stage013_tbl, stage014_tbl, stage015_tbl, 
	stage016_tbl, stage017_tbl, stage018_tbl, stage019_tbl, stage020_tbl,
	stage021_tbl, stage022_tbl, stage023_tbl, stage024_tbl,
	stageend_tbl
	]


#-------
#0x0:無し	
#0x1:ROCK	0x2:WHITE	0x3:RED		0x4:GREEN	#0x5:BLUE
#0x6:YELLOW	0x7:MIZU	0x8:PURPLE	0x9:ORANGE	0xa PINK	0x0b GRAY
#-------
#[1]240x240 Original Stage

stage101_tbl = [
	1,
	3,3,3,0,0,0,0,0,0,0,0,0,4,
	3,0,0,3,0,0,0,0,0,0,0,0,4,
	3,0,0,3,0,0,0,0,0,0,7,0,4,
	3,3,3,6,0,6,8,0,8,7,0,7,4,
	3,0,0,6,0,6,8,0,8,7,0,7,4,
	3,0,0,0,6,0,0,8,0,7,7,0,4,
	3,0,0,6,0,0,0,8,0,7,0,0,4,
	3,0,6,0,0,0,8,0,8,7,0,7,4,
	3,6,0,0,0,0,8,0,8,0,7,0,4,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	5,0,0,7,0,0,0,0,0,0,10,0,10,
	5,0,0,7,0,0,0,0,0,0,10,0,10,
	5,5,5,7,2,2,2,9,9,9,10,10,0,
	5,0,5,7,2,11,2,9,0,0,10,0,10,
	5,5,5,7,2,2,2,9,9,9,10,0,10,
	0xff]

#インベーダー
stage102_tbl = [
	2,
	2,2,0,0,0,0,0,0,0,2,0,0,0,
	2,2,2,2,2,0,0,0,0,0,2,0,0,
	2,2,2,2,2,2,0,0,0,2,2,2,2,
	2,11,11,2,2,2,0,0,2,2,11,2,2,
	2,2,2,2,2,2,0,2,2,2,2,2,2,
	2,2,2,2,0,0,0,2,0,2,2,2,2,
	0,2,2,2,0,0,0,2,0,2,0,0,0,
	2,0,0,2,2,0,0,0,0,0,2,2,0,
	0,0,2,2,0,0,2,2,0,0,0,0,0,
	0,0,0,0,0,2,2,2,2,0,0,0,0,
	0,0,0,0,2,2,2,2,2,2,0,0,0,
	0,0,0,2,2,11,2,2,11,2,2,0,0,
	0,0,0,2,2,2,2,2,2,2,2,0,0,
	0,0,0,0,2,0,2,2,0,2,0,0,0,
	0,0,0,2,0,0,0,0,0,0,2,0,0,
	0,0,0,0,2,0,0,0,0,2,0,0,0,
	0xff]

stage103_tbl = [
	4,
	2,3,4,5,6,7,8,9,2,3,4,5,6,
	0,3,4,5,6,7,8,9,2,3,4,5,6,
	0,0,4,5,6,7,8,9,2,3,4,5,6,
	0,0,0,5,6,7,8,9,2,3,4,5,6,
	0,0,0,0,6,7,8,9,2,3,4,5,6,
	0,0,0,0,0,7,8,9,2,3,4,5,6,
	0,0,0,0,0,0,8,9,2,3,4,5,6,
	0,0,0,0,0,0,0,9,2,3,4,5,6,
	0,0,0,0,0,0,0,0,2,3,4,5,6,
	0,0,0,0,0,0,0,0,0,3,4,5,6,
	0,0,0,0,0,0,0,0,0,0,4,5,6,
	0,0,0,0,0,0,0,0,0,0,0,5,6,
	0,0,0,0,0,0,0,0,0,0,0,0,6,
	0xff]

stage104_tbl = [
	4,
	0,0,2,2,2,0,0,0,0,0,0,0,0,
	0,0,2,3,2,0,0,0,0,0,0,0,0,
	0,0,2,2,2,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,1,1,1,0,0,0,1,1,1,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,2,2,2,0,0,
	0,0,0,0,0,0,0,0,2,5,2,0,0,
	0,0,0,0,0,0,0,0,2,2,2,0,0,
	0xff]

#富士山
stage105_tbl = [
	3,
	0,0,0,0,0,2,2,2,0,0,0,0,0,
	0,0,0,0,0,2,2,2,0,0,0,0,0,
	0,0,0,0,0,2,2,2,0,0,0,0,0,
	0,0,0,0,2,2,2,2,2,0,0,0,0,
	0,0,0,0,2,5,2,5,2,0,0,0,0,
	0,0,0,2,5,5,2,5,5,2,0,0,0,
	0,0,0,5,5,5,5,5,5,5,0,0,0,
	0,0,5,5,5,5,5,5,5,5,5,0,0,
	0,0,5,5,5,5,5,5,5,5,5,0,0,
	0,5,5,5,5,5,5,5,5,5,5,5,0,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	0xff]

stage106_tbl = [
	5,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	1,0,0,0,0,0,0,0,0,0,0,0,1,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	6,6,6,6,6,6,6,6,6,6,6,6,6,
	1,0,0,0,0,0,0,0,0,0,0,0,1,
	6,6,6,6,6,6,6,6,6,6,6,6,6,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	3,3,3,3,3,3,3,3,3,3,3,3,3,
	1,0,0,0,0,0,0,0,0,0,0,0,1,
	3,3,3,3,3,3,3,3,3,3,3,3,3,
	0xff]

stage107_tbl = [
	4,
	0,0,0,0,0,0,1,0,0,0,0,0,0,
	0,0,0,3,3,3,0,3,3,3,0,0,0,
	0,0,3,0,0,0,1,0,0,0,3,0,0,
	0,3,0,4,4,4,0,4,4,4,0,3,0,
	0,3,4,0,0,0,1,0,0,0,4,3,0,
	0,0,4,0,5,5,0,5,5,0,4,0,0,
	0,0,4,5,0,0,1,0,0,5,4,0,0,
	0,0,0,5,0,6,0,6,0,5,0,0,0,
	0,0,0,5,6,0,1,0,6,5,0,0,0,
	0,0,0,0,6,0,0,0,6,0,0,0,0,
	0,0,0,0,6,0,1,0,6,0,0,0,0,
	0xff]

stage108_tbl = [
	3,
	0,2,2,2,2,2,2,2,2,2,2,2,0,
	0,2,0,0,0,0,0,0,0,0,0,2,0,
	0,2,0,2,2,2,2,2,2,2,0,2,0,
	0,2,0,2,0,0,0,0,0,2,0,2,0,
	0,2,0,2,0,2,2,2,0,2,0,2,0,
	0,2,0,2,0,2,1,2,0,2,0,2,0,
	0,2,0,2,0,2,2,2,0,2,0,2,0,
	0,2,0,2,0,0,0,0,0,2,0,2,0,
	0,2,0,2,2,2,2,2,2,2,0,2,0,
	0,2,0,0,0,0,0,0,0,0,0,2,0,
	0,2,2,2,2,2,2,2,2,2,2,2,0,
	0xff]

#リンゴ
stage109_tbl = [
	1,
	0,0,0,0,0,9,9,0,4,4,4,0,0,
	0,0,0,0,0,0,9,4,4,4,4,4,0,
	0,0,0,0,11,11,9,11,4,4,4,0,0,
	0,0,11,11,3,3,9,3,3,11,11,0,0,
	0,11,3,3,3,11,11,11,3,3,3,11,0,
	11,3,1,3,3,3,3,3,3,3,3,3,11,
	11,3,1,3,3,3,3,3,3,3,3,3,11,
	11,3,3,3,3,3,3,3,3,3,3,3,11,
	11,3,1,3,3,3,3,3,3,3,3,3,11,
	11,3,3,1,3,3,3,3,3,3,3,3,11,
	0,11,3,3,3,3,3,3,3,3,3,11,0,
	0,0,11,11,6,6,6,6,6,11,11,0,0,
	0,0,0,0,11,11,11,11,11,0,0,0,0,
	0xff]

stage110_tbl = [
	4,
	0,0,0,0,0,0,5,0,0,0,0,0,0,
	0,0,0,0,7,7,5,6,6,0,0,0,0,
	0,0,0,7,7,7,10,6,6,6,0,0,0,
	0,0,7,7,7,10,10,10,6,6,6,0,0,
	0,0,7,7,10,10,10,10,10,6,6,0,0,
	0,7,7,7,10,10,10,10,10,6,6,6,0,
	0,7,7,7,10,10,10,10,10,6,6,6,0,
	0,7,7,7,10,10,10,10,10,6,6,6,0,
	0,11,0,0,11,0,11,0,11,0,0,11,0,
	0,0,0,0,0,0,11,0,0,0,0,0,0,
	0,0,0,0,0,0,11,0,0,0,0,0,0,
	0,0,0,0,0,0,11,0,0,0,0,0,0,
	0,0,0,0,8,0,8,0,0,0,0,0,0,
	0,0,0,0,8,8,8,0,0,0,0,0,0,
	0,0,0,0,0,8,0,0,0,0,0,0,0,
	0xff]

stage111_tbl = [
	2,
	2,2,2,2,2,2,2,2,2,2,2,2,0,
	1,1,1,1,1,1,1,1,1,1,1,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,2,2,2,2,2,2,2,2,2,2,2,2,
	0,1,1,1,1,1,1,1,1,1,1,1,1,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	2,2,2,2,2,2,2,2,2,2,2,2,0,
	1,1,1,1,1,1,1,1,1,1,1,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,2,2,2,2,2,2,2,2,2,2,2,2,
	0,1,1,1,1,1,1,1,1,1,1,1,1,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	2,2,2,2,2,2,2,2,2,2,2,2,0,
	1,1,1,1,1,1,1,1,1,1,1,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,2,2,2,2,2,2,2,2,2,2,2,2,
	0xff]

stage112_tbl = [
	1,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,1,0,8,0,7,0,0,
	0,9,0,8,0,1,2,1,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0,9,0,8,0,7,0,6,0,5,0,4,0,
	0,0,3,0,2,0,9,0,8,0,7,0,0,
	0xff]

stage113_tbl = [
	3,
	0,1,5,5,5,1,0,1,5,5,5,1,0,
	1,0,0,0,0,0,1,0,0,0,0,0,1,
	1,0,4,4,4,0,1,0,4,4,4,0,1,
	1,0,4,3,4,0,0,0,4,3,4,0,1,
	1,0,4,4,4,0,0,0,4,4,4,0,1,
	0,1,1,1,1,1,0,1,1,1,1,1,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,1,5,5,5,1,0,0,0,0,
	0,0,0,1,0,0,0,0,0,1,0,0,0,
	0,0,0,1,0,4,4,4,0,1,0,0,0,
	0,0,0,1,0,4,3,4,0,1,0,0,0,
	0,0,0,1,0,4,4,4,0,1,0,0,0,
	0,0,0,0,1,1,1,1,1,0,0,0,0,
	0xff]

stage114_tbl = [
	0,
	0,0,0,2,0,0,0,2,0,0,0,2,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,
	0,3,0,0,0,3,0,0,0,3,0,0,0,
	0,1,0,0,0,1,0,0,0,1,0,0,0,
	0,0,0,4,0,0,0,4,0,0,0,4,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,
	0,5,0,0,0,5,0,0,0,5,0,0,0,
	0,1,0,0,0,1,0,0,0,1,0,0,0,
	0,0,0,6,0,0,0,6,0,0,0,6,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,
	0,7,0,0,0,7,0,0,0,7,0,0,0,
	0,1,0,0,0,1,0,0,0,1,0,0,0,
	0,0,0,8,0,0,0,8,0,0,0,8,0,
	0,0,0,1,0,0,0,1,0,0,0,1,0,
	0,9,0,0,0,9,0,0,0,9,0,0,0,
	0,1,0,0,0,1,0,0,0,1,0,0,0,
	0xff]

stage115_tbl = [
	2,
	1,0,0,0,0,0,0,0,0,0,0,0,1,
	1,0,0,0,0,0,0,0,0,0,0,0,1,
	1,0,6,6,6,6,6,6,6,6,6,0,1,
	1,0,1,1,1,1,1,1,1,1,1,0,1,
	7,0,7,0,0,7,1,7,0,0,7,0,7,
	1,0,1,1,1,1,1,1,1,1,1,0,1,
	4,0,4,4,0,4,1,4,0,4,4,0,4,
	1,0,1,1,1,1,1,1,1,1,1,0,1,
	9,0,9,9,9,9,9,9,9,9,9,0,9,
	1,0,1,1,1,1,1,1,1,1,1,0,1,
	0xff]

stage116_tbl = [
	2,
	0,1,0,0,0,0,0,0,0,0,0,1,0,
	0,1,1,0,0,0,0,0,0,0,1,1,0,
	0,1,1,1,0,0,0,0,0,1,1,1,0,
	0,1,3,1,1,0,0,0,1,1,6,1,0,
	0,1,3,1,1,1,0,1,1,1,6,1,0,
	0,1,0,1,4,1,1,1,5,1,0,1,0,
	0,1,0,1,4,1,7,1,5,1,0,1,0,
	0,1,0,1,0,1,7,1,0,1,0,1,0,
	0,1,0,1,0,1,7,1,0,1,0,1,0,
	0,1,0,1,0,1,0,1,0,1,0,1,0,
	0,1,0,1,0,1,0,1,0,1,0,1,0,
	0,1,0,1,0,1,0,1,0,1,0,1,0,
	0,1,0,1,0,1,0,1,0,1,0,1,0,
	0,0,0,1,0,1,0,1,0,1,0,0,0,
	0,0,0,1,0,1,0,1,0,1,0,0,0,
	0,0,0,0,0,1,0,1,0,0,0,0,0,
	0,0,0,0,0,1,0,1,0,0,0,0,0,
	0xff]

#ハート
stage117_tbl = [
	1,
	0,0,0,11,11,0,0,0,11,11,0,0,0,
	0,0,11,5,7,11,0,11,8,10,11,0,0,
	0,11,5,7,5,7,11,8,10,8,10,11,0,
	0,11,7,5,7,5,8,10,8,10,8,11,0,
	11,7,5,7,5,7,5,8,10,8,10,8,11,
	11,5,7,5,7,5,8,10,8,10,8,10,11,
	11,7,5,7,5,7,5,8,10,8,10,8,11,
	11,5,7,5,7,5,8,10,8,10,8,10,11,
	0,11,5,7,5,7,5,8,10,8,10,11,0,
	0,11,7,5,7,5,8,10,8,10,8,11,0,
	0,0,11,7,5,7,5,8,10,8,11,0,0,
	0,0,11,5,7,5,8,10,8,10,11,0,0,
	0,0,0,11,5,7,5,8,10,11,0,0,0,
	0,0,0,0,11,5,8,10,11,0,0,0,0,
	0,0,0,0,0,11,5,11,0,0,0,0,0,
	0,0,0,0,0,0,11,0,0,0,0,0,0,
	0xff]

#斜め
stage118_tbl = [
	0,
	4,7,6,2,6,7,4,2,2,2,0,0,0,
	4,7,6,2,6,7,4,2,2,0,0,0,0,
	4,7,6,2,6,7,4,1,2,0,0,0,0,
	4,7,6,2,6,7,4,1,0,0,0,0,0,
	4,7,6,2,6,7,1,1,0,0,0,0,0,
	4,7,6,2,6,7,1,0,0,0,0,0,0,
	4,7,6,2,6,1,1,0,0,0,0,0,0,
	4,7,6,2,6,1,0,0,0,0,0,0,0,
	4,7,6,2,1,1,0,0,0,0,0,0,0,
	4,7,6,2,1,0,0,0,0,0,0,0,0,
	4,7,6,1,1,0,0,0,0,0,0,0,0,
	4,7,6,1,0,0,0,0,0,0,0,0,0,
	4,7,1,1,0,0,0,0,0,0,0,0,0,
	4,7,1,0,0,0,0,0,0,0,0,0,0,
	4,1,1,0,0,0,0,0,0,0,0,0,0,
	4,1,0,0,0,0,0,0,0,0,0,0,0,
	1,1,0,0,0,0,0,0,0,0,0,0,0,
	1,0,0,0,0,0,0,0,0,0,0,0,0,
	1,0,0,0,0,0,0,0,0,0,0,0,0,
	0xff]

#花火
stage119_tbl = [
	2,
	0,0,4,0,0,0,0,0,0,0,4,0,0,
	0,4,0,0,1,7,7,7,1,0,0,4,0,
	0,0,0,7,0,0,0,0,0,7,0,0,0,
	0,0,7,0,0,0,5,0,0,0,7,0,0,
	0,7,0,0,5,0,0,0,5,0,0,7,0,
	0,0,0,5,0,0,8,0,0,5,0,0,0,
	7,0,0,0,0,8,10,8,0,0,0,0,7,
	7,0,5,0,8,10,3,10,8,0,5,0,7,
	7,0,0,0,0,8,10,8,0,0,0,0,7,
	0,0,0,5,0,0,8,0,0,5,0,0,0,
	0,7,0,0,5,0,0,0,5,0,0,7,0,
	0,0,7,0,0,0,5,0,0,0,7,0,0,
	0,0,0,7,0,0,0,0,0,7,0,0,0,
	0,4,0,0,1,7,7,7,1,0,0,4,0,
	0,0,4,0,0,0,0,0,0,0,4,0,0,
	0xff]

#囲まれた
stage120_tbl = [
	0,
	0,1,5,5,5,5,5,5,0,0,4,1,0,
	0,1,5,5,5,5,5,5,5,0,0,1,0,
	0,1,5,5,5,5,5,5,5,5,0,0,0,
	0,0,0,5,5,5,5,5,5,5,5,1,0,
	0,1,0,0,5,5,5,5,5,5,5,1,0,
	0,1,3,0,0,5,5,5,5,5,5,1,0,
	0,1,3,3,0,0,5,5,5,5,5,1,0,
	0,1,3,3,3,0,0,5,5,5,5,1,0,
	0,1,3,3,3,3,0,0,5,5,5,1,0,
	0,1,3,3,3,3,3,0,0,5,5,1,0,
	0,1,3,3,3,3,3,3,0,0,5,1,0,
	0,1,3,3,3,3,3,3,3,0,0,1,0,
	0,1,3,3,3,3,3,3,3,3,0,0,0,
	0,1,3,3,3,3,3,3,3,3,3,1,0,
	0,0,1,3,3,3,3,3,3,3,3,1,0,
	0,0,0,1,3,3,3,3,3,3,3,1,0,
	0,0,0,0,1,1,1,1,1,1,1,0,0,
	0xff]

#ポケット
stage121_tbl = [
	0,
	6,6,6,6,8,1,1,1,8,6,6,6,6,
	6,6,6,6,8,1,3,1,8,6,6,6,6,
	1,6,6,1,8,4,4,4,8,1,6,6,1,
	1,6,6,1,8,4,5,4,8,1,6,6,1,
	1,6,6,1,8,5,0,5,8,1,6,6,1,
	1,1,1,1,5,0,0,0,5,1,1,1,1,
	10,1,1,5,0,0,0,0,0,5,1,1,10,
	10,10,0,0,0,0,0,0,0,0,0,10,10,
	0,0,0,0,7,1,0,1,7,0,0,0,0,
	0,0,7,7,7,1,0,1,7,7,7,0,0,
	0,0,1,7,7,1,0,1,7,7,1,0,0,
	0,0,1,1,1,1,0,1,1,1,1,0,0,
	0,0,0,1,1,0,0,0,1,1,0,0,0,
	0,0,0,0,0,4,0,4,0,0,0,0,0,
	0,0,0,0,0,4,4,4,0,0,0,0,0,
	0,0,0,0,0,1,3,1,0,0,0,0,0,
	0,0,0,0,0,1,1,1,0,0,0,0,0,
	0xff]

#だらだら
stage122_tbl = [
	0,
	1,3,3,1,3,3,3,3,3,1,3,3,1,
	3,3,3,3,3,3,1,1,3,3,3,3,3,
	3,1,1,3,3,3,3,3,3,3,3,3,3,
	3,3,3,3,1,1,3,1,3,1,1,3,1,
	1,3,3,3,3,3,3,3,3,3,3,3,3,
	3,3,1,1,3,1,3,1,1,3,3,3,3,
	3,3,3,3,3,3,3,3,3,3,1,1,1,
	1,1,1,3,3,3,3,3,3,3,3,3,3,
	3,3,3,3,3,1,1,3,1,3,3,3,3,
	3,3,3,1,3,3,3,3,3,3,3,1,1,
	3,1,3,3,3,3,3,3,1,1,3,3,3,
	3,3,3,1,1,3,1,3,0,0,3,3,3,
	3,3,3,3,3,3,3,3,0,0,3,1,3,
	3,1,1,0,0,3,1,1,0,0,3,3,3,
	3,3,3,0,0,3,0,0,0,0,1,1,3,
	3,0,0,0,0,3,0,0,0,0,0,0,3,
	0xff]

#迷路
stage123_tbl = [
	0,
	1,1,1,1,0,1,1,10,0,0,1,1,1,
	1,1,0,0,0,1,1,10,0,0,1,7,1,
	0,0,0,0,0,0,1,1,1,0,1,7,1,
	0,0,1,1,0,0,1,8,0,0,1,0,1,
	0,0,6,1,0,0,1,8,0,0,1,0,1,
	0,0,6,1,0,1,1,1,0,0,0,0,0,
	1,1,1,1,0,1,0,0,0,0,0,0,0,
	1,0,0,0,0,1,0,0,0,0,1,0,0,
	1,0,0,0,0,0,0,1,1,1,1,0,0,
	9,0,1,0,0,0,0,0,0,0,1,0,1,
	9,0,1,0,4,1,0,0,0,0,0,0,1,
	1,1,1,0,4,1,0,1,3,0,0,0,1,
	0,0,0,0,1,1,0,1,3,0,0,1,1,
	0,0,0,0,1,0,0,1,1,0,0,0,0,
	0,1,5,0,1,0,0,1,0,0,0,0,0,
	0,1,1,0,0,0,1,1,0,0,1,0,0,
	0,0,1,0,0,0,1,1,0,1,1,0,0,
	0,0,0,0,0,0,2,2,0,0,0,0,1,
	1,0,0,0,0,0,0,0,0,0,0,0,1,
	1,1,0,0,0,0,0,0,0,0,0,1,1,
	0xff]

stage124_tbl = [
	1,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	5,1,1,1,1,5,1,1,1,1,5,5,5,
	5,5,1,5,1,5,1,1,5,5,5,5,5,
	5,5,1,5,1,1,1,1,1,5,5,5,5,
	5,5,1,5,1,5,1,1,5,5,5,5,5,
	5,5,1,5,1,5,1,1,1,1,5,5,5,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	5,5,1,1,5,1,5,5,1,1,1,5,5,
	5,5,1,5,5,1,1,5,1,1,5,1,5,
	5,5,1,5,5,1,1,5,1,1,5,1,5,
	5,5,1,1,5,1,5,1,1,1,5,1,5,
	5,5,1,5,5,1,5,1,1,1,5,1,5,
	5,5,1,5,5,1,5,5,1,1,5,1,5,
	5,5,1,1,1,1,5,5,1,1,5,1,5,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	0xff]


stage1_tbl = [
	stage101_tbl, stage102_tbl, stage103_tbl, stage104_tbl, stage105_tbl, 
	stage106_tbl, stage107_tbl, stage108_tbl, stage109_tbl, stage110_tbl, 
	stage111_tbl, stage112_tbl, stage113_tbl, stage114_tbl, stage115_tbl, 
	stage116_tbl, stage117_tbl, stage118_tbl, stage119_tbl, stage120_tbl, 
	stage121_tbl, stage122_tbl, stage123_tbl, stage124_tbl, 
	stageend_tbl,
	]


stage_tbl = [stage0_tbl, stage1_tbl]

