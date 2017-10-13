#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Name: const.py
# Purpose:
#
# Author: 张歆韵(sean.Zhang)
#
# Created: 16-6-13 下午1:30

STATUS_STR = "status"

FUN_VER = "ver"

REDIS_PERMANENT = 86400  # 在redis中无过期时间(24小时)

SYS_RUN = 1
SYS_STOP = 2

SUSSES = 200

HTTP_CODE_OK = 200
HTTP_CODE_UNAVAILABLE = 503
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_NO_AUTH = 401

EXCEPTION_CODE = 100
STATUS_TIMEOUT = 110
STATUS_PAGE_VIEW = 10000

# http://gitlab.vxia.com.cn/system/share_docs/wikis/user_special
SYS_NOTICE_USER_ID = 100  # 系统提醒
SYS_INVITE_USER_ID = 200  # 好友邀请
SYS_TODAY_USER_ID = 300   # 今日提醒
SYS_CUSTOM_USER_ID = 400  # 微侠小二

USER_FRIEND = 1  # 好友
USER_BLACK = 3  # 黑名单

COMP_NORMAL = 1000  # 普通
COMP_VIP = 2000  # 实名认证

COMP_TYPE_GROUP = 0  # 群组
COMP_TYPE_COMP = 1  # 公司

ACCOUNT_FREEZE = 0
ACCOUNT_UNFREEZE = 1

IS_DEL_FLAG = "isdel"
SYNC_HASH = "md5_sha"

LOGIN_INNER = "in"  # 本系统证号登录
LOGIN_WECHAR = "wechat"  # 微信登陆
LOGIN_QQ = "qzone"  # qq登陆

EASYMOB_PRE = "hx"  # 环信前缀
EASYMOB_ORG = "weixia"  # 环信org
EASYMOB_APP = "vxia"  # 环信app

DOC_TYPE_WORD = "word"
DOC_TYPE_EXCEL = "excel"
DOC_TYPE_PPT = "ppt"
DOC_TYPE_PDF = "pdf"
DOC_TYPE_IMG = "img"

FAV_TYPE_FILE = "FILE"
FAV_TYPE_TXT = "TXT"
FAV_TYPE_IMAGE = "IMAGE"

MAP_HAS_KEY = 1  # map或doc中有指定的字段
MAP_HAS_KEY_AND_VAL = 2  # map或doc中有指定的字段并且字段值不为空

READ_SLAVE = True  # mongodb读写分离

READ_TYPE = "read_type"  # 读方式
READ_TYPE_PRIMARY = "PRIMARY"  # 主读READ_TYPE_SLAVE
READ_TYPE_SLAVE = "SLAVE"  # 从读

USER_INFO_ALL = "all"  # all: 所有信息
USER_INFO_ALL_PRI = "allpri"  # all: 所有主帐号信息
USER_INFO_ALL_CHILD = "allchi"  # all: 所有子帐号信息
USER_INFO_ALL_BY_PID = "allbypid"  # allbypid: 根据主帐号查询所有帐号信息
USER_INFO_BY_ID = "userbyid"  # pribypid: 根据主帐号id查询信息
USER_INFO_PRI_FOE_CHO = "priforcho"  # priforcho用户下拉菜单的主账户信息
USER_INFO_GRADE = "grade" #根据评级查询用户信息
USER_INFO_FQ = "fq"  # 后台过滤查询
USER_INFO_POINT = "point"  # 根据经纬度查询周边商户
USER_INFO_GOLD = "gold"  # 元宝/积分/金币
USER_INFO_ALL_GOLD = "allgold"  # all + gold
USER_INFO_STRANGER = "stranger"  # 陌生人
USER_INFO_SET = "setting"  # 设置页面,只抓取"微侠号/手机/邮箱"
USER_INFO_FRIEND = "friend"  # 加载好友信息,用于填充本地数据库,必须提供好友的userid
USER_INFO_ADDFRI = "addfri"  # 加微侠号为好友的时候用，不是好友显示简化信息，是好友显示全部信息，有一个isfri标志
USER_INFO_CHI_BY_ID = "chibyid"


PARK_INFO_ALL = "all"  # all: 所有园区信息
PARK_DISTRICT = "district"  # district: 所有园区所在区
PARK_TYPE = "pro_type"
PARK_AREA = "bel_ar"
PARK_TYPE_DICT = {"e": "易园", "we": "WE", "loft": "运动loft", "other": "其他"}
PARK_AREA_DICT = {"S": "南大区", "N": "北大区", "M": "中大区", "WE": "WE大区"}


USER_ROLE_C = "c"  # C类用户
USER_ROLE_B = "b"  # B类用户
USER_ROLE_S = "s"  # S类用户
USER_ROLE_M = "m"  # M类用户

USER_C_TO_B = "c_to_b"
USER_B_TO_C = "b_to_c"

CONCERN = 1  # 关注
BE_CONCERN = 2  # 被关注
MUTUAL_CONCERN = 3  #互相关注

MOBILE_NEW = "new"  # 绑定新手机
MOBILE_MOD = "mod"  # 修改绑定手机


C_BIND_B = "bind"  # c绑定b
C_UNBIND_B = "unbind"  # c解绑b
C_LEAVE_B = "leave"  # c离开b

FREEZE = "freeze"  # 绑定新手机
UNFREEZE = "unfreeze"  # 修改绑定手机

GROUP_JOIN = "join"  # 邀请加入群组
GROUP_SELF_JOIN = "self_join"  # 主动加入群组
GROUP_DEL = "del"  # 群组踢人
GROUP_EXIT = "exit"  # 退出群组
GROUP_CHG_ADMIN = "chg_admin"  # 转移群主
GROUP_CHG_AIDE = "chg_aide"  # 调整副群主

GROUP_ADMIN = "admin"  # 群主
GROUP_AIDE = "aide"  # 副群主
GROUP_IN = "in"  # 普通群众
GROUP_OUT = "out"  # 不是群成员

GROUP_NORMAL = 1  # 正常群组
GROUP_DISMISS = 2  # 被解散群组

GROUP_IMG_SYS = 1  # 系统自动生成
GROUP_IMG_USER = 2  # 用户上传(上传后就不能自动调整了)

SCH_POW_NONE = 1  # 不让TA查看我的日程安排
SCH_POW_ONLY_TIME = 2  # 只可以查看我日程的时间段
SCH_POW_DETAIL = 3  # 可以查看我的日程明细

USER_LOGO = 'user_logo'
GROUP_LOGO = 'grp_logo'
GROUP_LOGO_SYS = 'grp_logo_sys'
TABLE_IMG = 'table_img'
TABLE_VOICE = 'table_voice'

CHAT_DOC_UPLOAD = "chat_doc_upload"
FEEDBACK_IMG = 'feedback'
EMP_STAR_LIST = ["", "水瓶", "双鱼", "白羊", "金牛", "双子", "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯"]

S_SERVER_MERCH = 1  # "普通商家"
S_SERVER_COMMUNITY_CENTER = 2  # "社区中心"
S_ROLE_DICT = {1: "停车场", 2: "餐饮", 3: "工位", 4: "会议室"}  # s用户权限枚举
S_SERV_DICT = {1: "停车场", 2: "餐饮", 3: "工位", 4: "会议室"}  # s用户服务枚举
ROLE_B_DICT = {1: "HR", 2: "财务", 3: "商务", 4: "法务"}  # b用户权限组枚举
ROLE_M_DICT = {0: "总M", 1: "开发者", 2: "商务", 3: "运营", 4: "财务", 5: "数据", 6: "平台管理"}  # M用户权限组枚举
ROLE_W_DICT = {1: "C用户管理", 2: "论坛管理", 3: "广告配置", 4: "活动配置", 5: "公告管理"}  # W用户权限组枚举
PROJECT_DICT = {1: "易园系列", 2: "WE系列", 3: "LOFT系列"}

MAIN_FIELD_NAME_LST = [
        'con_po2',
        'pro_name',
        'sel_type',
        'f_imglst',
        'con2',
        'now_addr',
        'com_tel',
        'com_not',
        's_time',
        'con_id',
        'email2',
        'special',
        's_grade',
        'loc',
        'pro_type',
        'img',
        'contacts',
        'now_dis',
        'serv_lst',
        'con_po',
        'email',
        'province',
        're_sign',
        'e_time',
        'i_imglst',
        'park',
        'con_mob2',
        'park_id',
        'slogan',
        'com_addr',
        'con_id2',
        'con_mob',
        'com_desc',
        'url',
        'country',
        'vip',
        'op_time',
        'com_name']

PROFESSION_DICT = {
    "guanggao": u"广告",
    "xinwen": u"新闻和出版业",
    "jiaoyu": u"教育",
    "guangbo": u"广播、电视、电影和影视录音制作业",
    "wenhua": u"文化艺术",
    "tiyu": u"体育娱乐",
    "ruanjian": u"软件和信息技术服务",
    "hulianwang": u"互联网信息及相关服务",
    "qiyeguanli": u"企业管理服务",
    "falv": u"法律服务",
    "zixun": u"咨询与调查",
    "zhishichanquan": u"知识产权服务",
    "renli": u"人力资源服务",
    "lvxingshe": u"旅行社及相关服务",
    "shangwu": u"其他商务服务业",
    "canyin": u"餐饮",
    "jianzhu": u"建筑",
    "huobi": u"货币金融服务",
    "zibenshichang": u"资本市场服务",
    "fangdichan": u"房地产",
    "shipinyinliao": u"食品、饮料及烟草制品批发及零售",
    "fangzhi": u"纺织、服装及家庭用品批发及零售",
    "wenhuatiyu": u"文化、体育用品器材批发及零售",
    "zonghelingshou": u"综合零售",
    "zhizaoye": u"制造业",
    "jinkou": u"进口食品贸易",
    "shinei": u"室内设计",
    "qita": u"其他"
}


S_ORDER_DETAIL = 's_paymentdetail'
S_ORDER = 's_order'
S_ID = 's_id'

PWD = "pwd"
ACCOUNT = "account"

IOS = "ios"
ANDROID = "android"

PUSH_HOST = 'http://sdk.open.api.igexin.com/apiex.htm'


PUSH_IOS_CFG = {
                'APPID': 'lKTTVfsiZn84fhep7yPVp4',  # APPID由IGetui管理页面生成，是您的应用与SDK通信的标识之一，每个应用都对应一个唯一的AppID。
                'APPKEY': 'XMoKymuRTD6DDMmSL6ehs7',  # APPKEY预先分配的第三方应用对应的Key，是您的应用与SDK通信的标识之一。
                'MASTERSECRET': '3xGilvYG5o7LEqDipLWO94'  # MASTERSECRET个推服务端API鉴权码，用于验证调用方合法性。在调用个推服务端API时需要提供。（请妥善保管，避免通道被盗用）
                }

PUSH_ANDROID_CFG = {
                    'APPID': 'yL81k94ilp96EmI26YKut9',
                    'APPKEY': 'jusMVeIC3ZA3ZejSP5fCm3',
                    'MASTERSECRET': '4RXGrNgE797dW8EGYhHbJ4'
                    }

VIP_LV_LIST = [
    50,
    81,
    131,
    212,
    343,
    554,
    897,
    1452,
    2349,
    3800,
    6148,
    9948,
    16096,
    26043,
    42138,
    68179,
    110313,
    178486,
    288791,
    467263,
    756032,
    1223260,
    1979235,
    3202402,
    5181487,
    8383646,
    13564739,
    21947748,
    35511457,
    57457537,
    92966295,
]

RIAKCS_BUCKET = 'imgs'
MEM_KEY = 'mem_key'

CHAT_FOR_PROJECT = "project"

VIEW_POWER_WORKREPORT = "wr"
VIEW_POWER_SCH = "sch"

CHAT_TYPE_ISFILE = ['img', 'file']
CHAT_TYPE_PRAISE = 'ok'  # 点赞信息

ES_DOC = 'es_doc'
ES_QRY_NO_FIELDS = 0
ES_QRY_WITH_FIELDS = 1

WE_ROOT = "m_root"
VX_ADMIN = "vx_admin"   # 系统管理员
VX_DEV = "vx_dev"       # 开发人员
VX_KF = "vx_kf"         # 客服

PWD_RANGE = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ0123456789"  # 密码随机范围,英文+数字,去除了i,I,l,L,o,O

SSL_KEY_PRI = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCsEYbQWL1q74DS5EIZ2/56xLn/BX2pBN25W5CsYaUlTpYPbbFT
7Q9w9ed0rgQm1S8E8+Hg5sq1rkkte9pREdjtmGm9ARoqUEL8B1CrvXLfIHQIN/8S
Q6pxnT9nsl3wYcOJL+NtuJRn1kN+CzTgkU3pAvWTitTDUIhCxKJO7fBizQIDAQAB
AoGAHKxbA9MV1YENvZbt8PM5B+pKeFXI5+Z4sE+y3xbydzIOTYng9/RUE2XW6Rmq
dXInALNHW7v54aamaR7vdXz84ezvMsLapp5mdP/RLWhSwUbu1HzO+S2XBKYzp7Za
jORtT8pIjCcMJe19HjmlC3XAPs0INJdw6TTT/i9wotokhd0CQQDcv8I+7pLVfm58
uxfwfav9ZHZ5kck7T5d7M9gaO11Ebj3ot6LxBMfZaTEsn28+OOarRBE6dCDkvSkv
BluW37b3AkEAx4uzZxGPoCePAv84lGQD3RYxetXhMutWV5PTbrthm4j//qjvDWiM
nEZAzYkoN3OyuutY1ODLivcfOTtp0QUvWwJBAJ0daq6J9T4414C1VQuZFrGqMFzE
c3pgYsuQkc3R1Mcgw7WABlwO8AMAyLwe2flqXFsnfi+hecv0CnzqxIN0xO8CQQCs
SSn0a20eUglgBQvM0y2izW6bJ97wH9DEfJWonZCAwaCFN0ZuxT3iD6YTz8AxYGuI
h3qDEjOrIAKNX4bVOSzRAkA9+VSkVhFac/Oh68VAY//DkxHvKId0/pZqEhB/J4of
avfnCIspWjKdkKOWq3pY32F61+c/K0EgX0rVRqJcAMlt
-----END RSA PRIVATE KEY-----
'''
SSL_KEY_PUB = '''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsEYbQWL1q74DS5EIZ2/56xLn/
BX2pBN25W5CsYaUlTpYPbbFT7Q9w9ed0rgQm1S8E8+Hg5sq1rkkte9pREdjtmGm9
ARoqUEL8B1CrvXLfIHQIN/8SQ6pxnT9nsl3wYcOJL+NtuJRn1kN+CzTgkU3pAvWT
itTDUIhCxKJO7fBizQIDAQAB
-----END PUBLIC KEY-----
'''


