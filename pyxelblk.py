#タイトル：Pyxel Block
#ブロック崩し（Breaking blocks）
#
#更新履歴
#
#[TODO]★ステージエディットモード（将来的に追加予定）横幅サイズで切り替え＆再生保存機能も必要
#[TODO]★ネームエントリー（将来的に追加予定）
#[TODO]★おじゃま敵（敵キャラリソース作成（将来的に追加予定）
#[TODO]★アイテム類（将来的に追加予定）
#[TODO]★ステージ作成（アルカノイドステージ追加（横１３ブロック縦２０ブロック）（将来的に追加予定）
#以後アップデート対応で？
#
#公開
#
#既存バグ
#	09.12 右端の壁にヒットでなぜか反対側の壁際のブロックが消えることがある（２回見た）
#			枠チェックがブロックチェックの後だからではないだろうか？前にしてうまく動くのかどうなのか？
#			→前にもってきても同じだった・・・なぜに
#			★実験：ブロック消える時ボールの位置とブロックの位置を再比較する？
#
#★noteで「ブロック崩し」の作り方公開する？記事が良ければ有料\100とかで（ソースはgithubで公開も有り）
#★壊せないブロックを追加しただけで難易度が跳ね上がる
#
#今回はシンプルなブロックくずし程度に抑える？アイテム類まで入れるかどうか
#[TODO]デモプレイ
#[TODO]ステージ作成（CrystalHammerステージとオリジナルステージ：アルカノイドを参考にする）
#[TODO]設定画面作成
#[TODO]タイトル等ゲームシステム作成
#[TODO]ステージクリアやミス等の処理
#2024.09.12 すり抜け対策
#2024.09,11 こわれないブロック判定
#2024.09,10 反射による玉の角度＆速度調整
#2024.09.09 ヒットチェック作成
#2024.09.09 テキスト表示、スコア、残機表示
#2024.09.08 入力系組み込み
#2024.09.06 ブロック表示
#2024.09.05 リソース作成
#2024.09.04 作成開始

import pyxel

#-----------------------------------------------------------------
SCREEN_WIDTH		=	320		#ゲーム画面横サイズ（変更無しとする）
SCREEN_WIDTH2		=	240		#ゲーム画面横サイズ
SCREEN_HEIGHT		=	240		#ゲーム画面縦サイズ

LEFT_OFFSET			=	0x10	#左枠オフセット
RIGHT_OFFSET		=	0x10	#右枠オフセット
SCORE_HIGHT			=	0x08	#スコア位置分高さ
UP_OFFSET			=	0x10	#スコア位置＋壁の厚み

BLK_WIDTH			=	0x10	#ブロック横サイズ
BLK_HEIGHT			=	8		#ブロック縦サイズ


PALETTE_SHADOW		=	0x0b	#マルチカラー影色パレット
#-----------------------------------------------------------------
#[workass]変数
WORK_TOP			=	0
WORK_END			=	0x500
_ass = WORK_TOP
GWK = [WORK_TOP for _ass in range(WORK_END)]	#変数管理

game_adv			=	WORK_TOP+0x00		#game_control number
game_subadv			=	WORK_TOP+0x01		#game_control sub-number
stage_number		=	WORK_TOP+0x02		#0～49（予定）
stage_type			=	WORK_TOP+0x03		#0/1/2 : original / crystal hammer / arkanoid
multi_color_switch	=	WORK_TOP+0x04		#0/1 : ブロックマルチカラースイッチ
bg_switch			=	WORK_TOP+0x05		#0/1 : ブロック背景有り/無し
bg_type				=	WORK_TOP+0x06		#0/1/2 : ブロック背景タイプ（現在３種類）
start_height		=	WORK_TOP+0x07		#ステージブロックの先頭の高さ
ball_speed			=	WORK_TOP+0x08		#玉の基準スピード値
ball_degree			=	WORK_TOP+0x09		#玉の基準角度
ball_color			=	WORK_TOP+0x0a		#0/1/2 : 玉の色：青/赤/緑
rest_number			=	WORK_TOP+0x0b		#残機数
score				=	WORK_TOP+0x0c		#スコア（最大６桁）
highscore			=	WORK_TOP+0x0d		#ハイスコア（最大６桁）
blockmap_Hmax		=	WORK_TOP+0x0e		#ブロックマップ横最大サイズ
blockmap_Vmax		=	WORK_TOP+0x0f		#ブロックマップ縦最大サイズ

SCORE_MAX			=	999999
SCORE_KETA			=	6

G_TITLE				=	0
G_DEMOPLAY			=	1
G_GAME				=	2
G_OVER				=	3
G_STAGECLEAR		=	4
G_SETTING			=	5
G_DEBUG				=	6
G_END				=	7

save_cxpold			=	WORK_TOP+0x10
save_cypold			=	WORK_TOP+0x11
save_cxspd			=	WORK_TOP+0x12
save_cyspd			=	WORK_TOP+0x13
blockmap_shortofs	=	WORK_TOP+0x14		#横サイズオフセット

#--------------------------------------------
PLY_WORK			=	WORK_TOP+0xc0
cid					=	0x00		#ID番号
ccond				=	0x01		#状態フラグ
#状態フラグ内訳
F_LIVE				=	0x80		#[bit7]生(1)死(0)
F_ON				=	0x40		#[bit6]バーの上(1)移動中(0)
F_HIT				=	0x20		#[bit5]ヒット(1)

cxpos				=	0x02		#X座標
cypos				=	0x03		#Y座標
cxspd				=	0x04		#X移動スピード
cyspd				=	0x05		#Y移動スピード

canum				=	0x06		#アニメ番号
cacnt				=	0x07		#アニメカウンタ
caspd				=	0x08		#アニメスピードカウンタ

cmnum				=	0x09		#移動パターン番号
cmcnt				=	0x0a		#移動カウンタ
cmcnt2				=	0x0b		#移動カウンタ２
cwait				=	0x0c		#登場待ちカウンタ

cxpold				=	0x09		#移動前xpos保存用（玉用）
cypold				=	0x0a		#移動前ypos保存用（玉用）


cspd				=	0x0c		#基準移動速度
cdeg				=	0x0d		#移動角度（degree:0～89(359)）
chit				=	0x0e		#ヒット回数
chit2				=	0x0f		#ヒット回数（バーヒットでクリア）

CWORK_SIZE			=	0x10		#各種キャラクタワークサイズ

BALL_MAX			=	1		#★[TODO]（将来的に：3）
BALL_WORK			=	WORK_TOP+0xd0	#BALL_MAX分


#--------------------------------------------
#横方向：18、縦方向：20、18*20 = 360 = 0x228
#１個１バイト管理
#情報：色番号			デフォルトカラーは不要（キャラクタで区別）
#multi=0x1:	ROCK		def=0x7
#multi=0x2:	WHITE		def=0x7
#multi=0x3:	RED			def=0x8
#multi=0x4:	GREEN		def=0x3
#multi=0x5:	BLUE		def=0x5
#multi=0x6:	YELLOW		def=0xa
#multi=0x7:	MIZU		def=0x6
#multi=0x8:	PURPLE		def=0x2
#multi=0x9:	PINK		def=0xe
#multi=0xa:	ORANGE		def=0x9
#multi=0xb:	SHADOW		def=0x1
BLOCK_WORK		=	WORK_TOP+0x100

#BLOCK_WORK format
#bit 7654 3210
#	 |||| |  |
#	 |||| +--+
#	 ||||  色番号（0～9）
#	 |||+-？
#	 ||+--？
#	 |+--- BF_HIT(0/1=nohit/hit)
#	 *---- BF_LIVE(0/1=dead/live)

BF_LIVE			=	0x80
BF_HIT			=	0x40

#--------------------------------------------
#おじゃま敵
ENEMY_MAX		=	3
ENEMY_WORK		=	WORK_TOP+0x340
#--------------------------------------------
#アイテムは画面上最大８個まで
ITEM_MAX		=	8
ITEM_WORK		=	WORK_TOP+0x380
#--------------------------------------------
#アイテムショット弾
SHOT_MAX		=	16
SHOT_WORK		=	WORK_TOP+0x400

#-----------------------------------------------------------------
#キャラクタテーブル
#-----------------------------------------------------------------
ID_BALL				=	0x04		#玉ベース
ID_BLK_DEF			=	0x0c		#ブロックDEF開始id
ID_BLK_MULTI		=	0x17		#ブロックマルチ開始id

IDMAX = 0x67
#ctbl = [[0 for i in range(4)] for j in range(IDMAX)]
ctbl = [
	# u,    v,    us,   vs
	[ 0x10, 0x30, 0x20, 0x08 ],		#0x00 バーノーマル
	[ 0x00, 0x30, 0x10, 0x08 ],		#0x01 バー短い
	[ 0x00, 0x40, 0x40, 0x08 ],		#0x02 バー長い
	[ 0x00, 0x40, 0x20, 0x08 ],		#0x03 バーレーザー
	[ 0x34, 0x00, 0x04, 0x04 ],		#0x04 玉ノーマル（青）
	[ 0x38, 0x00, 0x07, 0x07 ],		#0x05 玉大（青）
	[ 0x30, 0x04, 0x04, 0x04 ],		#0x06 玉ノーマル（赤）
	[ 0x30, 0x08, 0x07, 0x07 ],		#0x07 玉大（赤）
	[ 0x34, 0x04, 0x04, 0x04 ],		#0x08 玉ノーマル（緑）
	[ 0x38, 0x08, 0x07, 0x07 ],		#0x09 玉大（緑）
	[ 0x30, 0x04, 0x04, 0x04 ],		#0x0a 白玉
	[ 0x30, 0x30, 0x10, 0x04 ],		#0x0b レーザー
	[ 0x60, 0x80, 0x10, 0x08 ],		#0x0c ブロックDEF：0x1:	ROCK	
	[ 0x70, 0x78, 0x10, 0x08 ],		#0x0d ブロックDEF：0x2:	WHITE(WHITE-GREEN)
	[ 0x40, 0x70, 0x10, 0x08 ],		#0x0e ブロックDEF：0x3:	RED		
	[ 0x50, 0x70, 0x10, 0x08 ],		#0x0f ブロックDEF：0x4:	GREEN	
	[ 0x40, 0x78, 0x10, 0x08 ],		#0x10 ブロックDEF：0x5:	BLUE	
	[ 0x50, 0x78, 0x10, 0x08 ],		#0x11 ブロックDEF：0x6:	YELLOW	
	[ 0x60, 0x78, 0x10, 0x08 ],		#0x12 ブロックDEF：0x7:	MIZU	
	[ 0x40, 0x80, 0x10, 0x08 ],		#0x13 ブロックDEF：0x8:	PURPLE	
	[ 0x60, 0x70, 0x10, 0x08 ],		#0x14 ブロックDEF：0x9:	ORANGE	
	[ 0x70, 0x70, 0x10, 0x08 ],		#0x15 ブロックDEF：0xa:	PINK	
	[ 0x70, 0x80, 0x10, 0x08 ],		#0x16 ブロックDEF：0xb:	SHADOW	
	[ 0xFF, 0x01, 0x10, 0x09 ],		#0x17 ブロックマルチ：0x1:	ROCK	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x18 ブロックマルチ：0x2:	WHITE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x19 ブロックマルチ：0x3:	RED		
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x1a ブロックマルチ：0x4:	GREEN	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x1b ブロックマルチ：0x5:	BLUE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x1c ブロックマルチ：0x6:	YELLOW	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x1d ブロックマルチ：0x7:	MIZU	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x1e ブロックマルチ：0x8:	PURPLE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x1f ブロックマルチ：0x9:	ORANGE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x20 ブロックマルチ：0xa:	PINK	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0x21 ブロックマルチ：0xb:	SHADOW	

	[ 0x20, 0x40, 0x10, 0x08 ],		#0x22 残機
	[ 0x80, 0x88, 0x00, 0x00 ],		#0x23 矢印左白
	[ 0x80, 0x90, 0x00, 0x00 ],		#0x24 矢印右白
	[ 0x90, 0x88, 0x00, 0x00 ],		#0x25 矢印左黄
	[ 0x90, 0x90, 0x00, 0x00 ],		#0x26 矢印右黄

	[ 0x38, 0x70, 0x08, 0x08 ],		#0x27 ' '（スペース）	白文字
	[ 0x30, 0x50, 0x08, 0x08 ],		#0x28 '('
	[ 0x38, 0x50, 0x08, 0x08 ],		#0x29 ')'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x2a （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x2b （空き）
	[ 0x10, 0x50, 0x08, 0x08 ],		#0x2c ','（カンマ）
	[ 0x20, 0x50, 0x08, 0x08 ],		#0x2d '-'（ハイフン）
	[ 0x18, 0x50, 0x08, 0x08 ],		#0x2e '.'（ピリオド）
	[ 0x28, 0x50, 0x08, 0x08 ],		#0x2f '/'（スラッシュ）

	[ 0x00, 0x48, 0x08, 0x08 ],		#0x30 '0'
	[ 0x08, 0x48, 0x08, 0x08 ],		#0x31 '1'
	[ 0x10, 0x48, 0x08, 0x08 ],		#0x32 '2'
	[ 0x18, 0x48, 0x08, 0x08 ],		#0x33 '3'
	[ 0x20, 0x48, 0x08, 0x08 ],		#0x34 '4'
	[ 0x28, 0x48, 0x08, 0x08 ],		#0x35 '5'
	[ 0x30, 0x48, 0x08, 0x08 ],		#0x36 '6'
	[ 0x38, 0x48, 0x08, 0x08 ],		#0x37 '7'
	[ 0x00, 0x50, 0x08, 0x08 ],		#0x38 '8'
	[ 0x08, 0x50, 0x08, 0x08 ],		#0x39 '9'

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3a （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3b （空き）
	[ 0x10, 0x70, 0x08, 0x08 ],		#0x3c '<'→'RD'	
	[ 0x18, 0x70, 0x08, 0x08 ],		#0x3d '>'→'ED'	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3e （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3f （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x40 （空き）
	[ 0x00, 0x58, 0x08, 0x08 ],		#0x41 'A'
	[ 0x08, 0x58, 0x08, 0x08 ],		#0x42 'B'
	[ 0x10, 0x58, 0x08, 0x08 ],		#0x43 'C'
	[ 0x18, 0x58, 0x08, 0x08 ],		#0x44 'D'
	[ 0x20, 0x58, 0x08, 0x08 ],		#0x45 'E'
	[ 0x28, 0x58, 0x08, 0x08 ],		#0x46 'G'
	[ 0x30, 0x58, 0x08, 0x08 ],		#0x47 'G'
	[ 0x38, 0x58, 0x08, 0x08 ],		#0x48 'H'
	[ 0x00, 0x60, 0x08, 0x08 ],		#0x49 'I'
	[ 0x08, 0x60, 0x08, 0x08 ],		#0x4a 'J'
	[ 0x10, 0x60, 0x08, 0x08 ],		#0x4b 'K'
	[ 0x18, 0x60, 0x08, 0x08 ],		#0x4c 'L'
	[ 0x20, 0x60, 0x08, 0x08 ],		#0x4d 'M'
	[ 0x28, 0x60, 0x08, 0x08 ],		#0x4e 'N'
	[ 0x30, 0x60, 0x08, 0x08 ],		#0x4f 'O'

	[ 0x38, 0x60, 0x08, 0x08 ],		#0x50 'P'
	[ 0x00, 0x68, 0x08, 0x08 ],		#0x51 'Q'
	[ 0x08, 0x68, 0x08, 0x08 ],		#0x52 'R'
	[ 0x10, 0x68, 0x08, 0x08 ],		#0x53 'S'
	[ 0x18, 0x68, 0x08, 0x08 ],		#0x54 'T'
	[ 0x20, 0x68, 0x08, 0x08 ],		#0x55 'U'
	[ 0x28, 0x68, 0x08, 0x08 ],		#0x56 'V'
	[ 0x30, 0x68, 0x08, 0x08 ],		#0x57 'W'
	[ 0x38, 0x68, 0x08, 0x08 ],		#0x58 'X'
	[ 0x00, 0x70, 0x08, 0x08 ],		#0x59 'Y'
	[ 0x08, 0x70, 0x08, 0x08 ],		#0x5a 'Z'

	[ 0x40, 0x00, 0x08, 0x08 ],		#0x5b アイテム青1：lOng
	[ 0x48, 0x00, 0x08, 0x08 ],		#0x5c アイテム緑1：Add
	[ 0x50, 0x00, 0x08, 0x08 ],		#0x5d アイテム赤1：Laser
	[ 0x58, 0x00, 0x08, 0x08 ],		#0x5e アイテム水1：Three
	[ 0x60, 0x00, 0x08, 0x08 ],		#0x5f アイテム黄1：Big-----一旦据え置き
	[ 0x68, 0x00, 0x08, 0x08 ],		#0x60 アイテム紫1：Short
	[ 0x40, 0x08, 0x08, 0x08 ],		#0x61 アイテム青2：lOng
	[ 0x48, 0x08, 0x08, 0x08 ],		#0x62 アイテム緑2：Add
	[ 0x50, 0x08, 0x08, 0x08 ],		#0x63 アイテム赤2：Laser
	[ 0x58, 0x08, 0x08, 0x08 ],		#0x64 アイテム水2：Three
	[ 0x60, 0x08, 0x08, 0x08 ],		#0x65 アイテム黄2：Big
	[ 0x68, 0x08, 0x08, 0x08 ],		#0x66 アイテム紫2：Short

	[ 0x38, 0xa0, 0x08, 0x08 ],		#0x67 ' '（スペース）	黄文字
	[ 0x30, 0x80, 0x08, 0x08 ],		#0x68 '('
	[ 0x38, 0x80, 0x08, 0x08 ],		#0x69 ')'
	[ 0x00, 0x80, 0x00, 0x00 ],		#0x6a （空き）
	[ 0x00, 0x80, 0x00, 0x00 ],		#0x6b （空き）
	[ 0x10, 0x80, 0x08, 0x08 ],		#0x6c ','（カンマ）
	[ 0x20, 0x80, 0x08, 0x08 ],		#0x6d '-'（ハイフン）
	[ 0x18, 0x80, 0x08, 0x08 ],		#0x6e '.'（ピリオド）
	[ 0x28, 0x80, 0x08, 0x08 ],		#0x6f '/'（スラッシュ）

	[ 0x00, 0x78, 0x08, 0x08 ],		#0x70 '0'
	[ 0x08, 0x78, 0x08, 0x08 ],		#0x71 '1'
	[ 0x10, 0x78, 0x08, 0x08 ],		#0x72 '2'
	[ 0x18, 0x78, 0x08, 0x08 ],		#0x73 '3'
	[ 0x20, 0x78, 0x08, 0x08 ],		#0x74 '4'
	[ 0x28, 0x78, 0x08, 0x08 ],		#0x75 '5'
	[ 0x30, 0x78, 0x08, 0x08 ],		#0x76 '6'
	[ 0x38, 0x78, 0x08, 0x08 ],		#0x77 '7'
	[ 0x00, 0x80, 0x08, 0x08 ],		#0x78 '8'
	[ 0x08, 0x80, 0x08, 0x08 ],		#0x79 '9'

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7a （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7b （空き）
	[ 0x10, 0xa0, 0x08, 0x08 ],		#0x7c '<'→'RD'	
	[ 0x18, 0xa0, 0x08, 0x08 ],		#0x7d '>'→'ED'	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7e （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7f （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x80 （空き）
	[ 0x00, 0x88, 0x08, 0x08 ],		#0x81 'A'
	[ 0x08, 0x88, 0x08, 0x08 ],		#0x82 'B'
	[ 0x10, 0x88, 0x08, 0x08 ],		#0x83 'C'
	[ 0x18, 0x88, 0x08, 0x08 ],		#0x84 'D'
	[ 0x20, 0x88, 0x08, 0x08 ],		#0x85 'E'
	[ 0x28, 0x88, 0x08, 0x08 ],		#0x86 'G'
	[ 0x30, 0x88, 0x08, 0x08 ],		#0x87 'G'
	[ 0x38, 0x88, 0x08, 0x08 ],		#0x88 'H'
	[ 0x00, 0x90, 0x08, 0x08 ],		#0x89 'I'
	[ 0x08, 0x90, 0x08, 0x08 ],		#0x8a 'J'
	[ 0x10, 0x90, 0x08, 0x08 ],		#0x8b 'K'
	[ 0x18, 0x90, 0x08, 0x08 ],		#0x8c 'L'
	[ 0x20, 0x90, 0x08, 0x08 ],		#0x8d 'M'
	[ 0x28, 0x90, 0x08, 0x08 ],		#0x8e 'N'
	[ 0x30, 0x90, 0x08, 0x08 ],		#0x8f 'O'

	[ 0x38, 0x90, 0x08, 0x08 ],		#0x90 'P'
	[ 0x00, 0x98, 0x08, 0x08 ],		#0x91 'Q'
	[ 0x08, 0x98, 0x08, 0x08 ],		#0x92 'R'
	[ 0x10, 0x98, 0x08, 0x08 ],		#0x93 'S'
	[ 0x18, 0x98, 0x08, 0x08 ],		#0x94 'T'
	[ 0x20, 0x98, 0x08, 0x08 ],		#0x95 'U'
	[ 0x28, 0x98, 0x08, 0x08 ],		#0x96 'V'
	[ 0x30, 0x98, 0x08, 0x08 ],		#0x97 'W'
	[ 0x38, 0x98, 0x08, 0x08 ],		#0x98 'X'
	[ 0x00, 0xa0, 0x08, 0x08 ],		#0x99 'Y'
	[ 0x08, 0xa0, 0x08, 0x08 ],		#0x9a 'Z'
	]

#entry_table = [0 for dot in range(0x2b)]
entry_table = [
	#0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
	'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
	'Q','R','S','T','U','V','W','X','Y','Z','.','-','/',' ','0','1',
	'2','3','4','5','6','7','8','9','>','<',' ']

#---------------------------------------------------------------------------------------------------
#指定された位置に8x8フォントを描画します
#	dn = ord(string)で取得したコード
#---------------------------------------------------------------------------------------------------
def font_put( _xp, _yp, _dn ):
	if( _dn == 0x00 ):		#スペース
		return

	_id = _dn
	pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

#---------------------------------------------------------------------------------------------------
#フォントテキストセット（side=1:右揃え（スコア用最大SCORE_KETA桁）））
#---------------------------------------------------------------------------------------------------
def set_font_text( _xp, _yp, _string, _side, _col=0 ):
	_code = 0x00
	#★[TODO]右詰めがうまくできてない（数値の並びが逆になる
	if _side == 1:
		if( ( len(_string) > SCORE_KETA ) or ( len(_string) < 0 ) ):
			return
		_codelist = list(_string)
		for i in range(SCORE_KETA):
			if( len(_string) < (SCORE_KETA-i) ):
				_code = 0x00
			else:
				_code = ord( _codelist[SCORE_KETA-1-i] )
				if( _col != 0 ):
					_code = _code + 0x40
			font_put( _xp + (i*8), _yp, _code )
	else:
		_codelist = list(_string)
		for i in range( len(_string) ):
			_code = ord( _codelist[i] )
			if( _col != 0 ):
				_code = _code + 0x40
			font_put( _xp + (i*8), _yp, _code )

#-----------------------------------------------------------------


#MULTI BLOCK
#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□■■■■■■■　■■■■■■■□
#1	■■■■■■■■　■■■■■■■■
#2	■■■■■■■■　■■■■■■■■
#3	■■■■■■■■　■■■■■■■■
#4	■■■■■■■■　■■■■■■■■
#5	■■■■■■■■　■■■■■■■■
#6	■■■■■■■■　■■■■■■■■
#7	■■■■■■■■　■■■■■■■■
#8	□■■■■■■■　■■■■■■■□

#mblk_tbl = [0 for tbl in range(0x8a)]
mblk_tbl = [
	0x10, 0x1, 0x20, 0x2, 0x30, 0x2, 0x40, 0x2, 0x50, 0x2, 0x60, 0x2, 0x70, 0x2, 0x80, 0x2, #0
	0x90, 0x2, 0xa0, 0x2, 0xb0, 0x2, 0xc0, 0x2, 0xd0, 0x2, 0xe0, 0x3, 0x01, 0x1, 0x11, 0x1, 
	0x21, 0x1, 0x31, 0x2, 0x41, 0x2, 0x51, 0x2, 0x61, 0x2, 0x71, 0x2, 0x81, 0x2, 0x91, 0x2, #1
	0xa1, 0x2, 0xb1, 0x2, 0xc1, 0x2, 0xd1, 0x3, 0xe1, 0x3, 0xf1, 0x3, 0x02, 0x2, 0x12, 0x2, 
	0x22, 0x3, 0x32, 0x3, 0x42, 0x3, 0x52, 0x3, 0x62, 0x3, 0x72, 0x3, 0x82, 0x3, 0x92, 0x3, #2
	0xa2, 0x3, 0xb2, 0x3, 0xc2, 0x3, 0xd2, 0x3, 0xe2, 0x6, 0xf2, 0x6, 0x03, 0x2, 0x13, 0x2, 
	0x23, 0x3, 0x33, 0x3, 0x43, 0x3, 0x53, 0x3, 0x63, 0x3, 0x73, 0x3, 0x83, 0x3, 0x93, 0x3, #3
	0xa3, 0x3, 0xb3, 0x3, 0xc3, 0x3, 0xd3, 0x3, 0xe3, 0x6, 0xf3, 0x6, 0x04, 0x2, 0x14, 0x2, 
	0x24, 0x3, 0x34, 0x3, 0x44, 0x3, 0x54, 0x3, 0x64, 0x3, 0x74, 0x3, 0x84, 0x3, 0x94, 0x3, #4
	0xa4, 0x3, 0xb4, 0x3, 0xc4, 0x3, 0xd4, 0x3, 0xe4, 0x6, 0xf4, 0x6, 0x05, 0x2, 0x15, 0x2, 
	0x25, 0x3, 0x35, 0x3, 0x45, 0x3, 0x55, 0x3, 0x65, 0x3, 0x75, 0x3, 0x85, 0x3, 0x95, 0x3, #5
	0xa5, 0x3, 0xb5, 0x3, 0xc5, 0x3, 0xd5, 0x3, 0xe5, 0x6, 0xf5, 0x6, 0x06, 0x2, 0x16, 0x2, 
	0x26, 0x3, 0x36, 0x3, 0x46, 0x3, 0x56, 0x3, 0x66, 0x3, 0x76, 0x3, 0x86, 0x3, 0x96, 0x3, #6
	0xa6, 0x3, 0xb6, 0x3, 0xc6, 0x3, 0xd6, 0x3, 0xe6, 0x6, 0xf6, 0x6, 0x07, 0x3, 0x17, 0x3, 
	0x27, 0x3, 0x37, 0x4, 0x47, 0x4, 0x57, 0x4, 0x67, 0x4, 0x77, 0x4, 0x87, 0x4, 0x97, 0x4, #7
	0xa7, 0x4, 0xb7, 0x4, 0xc7, 0x4, 0xd7, 0x5, 0xe7, 0x5, 0xf7, 0x5, 0x18, 0x3, 0x28, 0x4, 
	0x38, 0x4, 0x48, 0x4, 0x58, 0x4, 0x68, 0x4, 0x78, 0x4, 0x88, 0x4, 0x98, 0x4, 0xa8, 0x4, #8
	0xb8, 0x4, 0xc8, 0x4, 0xd8, 0x4, 0xe8, 0x5, 0xff, 0xff]

#MULTI ROCK
#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□■■■■■■■　■■■■■■■□
#1	■■■■■■■■　■■■■■■■■
#2	■■■■■■■■　■■■■■■■■
#3	■■■■■■■■　■■■■■■■■
#4	■■■■■■■■　■■■■■■■■
#5	■■■■■■■■　■■■■■■■■
#6	■■■■■■■■　■■■■■■■■
#7	■■■■■■■■　■■■■■■■■
#8	□■■■■■■■　■■■■■■■□

#rblk_tbl = [0 for tbl in range(0x8a)]
rblk_tbl = [
	0x10, 0x1, 0x20, 0x1, 0x30, 0x1, 0x40, 0x1, 0x50, 0x1, 0x60, 0x1, 0x70, 0x1, 0x80, 0x1, #0
	0x90, 0x1, 0xa0, 0x1, 0xb0, 0x1, 0xc0, 0x1, 0xd0, 0x1, 0xe0, 0x1, 0x01, 0x1, 0x11, 0x1, 
	0x21, 0x2, 0x31, 0x2, 0x41, 0x2, 0x51, 0x2, 0x61, 0x2, 0x71, 0x2, 0x81, 0x2, 0x91, 0x2, #1
	0xa1, 0x2, 0xb1, 0x2, 0xc1, 0x2, 0xd1, 0x2, 0xe1, 0x2, 0xf1, 0x3, 0x02, 0x1, 0x12, 0x2, 
	0x22, 0x2, 0x32, 0x2, 0x42, 0x2, 0x52, 0x2, 0x62, 0x2, 0x72, 0x2, 0x82, 0x2, 0x92, 0x2, #2
	0xa2, 0x2, 0xb2, 0x2, 0xc2, 0x2, 0xd2, 0x2, 0xe2, 0x2, 0xf2, 0x3, 0x03, 0x1, 0x13, 0x2, 
	0x23, 0x2, 0x33, 0x2, 0x43, 0x2, 0x53, 0x2, 0x63, 0x2, 0x73, 0x2, 0x83, 0x2, 0x93, 0x2, #3
	0xa3, 0x2, 0xb3, 0x2, 0xc3, 0x2, 0xd3, 0x2, 0xe3, 0x2, 0xf3, 0x3, 0x04, 0x1, 0x14, 0x2, 
	0x24, 0x2, 0x34, 0x2, 0x44, 0x2, 0x54, 0x2, 0x64, 0x2, 0x74, 0x2, 0x84, 0x2, 0x94, 0x2, #4
	0xa4, 0x2, 0xb4, 0x2, 0xc4, 0x2, 0xd4, 0x2, 0xe4, 0x2, 0xf4, 0x3, 0x05, 0x1, 0x15, 0x2, 
	0x25, 0x2, 0x35, 0x2, 0x45, 0x2, 0x55, 0x2, 0x65, 0x2, 0x75, 0x2, 0x85, 0x2, 0x95, 0x2, #5
	0xa5, 0x2, 0xb5, 0x2, 0xc5, 0x2, 0xd5, 0x2, 0xe5, 0x2, 0xf5, 0x3, 0x06, 0x1, 0x16, 0x2, 
	0x26, 0x2, 0x36, 0x2, 0x46, 0x2, 0x56, 0x2, 0x66, 0x2, 0x76, 0x2, 0x86, 0x2, 0x96, 0x2, #6
	0xa6, 0x2, 0xb6, 0x2, 0xc6, 0x2, 0xd6, 0x2, 0xe6, 0x2, 0xf6, 0x3, 0x07, 0x1, 0x17, 0x2, 
	0x27, 0x2, 0x37, 0x2, 0x47, 0x2, 0x57, 0x2, 0x67, 0x2, 0x77, 0x2, 0x87, 0x2, 0x97, 0x2, #7
	0xa7, 0x2, 0xb7, 0x2, 0xc7, 0x2, 0xd7, 0x2, 0xe7, 0x2, 0xf7, 0x3, 0x18, 0x3, 0x28, 0x3, 
	0x38, 0x3, 0x48, 0x3, 0x58, 0x3, 0x68, 0x3, 0x78, 0x3, 0x88, 0x3, 0x98, 0x3, 0xa8, 0x3, #8
	0xb8, 0x3, 0xc8, 0x3, 0xd8, 0x3, 0xe8, 0x3, 0xff, 0xff]

#MULTI BLOCKの影
#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□■□■□■□■　□■□■□■□□
#1	■□■□■□■□　■□■□■□■□
#2	□■□■□■□■　□■□■□■□□
#3	■□■□■□■□　■□■□■□■□
#4	□■□■□■□■　□■□■□■□□
#5	■□■□■□■□　■□■□■□■□
#6	□■□■□■□■　□■□■□■□□
#7	■□■□■□■□　■□■□■□■□
#8	□■□■□■□■　□■□■□■□□

#smblk_tbl = [0 for tbl in range(0x4e)]
smblk_tbl = [
	0x10, 0xb, 0x30, 0xb, 0x50, 0xb, 0x70, 0xb, 0x90, 0xb, 0xb0, 0xb, 0xd0, 0xb, 0x01, 0xb, #0
	0x21, 0xb, 0x41, 0xb, 0x61, 0xb, 0x81, 0xb, 0xa1, 0xb, 0xc1, 0xb, 0xe1, 0xb, 0x12, 0xb, 
	0x32, 0xb, 0x52, 0xb, 0x72, 0xb, 0x92, 0xb, 0xb2, 0xb, 0xd2, 0xb, 0xf2, 0xb, 0x03, 0xb, #1
	0x23, 0xb, 0x43, 0xb, 0x63, 0xb, 0x83, 0xb, 0xa3, 0xb, 0xc3, 0xb, 0xe3, 0xb, 0x14, 0xb, 
	0x34, 0xb, 0x54, 0xb, 0x74, 0xb, 0x94, 0xb, 0xb4, 0xb, 0xd4, 0xb, 0xf4, 0xb, 0x05, 0xb, #2
	0x25, 0xb, 0x45, 0xb, 0x65, 0xb, 0x85, 0xb, 0xa5, 0xb, 0xc5, 0xb, 0xe5, 0xb, 0x16, 0xb, 
	0x36, 0xb, 0x56, 0xb, 0x76, 0xb, 0x96, 0xb, 0xb6, 0xb, 0xd6, 0xb, 0xf6, 0xb, 0x07, 0xb, #3
	0x27, 0xb, 0x47, 0xb, 0x67, 0xb, 0x87, 0xb, 0xa7, 0xb, 0xc7, 0xb, 0xe7, 0xb, 0x18, 0xb, 
	0x38, 0xb, 0x58, 0xb, 0x78, 0xb, 0x98, 0xb, 0xb8, 0xb, 0xd8, 0xb, 0xff, 0xff]


#右端の影
#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□■□■□■□■　□□□□□□□□
#1	■□■□■□■□　□□□□□□□□
#2	□■□■□■□■　□□□□□□□□
#3	■□■□■□■□　□□□□□□□□
#4	□■□■□■□■　□□□□□□□□
#5	■□■□■□■□　□□□□□□□□
#6	□■□■□■□■　□□□□□□□□
#7	■□■□■□■□　□□□□□□□□
#8	□■□■□■□■　□□□□□□□□
#srblk_tbl = [0 for tbl in range(0x2a)]
srblk_tbl = [
	0x10, 0xb, 0x30, 0xb, 0x50, 0xb, 0x70, 0xb, 0x01, 0xb, 0x21, 0xb, 0x41, 0xb, 0x61, 0xb, #0
	0x12, 0xb, 0x32, 0xb, 0x52, 0xb, 0x72, 0xb, 0x03, 0xb, 0x23, 0xb, 0x43, 0xb, 0x63, 0xb, 
	0x14, 0xb, 0x34, 0xb, 0x54, 0xb, 0x74, 0xb, 0x05, 0xb, 0x25, 0xb, 0x45, 0xb, 0x65, 0xb, #1
	0x16, 0xb, 0x36, 0xb, 0x56, 0xb, 0x76, 0xb, 0x07, 0xb, 0x27, 0xb, 0x47, 0xb, 0x67, 0xb, 
	0x18, 0xb, 0x38, 0xb, 0x58, 0xb, 0x78, 0xb, 0xff, 0xff]

#右端の影２（ベタ版）
#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□■■■■■■■　□□□□□□□□
#1	■■■■■■■■　□□□□□□□□
#2	■■■■■■■■　□□□□□□□□
#3	■■■■■■■■　□□□□□□□□
#4	■■■■■■■■　□□□□□□□□
#5	■■■■■■■■　□□□□□□□□
#6	■■■■■■■■　□□□□□□□□
#7	■■■■■■■■　□□□□□□□□
#8	□■■■■■■■　□□□□□□□□
#srblk2_tbl = [0 for tbl in range(0x4e)]
srblk2_tbl = [
	0x10, 0xb, 0x20, 0xb, 0x30, 0xb, 0x40, 0xb, 0x50, 0xb, 0x60, 0xb, 0x70, 0xb, 0x01, 0xb, #0
	0x11, 0xb, 0x21, 0xb, 0x31, 0xb, 0x41, 0xb, 0x51, 0xb, 0x61, 0xb, 0x71, 0xb, 0x02, 0xb, 
	0x12, 0xb, 0x22, 0xb, 0x32, 0xb, 0x42, 0xb, 0x52, 0xb, 0x62, 0xb, 0x72, 0xb, 0x03, 0xb, #1
	0x13, 0xb, 0x23, 0xb, 0x33, 0xb, 0x43, 0xb, 0x53, 0xb, 0x63, 0xb, 0x73, 0xb, 0x04, 0xb, 
	0x14, 0xb, 0x24, 0xb, 0x34, 0xb, 0x44, 0xb, 0x54, 0xb, 0x64, 0xb, 0x74, 0xb, 0x05, 0xb, #2
	0x15, 0xb, 0x25, 0xb, 0x35, 0xb, 0x45, 0xb, 0x55, 0xb, 0x65, 0xb, 0x75, 0xb, 0x06, 0xb, 
	0x16, 0xb, 0x26, 0xb, 0x36, 0xb, 0x46, 0xb, 0x56, 0xb, 0x66, 0xb, 0x76, 0xb, 0x07, 0xb, #3
	0x17, 0xb, 0x27, 0xb, 0x37, 0xb, 0x47, 0xb, 0x57, 0xb, 0x67, 0xb, 0x77, 0xb, 0x18, 0xb, 
	0x28, 0xb, 0x38, 0xb, 0x48, 0xb, 0x58, 0xb, 0x68, 0xb, 0x78, 0xb, 0xff, 0xff]

#-----------------------------------------------------------------
#最初の高さ、ブロックの並び（色番号）320x240(横18縦最大20)、240x240(横13縦最大20)、終端0xff

#終端テーブル
stageend_tbl = [0 for tbl in range(1)]
stageend_tbl = [ 0xff ]

#-------
#0x0:無し	
#0x1:ROCK	0x2:WHITE	0x3:RED		0x4:GREEN	#0x5:BLUE
#0x6:YELLOW	0x7:MIZU	0x8:PURPLE	0x9:ORANGE	0xa PINK
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
	5,0,0,5,7,0,0,2,0,0,0,2,9,0,9,10,0,10,
	5,0,0,5,7,0,0,2,0,0,0,2,9,0,9,10,0,10,
	5,5,5,0,7,0,0,2,0,0,0,2,9,0,0,10,10,0,
	5,0,0,5,7,0,0,2,0,0,0,2,9,0,0,10,0,10,
	5,0,0,5,7,0,0,2,0,0,0,2,9,0,9,10,0,10,
	5,0,0,5,7,0,0,2,0,0,0,2,9,0,9,10,0,10,
	5,5,5,5,7,7,7,0,2,2,2,0,0,9,0,10,0,10,
	0xff]

stage002_tbl = [
	3,
	2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
	3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
	4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
	6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
	7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
	8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,
	9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
	0xff]

stage003_tbl = [
	5,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,1,0,0,4,4,0,0,1,0,0,0,0,0,
	0,0,0,0,0,1,0,3,3,3,3,0,1,0,0,0,0,0,
	0,0,0,0,0,1,2,2,2,2,2,2,1,0,0,0,0,0,
	0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0xff]

stage004_tbl = [
	5,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,1,5,5,1,0,0,
	0,0,0,7,7,1,8,8,8,8,8,8,1,6,6,1,0,0,
	0,0,1,6,6,1,8,8,8,8,8,8,1,7,7,1,0,0,
	0,0,1,5,5,1,8,8,8,8,8,8,1,0,0,1,0,0,
	0,0,1,1,1,1,8,8,8,8,8,8,1,0,0,1,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,
	0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,
	0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0xff]

stage005_tbl = [
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

stage006_tbl = [
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



stage0_tbl = [
	stage006_tbl, stage001_tbl, stage002_tbl, stage003_tbl, stage004_tbl, stage005_tbl, 
	stageend_tbl
	]

#-------
#0x0:無し	
#0x1:ROCK	0x2:WHITE	0x3:RED		0x4:GREEN	#0x5:BLUE
#0x6:YELLOW	0x7:MIZU	0x8:PURPLE	0x9:ORANGE	0xa PINK
#-------
#[1]320x240 Crystal Hammer Stage
stage101_tbl = [
	5,
	3,3,3,3,3,9,9,9,9,9,9,9,9,3,3,3,3,3,
	8,4,9,3,1,6,9,9,9,9,9,9,6,1,3,9,4,8,
	4,9,3,9,1,6,6,6,6,6,6,6,6,1,9,3,9,4,
	9,3,9,4,1,1,1,1,1,1,1,1,1,1,4,9,3,9,
	3,9,4,8,8,8,9,9,9,9,9,9,8,8,8,4,9,3,
	9,4,8,0,0,0,0,9,9,9,9,0,0,0,0,8,4,9,
	4,8,0,0,0,0,0,0,9,9,0,0,0,0,0,0,8,4,
	8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,2,2,0,0,0,0,0,0,2,2,0,0,0,0,
	0,0,0,0,2,2,0,0,0,0,0,0,2,2,0,0,0,0,
	0xff]


stage1_tbl = [
	stage101_tbl,
#	stage101_tbl, stage102_tbl, stage103_tbl, stage104_tbl, stage105_tbl,
#	stage106_tbl, stage107_tbl, stage108_tbl, stage109_tbl, stage110_tbl,
#	stage111_tbl, stage112_tbl, stage113_tbl, stage114_tbl, stage115_tbl,
#	stage116_tbl, stage117_tbl, stage118_tbl, stage119_tbl, stage110_tbl,
#	stage121_tbl, stage122_tbl, stage123_tbl, stage124_tbl, stage125_tbl,
#	stage126_tbl, stage127_tbl, stage128_tbl, stage129_tbl, stage120_tbl,
#	stage131_tbl, stage132_tbl, stage133_tbl, stage134_tbl, stage135_tbl,
#	stage136_tbl, stage137_tbl, stage138_tbl, stage139_tbl, stage130_tbl,
#	stage141_tbl, stage142_tbl, stage143_tbl, stage144_tbl, stage145_tbl,
#	stage146_tbl, stage147_tbl, stage148_tbl, stage149_tbl, stage150_tbl,
	stageend_tbl
	]


#-------
#0x0:無し	
#0x1:ROCK	0x2:WHITE	0x3:RED		0x4:GREEN	#0x5:BLUE
#0x6:YELLOW	0x7:MIZU	0x8:PURPLE	0x9:ORANGE	0xa PINK
#-------
#[2]240x240 Original Stage

stage201_tbl = [
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
	5,0,5,7,2,0,2,9,0,0,10,0,10,
	5,5,5,7,2,2,2,9,9,9,10,0,10,
	0xff]

stage202_tbl = [
	3,
	2,2,2,2,2,2,2,2,2,2,2,2,2,
	3,3,3,3,3,3,3,3,3,3,3,3,3,
	4,4,4,4,4,4,4,4,4,4,4,4,4,
	5,5,5,5,5,5,5,5,5,5,5,5,5,
	0xff]

stage203_tbl = [
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

stage204_tbl = [
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

stage205_tbl = [
	7,
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


stage2_tbl = [
	stage201_tbl, stage202_tbl, stage203_tbl, stage204_tbl, stage205_tbl, 
	stageend_tbl,
	]

#-------
#0x0:無し	
#0x1:ROCK	0x2:WHITE	0x3:RED		0x4:GREEN	#0x5:BLUE
#0x6:YELLOW	0x7:MIZU	0x8:PURPLE	0x9:ORANGE	0xa PINK
#-------
#[3]240x240 Arkanoid stage(Arkanoid1, Arkanoid2)
stage301_tbl = [
	4,
	2,3,4,5,6,7,8,9,3,4,5,6,7,
	0,2,4,5,6,7,8,9,3,4,5,6,7,
	0,0,2,5,6,7,8,9,3,4,5,6,7,
	0,0,0,2,6,7,8,9,3,4,5,6,7,
	0,0,0,0,2,7,8,9,3,4,5,6,7,
	0,0,0,0,0,2,8,9,3,4,5,6,7,
	0,0,0,0,0,0,2,9,3,4,5,6,7,
	0,0,0,0,0,0,0,2,3,4,5,6,7,
	0,0,0,0,0,0,0,0,2,4,5,6,7,
	0,0,0,0,0,0,0,0,0,2,5,6,7,
	0,0,0,0,0,0,0,0,0,0,2,6,7,
	0,0,0,0,0,0,0,0,0,0,0,2,7,
	0,0,0,0,0,0,0,0,0,0,0,0,2,
	0xff]

stage302_tbl = [
	2,
	6,6,6,6,6,6,6,6,6,6,6,6,6,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,1,1,1,1,0,0,0,1,1,1,1,1,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	8,8,8,8,8,8,8,8,8,8,8,8,8,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,1,1,1,1,1,1,1,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	7,7,7,7,7,7,7,7,7,7,7,7,7,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	1,1,1,1,1,0,0,0,1,1,1,1,1,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	3,3,3,3,3,3,3,3,3,3,3,3,3,
	0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,1,1,1,1,1,1,1,0,0,0,
	0xff]

stage3_tbl = [
	stage301_tbl, stage302_tbl,
#	stage301_tbl, stage302_tbl, stage303_tbl, stage304_tbl, stage305_tbl,
#	stage306_tbl, stage307_tbl, stage308_tbl, stage309_tbl, stage310_tbl,
#	stage311_tbl, stage312_tbl, stage313_tbl, stage314_tbl, stage315_tbl,
#	stage316_tbl, stage317_tbl, stage318_tbl, stage319_tbl, stage310_tbl,
#	stage321_tbl, stage322_tbl, stage323_tbl, stage324_tbl, stage325_tbl,
#	stage326_tbl, stage327_tbl, stage328_tbl, stage329_tbl, stage320_tbl,
#	stage331_tbl, stage332_tbl, stage333_tbl, stage334_tbl, stage335_tbl,
#	stage336_tbl, stage337_tbl, stage338_tbl, stage339_tbl, stage330_tbl,
#	stage341_tbl, stage342_tbl, stage343_tbl, stage344_tbl, stage345_tbl,
#	stage346_tbl, stage347_tbl, stage348_tbl, stage349_tbl, stage350_tbl,
#	stage351_tbl, stage352_tbl, stage353_tbl, stage354_tbl, stage355_tbl,
#	stage356_tbl, stage357_tbl, stage358_tbl, stage359_tbl, stage350_tbl,
#	stage361_tbl, stage362_tbl, stage363_tbl, stage364_tbl, 
	stageend_tbl
	]

stage_tbl = [stage0_tbl, stage1_tbl, stage2_tbl, stage3_tbl]

#-----------------------------------------------------------------
#ドットパターン描画
#-----------------------------------------------------------------
def dot_pattern( _dx, _dy, _tp, _adr ):
	_cnt = 0
	while (_adr[_cnt*2+0] != 0xff):
		_xp = pyxel.floor( _adr[_cnt*2+0]/0x10 )
		_yp = pyxel.floor( _adr[_cnt*2+0]&0x0f )
		_col = _adr[_cnt*2+1] + _tp * 0x10
		pyxel.pset( _dx + _xp, _dy + _yp, _col )
		_cnt+=1

#-----------------------------------------------------------------
#キャラクタセット
#	X座標, Y座標, id番号
#-----------------------------------------------------------------
def cput( _xp, _yp, _id, _shadow ):
	#ドットパターンタイプ？
	if( ctbl[_id][0] == 0xff ):
		#ブロック
		if( ctbl[_id][1] == 0 ):
			if( _shadow == 1 ):		#ブロックの影
				_cc = PALETTE_SHADOW
				_xp = _xp + 0x08
				_yp = _yp + 0x08
				dot_pattern( _xp, _yp, _cc, smblk_tbl )
			elif( _shadow == 2 ):	#ブロック右端の影
				_cc = PALETTE_SHADOW
				_xp = _xp + 0x08
				_yp = _yp + 0x08
				dot_pattern( _xp, _yp, _cc, srblk_tbl )
			else:					#通常ブロック
				_cc = _id - ID_BLK_MULTI + 1
				dot_pattern( _xp, _yp, _cc, mblk_tbl )
		#ロック
		elif( ctbl[_id][1] == 1 ):
			if( _shadow == 1 ):
				_cc = PALETTE_SHADOW
				_xp = _xp + 0x08
				_yp = _yp + 0x08
				dot_pattern( _xp, _yp, _cc, smblk_tbl )
			else:
				_cc = _id - ID_BLK_MULTI + 1
				dot_pattern( _xp, _yp, _cc, rblk_tbl )
	else:
			pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

#-----------------------------------------------------------------
#バー初期化
#-----------------------------------------------------------------
def bar_init():
	GWK[PLY_WORK + cid] = 0x00
	GWK[PLY_WORK + ccond] = F_LIVE
	GWK[PLY_WORK + cxpos] = int(SCREEN_WIDTH / 2) - int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )
	GWK[PLY_WORK + cypos] = SCREEN_HEIGHT - 0x10
	GWK[PLY_WORK + cxspd] = 0
	GWK[PLY_WORK + cyspd] = 0

#-----------------------------------------------------------------
#玉初期化
#-----------------------------------------------------------------
def ball_init():
	#ボール初期化
	GWK[ball_speed] = 3		#初期打ち出し速度
	GWK[ball_degree] = 45	#初期打ち出し角度

	for _cnt in range(BALL_MAX):
		_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
		GWK[_wk + cid] = ID_BALL + ( GWK[ball_color] * 2 )		#３色から選択
		if( _cnt == 0 ):
			GWK[_wk + ccond] = F_LIVE+F_ON
			GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] + int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )
			GWK[_wk + cypos] = GWK[PLY_WORK + cypos] - ctbl[GWK[_wk + cid]][2]
		else:
			GWK[_wk + ccond] = 0
			GWK[_wk + cxpos] = 0
			GWK[_wk + cypos] = 0

		#玉の移動スピードは基本スピードからXY差分で計測する（反射するたびに再計算する）
		#三方向分離の時も再計算必要
		GWK[_wk + cspd] = GWK[ball_speed]
		GWK[_wk + cdeg] = GWK[ball_degree]
		GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		GWK[_wk + cyspd] = GWK[_wk + cspd] * pyxel.sin(GWK[_wk + cdeg])


#-----------------------------------------------------------------
#各ステージ初期化
#-----------------------------------------------------------------
def stage_init():

	#スコア初期化
	GWK[score] = 0

	#バー初期化
	bar_init()

	#玉初期化
	ball_init()

	#ステージマップ初期化
	_stg_adr = stage_tbl[ GWK[stage_type] ]
	_adr = _stg_adr[ GWK[stage_number] ]
	_cnt = 0
	GWK[start_height] = _adr[_cnt]
	#stage end code?
	if( GWK[start_height] == 0xff ):
		return		#★[TODO]コール元で終端の場合の処理が必要
	_cnt += 1
	
	_bcnt = 0
	for _ycnt in range( GWK[blockmap_Vmax] - GWK[start_height] ):
		for _xcnt in range( GWK[blockmap_Hmax] ):
			_id = _adr[_cnt]
			if( _id == 0xff ):
				return
			elif( _id == 0 ):
				GWK[BLOCK_WORK + _bcnt] = _id
			else:
				GWK[BLOCK_WORK + _bcnt] = BF_LIVE + _id

			_bcnt += 1
			_cnt += 1

#-----------------------------------------------------------------
#ステージブロック表示
#-----------------------------------------------------------------
def stage_block():
	_bcnt = 0
	for _ycnt in range( GWK[blockmap_Vmax] - GWK[start_height] ):
		for _xcnt in range( GWK[blockmap_Hmax] ):
			_data = GWK[BLOCK_WORK + _bcnt]
			if( _data & BF_LIVE ):
				_id = _data & 0x0f
				if( _id == 0 ):
					pass
				else:
					if( GWK[multi_color_switch] != 0 ):
						_id = _id + ID_BLK_MULTI - 1
					else:
						_id = _id + ID_BLK_DEF - 1
					cput( LEFT_OFFSET + GWK[blockmap_shortofs] + ( _xcnt * BLK_WIDTH ), ( GWK[start_height] * BLK_HEIGHT ) + ( _ycnt * BLK_HEIGHT ) + UP_OFFSET, _id, 0 )
			_bcnt+=1

#-----------------------------------------------------------------
#影描画
#	ブロックDEF or MULTIの影は共通
#	★玉やバー、敵キャラの影も必要なので一旦表示しないで作成
#-----------------------------------------------------------------
def stage_block_shadow():
	_stg_adr = stage_tbl[ GWK[stage_type] ]
	_adr = _stg_adr[ GWK[stage_number] ]
	_cnt = 0
	_start_height = _adr[_cnt]
	#stage end code?
	if( GWK[start_height] == 0xff ):
		return		#★[TODO]コール元で終端の場合の処理が必要
	_cnt+=1
	
	for _ycnt in range( GWK[blockmap_Vmax] - _start_height ):
		for _xcnt in range( GWK[blockmap_Hmax] ):
			_id = _adr[_cnt]
			if( _id == 0xff ):
				return
			elif( _id == 0 ):
				pass
			else:
				_id = _id + ID_BLK_MULTI - 1		#ブロック
				_stype = 1
				if( _xcnt == (GWK[blockmap_Hmax]-1) ):		#右端？
					_stype = 2
				cput( LEFT_OFFSET + GWK[blockmap_shortofs] + ( _xcnt * BLK_WIDTH ), ( _start_height * BLK_HEIGHT ) + ( _ycnt * BLK_HEIGHT ) + UP_OFFSET, _id, _stype )
			_cnt+=1

#-----------------------------------------------------------------
#work clear
#-----------------------------------------------------------------
def work_clear():
	for _cnt in range( WORK_TOP, WORK_END ):
		GWK[_cnt] = 0

#-----------------------------------------------------------------
#入力（キーボード＆ジョイパッド）
#-----------------------------------------------------------------
#上
def getInputUP():
	if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
		return 1
	else:
		return 0
#下
def getInputDOWN():
	if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
		return 1
	else:
		return 0
#左
def getInputLEFT():
	if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
		return 1
	else:
		return 0
#右
def getInputRIGHT():
	if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
		return 1
	else:
		return 0
#button-A（決定）
def getInputA():
	if pyxel.btnp(pyxel.KEY_Z, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold=10, repeat=10):
		return 1
	else:
		return 0
#button-B（キャンセル）
def getInputB():
	if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
		return 1
	else:
		return 0
#button-X
def getInputX():
	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
		return 1
	else:
		return 0
#button-Y
def getInputY():
	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
		return 1
	else:
		return 0


#-----------------------------------------------------------------
#バーにヒットするたび玉の移動スピードを加速させる
#-----------------------------------------------------------------
def ball_add_speed_with_bar( _wk ):
	GWK[_wk + chit] += 1
	if( int( ( GWK[_wk + chit] % 10 ) ) == 0 ):
		GWK[_wk + cspd] = GWK[ball_speed] + ( ( GWK[_wk + chit] / 10 ) * 0.1 )
		#print("BALL-SPEED = ", GWK[_wk + cspd] );

#-----------------------------------------------------------------
#玉の反射角度調整
#	バーに当たらずに延々と繰り返し球がヒットを繰り返したとき反射角度を調整する
#	（速度も変更する）
#-----------------------------------------------------------------
def ball_degree_control( _wk ):
	#反射角度調整
	GWK[_wk + chit2] += 1
	#print("[ball_degree_control]", GWK[_wk + chit2] )
	if( GWK[_wk + chit2] > 30 ):
		if( GWK[_wk + cdeg] > 45 ):
			GWK[_wk + cdeg] -= pyxel.rndi(7,41)
		else:
			GWK[_wk + cdeg] += pyxel.rndi(7,41)

		#速度も同時に変更する
		if( GWK[_wk + cxspd] < 0 ):
			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
		else:
			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		if( GWK[_wk + cyspd] < 0 ):
			GWK[_wk + cyspd] = GWK[_wk + cspd] * pyxel.sin(GWK[_wk + cdeg]) * (-1)
		else:
			GWK[_wk + cyspd] = GWK[_wk + cspd] * pyxel.sin(GWK[_wk + cdeg])

		print("[ball_degree_control]",GWK[_wk + cdeg], GWK[_wk + cxspd], GWK[_wk + cyspd] )
		GWK[_wk + chit2] = 0

#-----------------------------------------------------------------
#玉のヒットチェック
#	座標から今いるブロックを計算してその周辺とのチェックを実施
#	対象：Y座標がバーの高さ
#		  Y座標がブロックの範囲
#		  ★[TODO]Y座標がおじゃま敵の範囲

#★[TODO]右端のブロックの場合はさらに右のブロックチェックは行わないようにする（左も同様
#★[TODO]既存バグ：横240にしたときのブロック判定の位置がおかしい

#-----------------------------------------------------------------
def ball_hit_check( _wk ):

	#[玉とバー]
	#玉の中心座標を取得
	_xp = int(GWK[_wk + cxpos]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
	_yp = int(GWK[_wk + cypos]) + int( ctbl[GWK[_wk + cid]][3] / 2 )

	#玉の移動方向が下以外はバーにヒットしない
	if( GWK[_wk + cyspd] > 0 ):
		#Y座標がバーの範囲内
		#バーのヒット範囲を取得
		_bxL = GWK[PLY_WORK + cxpos] - int( ctbl[GWK[_wk + cid]][2] / 2 )
		_bxR = GWK[PLY_WORK + cxpos] + ctbl[GWK[PLY_WORK + cid]][2] + int( ctbl[GWK[_wk + cid]][2] / 2 )
		_byU = GWK[PLY_WORK + cypos] - int( ctbl[GWK[_wk + cid]][3] / 2 )
		_byD = GWK[PLY_WORK + cypos] + ctbl[GWK[PLY_WORK + cid]][3] + int( ctbl[GWK[_wk + cid]][3] / 2 )

		if( ( ( _bxL <= _xp ) and ( _bxR > _xp ) ) and ( ( _byU <= _yp ) and ( _byD > _yp ) ) ):
			#バーの範囲内

#---分割
			#保存値を戻す
			GWK[_wk + cxpold] = GWK[save_cxpold]
			GWK[_wk + cypold] = GWK[save_cypold]
			GWK[_wk + cxspd] = GWK[save_cxspd]
			GWK[_wk + cyspd] = GWK[save_cyspd]
#---分割

			#めりこみ対応
			if( _bxL > _xp ):
				GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos]
			elif( _bxR < _xp ):
				GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] + ctbl[GWK[PLY_WORK + cid]][2]

			if( _byU > _yp ):
				GWK[_wk + cypos] = GWK[PLY_WORK + cypos]
			elif( _byD < _yp ):
				GWK[_wk + cypos] = GWK[PLY_WORK + cypos] + ctbl[GWK[PLY_WORK + cid]][3]
				
			#バーのどの位置に接触したかの判定で反射角度＆速度を決める（float判定）
			_div = ( GWK[_wk + cxpos] + ( ctbl[GWK[_wk + cid]][2] / 2 ) - _bxL )
			_b81 = ctbl[GWK[PLY_WORK + cid]][2] / 8			#1/8 左方向へ
			_b41 = ctbl[GWK[PLY_WORK + cid]][2] / 4			#2/8 左方向へ
			_b83 = ctbl[GWK[PLY_WORK + cid]][2] * 3 / 8		#3/8 方向変化無し
															#4/8 変化無し
			_b85 = ctbl[GWK[PLY_WORK + cid]][2] * 5 / 8		#5/8 方向変化無し
			_b43 = ctbl[GWK[PLY_WORK + cid]][2] * 3 / 4		#6/8 右方向へ
			_b87 = ctbl[GWK[PLY_WORK + cid]][2] * 7 / 8		#7/8 右方向へ
			
			#print("_div = ",_div, _b81, _b41, _b83, _b85, _b43, _b87)
			#左端から0/8～1/8 = speed= + → deg >= 30 → -20 左方向へ
			#                   speed= - → deg >= 30 → -20 左方向へ
			##左端から1/8～2/8 = speed= + → deg >= 20 → -10 左方向へ
			##                   speed= - → deg >= 20 → -10 左方向へ
			#左端から2/8～3/8 = speed= + → deg < 75 → +25 X方向変化無し
			#                   speed= - → deg < 75 → +25 X方向変化無し
			#左端から3/8～5/8 = Y方向反転のみX方向変化無し
			#左端から5/8～6/8 = speed= + → deg < 75 → +25 X方向変化無し
			#                   speed= - → deg < 75 → +25 X方向変化無し
			##左端から6/8～7/8 = speed= + → deg >= 20 → +10 右方向へ
			##                   speed= - → deg >= 20 → +10 右方向へ
			#左端から7/8～8/8 = speed= + → deg >= 30 → +20 右方向へ
			#                   speed= - → deg >= 30 → +20 右方向へ
			if( _div < _b81 ):
				#print("LEFT-1/8")
				if( GWK[_wk + cxspd] >= 0 ):
					if( GWK[_wk + cdeg] >= 30 ):
						GWK[_wk + cdeg] -= 20
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
				else:
					if( GWK[_wk + cdeg] >= 30 ):
						GWK[_wk + cdeg] -= 20
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
			elif( ( _div >= _b81 ) and ( _div < _b41 ) ):
				#print("LEFT-1/4")
				if( GWK[_wk + cxspd] >= 0 ):
					if( GWK[_wk + cdeg] >= 20 ):
						GWK[_wk + cdeg] -= 10
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
				else:
					if( GWK[_wk + cdeg] >= 20 ):
						GWK[_wk + cdeg] -= 10
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
			elif( ( _div >= _b41 ) and ( _div < _b83 ) ):
				#print("LEFT-3/8")
				if( GWK[_wk + cdeg] < 75 ):
					GWK[_wk + cdeg] += 25
					#xspdの符号は変えない
					if( GWK[_wk + cxspd] < 0 ):
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
					else:
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
			elif( ( _div >= _b85 ) and ( _div < _b43 ) ):
				#print("RIGHT-3/8")
				if( GWK[_wk + cdeg] < 75 ):
					GWK[_wk + cdeg] += 25
					#xspdの符号は変えない
					if( GWK[_wk + cxspd] < 0 ):
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
					else:
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
			elif( ( _div >= _b43 ) and ( _div < _b87 ) ):
				#print("RIGHT-1/4")
				if( GWK[_wk + cxspd] >= 0 ):
					if( GWK[_wk + cdeg] >= 20 ):
						GWK[_wk + cdeg] -= 10
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
				else:
					if( GWK[_wk + cdeg] >= 20 ):
						GWK[_wk + cdeg] -= 10
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
			elif( _div >= _b87 ):
				#print("RIGHT-1/8")
				if( GWK[_wk + cxspd] >= 0 ):
					if( GWK[_wk + cdeg] >= 30 ):
						GWK[_wk + cdeg] -= 20
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
				else:
					if( GWK[_wk + cdeg] >= 30 ):
						GWK[_wk + cdeg] -= 20
						GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
			
			#deg調整（0 or 90にはしない）
			if( GWK[_wk + cdeg] < 10 ):
				GWK[_wk + cdeg] = 10
			if( GWK[_wk + cdeg] > 80 ):
				GWK[_wk + cdeg] = 80
				
			GWK[_wk + cyspd] = GWK[_wk + cspd] * pyxel.sin(GWK[_wk + cdeg]) * (-1)

			#バーにヒットするたび加速
			ball_add_speed_with_bar( _wk )
			
			#角度調整カウンタクリア
			GWK[_wk + chit2] = 0
			#Bar Hit!
#---分割
			#ヒットセット
			GWK[_wk + ccond] |= F_HIT
#---分割

			return


	#[玉とブロック]
	#玉の中心座標を取得
	_xp = int(GWK[_wk + cxpos]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
	_yp = int(GWK[_wk + cypos]) + int( ctbl[GWK[_wk + cid]][3] / 2 )
	#玉の中心座標のブロック位置を算出
	_bx = int( ( _xp - LEFT_OFFSET + GWK[blockmap_shortofs] ) / BLK_WIDTH )
	_by = int( ( _yp - UP_OFFSET ) / BLK_HEIGHT )

	#ブロックの最低高さ以上
	if( ( _by >= GWK[start_height] ) and ( _by < GWK[blockmap_Vmax] ) ):
		#玉の中心が居るブロックの位置
		_block_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
		#存在するブロック？
		if( GWK[BLOCK_WORK + _block_pos] & BF_LIVE ):

			#移動前のブロックを算出
			_xpold = int(GWK[_wk + cxpold]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
			_ypold = int(GWK[_wk + cypold]) + int( ctbl[GWK[_wk + cid]][3] / 2 )
			_bxold = int( ( _xpold - LEFT_OFFSET + GWK[blockmap_shortofs] ) / BLK_WIDTH )
			_byold = int( ( _ypold - UP_OFFSET ) / BLK_HEIGHT )
			#_block_pos_old = (_byold - GWK[start_height]) * GWK[blockmap_Hmax] + _bxold

			#当たったブロックと移動前のブロックを比較して位置関係から反射方向を決める
			#玉の座標は当たる前に戻す（めりこみはずし）
			GWK[_wk + cxpos] = GWK[_wk + cxpold]
			GWK[_wk + cypos] = GWK[_wk + cypold]

			#print("NOW",_bx, _by, "OLD", _bxold, _byold)

#---分割
			#ヒットセット
			GWK[_wk + ccond] |= F_HIT
			#保存値を戻して反射速度＆角度を調整
			GWK[_wk + cxpold] = GWK[save_cxpold]
			GWK[_wk + cypold] = GWK[save_cypold]
			GWK[_wk + cxspd] = GWK[save_cxspd]
			GWK[_wk + cyspd] = GWK[save_cyspd]
#---分割


			##どちらも同じはありえないから考えない（ずっとヒット中ならありえるのか・・・
			#if(( _bx == _bxold )and( _by == _byold )):
			#	print("[SAME]", _bx, _by )
			#	show()		#★[DEBUG]止める（こなかった
			
			#Yブロックが同じならX反転
			if( _by == _byold ):
				GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
			#Xブロックが同じならY反転
			if( _bx == _bxold ):
				GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

			#共に異なる場合（斜め進入の場合）共に反転
			#if( ( _by != _byold ) and ( _bx != _bxold ) ):
			#	GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
			#	GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
			#↓
			#当たったブロック周辺のブロックの状況を見て判断
			if( ( _by != _byold ) and ( _bx != _bxold ) ):
				#(+,+)の場合
				_set = 0
				if( ( GWK[_wk + cxspd] >= 0 ) and ( GWK[_wk + cyspd] >= 0 ) ):
					#左に有り、上に無しの場合
					_check_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + (_bx - 1)
					if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
						_check_pos = ((_by-1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( ( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ) == 0 ):
							#Yのみ反転
							GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
							_set = 1
							#print("PP-1")
					#左に無し、上に有りの場合
					else:
						_check_pos = ((_by-1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1
							#print("PP-2")

				#(+,-)の場合
				elif( ( GWK[_wk + cxspd] >= 0 ) and ( GWK[_wk + cyspd] < 0 ) ):
					#左に有り、下に無しの場合
					_check_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + (_bx - 1)
					if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
						_check_pos = ((_by+1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( ( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ) == 0 ):
							#Yのみ反転
							GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
							_set = 1
							#print("PM-1")
					#左に無し、下に有りの場合
					else:
						_check_pos = ((_by+1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1
							#print("PM-2")

				#(-,+)の場合
				elif( ( GWK[_wk + cxspd] < 0 ) and ( GWK[_wk + cyspd] >= 0 ) ):
					#右に有り、上に無しの場合
					_check_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + (_bx + 1)
					if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
						_check_pos = ((_by-1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( ( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ) == 0 ):
							#Yのみ反転
							GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
							_set = 1
							#print("MP-1")
					#右に無し、上に有りの場合
					else:
						_check_pos = ((_by-1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1
							#print("MP-2")

				#(-,-)の場合
				elif( ( GWK[_wk + cxspd] < 0 ) and ( GWK[_wk + cyspd] < 0 ) ):
					#右に有り、下に無しの場合
					_check_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + (_bx + 1)
					if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
						_check_pos = ((_by+1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( ( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ) == 0 ):
							#Yのみ反転
							GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
							_set = 1
							#print("MM-1")
					#右に無し、下に有りの場合
					else:
						_check_pos = ((_by+1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1
							#print("MM-2")

				if( _set == 0 ):
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
					#print("OTHER")

			#Block Hit!
			_cid = GWK[BLOCK_WORK + _block_pos] & 0x0f
			#ROCK BLOCK ?
			if( _cid == 0x01 ):
				#print("ROCK HIT")
				pass
			else:
				GWK[BLOCK_WORK + _block_pos] = 0x00		#ブロック消滅
				#スコア加算
				GWK[score] += 10
				#★[TODO]アイテム出現

#===============================================================================
#更新
#===============================================================================
def update():

	if( GWK[game_adv] == G_TITLE ):
		#タイトル画面表示
		#stage_typeによってタイトルを変更する
		#320/240の切り替えでPyxel Originalの第１ステージを表示する
		pass
	elif( GWK[game_adv] == G_DEMOPLAY ):
		pass
	elif( GWK[game_adv] == G_GAME ):
		game_control()
	elif( GWK[game_adv] == G_OVER ):
		#ゲームオーバー表記、タイマーでタイトルに戻る
		pass
	elif( GWK[game_adv] == G_STAGECLEAR ):
		#ステージクリアー＆次のステージ準備してG_GAMEに戻る
		pass
	elif( GWK[game_adv] == G_SETTING ):
		#設定画面
		pass
	else:
		GWK[game_adv] = G_TITLE
		GWK[game_sub_adv] = 0


#-----------------------------------------------------------------
#ゲーム制御
#-----------------------------------------------------------------
def game_control():
	#バー制御（bar_control()）
	GWK[PLY_WORK + cxpos] = pyxel.mouse_x
	#枠内に収める
	if( GWK[PLY_WORK + cxpos] < (LEFT_OFFSET + GWK[blockmap_shortofs]) ):
		GWK[PLY_WORK + cxpos] = LEFT_OFFSET + GWK[blockmap_shortofs]
	elif( GWK[PLY_WORK + cxpos] > ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[PLY_WORK + cid]][2] ) ):
		GWK[PLY_WORK + cxpos] = ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[PLY_WORK + cid]][2] )

	for _cnt in range(BALL_MAX):
		_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
		#バーの上に玉が存在？（１個しかつかない）
		if( ( GWK[_wk + ccond] & (F_LIVE+F_ON) ) == (F_LIVE+F_ON) ):
			#左クリックで離れる
			if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
				GWK[_wk + ccond] = GWK[_wk + ccond] & ~F_ON;
				#Y方向移動速度が下向きなら上向きに変更する
				if( GWK[_wk + cyspd] > 0 ):
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
					#バーの上は１個のみなのでここで抜ける
					break

	_dead_count = 0
	#ボール制御（ball_control()）
	for _cnt in range(BALL_MAX):
		_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
		if( GWK[_wk + ccond] & F_LIVE ):
			#バーの上に載ってる
			if( GWK[_wk + ccond] & F_ON ):
				GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] + int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )
				GWK[_wk + cypos] = GWK[PLY_WORK + cypos] - ctbl[GWK[_wk + cid]][2]
			#移動中
			else:
#------
#				#移動前位置保存
#				GWK[save_cxpold] = GWK[_wk + cxpos]
#				GWK[save_cypold] = GWK[_wk + cypos]
#
#				#枠内チェック
#				#左右
#				if( GWK[_wk + cxpos] < (LEFT_OFFSET + GWK[blockmap_shortofs]) ):
#					GWK[_wk + cxpos] = LEFT_OFFSET + GWK[blockmap_shortofs]
#					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
#					GWK[_wk + ccond] |= F_HIT
#				elif( GWK[_wk + cxpos] > ( SCREEN_WIDTH - RIGHT_OFFSET - ctbl[GWK[_wk + cid]][2] ) ):
#					GWK[_wk + cxpos] = ( SCREEN_WIDTH - RIGHT_OFFSET - ctbl[GWK[_wk + cid]][2] )
#					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
#					GWK[_wk + ccond] |= F_HIT
#
#				#上下
#				if( GWK[_wk + cypos] < UP_OFFSET ):
#					GWK[_wk + cypos] = UP_OFFSET
#					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
#					GWK[_wk + ccond] |= F_HIT
#
#				elif( GWK[_wk + cypos] > ( SCREEN_HEIGHT - ctbl[GWK[_wk + cid]][3] ) ):	##★[TODO]下はフレームアウトチェック
#					GWK[_wk + cypos] = ( SCREEN_HEIGHT - ctbl[GWK[_wk + cid]][3] )		##★[TODO]
#					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)							##★[TODO]
#					GWK[_wk + ccond] |= F_HIT
#
#				if( GWK[_wk + ccond] & F_HIT ):
#					GWK[_wk + ccond] &= ~ F_HIT
#					#移動前位置保存
#					GWK[_wk + cxpold] = GWK[save_cxpold]
#					GWK[_wk + cypold] = GWK[save_cypold]
#					return
#------

				#すり抜け対応
				#xspdとyspdを比較、絶対値の大きい方を1.0単位で分割
				#xspdとyspdを同じ分割数で割って分割チェックを行う

				#[基本動作]
				#移動前座標を記憶
				#速度を加算して移動
				#枠内チェック実施
				#ヒットチェック実施（ヒットしてたらヒット処理（反射＆角度と速度を設定）して終了）
				#	ブロックヒットチェックでは移動前と移動後を比較
				#	移動後でヒットしてたら移動前に戻してヒット処理を実施して終了

				#全移動時の移動前座標を別途保存（分割チェック終了時に戻す）
				#全移動時の移動速度を別途保存（ヒット処理にて使用する）
				GWK[save_cxpold] = GWK[_wk + cxpos]
				GWK[save_cypold] = GWK[_wk + cypos]
				GWK[save_cxspd] = GWK[_wk + cxspd]
				GWK[save_cyspd] = GWK[_wk + cyspd]

				#分割チェック用速度を速度ワークにセットしてヒットチェックを実施
				#ループ処理するので、最終的にヒットしてなければ全移動時の移動前座標と移動速度を格納して終了する

				_temp_xspd = GWK[_wk + cxspd]
				if( _temp_xspd < 0 ):
					_temp_xspd = _temp_xspd * (-1)
				_temp_yspd = GWK[_wk + cyspd]
				if( _temp_yspd < 0 ):
					_temp_yspd = _temp_yspd * (-1)

				if( _temp_xspd >= _temp_yspd ):
					_temp_speed = _temp_xspd
				else:
					_temp_speed = _temp_yspd

				#分割数取得（1.0単位に分割）
				_temp_num = int(_temp_speed)
				_temp_check = _temp_speed - (float)(_temp_num)
				#小数部分の有無確認、あれば分割数+1
				if( _temp_check > 0 ):
					_temp_num += 1

				#分割速度をセット
				GWK[_wk + cxspd] = GWK[_wk + cxspd] / _temp_num
				GWK[_wk + cyspd] = GWK[_wk + cyspd] / _temp_num
				#分割判定
				for _cnt in range(_temp_num):
					#移動前座標を記憶
					GWK[_wk + cxpold] = GWK[_wk + cxpos]
					GWK[_wk + cypold] = GWK[_wk + cypos]
					#移動
					GWK[_wk + cxpos] = GWK[_wk + cxpos] + GWK[_wk + cxspd]
					GWK[_wk + cypos] = GWK[_wk + cypos] + GWK[_wk + cyspd]

					ball_hit_check( _wk )
					#ヒットしてたらここで分割チェックを終了
					if( GWK[_wk + ccond] & F_HIT ):
						break


				#分割判定終了後、最終的にヒットしてなかった
				if( ( GWK[_wk + ccond] & F_HIT ) == 0 ):
					#保存値を戻す
					GWK[_wk + cxpold] = GWK[save_cxpold]
					GWK[_wk + cypold] = GWK[save_cypold]
					GWK[_wk + cxspd] = GWK[save_cxspd]
					GWK[_wk + cyspd] = GWK[save_cyspd]
				else:
					#ヒットフラグを戻しておく
					GWK[_wk + ccond] &= ~F_HIT
					#玉の反射角度調整（固まり防止）
					ball_degree_control( _wk )

				#枠内チェック
				#左右
#				if( GWK[_wk + cxpos] < ( LEFT_OFFSET + GWK[blockmap_shortofs] + ctbl[GWK[_wk + cid]][2] ) ):
#					GWK[_wk + cxpos] = ( LEFT_OFFSET + GWK[blockmap_shortofs] + ctbl[GWK[_wk + cid]][2] )
#					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
				if( GWK[_wk + cxpos] < ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ):
					GWK[_wk + cxpos] = ( LEFT_OFFSET + GWK[blockmap_shortofs] )
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
				elif( GWK[_wk + cxpos] > ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[_wk + cid]][2] ) ):
					GWK[_wk + cxpos] = ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[_wk + cid]][2] )
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)

				elif( GWK[_wk + cxpos] > ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET ) ):
					GWK[_wk + cxpos] = ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET )
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)

				#上下
#				if( GWK[_wk + cypos] < ( UP_OFFSET + ctbl[GWK[_wk + cid]][3] ) ):
#					GWK[_wk + cypos] = ( UP_OFFSET + ctbl[GWK[_wk + cid]][3] )
#					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

				if( GWK[_wk + cypos] < UP_OFFSET ):
					GWK[_wk + cypos] = UP_OFFSET
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

				#elif( GWK[_wk + cypos] > ( SCREEN_HEIGHT - ctbl[GWK[_wk + cid]][3] ) ):	##★[TODO]下はフレームアウトチェック
				#	GWK[_wk + cypos] = ( SCREEN_HEIGHT - ctbl[GWK[_wk + cid]][3] )		##★[TODO]
				#	GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)							##★[TODO]

				#フレームアウトチェック
				elif( GWK[_wk + cypos] > ( SCREEN_HEIGHT + 0x10 ) ):
					GWK[_wk + ccond] = 0	#DEAD SET

		else:
			_dead_count += 1

	#すべての玉がフレームアウト？
	if( _dead_count >= BALL_MAX):
		#ミス
		#ゲームオーバー判定
		if( GWK[rest_number] <= 0 ):
			GWK[game_adv] = G_OVER
			GWK[game_subadv] = 0
		else:
			GWK[rest_number] -= 1
			#玉復帰セット
			ball_init()

	#★[TODO]（将来的に）アイテム制御
	#★[TODO]（将来的に）item_control()
	#★[TODO]（将来的に）#エネミー制御
	#★[TODO]（将来的に）enemy_control()

#===============================================================================
#描画
#===============================================================================
def draw():
	#画面クリア
	pyxel.cls(0)

	#背景描画
	#横320
	if( ( GWK[stage_type] == 0 ) or ( GWK[stage_type] == 1 ) ):
		if( GWK[bg_switch] == 0 ):
			pyxel.bltm(0, SCORE_HIGHT, 0, 0+SCREEN_WIDTH * 0, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH, SCREEN_HEIGHT)
		else:
			pyxel.bltm(0, SCORE_HIGHT, 0, 0+SCREEN_WIDTH * 1, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH, SCREEN_HEIGHT)
	#横240
	else:
		if( GWK[bg_switch] == 0 ):
			pyxel.bltm(40, SCORE_HIGHT, 0, (SCREEN_WIDTH*2)+SCREEN_WIDTH2 * 0, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH2, SCREEN_HEIGHT)
		else:
			pyxel.bltm(40, SCORE_HIGHT, 0, (SCREEN_WIDTH*2)+SCREEN_WIDTH2 * 1, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH2, SCREEN_HEIGHT)


	#★[TODO]（将来的に）ブロックの影の表示
	#★[TODO]（将来的に）stage_block_shadow()
	#ブロックの表示
	stage_block()
	
	#バー表示
	if( GWK[PLY_WORK+ccond] & F_LIVE ):
		cput( GWK[PLY_WORK+cxpos], GWK[PLY_WORK+cypos], GWK[PLY_WORK+cid], 0 )
	#玉表示
	for _cnt in range(BALL_MAX):
		_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
		if( GWK[_wk + ccond] & F_LIVE ):
			cput( GWK[_wk+cxpos], GWK[_wk+cypos], GWK[_wk+cid], 0 )
	
	#rest表記
	cput( 48, 0, 0x22, 0 )
	set_font_text( 64, 0, str(GWK[rest_number]), 0 )

	#stage表記
	set_font_text( 100, 0, 'STAGE ' + str(GWK[stage_type]) + "-" + str(GWK[stage_number]+1), 0 )
	#score表記
	set_font_text( 200, 0, 'SCORE ', 0 )
	set_font_text( 250, 0, str(GWK[score]), 0 )

#===============================================================================
#INIT
#===============================================================================
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60)
#[use Web]ESCキーを無効化
#pyxel.init(256, 256, fps=60, quit_key=pyxel.KEY_NONE, title='pyxelblk')

#リソース読み込み
pyxel.load("pyxelblk.pyxres")

#ワーククリア
work_clear()

#初期値セット
GWK[rest_number] = 2			#残機
GWK[stage_number] = 0			#0～	#設定でステージセレクト入れるかも？または別途？
GWK[score] = 0					#スコア（最大６桁）
GWK[highscore] = 0				#ハイスコア（最大６桁）

#初期値セット（★[TODO]設定で切り替え可能にする）
GWK[stage_type] = 0				#0/1/2/3 : 320x240original / crystal hammer / 240x240original/arkanoid
GWK[multi_color_switch] = 0		#0/1 : ブロックマルチカラースイッチ
GWK[bg_switch] = 1				#0/1 : ブロック背景有り/無し
GWK[bg_type] = 1				#0/1 : ブロック背景タイプ（現在２種類）bg_switch有りなら３種類
GWK[ball_color] = 1				#0/1/2 : 玉の色：青/赤/緑

if( ( GWK[stage_type] == 0 ) or ( GWK[stage_type] == 1 ) ):
	GWK[blockmap_Hmax] = 18		#ブロックマップ横最大サイズ
	GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
	GWK[blockmap_shortofs] = 0	#横オフセット
else:
	GWK[blockmap_Hmax] = 13		#ブロックマップ横最大サイズ
	GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
	GWK[blockmap_shortofs] = 40	#横オフセット(=(320-240)/2)

#ステージマップ初期化
stage_init()
GWK[game_adv] = G_GAME
GWK[game_subadv] = 0

#マウスカーソル表示（タイトルと設定のみ表示
#pyxel.mouse( visible = True )

#実行
pyxel.run(update, draw)

#Crystal Hammer 320x240(18x20)
#Arcanoid		240x240(13x20)


#設定									設定変数
#	stage type
#		Pyxel Original(320x240)			GWK[stage_type], GWK[blockmap_Hmax], GWK[blockmap_Vmax], GWK[blockmap_shortofs]
#		Crystal Hammer(320x240)
#		Pyxel Original(240x240)
#		Arkanoid1or2(240x240)
#
#	Block Type
#		Multi Color, Pyxel Default		GWK[multi_color_switch]=1/0
#
#	BG on/off（影が無いと見にくいので影入れないならこのスイッチは不要
#										GWK[bg_switch]=0/1
#	BG type
#										GWK[bg_type]=0/1/2
#	Ball Color
#										GWK[ball_color]=0/1/2	玉の色：青/赤/緑
#
# 矢印ボタンをマウスで選択して項目を選ぶ（カーソル重なったら黄色、クリックで項目切り替え）
#	SETTINGS
#
# STAGE TYPE
#	PYXEL ORIGINAL (320x240) - Arkanoid参考に作成
#	CRYSTAL HAMMER (320x240)
#	PYXEL ORIGINAL (240x240) - Arkanoid参考に作成してARKANOIDは入れないかも
#	ARKANOID       (240x240)
#
#	オリジナルステージはタイトルのみで続けて各ゲームステージを入れようか？
#	それならタイプは２種類で良いけど・・・
#
#	★こっちでいいかな？
#	または共にオリジナルステージとして、CRYSTAL HAMMERに似たステージを10個
#	アルカノイドに似たステージを10個ほど用意、、、とか
#	ステージはいくらでもあとから追加できますというふうにできればいいけど
#
# BG TYPE
#	PATTERN-0 / PATTERN-1
#
# BALL COLOR
#	BLUE / RED / GREEN
#
# BLOCK TYPE
#	MULTI COLOR / DEFAULT COLOR
#
# DEBUG用ステージセレクト
