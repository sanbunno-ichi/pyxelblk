#------------------------------------------
# title: Pyxel Block
# author: sanbunnoichi
# desc: Breaking blocks Game
# site: https://github.com/sanbunno-ichi/pyxelblk
# license: MIT
# version: 2.0
#
#更新履歴
#2024.10.03 version 2.0で更新
#更新内容：
#・アイテム追加
#・CONTINUE追加
#・三発で壊れるブロック追加
#・面エディタ追加（作成データはコンソール出力する）
#・ステージ追加
#
#2024.09.20 data_ptrによる高速化、Exit機能追加
#2024.09.17 github更新
#2024.09.04 作成開始
#------------------------------------------
import pyxel
import blktbl
#import time			#処理計測用

STAGE_TYPE0_MAX		=	24		#320x240 original
STAGE_TYPE1_MAX		=	24		#240x240 original

#-----------------------------------------------------------------
SCREEN_WIDTH		=	320		#ゲーム画面横サイズ（変更無しとする）
SCREEN_WIDTH2		=	240		#ゲーム画面横サイズ
SCREEN_HEIGHT		=	240		#ゲーム画面縦サイズ

LEFT_OFFSET			=	0x10	#左枠オフセット
RIGHT_OFFSET		=	0x10	#右枠オフセット
SCORE_HEIGHT		=	0x08	#スコア位置分高さ
UP_OFFSET			=	0x10	#スコア位置＋壁の厚み

BLK_WIDTH			=	0x10	#ブロック横サイズ
BLK_HEIGHT			=	8		#ブロック縦サイズ

PALETTE_SHADOW		=	0x0c	#マルチカラー影色パレット

FONT_WIDTH			=	8		#FONT WIDTHサイズ
FONT_HEIGHT			=	8		#FONT HEIGHTサイズ

TITLE_START_OFS		=	5*FONT_WIDTH		#５文字'START'
TITLE_START_X		=	int(SCREEN_WIDTH / 2) - int(TITLE_START_OFS/2)
TITLE_START_Y		=	180
TITLE_SETTING_OFS	=	7*FONT_WIDTH		#７文字'SETTING'
TITLE_SETTING_X		=	int(SCREEN_WIDTH / 2) - int(TITLE_SETTING_OFS/2)
TITLE_SETTING_Y		=	195
TITLE_EXIT_OFS		=	4*FONT_WIDTH		#４文字'EXIT'
TITLE_EXIT_X		=	int(SCREEN_WIDTH / 2) - int(TITLE_EXIT_OFS/2)
TITLE_EXIT_Y		=	210

SETTING_TOP_X		=	TITLE_SETTING_X
SETTING_TOP_Y		=	0x20
SETTING_TITLE_X		=	0x10
SETTING_LEFT_X		=	0x70
SETTING_ITEM_X		=	0x88
SETTING_RIGHT_X		=	0x120
SETTING_XOFS		=	(SETTING_RIGHT_X + 0x10 - SETTING_TITLE_X)
SETTING_YOFS		=	12
SETTING_Y			=	0x40
SETTING_ITEM_MAX	=	12

EDITOR_UP			= 0xb8
EDITOR_LEFT_SIDE	= 0x40
EDITOR_RIGHT_SIDE	= 0xa0

EDITOR_ITEM_MAX		= 10

#-----------------------------------------------------------------
#[workass]変数
WORK_TOP			=	0
WORK_END			=	0x800
_ass = WORK_TOP
GWK = [WORK_TOP for _ass in range(WORK_END)]	#変数管理(RAM領域)

game_adv			=	WORK_TOP+0x00		#game_control number
game_subadv			=	WORK_TOP+0x01		#game_control sub-number
stage_number		=	WORK_TOP+0x02		#0～49（予定）
stage_type			=	WORK_TOP+0x03		#0/1 : original 320x240/240x240
multi_color_switch	=	WORK_TOP+0x04		#0/1 : ブロックマルチカラースイッチ
debug_stage_number	=	WORK_TOP+0x05		#デバッグ用ステージ番号（設定でセットする）
bg_type				=	WORK_TOP+0x06		#0/1/2 : ブロック背景タイプ（現在３種類）
start_height		=	WORK_TOP+0x07		#ステージブロックの先頭の高さ
ball_speed			=	WORK_TOP+0x08		#玉の基準スピード値
ball_degree			=	WORK_TOP+0x09		#玉の基準角度
ball_color			=	WORK_TOP+0x0a		#0/1/2 : 玉の色：青/赤/緑
rest_number			=	WORK_TOP+0x0b		#残機数
score				=	WORK_TOP+0x0c		#スコア（最大６桁）
demoplay_counter	=	WORK_TOP+0x0d		#デモプレイカウンター
blockmap_Hmax		=	WORK_TOP+0x0e		#ブロックマップ横最大サイズ
blockmap_Vmax		=	WORK_TOP+0x0f		#ブロックマップ縦最大サイズ

SCORE_MAX			=	999999
SCORE_KETA			=	6

G_TITLE				=	0
G_DEMOPLAY			=	1
G_GAME				=	2
G_CONTINUE			=	3
G_OVER				=	4
G_STAGECLEAR		=	5
G_SETTING			=	6
G_EDITOR			=	7
G_DEBUG				=	8
G_END				=	9

save_cxpold			=	WORK_TOP+0x10
save_cypold			=	WORK_TOP+0x11
save_cxspd			=	WORK_TOP+0x12
save_cyspd			=	WORK_TOP+0x13
blockmap_shortofs	=	WORK_TOP+0x14	#320->240 変更の際の横サイズオフセット
title_select		=	WORK_TOP+0x15
setting_select		=	WORK_TOP+0x16
field_switch		=	WORK_TOP+0x17
continue_switch		=	WORK_TOP+0x18
item_switch			=	WORK_TOP+0x19
wait_counter		=	WORK_TOP+0x1a
title_counter		=	WORK_TOP+0x1b
highscore_0			=	WORK_TOP+0x1c	#stage_type=0のハイスコア
highscore_1			=	WORK_TOP+0x1d	#stage_type=1のハイスコア
#（空き）			=	WORK_TOP+0x1e
#（空き）			=	WORK_TOP+0x1f

continue_result		=	WORK_TOP+0x20	#0/1/2 = not set/NO/YES
editor_type			=	WORK_TOP+0x21	#設定内のeditorの項目
editor_subadv		=	WORK_TOP+0x22
editor_select		=	WORK_TOP+0x23
editor_select_ac	=	WORK_TOP+0x24
editor_result_ac	=	WORK_TOP+0x25
editor_blockid		=	WORK_TOP+0x26	#セットしうるブロックID番号（1～11）
testplay_switch		=	WORK_TOP+0x27
item_appcnt			=	WORK_TOP+0x28
auto_counter		=	WORK_TOP+0x29	#デモプレイ中のオートショットカウンタ

#--------------------------------------------
PLY_WORK			=	WORK_TOP+0xc0
cid					=	0x00		#ID番号
ccond				=	0x01		#状態フラグ
#状態フラグ内訳
F_LIVE				=	0x80		#[bit7]生(1)死(0)
F_ON				=	0x40		#[bit6]パドルの上(1)移動中(0)		玉のみ
F_ONREADY			=	0x20		#[bit5]次に当たった玉はくっつく		パドルのみ
F_HIT				=	0x10		#[bit4]ヒット(1)

cxpos				=	0x02		#X座標
cypos				=	0x03		#Y座標
cxspd				=	0x04		#X移動スピード
cyspd				=	0x05		#Y移動スピード

canum				=	0x06		#アニメ番号
cacnt				=	0x07		#アニメカウンタ
caspd				=	0x08		#アニメスピードカウンタ


cmnum				=	0x09		#移動パターン番号、パドルの取得アイテム番号
cmcnt				=	0x0a		#移動カウンタ
cmcnt2				=	0x0b		#移動カウンタ２
cwait				=	0x0c		#登場待ちカウンタ

cxpold				=	0x09		#移動前xpos保存用（玉用）
cypold				=	0x0a		#移動前ypos保存用（玉用）
cbig				=	0x0b		#Bigall（玉用）

cspd				=	0x0c		#基準移動速度
cdeg				=	0x0d		#移動角度（degree:0～89(359)）
chit				=	0x0e		#ヒット回数
chit2				=	0x0f		#ヒット回数（パドルヒットでクリア）

CWORK_SIZE			=	0x10		#各種キャラクタワークサイズ



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
BLOCK_WORK_SIZE	=	0x240			#横方向：18、縦方向：20、18*20 = 360 = 0x228
#BLOCK_WORK format
#bit fedc ba98 7654 3210
#	 |  | |  | |||| |  |
#	 |  | |  | |||| +--+
#	 |  | |  | ||||  色番号（0～11）
#	 |  | |  | |||+- ？
#	 |  | |  | ||+-- BF_ANIM
#	 |  | |  | |+--- BF_HIT(0/1=nohit/hit)
#	 |  | |  | *---- BF_LIVE(0/1=dead/live)
#    |  | +--+
#    +--+  耐久力（0～15
#     アニメカウンタ(0～15
BF_LIVE			=	0x80
BF_HIT			=	0x40	#（未使用）
BF_ANIM			=	0x20

#--------------------------------------------
SAVE_BLOCK_WORK	=	BLOCK_WORK + BLOCK_WORK_SIZE		#WORK_TOP+0x340
#--------------------------------------------
#アイテムは画面上最大８個まで
ITEM_MAX		=	8
ITEM_WORK		=	SAVE_BLOCK_WORK + BLOCK_WORK_SIZE	#WORK_TOP+0x580
ITEM_THREE_BALL	=	3

ITEM_TYPE_LONG	=	1
ITEM_TYPE_ADD	=	2
ITEM_TYPE_LASER	=	3
ITEM_TYPE_THREE	=	4
ITEM_TYPE_BIG	=	5
ITEM_TYPE_SHORT	=	6
#--------------------------------------------
#アイテムショット弾
SHOT_MAX		=	16
SHOT_WORK		=	ITEM_WORK + ( CWORK_SIZE * ITEM_MAX )	#WORK_TOP+0x600

BALL_MAX		=	16
BALL_WORK		=	SHOT_WORK + ( CWORK_SIZE * SHOT_MAX )	#WORK_TOP+0x700
BALL_BASE_SPEED		=	3
BALL_BASE_DEGREE	=	50

#-----------------------------------------------------------------
#キャラクタテーブル
#-----------------------------------------------------------------
ID_BALL				=	0x04		#玉ベース
ID_BLK_DEF			=	0x0c		#ブロックDEF開始id
ID_BLK_MULTI		=	0xab		#ブロックマルチ開始id

IDMAX = 0xe4
ctbl = [
	# u,    v,    us,   vs
	[ 0x10, 0x30, 0x20, 0x08 ],		#0x00 パドルノーマル
	[ 0x00, 0x30, 0x10, 0x08 ],		#0x01 パドル短い
	[ 0x00, 0x38, 0x40, 0x08 ],		#0x02 パドル長い
	[ 0x00, 0x40, 0x20, 0x08 ],		#0x03 パドルレーザー
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
	[ 0x50, 0x80, 0x10, 0x08 ],		#0x17 ブロックDEF：0xb:	GRAY	
	[ 0x70, 0x80, 0x10, 0x08 ],		#0x16 ブロックDEF：0xc:	SHADOW	
	[ 0x00, 0x00, 0x10, 0x08 ],		#0x18 ブロックDEF：（空）

	[ 0x60, 0x88, 0x10, 0x08 ],		#0x19 ブロックDEF：0xb:	GRAY キラリ1
	[ 0x70, 0x88, 0x10, 0x08 ],		#0x1a ブロックDEF：0xb:	GRAY キラリ2
	[ 0x60, 0x90, 0x10, 0x08 ],		#0x1b ブロックDEF：0xb:	GRAY キラリ3
	[ 0x70, 0x90, 0x10, 0x08 ],		#0x1c ブロックDEF：0xb:	GRAY キラリ4
	[ 0x60, 0x68, 0x10, 0x08 ],		#0x1d EDITOR 枠
	[ 0x70, 0x68, 0x10, 0x08 ],		#0x1e EDITOR 枠下限（上線のみ）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x1f （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x20 ' '（スペース）	白文字（スペースは0x20）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x21 （白文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x22 （白文字予約）	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x23 （白文字予約）	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x24 （白文字予約）	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x25 （白文字予約）	

	[ 0x20, 0x40, 0x10, 0x08 ],		#0x26 残機

	[ 0x38, 0x70, 0x08, 0x08 ],		#0x27 
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

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x5b （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x5c （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x5d （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x5e （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x5f （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x60 ' '（スペース）	黄文字
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x61 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x62 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x63 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x64 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x65 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x66 （黄文字予約）

	[ 0x38, 0xa0, 0x08, 0x08 ],		#0x67 
	[ 0x30, 0x80, 0x08, 0x08 ],		#0x68 '('
	[ 0x38, 0x80, 0x08, 0x08 ],		#0x69 ')'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x6a （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x6b （空き）
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

	[ 0x40, 0x88, 0x10, 0x08 ],		#0x9b 矢印左白
	[ 0x40, 0x90, 0x10, 0x08 ],		#0x9c 矢印右白
	[ 0x50, 0x88, 0x10, 0x08 ],		#0x9d 矢印左黄
	[ 0x50, 0x90, 0x10, 0x08 ],		#0x9e 矢印右黄

	[ 0x78, 0x20, 0x08, 0x08 ],		#0x9f アイテム無し
	[ 0x40, 0x00, 0x08, 0x08 ],		#0xa0 アイテム青1：lOng
	[ 0x60, 0x10, 0x08, 0x08 ],		#0xa1 アイテム青2
	[ 0x68, 0x10, 0x08, 0x08 ],		#0xa2 アイテム青3
	[ 0x70, 0x10, 0x08, 0x08 ],		#0xa3 アイテム青4
	[ 0x40, 0x08, 0x08, 0x08 ],		#0xa4 アイテム青5
	[ 0x60, 0x18, 0x08, 0x08 ],		#0xa5 アイテム青6
	[ 0x68, 0x18, 0x08, 0x08 ],		#0xa6 アイテム青7
	[ 0x70, 0x18, 0x08, 0x08 ],		#0xa7 アイテム青8
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa8 （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa9 （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xaa （空き）

	[ 0xFF, 0x01, 0x10, 0x09 ],		#0xab ブロックマルチ：0x1:	ROCK	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xac ブロックマルチ：0x2:	WHITE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xad ブロックマルチ：0x3:	RED		
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xae ブロックマルチ：0x4:	GREEN	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xaf ブロックマルチ：0x5:	BLUE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb0 ブロックマルチ：0x6:	YELLOW	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb1 ブロックマルチ：0x7:	MIZU	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb2 ブロックマルチ：0x8:	PURPLE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb3 ブロックマルチ：0x9:	ORANGE	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb4 ブロックマルチ：0xa:	PINK	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb5 ブロックマルチ：0xb:	GRAY	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb6 ブロックマルチ：0xc:	SHADOW	
	[ 0xFF, 0x00, 0x10, 0x09 ],		#0xb7 ブロックマルチ：0xd:	（空）	

	[ 0xFF, 0x00, 0x10, 0x08 ],		#0xb8 ブロックマルチ：0xb:	GRAY キラリ1
	[ 0xFF, 0x00, 0x10, 0x08 ],		#0xb9 ブロックマルチ：0xb:	GRAY キラリ2
	[ 0xFF, 0x00, 0x10, 0x08 ],		#0xba ブロックマルチ：0xb:	GRAY キラリ3
	[ 0xFF, 0x00, 0x10, 0x08 ],		#0xbb ブロックマルチ：0xb:	GRAY キラリ4

	[ 0x48, 0x00, 0x08, 0x08 ],		#0xbc アイテム緑1：Add
	[ 0x60, 0x20, 0x08, 0x08 ],		#0xbd アイテム緑2
	[ 0x68, 0x20, 0x08, 0x08 ],		#0xbe アイテム緑3
	[ 0x70, 0x20, 0x08, 0x08 ],		#0xbf アイテム緑4
	[ 0x48, 0x08, 0x08, 0x08 ],		#0xc0 アイテム緑5
	[ 0x60, 0x28, 0x08, 0x08 ],		#0xc1 アイテム緑6
	[ 0x68, 0x28, 0x08, 0x08 ],		#0xc2 アイテム緑7
	[ 0x70, 0x28, 0x08, 0x08 ],		#0xc3 アイテム緑8

	[ 0x50, 0x00, 0x08, 0x08 ],		#0xc4 アイテム赤1：Laser
	[ 0x60, 0x30, 0x08, 0x08 ],		#0xc5 アイテム赤2
	[ 0x68, 0x30, 0x08, 0x08 ],		#0xc6 アイテム赤3
	[ 0x70, 0x30, 0x08, 0x08 ],		#0xc7 アイテム赤4
	[ 0x50, 0x08, 0x08, 0x08 ],		#0xc8 アイテム赤5
	[ 0x60, 0x38, 0x08, 0x08 ],		#0xc9 アイテム赤6
	[ 0x68, 0x38, 0x08, 0x08 ],		#0xca アイテム赤7
	[ 0x70, 0x38, 0x08, 0x08 ],		#0xcb アイテム赤8

	[ 0x58, 0x00, 0x08, 0x08 ],		#0xcc アイテム水1：Three
	[ 0x60, 0x40, 0x08, 0x08 ],		#0xcd アイテム水2
	[ 0x68, 0x40, 0x08, 0x08 ],		#0xce アイテム水3
	[ 0x70, 0x40, 0x08, 0x08 ],		#0xcf アイテム水4
	[ 0x58, 0x08, 0x08, 0x08 ],		#0xd0 アイテム水5
	[ 0x60, 0x48, 0x08, 0x08 ],		#0xd1 アイテム水6
	[ 0x68, 0x48, 0x08, 0x08 ],		#0xd2 アイテム水7
	[ 0x70, 0x48, 0x08, 0x08 ],		#0xd3 アイテム水8

	[ 0x60, 0x00, 0x08, 0x08 ],		#0xd4 アイテム黄1：Big
	[ 0x60, 0x50, 0x08, 0x08 ],		#0xd5 アイテム黄2
	[ 0x68, 0x50, 0x08, 0x08 ],		#0xd6 アイテム黄3
	[ 0x70, 0x50, 0x08, 0x08 ],		#0xd7 アイテム黄4
	[ 0x60, 0x08, 0x08, 0x08 ],		#0xd8 アイテム黄5
	[ 0x60, 0x58, 0x08, 0x08 ],		#0xd9 アイテム黄6
	[ 0x68, 0x58, 0x08, 0x08 ],		#0xda アイテム黄7
	[ 0x70, 0x58, 0x08, 0x08 ],		#0xdb アイテム黄8

	[ 0x68, 0x00, 0x08, 0x08 ],		#0xdc アイテム紫1：Short
	[ 0x70, 0x00, 0x08, 0x08 ],		#0xdd アイテム紫2
	[ 0x78, 0x00, 0x08, 0x08 ],		#0xde アイテム紫3
	[ 0x78, 0x10, 0x08, 0x08 ],		#0xdf アイテム紫4
	[ 0x68, 0x08, 0x08, 0x08 ],		#0xe0 アイテム紫5
	[ 0x70, 0x08, 0x08, 0x08 ],		#0xe1 アイテム紫6
	[ 0x78, 0x08, 0x08, 0x08 ],		#0xe2 アイテム紫7
	[ 0x78, 0x18, 0x08, 0x08 ],		#0xe3 アイテム紫8
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
	#[TODO]右詰めがうまくできてない（数値の並びが逆になる
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

#---------------------------------------------------------------------------------------------------
#MULTI BG table
#0x20x0x20
mbg_tbl = [0 for tbl in range(0x20)]
mbg_tbl[0x00] = [0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1]
mbg_tbl[0x01] = [0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xde]
mbg_tbl[0x02] = [0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde]
mbg_tbl[0x03] = [0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde]
mbg_tbl[0x04] = [0xde,0xde,0xde,0xd1,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde,0xde]
mbg_tbl[0x05] = [0xde,0xde,0xd1,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde,0xde,0xde]
mbg_tbl[0x06] = [0xde,0xd1,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xd1,0xde,0xde,0xde,0xde,0xde,0xde]
mbg_tbl[0x07] = [0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde]
mbg_tbl[0x08] = [0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1]
mbg_tbl[0x09] = [0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xdf]
mbg_tbl[0x0a] = [0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xdf,0xdf]
mbg_tbl[0x0b] = [0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xdf,0xdf,0xdf]
mbg_tbl[0x0c] = [0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xdf,0xdf,0xdf,0xdf]
mbg_tbl[0x0d] = [0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf]
mbg_tbl[0x0e] = [0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf]
mbg_tbl[0x0f] = [0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf]
mbg_tbl[0x10] = [0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1]
mbg_tbl[0x11] = [0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd6]
mbg_tbl[0x12] = [0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd6,0xd6]
mbg_tbl[0x13] = [0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd6,0xd6,0xd6]
mbg_tbl[0x14] = [0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd6,0xd6,0xd6,0xd6]
mbg_tbl[0x15] = [0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6]
mbg_tbl[0x16] = [0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6]
mbg_tbl[0x17] = [0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6]
mbg_tbl[0x18] = [0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1]
mbg_tbl[0x19] = [0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xda]
mbg_tbl[0x1a] = [0xda,0xda,0xd1,0xd6,0xd6,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xda,0xda]
mbg_tbl[0x1b] = [0xda,0xda,0xda,0xd1,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xda,0xda,0xda]
mbg_tbl[0x1c] = [0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xda,0xda,0xda,0xda]
mbg_tbl[0x1d] = [0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd1,0xda,0xda,0xda,0xda,0xda]
mbg_tbl[0x1e] = [0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd6,0xd6,0xd1,0xda,0xda,0xda,0xda,0xda,0xda]
mbg_tbl[0x1f] = [0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda]

#0x10x0x20（240dot不足分用）
mbg2_tbl = [0 for tbl in range(0x20)]
mbg2_tbl[0x00] = [0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1]
mbg2_tbl[0x01] = [0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb]
mbg2_tbl[0x02] = [0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb]
mbg2_tbl[0x03] = [0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb]
mbg2_tbl[0x04] = [0xde,0xde,0xde,0xd1,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb]
mbg2_tbl[0x05] = [0xde,0xde,0xd1,0xdb,0xdb,0xd1,0xda,0xda,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb]
mbg2_tbl[0x06] = [0xde,0xd1,0xdb,0xdb,0xdb,0xdb,0xd1,0xda,0xda,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb]
mbg2_tbl[0x07] = [0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb]
mbg2_tbl[0x08] = [0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1]
mbg2_tbl[0x09] = [0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf]
mbg2_tbl[0x0a] = [0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf]
mbg2_tbl[0x0b] = [0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf]
mbg2_tbl[0x0c] = [0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf]
mbg2_tbl[0x0d] = [0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf]
mbg2_tbl[0x0e] = [0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xdb,0xdb,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf]
mbg2_tbl[0x0f] = [0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf]
mbg2_tbl[0x10] = [0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1]
mbg2_tbl[0x11] = [0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde]
mbg2_tbl[0x12] = [0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde]
mbg2_tbl[0x13] = [0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde]
mbg2_tbl[0x14] = [0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde]
mbg2_tbl[0x15] = [0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde]
mbg2_tbl[0x16] = [0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xdf,0xdf,0xd1,0xde,0xde,0xde,0xde,0xde,0xde]
mbg2_tbl[0x17] = [0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde]
mbg2_tbl[0x18] = [0xd1,0xd6,0xd6,0xd6,0xd6,0xd6,0xd6,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1]
mbg2_tbl[0x19] = [0xda,0xd1,0xd6,0xd6,0xd6,0xd6,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda]
mbg2_tbl[0x1a] = [0xda,0xda,0xd1,0xd6,0xd6,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda]
mbg2_tbl[0x1b] = [0xda,0xda,0xda,0xd1,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda]
mbg2_tbl[0x1c] = [0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda]
mbg2_tbl[0x1d] = [0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda]
mbg2_tbl[0x1e] = [0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xde,0xde,0xd1,0xda,0xda,0xda,0xda,0xda,0xda]
mbg2_tbl[0x1f] = [0xda,0xda,0xda,0xda,0xda,0xda,0xda,0xd1,0xd1,0xda,0xda,0xda,0xda,0xda,0xda,0xda]

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

mblk_tbl = [
	#16x9
	0,1,2,2,2,2,2,2,2,2,2,2,2,2,3,0, 
	1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5, 
	0,3,4,4,4,4,4,4,4,4,4,4,4,4,5,0,
]

#キラリ１
mk1blk_tbl = [
	#16x9
	0,1,2,2,2,2,2,2,2,2,2,2,2,2,3,0, 
	1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,3,3,3,3,3,1,1,1,1,6,6, 
	3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5, 
	0,3,4,4,4,4,4,4,4,4,4,4,4,4,5,0,
]
#キラリ2
mk2blk_tbl = [
	#16x9
	0,1,2,2,2,2,2,2,2,2,2,2,2,2,3,0, 
	1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,1,6,6, 
	2,2,3,3,3,1,1,1,1,1,1,1,1,1,6,6, 
	3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5, 
	0,3,4,4,4,4,4,4,4,4,4,4,4,4,5,0,
]
#キラリ3
mk3blk_tbl = [
	#16x9
	0,1,2,2,2,2,2,2,2,2,2,2,2,2,3,0, 
	1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3, 
	2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6, 
	2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6, 
	2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6, 
	2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6, 
	2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6, 
	3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5, 
	0,3,4,4,4,4,4,4,4,4,4,4,4,4,5,0,
]
#キラリ4
mk4blk_tbl = [
	#16x9
	0,1,2,2,2,2,2,2,2,2,2,2,2,2,3,0, 
	1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3, 
	2,2,1,1,1,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,1,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,1,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	2,2,3,3,3,3,3,3,3,3,3,3,3,3,6,6, 
	3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5, 
	0,3,4,4,4,4,4,4,4,4,4,4,4,4,5,0,
]

#ROCK
rblk_tbl = [
	#16x9
	0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0, 
	1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3, 
	0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0, 
	]

#-----------------------------------------------------------------
#効果音セット
#-----------------------------------------------------------------
def se_set(_number):
	#タイトル時効果音は出力しない
	if( ( GWK[game_adv] != G_TITLE ) and ( GWK[game_adv] != G_DEMOPLAY ) ):
		pyxel.play( 3,_number )

#-----------------------------------------------------------------
#面エディタ
#BG 320:X=0x000,Y=0x300,XS=0x140,YS=0x0E0
#BG 240:X=0x140	Y=0x300,XS=0x0E0,YS=0x0E0
#
#	+-------------------------------+
#	|								|20
#	|								|↓
#	|	バックに枠表示(BGで表示)	|
#	|								|
#	|								|
#	+-------------------------------+
#	|					ALL CLEAR(1)|
#	|								|
#	|PRINT(2)		 	 select		|	select blockで選択されたブロック
#	|					←block→	|	を枠内マウス左クリックで設置、右クリックで削除
#	|					(4)	  (5)	|
#	|								|
#	|EXIT(3)			TESTPLAY(6)	|	「TESTPLAY」で今のステージをテストする
#	+-------------------------------+
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#作成した面データをコンソールに表示する
#表示されたテーブルを面データに登録する
#ステージ数を増やした場合、ソース最初の STAGE_TYPE0_MAX 等の数値を変更すること
#-----------------------------------------------------------------
def editor_print():
	#ステージブロックの先頭の高さを検出
	_start_height = 0
	_start_cnt = 0
	for _cnt in range(BLOCK_WORK_SIZE):
		if( GWK[BLOCK_WORK + _cnt] != 0 ):
			_start_height = int( _cnt / GWK[blockmap_Hmax] )
			_start_cnt = _start_height * GWK[blockmap_Hmax]
			break

	#下限位置を取得
	_end_height = 0
	_end_cnt = 0
	for _cnt in range(BLOCK_WORK_SIZE):
		if( GWK[BLOCK_WORK + _cnt] != 0 ):
			_end_cnt = int( _cnt / GWK[blockmap_Hmax] ) + 1

	_end_height = _end_cnt

	#stage000_tbl = [
	#	<_start_height>,
	#	x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,
	#	x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,
	#	x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,
	#	x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,
	#	0xff]
	#の形式で出力したい
	#print(xxxxx, end='') で改行しなくなる
	print( 'stage000_tbl = [' )
	print( '\t' + str( _start_height ) + ',' )
	_cnt = 0
	for _yp in range( _end_height - _start_height ):
		print( '\t', end='' )
		for _xp in range( GWK[blockmap_Hmax] ):
			print( str(GWK[BLOCK_WORK + _start_cnt + _cnt]) + ',', end='' )
			_cnt+=1
		print()
	print('\t0xff]')

#-----------------------------------------------------------------
#面編集
#-----------------------------------------------------------------
def editor():
	if( GWK[editor_subadv] == 0 ):
		#初期化
		block_work_init()
		GWK[editor_select] = 0
		GWK[editor_select_ac] = 0
		GWK[editor_result_ac] = 0
		GWK[editor_blockid] = 3
		GWK[start_height] = 0		#編集中は0のまま
		GWK[testplay_switch] = 0
		#マウスカーソル表示
		pyxel.mouse( visible = True )
		GWK[editor_subadv] = 1

	elif( GWK[editor_subadv] == 1 ):
		#編集
		if( GWK[editor_type] == 1 ):
			#320
			GWK[blockmap_Hmax] = 18		#ブロックマップ横最大サイズ
			GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
			GWK[blockmap_shortofs] = 0	#横オフセット
		else:
			#240
			GWK[blockmap_Hmax] = 13		#ブロックマップ横最大サイズ
			GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
			GWK[blockmap_shortofs] = 40	#横オフセット(=(320-240)/2)

		#GWK[editor_select] = 0は欠番とする（非選択時0になるので）

		#マウスカーソルの位置で項目番号をセット
		#(1)ALL CLEAR
		if( ( pyxel.mouse_y >= EDITOR_UP ) and ( pyxel.mouse_y < EDITOR_UP + FONT_HEIGHT )
			and ( pyxel.mouse_x >= EDITOR_RIGHT_SIDE+0x0C ) and ( pyxel.mouse_x < ( EDITOR_RIGHT_SIDE+0x0C + (8*9) ) ) ):
			GWK[editor_select] = 1
		#(2)PRINT
		elif( ( pyxel.mouse_y >= EDITOR_UP+0x18 ) and ( pyxel.mouse_y < EDITOR_UP+0x18 + FONT_HEIGHT )
			and ( pyxel.mouse_x >= EDITOR_LEFT_SIDE ) and ( pyxel.mouse_x < ( EDITOR_LEFT_SIDE + (8*5) ) ) ):
			GWK[editor_select] = 2
		#(3)EXIT
		elif( ( pyxel.mouse_y >= EDITOR_UP+0x28 ) and ( pyxel.mouse_y < EDITOR_UP+0x28 + FONT_HEIGHT )
			and ( pyxel.mouse_x >= EDITOR_LEFT_SIDE ) and ( pyxel.mouse_x < ( EDITOR_LEFT_SIDE + (8*4) ) ) ):
			GWK[editor_select] = 3
		#(4)矢印左
		elif( ( pyxel.mouse_y >= EDITOR_UP+0x18 ) and ( pyxel.mouse_y < EDITOR_UP+0x18 + FONT_HEIGHT )
			and ( pyxel.mouse_x >= ( EDITOR_RIGHT_SIDE+0x18 ) ) and ( pyxel.mouse_x < ( EDITOR_RIGHT_SIDE+0x18 + 0x10 ) ) ):
			GWK[editor_select] = 4
		#(5)矢印右
		elif( ( pyxel.mouse_y >= EDITOR_UP+0x18 ) and ( pyxel.mouse_y < EDITOR_UP+0x18 + FONT_HEIGHT )
			and ( pyxel.mouse_x >= ( EDITOR_RIGHT_SIDE+0x38 ) ) and ( pyxel.mouse_x < ( EDITOR_RIGHT_SIDE+0x38 + 0x10 ) ) ):
			GWK[editor_select] = 5
		#(6)TEST PLAY
		elif( ( pyxel.mouse_y >= EDITOR_UP+0x28 ) and ( pyxel.mouse_y < EDITOR_UP+0x28 + FONT_HEIGHT )
			and ( pyxel.mouse_x >= ( EDITOR_RIGHT_SIDE+0x0C ) ) and ( pyxel.mouse_x < ( EDITOR_RIGHT_SIDE+0x0C + (8*9) ) ) ):
			GWK[editor_select] = 6

		#編集エリアの場合ブロックをセット
		elif( ( pyxel.mouse_y >= UP_OFFSET ) and ( pyxel.mouse_y < ( UP_OFFSET + ( GWK[blockmap_Vmax] * 8 ) ) )
			and ( pyxel.mouse_x >= ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ) and ( pyxel.mouse_x < ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET ) ) ):

			GWK[editor_select] = 0

			#今のマウスカーソルの位置からブロック位置を取得
			_bx = int( ( pyxel.mouse_x - ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ) / BLK_WIDTH )
			_by = int( ( pyxel.mouse_y - UP_OFFSET ) / BLK_HEIGHT )
			_block_pos = _by * GWK[blockmap_Hmax] + _bx
			
			#マウス左クリック	
			if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
				#ブロックIDをセット
				GWK[BLOCK_WORK + _block_pos] = GWK[editor_blockid]
			
			#マウス右クリック
			elif( pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) ):
				#ブロックIDをクリア
				GWK[BLOCK_WORK + _block_pos] = 0

		#ALL CLEARのYES/NO選択
		if( ( GWK[editor_select] == 1 ) and ( GWK[editor_select_ac] == 1 ) ):
			if( ( pyxel.mouse_y >= EDITOR_UP ) and ( pyxel.mouse_y < EDITOR_UP + FONT_HEIGHT )
				and ( pyxel.mouse_x >= EDITOR_RIGHT_SIDE+0x0C ) and ( pyxel.mouse_x < ( EDITOR_RIGHT_SIDE+0x0C + (8*3) ) ) ):
				GWK[editor_result_ac] = 1		#YES
			elif( ( pyxel.mouse_y >= EDITOR_UP ) and ( pyxel.mouse_y < EDITOR_UP + FONT_HEIGHT )
				and ( pyxel.mouse_x >= EDITOR_RIGHT_SIDE+0x0C+(8*5) ) and ( pyxel.mouse_x < ( EDITOR_RIGHT_SIDE+0x0C + (8*7) ) ) ):
				GWK[editor_result_ac] = 2		#NO
		else:
			GWK[editor_result_ac] = 0

		#マウス左クリック	
		if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
			if( GWK[editor_select] == 1 ):
				se_set(4)
				if( GWK[editor_select_ac] == 0 ):
					#YES/NOを聞く
					GWK[editor_select_ac] = 1
				elif( GWK[editor_select_ac] == 1 ):
					if( GWK[editor_result_ac] == 1 ):
						#YES
						#ALL CLEAR実施
						block_work_init()
						GWK[editor_select_ac] = 0
					elif( GWK[editor_result_ac] == 2 ):
						#NO
						GWK[editor_select_ac] = 0
					else:
						pass
				else:
					pass
						
			elif( GWK[editor_select] == 2 ):
				se_set(4)
				#PRINT
				editor_print()
			elif( GWK[editor_select] == 3 ):
				se_set(4)
				#EXIT
				GWK[game_adv] = G_TITLE
				GWK[game_subadv] = 0
				GWK[title_select] = 0
			elif( GWK[editor_select] == 4 ):
				#矢印左
				se_set(4)
				GWK[editor_blockid] = GWK[editor_blockid] - 1
				if( GWK[editor_blockid] <= 0 ):
					GWK[editor_blockid] = 0x0b
			elif( GWK[editor_select] == 5 ):
				#矢印右
				se_set(4)
				GWK[editor_blockid] = GWK[editor_blockid] + 1
				if( GWK[editor_blockid] > 0x0b ):
					GWK[editor_blockid] = 1
			elif( GWK[editor_select] == 6 ):
				#TEST PLAY
				se_set(4)
				#現編集画面を退避
				block_work_save()
				#テストプレイ開始
				GWK[testplay_switch] = 1

				#面エディタのフォント関連を削除
				_scrptr = pyxel.screen.data_ptr()
				for _yp in range(SCREEN_HEIGHT - EDITOR_UP):
					for _xp in range(EDITOR_RIGHT_SIDE+0x48 - EDITOR_LEFT_SIDE):
						_scrptr[ ( ( EDITOR_UP + _yp ) * SCREEN_WIDTH ) + ( EDITOR_LEFT_SIDE + _xp ) ] = 0
						#pyxel.pset( _xp, _yp, 0 )

				#game_control()内で初期化させる
				GWK[game_subadv] = 4
				GWK[editor_subadv] = 2

	#TEST PLAY
	elif( GWK[editor_subadv] == 2 ):
		game_control()

	#TEST PLAYからの戻り用
	elif( GWK[editor_subadv] == 3 ):
		GWK[editor_select] = 0
		GWK[testplay_switch] = 0
		#退避したブロックワークを戻す
		block_work_resave()
		#マウスカーソル表示
		pyxel.mouse( visible = True )
		GWK[editor_subadv] = 1


#-----------------------------------------------------------------
#ブロックワーク初期化
#-----------------------------------------------------------------
def block_work_init():
	for _cnt in range(BLOCK_WORK_SIZE):
		GWK[BLOCK_WORK + _cnt] = 0

#-----------------------------------------------------------------
#ブロックワーク一時退避＆LIVE set
#-----------------------------------------------------------------
def block_work_save():
	for _cnt in range(BLOCK_WORK_SIZE):
		#保存
		GWK[SAVE_BLOCK_WORK + _cnt] = GWK[BLOCK_WORK + _cnt]
		if(( GWK[BLOCK_WORK + _cnt] & 0x0f ) != 0 ):
			GWK[BLOCK_WORK + _cnt] |= BF_LIVE

#-----------------------------------------------------------------
#退避したブロックワークを戻す
#-----------------------------------------------------------------
def block_work_resave():
	for _cnt in range(BLOCK_WORK_SIZE):
		GWK[BLOCK_WORK + _cnt] = GWK[SAVE_BLOCK_WORK + _cnt]

#-----------------------------------------------------------------
#面エディタ描画
#-----------------------------------------------------------------
def editor_draw():
	#BG
	if( GWK[editor_type] == 1 ):
		pyxel.bltm( 0, SCORE_HEIGHT, 0, 0x000, 0x300, SCREEN_WIDTH, SCREEN_HEIGHT)		#320
	else:
		pyxel.bltm(40, SCORE_HEIGHT, 0, 0x140, 0x300, SCREEN_WIDTH2, SCREEN_HEIGHT)		#240
	#title
	set_font_text( SCREEN_WIDTH/2 - (8*6), 0, 'STAGE EDITOR', 0, 0 )

	#面エディタ編集中
	if( GWK[editor_subadv] == 1 ):
		set_font_text( EDITOR_RIGHT_SIDE, EDITOR_UP+0x10, 'SELECT BLOCK', 0, 0 )

		for _cnt in range(EDITOR_ITEM_MAX):
			if( GWK[editor_select] == _cnt ):
				_selcol = 1
			else:
				_selcol = 0
		
			#項目No.1 : ALL CLEAR
			if( _cnt == 1 ):
				if( GWK[editor_select_ac] == 0 ):
					set_font_text( EDITOR_RIGHT_SIDE+0x0C, EDITOR_UP, 'ALL CLEAR', 0, _selcol )
				elif( GWK[editor_select_ac] == 1 ):
					if( GWK[editor_result_ac] == 1 ):
						set_font_text( EDITOR_RIGHT_SIDE+0x0C, EDITOR_UP, 'YES', 0, 1 )
						set_font_text( EDITOR_RIGHT_SIDE+0x0C+(8*3), EDITOR_UP, ' / NO', 0, 0 )
					elif( GWK[editor_result_ac] == 2 ):
						set_font_text( EDITOR_RIGHT_SIDE+0x0C, EDITOR_UP, 'YES / ', 0, 0 )
						set_font_text( EDITOR_RIGHT_SIDE+0x0C+(8*6), EDITOR_UP, 'NO', 0, 1 )
					else:
						set_font_text( EDITOR_RIGHT_SIDE+0x0C, EDITOR_UP, 'YES / NO', 0, 0 )

			#項目No.2 : PRINT
			elif( _cnt == 2 ):
				set_font_text( EDITOR_LEFT_SIDE, EDITOR_UP+0x18, 'PRINT', 0, _selcol )

			#項目No.3 : EXIT
			elif( _cnt == 3 ):
				set_font_text( EDITOR_LEFT_SIDE, EDITOR_UP+0x28, 'EXIT', 0, _selcol )

			#項目No.4 : SELECT BLOCK矢印左
			elif( _cnt == 4 ):
				#矢印左
				if( _selcol == 0 ):
					cput( EDITOR_RIGHT_SIDE+0x18, EDITOR_UP+0x18, 0x9b )
				else:
					cput( EDITOR_RIGHT_SIDE+0x18, EDITOR_UP+0x18, 0x9d )

			#項目No.5 : SELECT BLOCK矢印右
			elif( _cnt == 5 ):
				#矢印右
				if( _selcol == 0 ):
					cput( EDITOR_RIGHT_SIDE+0x38, EDITOR_UP+0x18, 0x9c )
				else:
					cput( EDITOR_RIGHT_SIDE+0x38, EDITOR_UP+0x18, 0x9e )

			#項目No.6 : TEST PLAY
			elif( _cnt == 6 ):
				set_font_text( EDITOR_RIGHT_SIDE+0x0C, EDITOR_UP+0x28, 'TEST PLAY', 0, _selcol )

		#block
		if( GWK[multi_color_switch] != 0 ):
			_id = GWK[editor_blockid] + ID_BLK_MULTI - 1
		else:
			_id = GWK[editor_blockid] + ID_BLK_DEF - 1
		cput( EDITOR_RIGHT_SIDE+0x28, EDITOR_UP+0x18, _id )


		#ステージブロック
		for _by in range(GWK[blockmap_Vmax]):
			for _bx in range(GWK[blockmap_Hmax]):
				_block_pos = _by * GWK[blockmap_Hmax] + _bx
				_id = GWK[BLOCK_WORK + _block_pos] & 0x0f
				if( _id != 0 ):
					if( GWK[multi_color_switch] != 0 ):
						_id = _id + ID_BLK_MULTI - 1
					else:
						_id = _id + ID_BLK_DEF - 1
					cput( ( LEFT_OFFSET + GWK[blockmap_shortofs] ) + ( _bx * BLK_WIDTH ), ( _by * BLK_HEIGHT ) + UP_OFFSET, _id )

	#TEST PLAY
	elif( GWK[editor_subadv] == 2 ):
		#ブロック表示
		stage_block()

		#ショット描画
		shot_draw()

		#アイテム描画
		item_draw()
		
		#パドル表示
		if( GWK[PLY_WORK+ccond] & F_LIVE ):
			cput( GWK[PLY_WORK+cxpos], GWK[PLY_WORK+cypos], GWK[PLY_WORK+cid] )

		#玉表示
		for _cnt in range(BALL_MAX):
			_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
			if( GWK[_wk + ccond] & F_LIVE ):
				cput( GWK[_wk+cxpos], GWK[_wk+cypos], GWK[_wk+cid] )
		#rest表記
		cput( 48, 0, 0x26 )
		set_font_text( 64, 0, str(GWK[rest_number]), 0 )

#-----------------------------------------------------------------
#ドットパターン描画（ブロックは16dotx9dot）
#-----------------------------------------------------------------
def dot_pattern( _dx, _dy, _tp, _adr ):
	_scrptr = pyxel.screen.data_ptr()
	for _yp in range(9):
		for _xp in range(16):
			_scrptr[ ( ( _dy + _yp ) * SCREEN_WIDTH ) + ( _dx + _xp ) ] = _adr[_yp * 16 + _xp] + ( _tp * 0x10 )

#-----------------------------------------------------------------
#ドットパターン描画BG（BGパターンは32dotx32dot）
#-----------------------------------------------------------------
def dot_pattern_BG( _dx, _dy, _adr ):
	_scrptr = pyxel.screen.data_ptr()
	for _yp in range(0x20):
		_s = ( ( _dy + _yp ) * SCREEN_WIDTH ) + _dx
		_e = _s + 0x20
		_scrptr[ _s : _e ] = _adr[_yp]

#X方向半分描画（240dot不足分）
def dot_pattern_BG2( _dx, _dy, _adr ):
	_scrptr = pyxel.screen.data_ptr()
	for _yp in range(0x20):
		_s = ( ( _dy + _yp ) * SCREEN_WIDTH ) + _dx
		_e = _s + 0x10
		_scrptr[ _s : _e ] = _adr[_yp]

#-----------------------------------------------------------------
#キャラクタセット
#	X座標, Y座標, id番号
#-----------------------------------------------------------------
def cput( _xp, _yp, _id ):
	#ドットパターンタイプ？
	if( ctbl[_id][0] == 0xff ):
		#ブロック
		if( ctbl[_id][1] == 0 ):
			if( _id == 0xb8 ):
				_cc = 0x0b
				dot_pattern( _xp, _yp, _cc, mk1blk_tbl )
			elif( _id == 0xb9 ):
				_cc = 0x0b
				dot_pattern( _xp, _yp, _cc, mk2blk_tbl )
			elif( _id == 0xba ):
				_cc = 0x0b
				dot_pattern( _xp, _yp, _cc, mk3blk_tbl )
			elif( _id == 0xbb ):
				_cc = 0x0b
				dot_pattern( _xp, _yp, _cc, mk4blk_tbl )
			else:
				_cc = _id - ID_BLK_MULTI + 1
				dot_pattern( _xp, _yp, _cc, mblk_tbl )
		#ロック
		elif( ctbl[_id][1] == 1 ):
			_cc = _id - ID_BLK_MULTI + 1
			dot_pattern( _xp, _yp, _cc, rblk_tbl )
	else:
			pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

#-----------------------------------------------------------------
#パドル初期化
#-----------------------------------------------------------------
def paddle_init():
	for _cnt in range( PLY_WORK, PLY_WORK + CWORK_SIZE ):
		GWK[_cnt] = 0

	GWK[PLY_WORK + cid] = 0x00
	GWK[PLY_WORK + ccond] = F_LIVE
	GWK[PLY_WORK + cxpos] = int(SCREEN_WIDTH / 2) - int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )
	GWK[PLY_WORK + cypos] = SCREEN_HEIGHT - 0x10

#-----------------------------------------------------------------
#玉初期化
#-----------------------------------------------------------------
def ball_init():
	for _cnt in range( BALL_WORK, BALL_WORK + ( CWORK_SIZE * BALL_MAX ) ):
		GWK[_cnt] = 0


	#ボール初期化
	GWK[ball_speed] = BALL_BASE_SPEED		#初期打ち出し速度
	GWK[ball_degree] = BALL_BASE_DEGREE		#初期打ち出し角度

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
		GWK[_wk + cbig] = 0

#-----------------------------------------------------------------
#ゲーム開始初期化
#-----------------------------------------------------------------
def start_init():

	#各種ワーク初期化
	stage_init()

	#スコア初期化
	GWK[score] = 0
	#残機初期化
	GWK[rest_number] = 2

	#ステージマップセット
	new_stage_set()

#-----------------------------------------------------------------
#ゲーム再開初期化
#-----------------------------------------------------------------
def restart_init():

	#各種ワーク初期化
	stage_init()

	#ステージマップセット
	new_stage_set()

#-----------------------------------------------------------------
#ステージマップセット
#	return 1 : all clear
#-----------------------------------------------------------------
def new_stage_set():
	_stg_adr = blktbl.stage_tbl[ GWK[stage_type] ]

	_adr = _stg_adr[ GWK[stage_number] ]
	_cnt = 0
	GWK[start_height] = _adr[_cnt]

	#stage end code?
	if( GWK[start_height] == 0xff ):
		return 1		#ステージオールクリアを返す
	_cnt += 1
	
	_bcnt = 0
	for _ycnt in range( GWK[blockmap_Vmax] - GWK[start_height] ):
		for _xcnt in range( GWK[blockmap_Hmax] ):
			_id = _adr[_cnt]
			if( _id == 0xff ):
				return
			elif( _id == 0 ):
				GWK[BLOCK_WORK + _bcnt] = _id
			elif( _id == 0x0b ):
				GWK[BLOCK_WORK + _bcnt] = ( BF_LIVE + _id ) | 0x300		#耐久力3セット
			else:
				GWK[BLOCK_WORK + _bcnt] = BF_LIVE + _id

			_bcnt += 1
			_cnt += 1
	return 0

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
				elif( ( _id == 0x0b ) and ( _data & BF_ANIM ) ):
					_acnt = 5 - ( ( _data >> 12 ) & 0x0f )
					if( _acnt < 0 ):
						_acnt = 0
						
					if( _acnt == 0 ):
						if( GWK[multi_color_switch] != 0 ):
							_id = _id + ID_BLK_MULTI - 1
						else:
							_id = _id + ID_BLK_DEF - 1
						cput( ( LEFT_OFFSET + GWK[blockmap_shortofs] ) + ( _xcnt * BLK_WIDTH ), ( GWK[start_height] * BLK_HEIGHT ) + ( _ycnt * BLK_HEIGHT ) + UP_OFFSET, _id )

					else:
						if( GWK[multi_color_switch] != 0 ):
							_id = 0xb8 + _acnt - 1
						else:
							_id = 0x19 + _acnt - 1
						cput( ( LEFT_OFFSET + GWK[blockmap_shortofs] ) + ( _xcnt * BLK_WIDTH ), ( GWK[start_height] * BLK_HEIGHT ) + ( _ycnt * BLK_HEIGHT ) + UP_OFFSET, _id )

				else:
					if( GWK[multi_color_switch] != 0 ):
						_id = _id + ID_BLK_MULTI - 1
					else:
						_id = _id + ID_BLK_DEF - 1
					cput( ( LEFT_OFFSET + GWK[blockmap_shortofs] ) + ( _xcnt * BLK_WIDTH ), ( GWK[start_height] * BLK_HEIGHT ) + ( _ycnt * BLK_HEIGHT ) + UP_OFFSET, _id )
			_bcnt+=1

#-----------------------------------------------------------------
#work clear
#-----------------------------------------------------------------
def work_clear():
	for _cnt in range( WORK_TOP, WORK_END ):
		GWK[_cnt] = 0

#-----------------------------------------------------------------
#work 電源ON時の初期値セット
#-----------------------------------------------------------------
def work_init():
	GWK[rest_number] = 2				#残機
	GWK[stage_number] = 0				#0～
	GWK[score] = 0						#スコア（最大６桁）
	GWK[highscore_0] = 0				#stage_type=0のハイスコア（最大６桁）
	GWK[highscore_1] = 0				#stage_type=1のハイスコア（最大６桁）

	GWK[stage_type] = 0					#0/1 : 320x240 / 240x240
	if( GWK[stage_type] == 0 ):
		GWK[blockmap_Hmax] = 18			#ブロックマップ横最大サイズ
		GWK[blockmap_Vmax] = 20			#ブロックマップ縦最大サイズ
		GWK[blockmap_shortofs] = 0		#横オフセット
	else:
		GWK[blockmap_Hmax] = 13			#ブロックマップ横最大サイズ
		GWK[blockmap_Vmax] = 20			#ブロックマップ縦最大サイズ
		GWK[blockmap_shortofs] = 40		#横オフセット(=(320-240)/2)

	GWK[multi_color_switch] = 1			#0/1 : ブロックマルチカラースイッチ
	GWK[bg_type] = 1					#0/1 : ブロック背景タイプ（現在２種類）
	GWK[ball_color] = 1					#0/1/2 : 玉の色：青/赤/緑

	GWK[field_switch] = 1				#フィールドスイッチ（ブロック背景有り/無し）
	GWK[continue_switch] = 1			#CONTINUEスイッチ
	GWK[item_switch] = 1				#アイテムスイッチ
	GWK[editor_type] = 0				#面エディタスイッチ
	GWK[testplay_switch] = 0			#テストプレイスイッチ

#-----------------------------------------------------------------
#タイトルに戻る場合の初期値セット
#-----------------------------------------------------------------
def title_init():
	GWK[rest_number] = 2				#残機
	GWK[stage_number] = 0				#0～
	GWK[score] = 0						#スコア（最大６桁）
	
	stage_init()

#-----------------------------------------------------------------
#各種ワーク初期化
#-----------------------------------------------------------------
def stage_init():
	if( GWK[stage_type] == 0 ):
		GWK[blockmap_Hmax] = 18			#ブロックマップ横最大サイズ
		GWK[blockmap_Vmax] = 20			#ブロックマップ縦最大サイズ
		GWK[blockmap_shortofs] = 0		#横オフセット
	else:
		GWK[blockmap_Hmax] = 13			#ブロックマップ横最大サイズ
		GWK[blockmap_Vmax] = 20			#ブロックマップ縦最大サイズ
		GWK[blockmap_shortofs] = 40		#横オフセット(=(320-240)/2)

	GWK[testplay_switch] = 0			#テストプレイスイッチ

	#パドル初期化
	paddle_init()

	#玉初期化
	ball_init()

	#ブロック初期化
	for _cnt in range( BLOCK_WORK_SIZE ):
		GWK[BLOCK_WORK + _cnt] = 0

	#アイテムワーク削除
	for _cnt in range( ITEM_MAX * CWORK_SIZE ):
		GWK[ITEM_WORK + _cnt] = 0

	#ショットワーク削除
	for _cnt in range( SHOT_MAX * CWORK_SIZE ):
		GWK[SHOT_WORK + _cnt] = 0

#-----------------------------------------------------------------
#アイテム出現
#[1] 0xa0	アイテム青：lOng	青
#[2] 0xbc	アイテム緑：Add		緑
#[3] 0xc4	アイテム赤：Laser	赤
#[4] 0xcc	アイテム水：Three	水
#[5] 0xd4	アイテム黄：Big		オレンジ
#[6] 0xdc	アイテム紫：Short	紫
#-----------------------------------------------------------------
def item_appear(_block_pos):

	#設定でOFFになっていたら処理しない
	if( GWK[item_switch] == 0 ):
		return

	GWK[item_appcnt] += 1
	if( GWK[item_appcnt] < 5 ):
		return

	GWK[item_appcnt] = 0

	#アイテムワークの空き取得
	_setcnt = -1
	for _cnt in range( ITEM_MAX ):
		_wk = ITEM_WORK + ( CWORK_SIZE * _cnt )
		if( ( GWK[_wk + ccond] & F_LIVE ) == 0 ):
			_setcnt = _cnt
			break
	
	if( _setcnt >= 0 ):
		_item = 0
		_data = pyxel.rndi(0,9)
		if( ( _data == 5 ) or ( _data == 1 ) ):		#2pts.
			_item = ITEM_TYPE_LONG
		elif( _data == 4 ):
			_item = ITEM_TYPE_ADD
		elif( _data == 3 ):
			_item = ITEM_TYPE_LASER
		elif( _data == 7 ):
			_item = ITEM_TYPE_THREE
		elif( _data == 9 ):
			_item = ITEM_TYPE_BIG
		elif((  _data == 6 ) or ( _data == 2 ) or ( _data == 0 ) ):	#3pts.
			_item = ITEM_TYPE_SHORT
		if( _item > 0 ):
			#アイテム出現
			_wk = ITEM_WORK + ( CWORK_SIZE * _setcnt )
			GWK[_wk + ccond] |= F_LIVE
			GWK[_wk + cid] = _item
	
			#_block_posから座標取得
			#算出：_block_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + _bx

			_bx = int( _block_pos % GWK[blockmap_Hmax] )
			_by = int( _block_pos / GWK[blockmap_Hmax] ) + GWK[start_height]

			GWK[_wk + cxpos] = LEFT_OFFSET + GWK[blockmap_shortofs] + ( _bx * BLK_WIDTH ) + 4
			GWK[_wk + cypos] = UP_OFFSET + ( _by * BLK_HEIGHT )
			
			GWK[_wk + cxspd] = 0
			GWK[_wk + cyspd] = 1	#アイテム落下スピード

			GWK[_wk + canum] = 0
			GWK[_wk + cacnt] = 0

#-----------------------------------------------------------------
#分裂玉の移動方向を取得（0～359）
#	0～15, 75～105, 165～195, 255～285, 345～359 は設定しないようにする
#-----------------------------------------------------------------
def getdeg_three_ball():
	_deg = pyxel.rndi(0,359)
	if( 15 > _deg ):
		_deg = 15
	elif( ( 75 < _deg ) and ( 90 > _deg ) ):
		_deg = 75
	elif( ( 90 <= _deg ) and ( 105 > _deg ) ):
		_deg = 105
	elif( ( 165 < _deg ) and ( 180 > _deg ) ):
		_deg = 165
	elif( ( 180 <= _deg ) and ( 195 > _deg ) ):
		_deg = 195
	elif( ( 255 < _deg ) and ( 270 > _deg ) ):
		_deg = 255
	elif( ( 270 <= _deg ) and ( 285 > _deg ) ):
		_deg = 285
	elif( ( 345 < _deg ) and ( 360 > _deg ) ):
		_deg = 345

	return _deg

#-----------------------------------------------------------------
#アイテム制御
#-----------------------------------------------------------------
def item_control():
	#設定でOFFになっていたら処理しない
	if( GWK[item_switch] == 0 ):
		return

	for _cnt in range( ITEM_MAX ):
		_wk = ITEM_WORK + ( CWORK_SIZE * _cnt )
		if( GWK[_wk + ccond] & F_LIVE ):
			GWK[_wk + cypos] = GWK[_wk + cypos] + GWK[_wk + cyspd]
			#フレームアウトチェック
			if( GWK[_wk + cypos] > ( SCREEN_HEIGHT + 0x10 ) ):
				GWK[_wk + ccond] = 0	#DEAD SET
			else:
				#パドルヒットチェック
				#※アイテムはcidがITEM_TYPEなのでキャラクタIDではない
				#※よってHIT範囲はアニメパターンから取得する必要あるがアニメパターンは描画時のみ参照してるため
				#※ここでは設定してない。よってアイテムサイズは固定なのでここではその固定サイズを指定する

				#アイテム固定サイズ
				_item_xsize = 8		#ctbl[GWK[_wk + cid]][2]
				_item_ysize = 8		#ctbl[GWK[_wk + cid]][3]

				#アイテムの中心座標取得
				#_xp = int(GWK[_wk + cxpos]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
				_xp = int(GWK[_wk + cxpos]) + int( _item_xsize / 2 )
				#_yp = int(GWK[_wk + cypos]) + int( ctbl[GWK[_wk + cid]][3] / 2 )
				_yp = int(GWK[_wk + cypos]) + int( _item_ysize / 2 )
				#パドルのヒット範囲を取得
				#_bxL = GWK[PLY_WORK + cxpos] - int( ctbl[GWK[_wk + cid]][2] / 2 )
				_bxL = GWK[PLY_WORK + cxpos] - int( _item_xsize / 2 )
				#_bxR = GWK[PLY_WORK + cxpos] + ctbl[GWK[PLY_WORK + cid]][2] + int( ctbl[GWK[_wk + cid]][2] / 2 )
				_bxR = GWK[PLY_WORK + cxpos] + ctbl[GWK[PLY_WORK + cid]][2] + int( _item_xsize / 2 )
				#_byU = GWK[PLY_WORK + cypos] - int( ctbl[GWK[_wk + cid]][3] / 2 )
				_byU = GWK[PLY_WORK + cypos] - int( _item_ysize / 2 )
				#_byD = GWK[PLY_WORK + cypos] + ctbl[GWK[PLY_WORK + cid]][3] + int( ctbl[GWK[_wk + cid]][3] / 2 )
				_byD = GWK[PLY_WORK + cypos] + ctbl[GWK[PLY_WORK + cid]][3] + int( _item_ysize / 2 )
				if( ( ( _bxL <= _xp ) and ( _bxR > _xp ) ) and ( ( _byU <= _yp ) and ( _byD > _yp ) ) ):
					#パドルの範囲内
					GWK[_wk + ccond] =  GWK[_wk + ccond] & ~F_LIVE
					se_set(6)

					#スコア加算
					score_add( 10 )

					#取得したアイテム効果を実現
					#[1]アイテム青：lOng	青			LONG
					#[2]アイテム緑：Add		緑			パドルにくっつく
					#[3]アイテム赤：Laser	赤			Laser発射可能	0x03
					#[4]アイテム水：Three	水			玉x3
					#[5]アイテム黄：Big		オレンジ	BigBall（パドル３回ヒットで戻る
					#[6]アイテム紫：Short	紫			SHORT
					
					#LONG
					if( GWK[_wk + cid] == ITEM_TYPE_LONG ):
						if( GWK[PLY_WORK + cid] == 0x01 ):
							#長さSHORT:0x01→O[1]→NORMAL:0x00
							GWK[PLY_WORK + cid] = 0x00
							#GWK[PLY_WORK + cxpos] -= 4

						elif( GWK[PLY_WORK + cid] == 0x00 ):
							#長さNORMAL:0x00→O[1]→LONG:0x02
							GWK[PLY_WORK + cid] = 0x02
							#GWK[PLY_WORK + cxpos] -= 8

						elif( GWK[PLY_WORK + cid] == 0x02 ):
							#長さLONG:0x02→O[1]→LONG:0x02
							GWK[PLY_WORK + cid] = 0x02
						else:
							#LASER→NORMAL:0x00→LONG:0x02
							GWK[PLY_WORK + cid] = 0x02
							#GWK[PLY_WORK + cxpos] -= 8

					#SHORT
					elif( GWK[_wk + cid] == ITEM_TYPE_SHORT ):
						if( GWK[PLY_WORK + cid] == 0x01 ):
							#長さSHORT:0x01→S[6]→SHORT:0x01
							GWK[PLY_WORK + cid] = 0x01

						elif( GWK[PLY_WORK + cid] == 0x00 ):
							#長さNORMAL:0x00→S[6]→SHORT:0x01
							GWK[PLY_WORK + cid] = 0x01
							#GWK[PLY_WORK + cxpos] += 4

						elif( GWK[PLY_WORK + cid] == 0x02 ):
							#長さLONG:0x02→S[6]→NORMAL:0x00
							GWK[PLY_WORK + cid] = 0x00
							#GWK[PLY_WORK + cxpos] += 8

						else:
							#LASER→NORMAL:0x00→SHORT:0x01
							GWK[PLY_WORK + cid] = 0x01
							#GWK[PLY_WORK + cxpos] += 4

					#LASER
					elif( GWK[_wk + cid] == ITEM_TYPE_LASER ):
						GWK[PLY_WORK + cid] = 0x03

					elif( GWK[_wk + cid] == ITEM_TYPE_ADD ):
						#次にヒットした玉がくっつく
						GWK[PLY_WORK + ccond] |= F_ONREADY
						#パドルはNORMALに戻る
						GWK[PLY_WORK + cid] = 0x00
						pass
					elif( GWK[_wk + cid] == ITEM_TYPE_THREE ):
						#ひとつの玉が三分割（分割重複したら無限増殖するかも・・・最大数設置必要
						_baseposx = 0
						_baseposy = 0
						_basespdx = 0
						_basespdy = 0
						_cnt3 = BALL_MAX
						for _cnt2 in range( BALL_MAX ):
							#生きてるボールのひとつが三分割
							_wk2 = BALL_WORK + ( CWORK_SIZE * _cnt2 )
							if( GWK[_wk2 + ccond] & F_LIVE ):
								#現在のスピード(+0.5:暫定)から三方向に分裂する
								_deg = getdeg_three_ball()
								_baseposx = GWK[_wk2 + cxpos]
								_baseposy = GWK[_wk2 + cypos]
								_basespdx = GWK[_wk2 + cxspd] + 0.5
								_basespdy = GWK[_wk2 + cyspd] + 0.5
								
								#ベーススピード調整
								if( _basespdx < BALL_BASE_SPEED ):
									_basespdx = BALL_BASE_SPEED
								if( _basespdy < BALL_BASE_SPEED ):
									_basespdy = BALL_BASE_SPEED
								
								GWK[_wk2 + cxspd] = _basespdx * pyxel.cos(_deg)
								GWK[_wk2 + cyspd] = _basespdy * pyxel.sin(_deg)
								_cnt3 = _cnt2 + 1
								break
						_cnt4 = 0
						for _cnt3 in range( BALL_MAX ):
							_wk2 = BALL_WORK + ( CWORK_SIZE * _cnt3 )
							if( ( GWK[_wk2 + ccond] & F_LIVE ) == 0 ):
								GWK[_wk2 + ccond] = F_LIVE
								GWK[_wk2 + cid] = ID_BALL + ( GWK[ball_color] * 2 )		#３色から選択
								GWK[_wk2 + cxpos] = _baseposx
								GWK[_wk2 + cypos] = _baseposy
								GWK[_wk2 + cbig] = 0
								_deg = getdeg_three_ball()
								GWK[_wk2 + cxspd] = _basespdx * pyxel.cos(_deg)
								GWK[_wk2 + cyspd] = _basespdy * pyxel.sin(_deg)
								_cnt4 += 1
								if( _cnt4 >= (ITEM_THREE_BALL-1) ):
									break
						#パドルはNORMALに戻る
						GWK[PLY_WORK + cid] = 0x00
					elif( GWK[_wk + cid] == ITEM_TYPE_BIG ):
						#玉全部ビッグ（貫通）になる
						for _cnt2 in range( BALL_MAX ):
							_wk2 = BALL_WORK + ( CWORK_SIZE * _cnt2 )
							if( GWK[_wk2 + ccond] & F_LIVE ):
								if( GWK[_wk2 + cid] == 0x04 ):
									GWK[_wk2 + cid] = 0x05
								elif( GWK[_wk2 + cid] == 0x06 ):
									GWK[_wk2 + cid] = 0x07
								elif( GWK[_wk2 + cid] == 0x08 ):
									GWK[_wk2 + cid] = 0x09
								GWK[_wk2 + cbig] = 3		#玉１個につき、3回パドルに当たったら戻る
						#パドルはNORMALに戻る
						GWK[PLY_WORK + cid] = 0x00
					
					
					if( GWK[_wk + cid] != ITEM_TYPE_ADD ):
						#くっつき以外の場合はくっつきクリア
						GWK[PLY_WORK + ccond] &= ~F_ONREADY

						#パドルにくっついている玉をはずす
						for _cnt in range(BALL_MAX):
							_wk2 = BALL_WORK + ( CWORK_SIZE * _cnt )
							if( ( GWK[_wk2 + ccond] & (F_LIVE+F_ON) ) == (F_LIVE+F_ON) ):
								GWK[_wk2 + ccond] = GWK[_wk2 + ccond] & ~F_ON;
								#Y方向移動速度が下向きなら上向きに変更する
								if( GWK[_wk + cyspd] > 0 ):
									GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
								#パドルの上は１個のみなのでここで抜ける
								break

					if( GWK[_wk + cid] != ITEM_TYPE_BIG ):
						#BigBall以外なら元に戻る
						for _cnt2 in range( BALL_MAX ):
							_wk2 = BALL_WORK + ( CWORK_SIZE * _cnt2 )
							if( GWK[_wk2 + ccond] & F_LIVE ):
								GWK[_wk2 + cbig] = 0
								if( GWK[_wk2 + cid] == 0x05 ):
									GWK[_wk2 + cid] = 0x04
								elif( GWK[_wk2 + cid] == 0x07 ):
									GWK[_wk2 + cid] = 0x06
								elif( GWK[_wk2 + cid] == 0x09 ):
									GWK[_wk2 + cid] = 0x08

#-----------------------------------------------------------------
#アイテム描画（回転アニメーション）
#-----------------------------------------------------------------
def item_draw():

	item_anim_tbl = [
		0x9f, 0xa3, 0xa2, 0xa1, 0xa0, 0xa1, 0xa2, 0xa3, 	#アイテム青：lOng	青
		0x9f, 0xa7, 0xa6, 0xa5, 0xa4, 0xa5, 0xa6, 0xa7,

		0x9f, 0xbf, 0xbe, 0xbd, 0xbc, 0xbd, 0xbe, 0xbf,		#アイテム緑：Add	緑
		0x9f, 0xc3, 0xc2, 0xc1, 0xc0, 0xc1, 0xc2, 0xc3,

		0x9f, 0xc7, 0xc6, 0xc5, 0xc4, 0xc5, 0xc6, 0xc7,		#アイテム赤：Laser	赤
		0x9f, 0xcb, 0xca, 0xc9, 0xc8, 0xc9, 0xca, 0xcb,

		0x9f, 0xcf, 0xce, 0xcd, 0xcc, 0xcd, 0xce, 0xcf,		#アイテム水：Three	水
		0x9f, 0xd3, 0xd2, 0xd1, 0xd0, 0xd1, 0xd2, 0xd3,

		0x9f, 0xd7, 0xd6, 0xd5, 0xd4, 0xd5, 0xd6, 0xd7,		#アイテム黄：Big	オレンジ
		0x9f, 0xdb, 0xda, 0xd9, 0xd8, 0xd9, 0xda, 0xdb,

		0x9f, 0xdf, 0xde, 0xdd, 0xdc, 0xdd, 0xde, 0xdf,		#アイテム紫：Short	紫
		0x9f, 0xe3, 0xe2, 0xe1, 0xe0, 0xe1, 0xe2, 0xe3,
	]

	#設定でOFFになっていたら処理しない
	if( GWK[item_switch] == 0 ):
		return
	for _cnt in range( ITEM_MAX ):
		_wk = ITEM_WORK + ( CWORK_SIZE * _cnt )
		if( GWK[_wk + ccond] & F_LIVE ):
			#パターンアニメーション
			GWK[_wk + cacnt] += 1
			if( GWK[_wk + cacnt] >= 32 ):
				GWK[_wk + cacnt] = 0
			
			_aid = item_anim_tbl[ ( GWK[_wk + cid] - 1 ) * 16 + int(GWK[_wk + cacnt] / 2 )]
			cput( GWK[_wk+cxpos], GWK[_wk+cypos], _aid )

#-----------------------------------------------------------------
#パドルにヒットするたび玉の移動スピードを加速させる
#-----------------------------------------------------------------
def ball_add_speed_with_paddle( _wk ):
	GWK[_wk + chit] += 1
	if( int( ( GWK[_wk + chit] % 10 ) ) == 0 ):
		GWK[_wk + cspd] = GWK[ball_speed] + ( ( GWK[_wk + chit] / 10 ) * 0.1 )

#-----------------------------------------------------------------
#玉の反射角度調整
#	パドルに当たらずに延々と繰り返し球がヒットを繰り返したとき反射角度を調整する
#	（速度も変更する）
#-----------------------------------------------------------------
def ball_degree_control( _wk ):
	#反射角度調整
	GWK[_wk + chit2] += 1
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

		GWK[_wk + chit2] = 0

#-----------------------------------------------------------------
#玉のヒットチェック
#	座標から今いるブロックを計算してその周辺とのチェックを実施
#	対象：Y座標がパドルの高さ
#		  Y座標がブロックの範囲
#-----------------------------------------------------------------
def ball_hit_check( _wk ):

	#[玉とパドル]
	#玉の中心座標を取得
	_xp = int(GWK[_wk + cxpos]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
	_yp = int(GWK[_wk + cypos]) + int( ctbl[GWK[_wk + cid]][3] / 2 )

	#Y座標がパドルの範囲内
	#パドルのヒット範囲を取得
	_bxL = GWK[PLY_WORK + cxpos] - int( ctbl[GWK[_wk + cid]][2] / 2 )
	_bxR = GWK[PLY_WORK + cxpos] + ctbl[GWK[PLY_WORK + cid]][2] + int( ctbl[GWK[_wk + cid]][2] / 2 )
	_byU = GWK[PLY_WORK + cypos] - int( ctbl[GWK[_wk + cid]][3] / 2 )
	_byD = GWK[PLY_WORK + cypos] + ctbl[GWK[PLY_WORK + cid]][3] + int( ctbl[GWK[_wk + cid]][3] / 2 )

	if( ( ( _bxL <= _xp ) and ( _bxR > _xp ) ) and ( ( _byU <= _yp ) and ( _byD > _yp ) ) ):
		#パドルの範囲内

		#めりこむ前に戻す
		GWK[_wk + cxpos] = GWK[_wk + cxpold]
		GWK[_wk + cypos] = GWK[_wk + cypold]

		#保存値を戻す
		GWK[_wk + cxpold] = GWK[save_cxpold]
		GWK[_wk + cypold] = GWK[save_cypold]
		GWK[_wk + cxspd] = GWK[save_cxspd]
		GWK[_wk + cyspd] = GWK[save_cyspd]

		#玉の中心座標を再取得
		_xp = int(GWK[_wk + cxpos]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
		_yp = int(GWK[_wk + cypos]) + int( ctbl[GWK[_wk + cid]][3] / 2 )

		#めりこみ対応２（まだ中にいるようなら追い出す）
		if( ( _yp - _byU ) <  ( _byD - _yp ) ):
			#パドルの上へ
			GWK[_wk + cypos] = GWK[PLY_WORK + cypos] - ctbl[GWK[_wk + cid]][3]
		else:
			#パドルの左右へ
			if( ( _xp - _bxL ) <  ( _bxR - _xp ) ):
				#パドルの左へ
				GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] - ctbl[GWK[_wk + cid]][2]
			else:
				#パドルの右へ
				GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] + ctbl[GWK[PLY_WORK + cid]][2] + ctbl[GWK[_wk + cid]][2]

		#パドルのどの位置に接触したかの判定で反射角度＆速度を決める（float判定）
		_b80 = _bxL
		_b81 = _bxL + (( _bxR - _bxL ) * 1 / 8 )
		_b82 = _bxL + (( _bxR - _bxL ) * 2 / 8 )
		_b83 = _bxL + (( _bxR - _bxL ) * 3 / 8 )
		_b85 = _bxL + (( _bxR - _bxL ) * 5 / 8 )
		_b86 = _bxL + (( _bxR - _bxL ) * 6 / 8 )
		_b87 = _bxL + (( _bxR - _bxL ) * 7 / 8 )
		_b88 = _bxR
		
		#      |b80|b81|b82|b83|b84|b85|b86|b87|b88|
		# LEFT   |   |   |   |   |   |   |   |   |   RIGHT

		#print("_div = ",_div, _b81, _b82, _b83, _b85, _b86, _b87)
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

		#左端
		if( _b80 > _xp ):
			GWK[_wk + cdeg] = 20
			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
		elif( ( _b80 <= _xp ) and ( _b81 > _xp ) ):
			if( GWK[_wk + cxspd] >= 0 ):
				if( GWK[_wk + cdeg] >= 30 ):
					GWK[_wk + cdeg] -= 20

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			else:
				if( GWK[_wk + cdeg] >= 30 ):
					GWK[_wk + cdeg] -= 20

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
		elif( ( _b81 <= _xp ) and ( _b82 > _xp ) ):
			if( GWK[_wk + cxspd] >= 0 ):
				if( GWK[_wk + cdeg] >= 20 ):
					GWK[_wk + cdeg] -= 10

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			else:
				if( GWK[_wk + cdeg] >= 20 ):
					GWK[_wk + cdeg] -= 10

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
		elif( ( _b82 <= _xp ) and ( _b83 > _xp ) ):
			if( GWK[_wk + cdeg] < 70 ):
				GWK[_wk + cdeg] += 25

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

				#xspdの符号は変えない
				if( GWK[_wk + cxspd] < 0 ):
					GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
				else:
					GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		elif( ( _b85 <= _xp ) and ( _b86 > _xp ) ):
			if( GWK[_wk + cdeg] < 70 ):
				GWK[_wk + cdeg] += 25

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

				#xspdの符号は変えない
				if( GWK[_wk + cxspd] < 0 ):
					GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg]) * (-1)
				else:
					GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		elif( ( _b86 <= _xp ) and ( _b87 > _xp ) ):
			if( GWK[_wk + cxspd] >= 0 ):
				if( GWK[_wk + cdeg] >= 20 ):
					GWK[_wk + cdeg] -= 10

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			else:
				if( GWK[_wk + cdeg] >= 20 ):
					GWK[_wk + cdeg] -= 10

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		elif( ( _b87 <= _xp ) and ( _b88 > _xp ) ):
			if( GWK[_wk + cxspd] >= 0 ):
				if( GWK[_wk + cdeg] >= 30 ):
					GWK[_wk + cdeg] -= 20

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			else:
				if( GWK[_wk + cdeg] >= 30 ):
					GWK[_wk + cdeg] -= 20

				#deg調整（0 or 90にはしない）
				if( GWK[_wk + cdeg] < 20 ):
					GWK[_wk + cdeg] = 20
				if( GWK[_wk + cdeg] > 70 ):
					GWK[_wk + cdeg] = 70

			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		#右端
		elif( _b88 <= _xp ):
			GWK[_wk + cdeg] = 20
			GWK[_wk + cxspd] = GWK[_wk + cspd] * pyxel.cos(GWK[_wk + cdeg])
		
		GWK[_wk + cyspd] = GWK[_wk + cspd] * pyxel.sin(GWK[_wk + cdeg]) * (-1)

		#パドルにヒットするたび加速
		ball_add_speed_with_paddle( _wk )
		
		#角度調整カウンタクリア
		GWK[_wk + chit2] = 0
		#Paddle Hit!
		#ヒットセット
		GWK[_wk + ccond] |= F_HIT
		se_set(4)

		#玉がパドルにくっつく予定？
		if( GWK[PLY_WORK + ccond] & F_ONREADY ):
			_isON = False
			#すでにくっついている玉は無いか確認する
			for _cnt in range(BALL_MAX):
				_wk2 = BALL_WORK + ( CWORK_SIZE * _cnt )
				if( ( GWK[_wk2 + ccond] & (F_LIVE+F_ON) ) == (F_LIVE+F_ON) ):
					#あった
					_isON = True
					break
			if( _isON == False ):
				#くっつく
				GWK[_wk + ccond] |= F_ON

		#貫通玉の時、パドルに3回当たると元に戻る
		if( ( GWK[_wk + cid] == 0x05 ) or ( GWK[_wk + cid] == 0x07 ) or ( GWK[_wk + cid] == 0x09 ) ):
			if( GWK[_wk + cbig] > 0 ):
				GWK[_wk + cbig] = GWK[_wk + cbig] - 1
				if( GWK[_wk + cbig] <= 0 ):
					GWK[_wk + cbig] = 0
					if( GWK[_wk + cid] == 0x05 ):
						GWK[_wk + cid] = 4
					elif( GWK[_wk + cid] == 0x07 ):
						GWK[_wk + cid] = 6
					elif( GWK[_wk + cid] == 0x09 ):
						GWK[_wk + cid] = 8

		return


	#[玉とブロック]
	#玉の中心座標を取得
	_xp = int(GWK[_wk + cxpos]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
	_yp = int(GWK[_wk + cypos]) + int( ctbl[GWK[_wk + cid]][3] / 2 )
	#玉の中心座標のブロック位置を算出
	_bx = int( ( _xp - ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ) / BLK_WIDTH )
	_by = int( ( _yp - UP_OFFSET ) / BLK_HEIGHT )

	_saved_xspd = GWK[save_cxspd]
	_saved_yspd = GWK[save_cyspd]

	#ブロック範囲内
	if( ( _by >= GWK[start_height] ) and ( _by < GWK[blockmap_Vmax] ) and ( ( _bx >= 0 ) and ( _bx < GWK[blockmap_Hmax] ) ) ) :
		#玉の中心が居るブロックの位置
		_block_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
		#存在するブロック？
		if( GWK[BLOCK_WORK + _block_pos] & BF_LIVE ):

			#移動前のブロックを算出
			_xpold = int(GWK[_wk + cxpold]) + int( ctbl[GWK[_wk + cid]][2] / 2 )
			_ypold = int(GWK[_wk + cypold]) + int( ctbl[GWK[_wk + cid]][3] / 2 )
			_bxold = int( ( _xpold - ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ) / BLK_WIDTH )
			_byold = int( ( _ypold - UP_OFFSET ) / BLK_HEIGHT )
			#_block_pos_old = (_byold - GWK[start_height]) * GWK[blockmap_Hmax] + _bxold

			#当たったブロックと移動前のブロックを比較して位置関係から反射方向を決める
			#玉の座標は当たる前に戻す（めりこみはずし）
			GWK[_wk + cxpos] = GWK[_wk + cxpold]
			GWK[_wk + cypos] = GWK[_wk + cypold]

			#ヒットセット
			GWK[_wk + ccond] |= F_HIT
			#保存値を戻して反射速度＆角度を調整
			GWK[_wk + cxpold] = GWK[save_cxpold]
			GWK[_wk + cypold] = GWK[save_cypold]
			GWK[_wk + cxspd] = GWK[save_cxspd]
			GWK[_wk + cyspd] = GWK[save_cyspd]


			##どちらも同じはありえないから考えない（ずっとヒット中ならありえるのか・・・
			#if(( _bx == _bxold )and( _by == _byold )):
			#	print("[SAME]", _bx, _by )
			#	show()		#[DEBUG]止める（こなかった
			
			#Yブロックが同じならX反転
			if( _by == _byold ):
				GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
			#Xブロックが同じならY反転
			if( _bx == _bxold ):
				GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

			#共に異なる場合（斜め進入の場合）共に反転
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
					#左に無し、上に有りの場合
					else:
						_check_pos = ((_by-1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1

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

					#左に無し、下に有りの場合
					else:
						_check_pos = ((_by+1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1

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

					#右に無し、上に有りの場合
					else:
						_check_pos = ((_by-1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1

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

					#右に無し、下に有りの場合
					else:
						_check_pos = ((_by+1) - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
						if( GWK[BLOCK_WORK + _check_pos] & BF_LIVE ):
							#Xのみ反転
							GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
							_set = 1

				if( _set == 0 ):
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

			#ブロックに当たった処理
			block_hit(_block_pos, _wk)

			_cid = GWK[BLOCK_WORK + _block_pos] & 0x0f
			#壊れないブロック以外
			if( _cid != 0x01 ):
				#貫通玉なら反射しない
				if( ( GWK[_wk + cid] == 0x05 ) or ( GWK[_wk + cid] == 0x07 ) or ( GWK[_wk + cid] == 0x09 ) ):
					GWK[_wk + cxspd] = _saved_xspd
					GWK[_wk + cyspd] = _saved_yspd


	#ステージクリア判定
	_live_check = 0
	for _cnt in range( BLOCK_WORK_SIZE ):
		if( GWK[BLOCK_WORK + _cnt] & BF_LIVE ):
			#壊せないブロックは除外
			if( ( GWK[BLOCK_WORK + _cnt] & 0x0f ) != 0x01 ):
				_live_check = 1
				break

	#もうブロック無いよ
	if( _live_check == 0 ):
		if( GWK[game_adv] == G_DEMOPLAY ):
			title_set()
		else:
			#クリア時アイテムは消しておく
			#アイテムワーク削除
			for _cnt in range( ITEM_MAX * CWORK_SIZE ):
				GWK[ITEM_WORK + _cnt] = 0

			if( GWK[testplay_switch] == 0 ):
				GWK[game_adv] = G_STAGECLEAR
				GWK[game_subadv] = 0
				se_set(33)
			#面エディタのテストプレイ中？
			elif( ( GWK[testplay_switch] == 1 ) and ( GWK[game_adv] == G_EDITOR ) ):
				GWK[editor_subadv] = 3
			else:
				print("####[ball_hit_check] ERROR GWK[game_adv]:", GWK[game_adv] );

#===============================================================================
#更新
#===============================================================================
def update():
	if( GWK[game_adv] == G_TITLE ):
		#タイトル画面表示
		if( GWK[game_subadv] == 0 ):	#初期化
			#タイトル画面作成
			GWK[stage_number] = 0
			start_init()

			#マウスカーソル表示
			pyxel.mouse( visible = True )

			GWK[game_subadv] = 1

		elif( GWK[game_subadv] == 1 ):	#項目選択待ち

			GWK[title_counter] += 1

			if( GWK[title_counter] > 500 ):
				#デモプレイ開始
				GWK[game_adv] = G_DEMOPLAY
				GWK[game_subadv] = 0
			else:
				#開始入力待ち
				if( ( pyxel.mouse_y >= TITLE_START_Y ) and ( pyxel.mouse_y < ( TITLE_START_Y + FONT_HEIGHT ) )
					and ( pyxel.mouse_x >= TITLE_START_X ) and ( pyxel.mouse_x < ( TITLE_START_X + TITLE_START_OFS ) ) ):
					GWK[title_select] = 0

				if( ( pyxel.mouse_y >= TITLE_SETTING_Y ) and ( pyxel.mouse_y < ( TITLE_SETTING_Y + FONT_HEIGHT ) ) 
					and ( pyxel.mouse_x >= TITLE_SETTING_X ) and ( pyxel.mouse_x < ( TITLE_SETTING_X + TITLE_SETTING_OFS ) ) ):
					GWK[title_select] = 1

				if( ( pyxel.mouse_y >= TITLE_EXIT_Y ) and ( pyxel.mouse_y < ( TITLE_EXIT_Y + FONT_HEIGHT ) ) 
					and ( pyxel.mouse_x >= TITLE_EXIT_X ) and ( pyxel.mouse_x < ( TITLE_EXIT_X + TITLE_EXIT_OFS ) ) ):
					GWK[title_select] = 2

				if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
					if( GWK[title_select] == 0 ):
						#ゲーム開始
						GWK[game_adv] = G_GAME
						GWK[game_subadv] = 0
						se_set(32)

					elif( GWK[title_select] == 1 ):
						#設定画面へ
						GWK[game_adv] = G_SETTING
						GWK[setting_select] = 0
						se_set(32)

					else:
						pyxel.quit()

					GWK[game_subadv] = 0

	elif( GWK[game_adv] == G_DEMOPLAY ):
		game_control()
	elif( GWK[game_adv] == G_GAME ):
		game_control()
	elif( GWK[game_adv] == G_CONTINUE ):
		if( GWK[game_subadv] == 0 ):

			#マウスカーソル表示
			pyxel.mouse( visible = True )

			GWK[continue_result] = 0		#not set
			GWK[game_subadv] = 1

			#ハイスコア更新
			if( GWK[stage_type] == 0 ):
				if( GWK[highscore_0] < GWK[score] ):
					GWK[highscore_0] = GWK[score]
			elif( GWK[stage_type] == 1 ):
				if( GWK[highscore_1] < GWK[score] ):
					GWK[highscore_1] = GWK[score]

		elif( GWK[game_subadv] == 1 ):

			if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
				#set_font_text( int(SCREEN_WIDTH/2) - int(8*8/2), 180, 'YES / NO', 0 )
				_xp = int(SCREEN_WIDTH/2) - int(8*8/2)
				_yp = 180

				GWK[continue_result] = 0
				if( ( pyxel.mouse_y >= _yp ) and ( pyxel.mouse_y < ( _yp + FONT_HEIGHT ) ) 
					and ( pyxel.mouse_x >= _xp ) and ( pyxel.mouse_x < ( _xp + (8*3) ) ) ):
					GWK[continue_result] = 2	#YES
				elif( ( pyxel.mouse_y >= _yp ) and ( pyxel.mouse_y < ( _yp + FONT_HEIGHT ) ) 
					and ( pyxel.mouse_x >= (_xp + (8*6)) ) and ( pyxel.mouse_x < ( _xp + (8*8) ) ) ):
					GWK[continue_result] = 1	#NO

				#NO
				if( GWK[continue_result] == 1 ):
					GWK[game_subadv] = 0
					GWK[game_adv] = G_OVER

				#YES
				elif( GWK[continue_result] == 2 ):
					GWK[game_subadv] = 3
					GWK[game_adv] = G_GAME

	elif( GWK[game_adv] == G_OVER ):
		if( GWK[game_subadv] == 0 ):
			GWK[wait_counter] = 0
			GWK[game_subadv] = 1			
		elif( GWK[game_subadv] == 1 ):
			GWK[wait_counter] += 1
			if( GWK[wait_counter] > 100 ):
				#タイトルに戻る
				title_set()

	elif( GWK[game_adv] == G_STAGECLEAR ):
		if( GWK[game_subadv] == 0 ):
			GWK[wait_counter] = 0
			GWK[game_subadv] = 1			
		elif( GWK[game_subadv] == 1 ):
			GWK[wait_counter] += 1
			if( GWK[wait_counter] > 100 ):
				GWK[stage_number] += 1
				#次のステージマップセット
				_result = new_stage_set()
				if( _result == 1 ):
					#ステージ番号クリアー
					GWK[stage_number] = 0
				
				#ゲーム継続
				GWK[game_adv] = G_GAME
				GWK[game_subadv] = 2	#ゲーム再開

	elif( GWK[game_adv] == G_SETTING ):
		#設定画面
		setting_control()
	elif( GWK[game_adv] == G_EDITOR ):
		#面エディタ
		editor()
	else:
		GWK[game_adv] = G_TITLE
		GWK[game_subadv] = 0


#-----------------------------------------------------------------
#Goto Title
#-----------------------------------------------------------------
def title_set():
	GWK[game_adv] = G_TITLE
	GWK[game_subadv] = 0
	GWK[title_select] = 0
	GWK[title_counter] = 0

#-----------------------------------------------------------------
#設定更新
#	項目No.0 : STAGE TYPE（0:320x240, 1:240x240）			stage_type
#	項目No.1 : BLOCK TYPE（0:DEFAULT COLOR, 1:MULTI COLOR）	multi_color_switch
#	項目No.2 : BG    TYPE（0/1）							bg_type
#	項目No.3 : BALL  COLOR（0:BLUE / 1:RED / 2:GREEN）		ball_color
#	項目No.4 : FIELD ON/OFF									field_switch
#	項目No.5 : CONTINUE ON/OFF								continue_switch
#	項目No.6 : ITEM ON/OFF									item_switch
#	（空き：No.7）
#	EXITボタン（項目No.8）
#	（空き：No.9）
#	[項目No.10 : STAGE EDITOR								editor_type
#	[ENTER STAGE EDITOR（項目No.11）
#-----------------------------------------------------------------
def setting_control():
	if( GWK[game_subadv] == 0 ):
		#初期化
		#マウスカーソル表示
		pyxel.mouse( visible = True )
		GWK[game_subadv] = 1

	elif( GWK[game_subadv] == 1 ):
		#選択
		for _cnt in range(SETTING_ITEM_MAX):
			if( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_TITLE_X ) and ( pyxel.mouse_x < ( SETTING_TITLE_X + SETTING_XOFS ) ) ):
				GWK[setting_select] = _cnt

		if( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
			_cnt = GWK[setting_select]
			if( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_LEFT_X ) and ( pyxel.mouse_x < ( SETTING_LEFT_X + 0x10 ) ) ):
				#左選択

				if( _cnt == 0 ):	#項目No.0 : STAGE TYPE（0.1:320x240, 2,3:240x240）
					se_set(4)
					GWK[stage_type] -= 1
					if( GWK[stage_type] < 0 ):
						GWK[stage_type] = 1

					if( GWK[stage_type] == 0 ):
						GWK[blockmap_Hmax] = 18		#ブロックマップ横最大サイズ
						GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
						GWK[blockmap_shortofs] = 0	#横オフセット
					else:
						GWK[blockmap_Hmax] = 13		#ブロックマップ横最大サイズ
						GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
						GWK[blockmap_shortofs] = 40	#横オフセット(=(320-240)/2)

				elif( _cnt == 1 ):	#項目No.1 : BLOCK TYPE（0:DEFAULT COLOR, 1:MULTI COLOR）
					se_set(4)
					GWK[multi_color_switch] = ( GWK[multi_color_switch] + 1 ) & 1
				elif( _cnt == 2 ):	#項目No.2 : BG    TYPE（0/1）
					se_set(4)
					GWK[bg_type] = ( GWK[bg_type] + 1 ) & 1
				elif( _cnt == 3 ):	#項目No.3 : BALL  COLOR（0:BLUE / 1:RED / 2:GREEN）
					se_set(4)
					GWK[ball_color] -= 1
					if( GWK[ball_color] < 0 ):
						GWK[ball_color] = 2
				elif( _cnt == 4 ):	#項目No.4 : FIELD ON/OFF（ONなら影もON）
					se_set(4)
					GWK[field_switch] = ( GWK[field_switch] + 1 ) & 1
				elif( _cnt == 5 ):	#項目No.5 : CONTINUE ON/OFF
					se_set(4)
					GWK[continue_switch] = ( GWK[continue_switch] + 1 ) & 1
				elif( _cnt == 6 ):	#項目No.6 : ITEM ON/OFF
					se_set(4)
					GWK[item_switch] = ( GWK[item_switch] + 1 ) & 1
				elif( _cnt == 10 ):	#項目No.10 : STAGE EDITOR
					se_set(4)
					GWK[editor_type] -= 1
					if( GWK[editor_type] < 0 ):
						GWK[editor_type] = 2

			elif( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_TITLE_X ) and ( pyxel.mouse_x < ( SETTING_TITLE_X + (8*4) ) ) ):

				if( _cnt == 8 ):	#EXIT
					se_set(4)
					GWK[game_adv] = G_TITLE
					GWK[game_subadv] = 0
					GWK[title_select] = 0
			elif( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_TITLE_X ) and ( pyxel.mouse_x < ( SETTING_TITLE_X + (8*18) ) ) ):
				if( ( GWK[editor_type] != 0 ) and ( _cnt == 11 ) ):		#ENTER STAGE EDITOR
					se_set(4)
					GWK[game_adv] = G_EDITOR
					GWK[game_subadv] = 0
					GWK[editor_subadv] = 0

			elif( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_RIGHT_X ) and ( pyxel.mouse_x < ( SETTING_RIGHT_X + 0x10 ) ) ):
				#右選択
				if( _cnt == 0 ):	#項目No.0 : STAGE TYPE（0.1:320x240, 2,3:240x240）
					se_set(4)
					GWK[stage_type] += 1
					if( GWK[stage_type] > 1 ):
						GWK[stage_type] = 0

					if( GWK[stage_type] == 0 ):
						GWK[blockmap_Hmax] = 18		#ブロックマップ横最大サイズ
						GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
						GWK[blockmap_shortofs] = 0	#横オフセット
					else:
						GWK[blockmap_Hmax] = 13		#ブロックマップ横最大サイズ
						GWK[blockmap_Vmax] = 20		#ブロックマップ縦最大サイズ
						GWK[blockmap_shortofs] = 40	#横オフセット(=(320-240)/2)

				elif( _cnt == 1 ):	#項目No.1 : BLOCK TYPE（0:DEFAULT COLOR, 1:MULTI COLOR）
					se_set(4)
					GWK[multi_color_switch] = ( GWK[multi_color_switch] + 1 ) & 1
				elif( _cnt == 2 ):	#項目No.2 : BG    TYPE（0/1）
					se_set(4)
					GWK[bg_type] = ( GWK[bg_type] + 1 ) & 1
				elif( _cnt == 3 ):	#項目No.3 : BALL  COLOR（0:BLUE / 1:RED / 2:GREEN）
					se_set(4)
					GWK[ball_color] += 1
					if( GWK[ball_color] > 2 ):
						GWK[ball_color] = 0
				elif( _cnt == 4 ):	#項目No.4 : FIELD ON/OFF（ONなら影もON）
					se_set(4)
					GWK[field_switch] = ( GWK[field_switch] + 1 ) & 1
				elif( _cnt == 5 ):	#項目No.5 : CONTINUE ON/OFF
					se_set(4)
					GWK[continue_switch] = ( GWK[continue_switch] + 1 ) & 1
				elif( _cnt == 6 ):	#項目No.6 : ITEM ON/OFF
					se_set(4)
					GWK[item_switch] = ( GWK[item_switch] + 1 ) & 1
				elif( _cnt == 10 ):	#項目No.10 : STAGE EDITOR
					se_set(4)
					GWK[editor_type] += 1
					if( GWK[editor_type] > 2 ):
						GWK[editor_type] = 0

			elif( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_TITLE_X ) and ( pyxel.mouse_x < ( SETTING_TITLE_X + (8*4) ) ) ):
				if( _cnt == 8 ):	#EXIT
					se_set(4)
					GWK[game_adv] = G_TITLE
					GWK[game_subadv] = 0
					GWK[title_select] = 0
			elif( ( pyxel.mouse_y >= ( SETTING_Y + ( SETTING_YOFS * _cnt ) ) ) and ( pyxel.mouse_y < ( SETTING_Y + ( SETTING_YOFS * _cnt ) + FONT_HEIGHT ) )
				and ( pyxel.mouse_x >= SETTING_TITLE_X ) and ( pyxel.mouse_x < ( SETTING_TITLE_X + (8*18) ) ) ):
				if( ( GWK[editor_type] != 0 ) and ( _cnt == 11 ) ):		#ENTER STAGE EDITOR
					se_set(4)
					GWK[game_adv] = G_EDITOR
					GWK[game_subadv] = 0
					GWK[editor_subadv] = 0

#-----------------------------------------------------------------
#設定描画
#-----------------------------------------------------------------
def setting_draw():
	set_font_text( SETTING_TOP_X, SETTING_TOP_Y, 'SETTING', 0, 0 )
	for _cnt in range(SETTING_ITEM_MAX):
		if( GWK[setting_select] == _cnt ):
			_selcol = 1
		else:
			_selcol = 0
			
		#項目No.0 : STAGE TYPE（0.1:320x240, 2,3:240x240）
		if( _cnt == 0 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'STAGE TYPE', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[stage_type] == 0 ):
				_str = '320X240 STAGE'
			elif( GWK[stage_type] == 1 ):
				_str = '240X240 STAGE'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		#項目No.1 : BLOCK TYPE（0:DEFAULT COLOR, 1:MULTI COLOR）
		elif( _cnt == 1 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'BLOCK TYPE', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[multi_color_switch] == 0 ):
				_str = 'DEFAULT COLOR'
			else:
				_str = 'MULTI COLOR'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		#項目No.2 : BG    TYPE（0/1）
		elif( _cnt == 2 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'BG TYPE', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[bg_type] == 0 ):
				_str = 'PATTERN-0'
			else:
				_str = 'PATTERN-1'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		#項目No.3 : BALL  COLOR（0:BLUE / 1:RED / 2:GREEN）
		elif( _cnt == 3 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'BALL COLOR', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[ball_color] == 0 ):
				_str = 'BLUE'
			elif( GWK[ball_color] == 1 ):
				_str = 'RED'
			else:
				_str = 'GREEN'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		#項目No.4 : FIELD ON/OFF（ONなら影もON）
		elif( _cnt == 4 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'FIELD SW', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[field_switch] == 0 ):
				_str = 'FIELD OFF'
			else:
				_str = 'FIELD ON'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		#項目No.5 : CONTINUE ON/OFF
		elif( _cnt == 5 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'CONTINUE SW', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[continue_switch] == 0 ):
				_str = 'CONTINUE OFF'
			else:
				_str = 'CONTINUE ON'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		#項目No.6 : ITEM ON/OFF
		elif( _cnt == 6 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'ITEM SW', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[item_switch] == 0 ):
				_str = 'ITEM OFF'
			else:
				_str = 'ITEM ON'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )
		elif( _cnt == 8 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'EXIT', 0, _selcol )

		#項目No.10 : STAGE EDITOR
		elif( _cnt == 10 ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'STAGE EDITOR', 0, _selcol )
			#矢印左
			if( _selcol == 0 ):
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9b )
			else:
				cput( SETTING_LEFT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9d )

			if( GWK[editor_type] == 0 ):
				_str = 'OFF'
			elif( GWK[editor_type] == 1 ):
				_str = 'WIDTH 320 SIZE'
			elif( GWK[editor_type] == 2 ):
				_str = 'WIDTH 240 SIZE'
			set_font_text( SETTING_ITEM_X, SETTING_Y + ( SETTING_YOFS * _cnt ), _str, 0, _selcol )

			#矢印右
			if( _selcol == 0 ):
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9c )
			else:
				cput( SETTING_RIGHT_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 0x9e )

		elif( ( GWK[editor_type] != 0 ) and ( _cnt == 11 ) ):
			set_font_text( SETTING_TITLE_X, SETTING_Y + ( SETTING_YOFS * _cnt ), 'ENTER STAGE EDITOR', 0, _selcol )



#-----------------------------------------------------------------
#ショットとブロックのヒットチェック
#-----------------------------------------------------------------
def shot_and_block_check():
	for _cnt in range( SHOT_MAX ):
		_wk = SHOT_WORK + ( CWORK_SIZE * _cnt )
		if( GWK[_wk + ccond] & F_LIVE ):
			#ショット動作
			GWK[_wk + cxpos] = GWK[_wk + cxpos] + GWK[_wk + cxspd]
			GWK[_wk + cypos] = GWK[_wk + cypos] + GWK[_wk + cyspd]
			if( GWK[_wk + cypos] < UP_OFFSET ):
				GWK[_wk + cypos] = UP_OFFSET
				GWK[_wk + ccond] = 0
				#continue

		if( GWK[_wk + ccond] & F_LIVE ):
			#ショットの左端座標を取得
			_xp = int(GWK[_wk + cxpos])
			_yp = int(GWK[_wk + cypos])

			#ショットの左端座標のブロック位置を算出
			_bx = int( ( _xp - ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ) / BLK_WIDTH )
			_by = int( ( _yp - UP_OFFSET ) / BLK_HEIGHT )

			#ブロック範囲内
			if( ( _by >= GWK[start_height] ) and ( _by < GWK[blockmap_Vmax] ) and ( ( _bx >= 0 ) and ( _bx < GWK[blockmap_Hmax] ) ) ) :
				#玉の中心が居るブロックの位置
				_block_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
				#存在するブロック？
				if( GWK[BLOCK_WORK + _block_pos] & BF_LIVE ):
					#ブロックに当たった処理
					block_hit(_block_pos, _wk)
					GWK[_wk + ccond] = 0
					return

			#ショットの右端座標を取得
			_xp = int(GWK[_wk + cxpos]) + ctbl[GWK[_wk + cid]][2]
			_yp = int(GWK[_wk + cypos])

			#ショットの右端座標のブロック位置を算出
			_bx = int( ( _xp - ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ) / BLK_WIDTH )
			_by = int( ( _yp - UP_OFFSET ) / BLK_HEIGHT )

			#ブロック範囲内
			if( ( _by >= GWK[start_height] ) and ( _by < GWK[blockmap_Vmax] ) and ( ( _bx >= 0 ) and ( _bx < GWK[blockmap_Hmax] ) ) ) :
				#玉の中心が居るブロックの位置
				_block_pos = (_by - GWK[start_height]) * GWK[blockmap_Hmax] + _bx
				#存在するブロック？
				if( GWK[BLOCK_WORK + _block_pos] & BF_LIVE ):
					#ブロックに当たった処理
					block_hit(_block_pos, _wk)
					GWK[_wk + ccond] = 0
					return


#-----------------------------------------------------------------
#ブロックに当たった処理
#-----------------------------------------------------------------
def block_hit(_block_pos, _wk):
	_erase_flag = False
	#Block Hit!
	_cid = GWK[BLOCK_WORK + _block_pos] & 0x0f
	#ROCK BLOCK ?
	if( _cid == 0x01 ):
		se_set(5)
	
	#No.11 GRAY BLOCK（耐久有り、ひとまず３発で）
	elif( _cid == 0x0b ):
		se_set(5)

		#耐久力取得
		_durab = ( GWK[BLOCK_WORK + _block_pos] >> 8 ) & 0x0f
		_durab -= 1

		#貫通玉なら消滅
		if( ( GWK[_wk + cid] == 0x05 ) or ( GWK[_wk + cid] == 0x07 ) or ( GWK[_wk + cid] == 0x09 ) ):
			_durab = 0

		#耐久力オーバー
		if( _durab <= 0 ):
			GWK[BLOCK_WORK + _block_pos] = GWK[BLOCK_WORK + _block_pos] & 0x00ff
			#→ブロック消滅へ
			_erase_flag = True
		else:
			#耐久力減らしてアニメカウンタ初期化
			GWK[BLOCK_WORK + _block_pos] = ( GWK[BLOCK_WORK + _block_pos] & 0x00ff ) | ( _durab << 8 ) | 0x5000 | BF_ANIM
	else:
		_erase_flag = True

	#ブロック消滅
	if( _erase_flag ):
		GWK[BLOCK_WORK + _block_pos] = 0x00
		se_set(5)

		#アイテム出現
		item_appear(_block_pos)

		#スコア加算
		score_add( 20 )

#-----------------------------------------------------------------
#スコア加算
#-----------------------------------------------------------------
def score_add( _addscore ):

	if( GWK[PLY_WORK + cid] == 0x01 ):		#SHORT
		_addscore *= 2
	elif( GWK[PLY_WORK + cid] == 0x02 ):	#LONG
		_addscore /= 2

	GWK[score] += int(_addscore)
	if( GWK[score] > SCORE_MAX ):
		GWK[score] = SCORE_MAX		#カンスト
	if( int(GWK[score] % 5000 ) == 0 ):
		#玉+1
		GWK[rest_number] += 1
		se_set(27)

#-----------------------------------------------------------------
#玉制御
#-----------------------------------------------------------------
def ball_control():
	_dead_count = 0
	for _cnt in range(BALL_MAX):
		_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
		#パドルの上に玉が存在？（１個しかつかない）
		if( ( GWK[_wk + ccond] & (F_LIVE+F_ON) ) == (F_LIVE+F_ON) ):
			#左クリックで離れる
			#if( ( ( GWK[game_adv] == G_GAME ) or ( ( GWK[game_adv] == G_EDITOR ) and ( GWK[testplay_switch] == 1 ) ) ) and ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ) ):
			if( ( ( GWK[game_adv] == G_GAME ) or ( ( GWK[game_adv] == G_EDITOR ) ) ) and ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ) ):
				GWK[_wk + ccond] = GWK[_wk + ccond] & ~F_ON;
				#Y方向移動速度が下向きなら上向きに変更する
				if( GWK[_wk + cyspd] > 0 ):
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

			#デモプレイ中は即解除する
			elif( GWK[game_adv] == G_DEMOPLAY ):
				GWK[_wk + ccond] = GWK[_wk + ccond] & ~F_ON;
				#Y方向移動速度が下向きなら上向きに変更する
				if( GWK[_wk + cyspd] > 0 ):
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)

				if( GWK[_wk + cxpos] < ( SCREEN_WIDTH / 2 ) ):
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)

		#通常処理
		if( GWK[_wk + ccond] & F_LIVE ):

			#パドルの上に載ってる
			if( GWK[_wk + ccond] & F_ON ):
				GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] + int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )
				GWK[_wk + cypos] = GWK[PLY_WORK + cypos] - ctbl[GWK[_wk + cid]][2]

			#移動中
			else:
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

				#玉の枠内チェック
				#左右
				if( GWK[_wk + cxpos] < ( LEFT_OFFSET + GWK[blockmap_shortofs] ) ):
					GWK[_wk + cxpos] = ( LEFT_OFFSET + GWK[blockmap_shortofs] )
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
					se_set(4)

				elif( GWK[_wk + cxpos] > ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[_wk + cid]][2] ) ):
					GWK[_wk + cxpos] = ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[_wk + cid]][2] )
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
					se_set(4)

				elif( GWK[_wk + cxpos] > ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET ) ):
					GWK[_wk + cxpos] = ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET )
					GWK[_wk + cxspd] = GWK[_wk + cxspd] * (-1)
					se_set(4)
				#上（下）
				if( GWK[_wk + cypos] < UP_OFFSET ):
					GWK[_wk + cypos] = UP_OFFSET
					GWK[_wk + cyspd] = GWK[_wk + cyspd] * (-1)
					se_set(4)

				#フレームアウトチェック
				elif( GWK[_wk + cypos] > ( SCREEN_HEIGHT + 0x10 ) ):
					GWK[_wk + ccond] = 0	#DEAD SET
					#se_set(29)

		else:
			_dead_count += 1

	#すべての玉がフレームアウト？
	if( _dead_count >= BALL_MAX):
		#ミス
		se_set(29)

		#ミス時アイテムは消しておく
		#アイテムワーク削除
		for _cnt in range( ITEM_MAX * CWORK_SIZE ):
			GWK[ITEM_WORK + _cnt] = 0

		#ゲームオーパドル判定
		if( GWK[rest_number] <= 0 ):
			if( GWK[testplay_switch] == 0 ):
				if( GWK[continue_switch] == 1 ):
					GWK[game_adv] = G_CONTINUE
				else:
					GWK[game_adv] = G_OVER

				GWK[game_subadv] = 0
				
			#面エディタのテストプレイ中？
			elif( ( GWK[testplay_switch] == 1 ) and ( GWK[game_adv] == G_EDITOR ) ):
				GWK[editor_subadv] = 3
			else:
				print("####[game_control] ERROR GWK[game_adv]:", GWK[game_adv])
		else:
			#残機-1
			GWK[rest_number] -= 1

			#パドル初期化
			paddle_init()
			#玉復帰セット
			ball_init()

#-----------------------------------------------------------------
#レーザーショット発生
#-----------------------------------------------------------------
def shot_appear():
	for _cnt in range( SHOT_MAX ):
		_wk = SHOT_WORK + ( CWORK_SIZE * _cnt )
		if( ( GWK[_wk + ccond] & F_LIVE ) == 0 ):
			GWK[_wk + ccond] = F_LIVE
			GWK[_wk + cid] = 0x0b
			GWK[_wk + cxpos] = GWK[PLY_WORK + cxpos] + 0x08
			GWK[_wk + cypos] = GWK[PLY_WORK + cypos] - 0x08
			GWK[_wk + cxspd] = 0
			GWK[_wk + cyspd] = -4
			se_set(19)
			break

#-----------------------------------------------------------------
#レーザーショット描画
#-----------------------------------------------------------------
def shot_draw():
	for _cnt in range( SHOT_MAX ):
		_wk = SHOT_WORK + ( CWORK_SIZE * _cnt )
		if( GWK[_wk + ccond] & F_LIVE ):
			cput( GWK[_wk + cxpos], GWK[_wk + cypos], GWK[_wk + cid] )

#-----------------------------------------------------------------
#ゲーム制御
#-----------------------------------------------------------------
def game_control():
	if( GWK[game_subadv] == 0 ):
		#ゲーム開始初期化
		start_init()
		GWK[game_subadv] = 1

		#マウスカーソル非表示
		pyxel.mouse( visible = False )
		
		GWK[demoplay_counter] = 0

	elif( GWK[game_subadv] == 2 ):
		#ゲーム再開初期化
		restart_init()
		GWK[game_subadv] = 1

		#マウスカーソル非表示
		pyxel.mouse( visible = False )

	#コンティニューからの再開
	elif( GWK[game_subadv] == 3 ):
		#スコア初期化
		GWK[score] = 0
		#残機初期化
		GWK[rest_number] = 2
		#パドル初期化
		paddle_init()
		#玉初期化
		ball_init()
		#マウスカーソル非表示
		pyxel.mouse( visible = False )
		GWK[game_subadv] = 1

	#テストプレイ初期化
	elif( GWK[game_subadv] == 4 ):

		#スコア初期化
		GWK[score] = 0
		#残機初期化
		GWK[rest_number] = 0		#１機のみ？

		#パドル初期化
		paddle_init()
		#玉初期化
		ball_init()
		
		#マウスカーソル非表示
		pyxel.mouse( visible = False )

		GWK[game_subadv] = 1

	elif( GWK[game_subadv] == 1 ):
		#ゲーム中

		#パドル制御（paddle_control()）
		if( GWK[game_adv] != G_DEMOPLAY ):
			GWK[PLY_WORK + cxpos] = pyxel.mouse_x - int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )
		else:
			GWK[PLY_WORK + cxpos] = GWK[BALL_WORK + cxpos] - int( ctbl[GWK[PLY_WORK + cid]][2] / 2 )

			GWK[demoplay_counter] += 1
			#デモプレイ中マウスクリックまたはタイマーでで抜ける
			if( ( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ) or
				( pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) ) or
				( GWK[demoplay_counter] > 1500 ) ):
				title_set()

		#パドル座標がマウス座標になっているので玉チェック前に枠内チェックが必要
		#パドル座標を枠内に収める
		if( GWK[PLY_WORK + cxpos] < (LEFT_OFFSET + GWK[blockmap_shortofs]) ):
			GWK[PLY_WORK + cxpos] = LEFT_OFFSET + GWK[blockmap_shortofs]
		elif( GWK[PLY_WORK + cxpos] > ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[PLY_WORK + cid]][2] ) ):
			GWK[PLY_WORK + cxpos] = ( SCREEN_WIDTH - GWK[blockmap_shortofs] - RIGHT_OFFSET - ctbl[GWK[PLY_WORK + cid]][2] )

		#パドルからショットON（レーザー取得時左クリックでレーザーショットON）
		if( GWK[PLY_WORK + cid] == 0x03 ):		#レーザーパドル
			#デモプレイ中はオート連射
			if( GWK[game_adv] == G_DEMOPLAY ):
				#オート連射カウンタ
				GWK[auto_counter] += 1
				if( GWK[auto_counter] > 5 ):
					GWK[auto_counter] = 0
					shot_appear()

			#マウス左クリックでショットON
			elif( pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) ):
				shot_appear()

		#玉制御
		ball_control()

		#ショットとブロックのヒットチェック
		shot_and_block_check()

		#アイテム制御
		item_control()

		#ブロックアニメーション（固いブロックキラリ）
		for _cnt in range( BLOCK_WORK_SIZE ):
			if( ( GWK[BLOCK_WORK + _cnt] & ( BF_LIVE + BF_ANIM ) ) == ( BF_LIVE + BF_ANIM ) ):
				if( ( GWK[BLOCK_WORK + _cnt] & 0x0f ) == 0x0b ):
					_acnt = GWK[BLOCK_WORK + _cnt] >> 12
					_acnt = _acnt - 1
					if( _acnt <= 0 ):
						#ANIMフラグクリア
						GWK[BLOCK_WORK + _cnt] &= ( 0x00ff - BF_ANIM )
					else:
						GWK[BLOCK_WORK + _cnt] &= 0x0fff
						GWK[BLOCK_WORK + _cnt] = GWK[BLOCK_WORK + _cnt] | ( _acnt << 12 )

#===============================================================================
#描画
#===============================================================================
def draw():
#-------
#	start = time.time()			# 現在時刻（処理開始前）を取得
#-------

	#画面クリア
	pyxel.cls(0)
	#設定
	if( GWK[game_adv] == G_SETTING ):
		setting_draw()
		return
	elif( GWK[game_adv] == G_EDITOR ):
		editor_draw()
		return


	#背景描画
	#横320
	if( GWK[stage_type] == 0 ):
		if( GWK[field_switch] == 1 ):
			pyxel.bltm(0, SCORE_HEIGHT, 0, 0+SCREEN_WIDTH * 1, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH, SCREEN_HEIGHT)

			for _dy in range(int((SCREEN_HEIGHT - UP_OFFSET)/0x20)):
				for _dx in range(int((SCREEN_WIDTH - ((LEFT_OFFSET + GWK[blockmap_shortofs]) * 2 ))/0x20)):
					dot_pattern_BG( ( _dx * 0x20 ) + LEFT_OFFSET + GWK[blockmap_shortofs], (_dy * 0x20 ) + UP_OFFSET, mbg_tbl )
		else:
			pyxel.bltm(0, SCORE_HEIGHT, 0, 0+SCREEN_WIDTH * 1, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH, SCREEN_HEIGHT)
	#横240
	else:
		if( GWK[field_switch] == 1 ):
			pyxel.bltm(40, SCORE_HEIGHT, 0, (SCREEN_WIDTH*2)+SCREEN_WIDTH2 * 1, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH2, SCREEN_HEIGHT)

			for _dy in range(int((SCREEN_HEIGHT - UP_OFFSET)/0x20)):
				for _dx in range(int((SCREEN_WIDTH - ((LEFT_OFFSET + GWK[blockmap_shortofs]) * 2 ))/0x20)):
					dot_pattern_BG( ( _dx * 0x20 ) + LEFT_OFFSET + GWK[blockmap_shortofs], ( _dy * 0x20 ) + UP_OFFSET, mbg_tbl )
			#X方向不足分追加
			_dx+=1
			for _dy in range(int((SCREEN_HEIGHT - UP_OFFSET)/0x20)):
				dot_pattern_BG2( ( _dx * 0x20 ) + LEFT_OFFSET + GWK[blockmap_shortofs], ( _dy * 0x20  ) + UP_OFFSET, mbg2_tbl )
		else:
			pyxel.bltm(40, SCORE_HEIGHT, 0, (SCREEN_WIDTH*2)+SCREEN_WIDTH2 * 1, (SCREEN_HEIGHT+0x10) * GWK[bg_type], SCREEN_WIDTH2, SCREEN_HEIGHT)


	#ブロックの表示
	stage_block()

	#ショット描画
	shot_draw()

	#アイテム描画
	item_draw()

	#タイトル
	if( GWK[game_adv] == G_TITLE ):
		#選択項目表示
		_selcol = 0
		if( GWK[title_select] == 0 ):
			_selcol = 1
		set_font_text( TITLE_START_X, TITLE_START_Y, 'START', 0, _selcol )

		_selcol = 0
		if( GWK[title_select] == 1 ):
			_selcol = 1
		set_font_text( TITLE_SETTING_X, TITLE_SETTING_Y, 'SETTING', 0, _selcol )

		_selcol = 0
		if( GWK[title_select] == 2 ):
			_selcol = 1
		set_font_text( TITLE_EXIT_X, TITLE_EXIT_Y, 'EXIT', 0, _selcol )

		#version表記
		set_font_text( 100, 0, 'VER.2024.10.03', 0 )

		#ハイスコア表記
		if( GWK[stage_type] == 0 ):
			if( GWK[highscore_0] > 0 ):
				set_font_text( int(SCREEN_WIDTH/2) - (9*8), 0x10, 'HIGH-SCORE  '+ str(GWK[highscore_0]), 0 )
		else:
			if( GWK[highscore_1] > 0 ):
				set_font_text( int(SCREEN_WIDTH2/2) - (9*8), 0x10, 'HIGH-SCORE  '+ str(GWK[highscore_1]), 0 )
	else:
		#パドル表示
		if( GWK[PLY_WORK+ccond] & F_LIVE ):
			cput( GWK[PLY_WORK+cxpos], GWK[PLY_WORK+cypos], GWK[PLY_WORK+cid] )
		#玉表示
		for _cnt in range(BALL_MAX):
			_wk = BALL_WORK + ( CWORK_SIZE * _cnt )
			if( GWK[_wk + ccond] & F_LIVE ):
				cput( GWK[_wk+cxpos], GWK[_wk+cypos], GWK[_wk+cid] )
		
		#rest表記
		cput( 48, 0, 0x26 )
		set_font_text( 64, 0, str(GWK[rest_number]), 0 )

		#stage表記
		set_font_text( 100, 0, 'STAGE ' + str(GWK[stage_type]+1) + "-" + str(GWK[stage_number]+1), 0 )
		#score表記
		set_font_text( 200, 0, 'SCORE ', 0 )
		set_font_text( 250, 0, str(GWK[score]), 0 )

		#ゲームオーバーなら表記
		if( GWK[game_adv] == G_OVER ):
			set_font_text( int(SCREEN_WIDTH/2) - int(10*8/2), 170, 'GAME  OVER', 0 )
		#ステージクリアなら表記
		elif( GWK[game_adv] == G_STAGECLEAR ):
			set_font_text( int(SCREEN_WIDTH/2) - int(12*8/2), 170, 'STAGE  CLEAR', 0 )
		#コンティニューなら表記
		elif( GWK[game_adv] == G_CONTINUE ):
			set_font_text( int(SCREEN_WIDTH/2) - int(8*8/2), 170, 'CONTINUE', 0 )
			set_font_text( int(SCREEN_WIDTH/2) - int(8*8/2), 180, 'YES / NO', 0 )

#-------
#	end = time.time()			# 現在時刻（処理完了後）を取得
#	time_diff = end - start		# 処理完了後の時刻から処理開始前の時刻を減算する
#	print(time_diff)			# 処理にかかった時間データを使用
#-------
#===============================================================================
#INIT&RUN
#===============================================================================
#pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60)
#[use Web]ESCキーを無効化
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60, quit_key=pyxel.KEY_NONE, title='pyxelblk')

#リソース読み込み（マルチカラー有り）
pyxel.load("pyxelblk.pyxres")
#ワーククリア
work_clear()
#初期値セット
work_init()
#Goto タイトル
title_set()

#実行
pyxel.run(update, draw)
