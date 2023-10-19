from basic import cal_utils


class Planet:

    def __init__(self, i: str, cn: str, ocr_str: str = None):
        self.id: str = i  # id 用在找文件夹之类的
        self.cn: str = cn  # 中文
        self.ocr_str: str = ocr_str if ocr_str is not None else cn # 用于ocr

    def __str__(self):
        return '%s - %s' % (self.cn, self.id)


P01_KZJ = Planet("kjzht", "空间站黑塔", ocr_str='空间站')
P02_YYL = Planet("yll6", "雅利洛", ocr_str='雅利洛')
P03_XZLF = Planet("zxlf", "罗浮仙舟", ocr_str='罗浮')

PLANET_LIST = [P01_KZJ, P02_YYL, P03_XZLF]


def get_planet_by_cn(cn: str) -> Planet:
    """
    根据星球的中文 获取对应常量
    :param cn: 星球中文
    :return: 常量
    """
    for i in PLANET_LIST:
        if i.cn == cn:
            return i
    return None


class Region:

    def __init__(self, i: str, cn: str, planet: Planet, level: int = 0):
        self.id: str = i  # id 用在找文件夹之类的
        self.cn: str = cn  # 中文 用在OCR
        self.planet: Planet = planet
        self.level: int = level

    def __str__(self):
        return '%s - %s' % (self.cn, self.id)

    def get_pr_id(self):
        return '%s-%s' % (self.planet.id, self.id)

    def get_level_str(self):
        """
        层数 正数用 l1 负数用 b1
        :return:
        """
        if self.level == 0:
            return ''
        elif self.level > 0:
            return '-l%d' % self.level
        elif self.level < 0:
            return 'b%d' % abs(self.level)

    def get_rl_id(self):
        """
        :return 区域id + 楼层id 用于文件夹
        """
        if self.level == 0:
            return '%s' % self.id
        elif self.level > 0:
            return '%s-l%d' % (self.id, self.level)
        elif self.level < 0:
            return '%s-b%d' % (self.id, abs(self.level))

    def get_prl_id(self):
        """
        :return 星球id + 区域id + 楼层id 用于文件夹
        """
        if self.level == 0:
            return '%s-%s' % (self.planet.id, self.id)
        elif self.level > 0:
            return '%s-%s-l%d' % (self.planet.id, self.id, self.level)
        elif self.level < 0:
            return '%s-%s-b%d' % (self.planet.id, self.id, abs(self.level))

    def another_floor(self):
        return self.level != 0


R0_GJCX = Region("gjcx", "观景车厢", None)

P01_R01_ZKCD = Region("zkcd", "主控舱段", P01_KZJ)
P01_R02_JZCD = Region("jzcd", "基座舱段", P01_KZJ)
P01_R03_SRCD_B1 = Region("srcd", "收容舱段", P01_KZJ, -1)
P01_R03_SRCD_L1 = Region("srcd", "收容舱段", P01_KZJ, 1)
P01_R03_SRCD_L2 = Region("srcd", "收容舱段", P01_KZJ, 2)
P01_R04_ZYCD_L1 = Region("zycd", "支援舱段", P01_KZJ, 1)
P01_R04_ZYCD_L2 = Region("zycd", "支援舱段", P01_KZJ, 2)

P02_R01_L1 = Region("xzq", "行政区", P02_YYL, level=1)
P02_R01_B1 = Region("xzq", "行政区", P02_YYL, level=-1)
P02_R02 = Region("cjxy", "城郊雪原", P02_YYL)
P02_R03 = Region("bytl", "边缘通路", P02_YYL)
P02_R04 = Region("twjq", "铁卫禁区", P02_YYL)
P02_R05 = Region("cxhl", "残响回廊", P02_YYL)
P02_R06 = Region("ydl", "永冬岭", P02_YYL)
P02_R07 = Region("zwzz", "造物之柱", P02_YYL)
P02_R08_L2 = Region("jwqsyc", "旧武器试验场", P02_YYL, level=2)
P02_R09 = Region("pyz", "磐岩镇", P02_YYL)
P02_R10 = Region("dkq", "大矿区", P02_YYL)
P02_R11_L1 = Region("mdz", "铆钉镇", P02_YYL, level=1)
P02_R11_L2 = Region("mdz", "铆钉镇", P02_YYL, level=2)
P02_R12_L1 = Region("jxjl", "机械聚落", P02_YYL, level=1)
P02_R12_L2 = Region("jxjl", "机械聚落", P02_YYL, level=2)

PLANET_2_REGION = {
    P01_KZJ.id: [P01_R01_ZKCD, P01_R02_JZCD, P01_R03_SRCD_L1, P01_R03_SRCD_L2, P01_R03_SRCD_B1, P01_R04_ZYCD_L1, P01_R04_ZYCD_L2],
    P02_YYL.id: [P02_R01_L1, P02_R01_B1, P02_R02, P02_R03, P02_R04, P02_R05, P02_R06, P02_R07, P02_R08_L2, P02_R09, P02_R10,
                 P02_R11_L1, P02_R11_L2, P02_R12_L1, P02_R12_L2],
    P03_XZLF.id: []
}


def get_region_by_cn(cn: str, planet: Planet, level: int = 0) -> Region:
    """
    根据区域的中文 获取对应常量
    :param cn: 区域的中文
    :param planet: 所属星球 传入后会判断 为以后可能重名准备
    :param level: 层数
    :return: 常量
    """
    for i in PLANET_2_REGION[planet.id]:
        if i.cn != cn:
            continue
        if level is not None and i.level != level:
            continue
        return i
    return None


class TransportPoint:

    def __init__(self, id: str, cn: str, region: Region, template_id: str, lm_pos: tuple, ocr_str: str = None):
        self.id: str = id  # 英文 用在找图
        self.cn: str = cn  # 中文 用在OCR
        self.region: Region = region  # 所属区域
        self.planet: Planet = region.planet  # 所属星球
        self.template_id: str = template_id  # 匹配模板
        self.lm_pos: tuple = lm_pos  # 在大地图的坐标
        self.ocr_str: str = cn if ocr_str is None else ocr_str

    def __str__(self):
        return '%s - %s' % (self.cn, self.id)


P01_R01_SP01 = TransportPoint('', '', P01_R01_ZKCD, 'mm_tp_03', (529, 231))
P01_R01_SP02 = TransportPoint('', '', P01_R01_ZKCD, 'mm_tp_03', (592, 691))
P01_R01_SP03_HTBGS = TransportPoint('htdbgs', '办公室', P01_R01_ZKCD, 'mm_tp_04', (245, 796))
P01_R01_SP04 = TransportPoint('', '', P01_R01_ZKCD, 'mm_sp_01', (228, 744))
P01_R01_SP05 = TransportPoint('', '', P01_R01_ZKCD, 'mm_sp_02', (562, 837))
P01_R01_SP06 = TransportPoint('', '', P01_R01_ZKCD, 'mm_sp_04', (535, 628))

P01_R02_SP01_JKS = TransportPoint('jks', '监控室', P01_R02_JZCD, 'mm_tp_03', (635, 143))
P01_R02_SP02 = TransportPoint('', '', P01_R02_JZCD, 'mm_tp_03', (493, 500))
P01_R02_SP03 = TransportPoint('', '', P01_R02_JZCD, 'mm_tp_06', (540, 938))
P01_R02_SP04 = TransportPoint('', '', P01_R02_JZCD, 'mm_tp_06', (556, 986))

# 空间站黑塔 - 收容舱段
P01_R03_SP01_KZZXW = TransportPoint('kzzxw', '控制中心外', P01_R03_SRCD_L1, 'mm_tp_03', (365, 360))
P01_R03_SP02 = TransportPoint('zt', '中庭', P01_R03_SRCD_L1, 'mm_tp_03', (619, 331))
P01_R03_SP03 = TransportPoint('', '', P01_R03_SRCD_L2, 'mm_tp_03', (758, 424))
P01_R03_SP04 = TransportPoint('', '', P01_R03_SRCD_L2, 'mm_tp_03', (1033, 495))
P01_R03_SP05_HMZL = TransportPoint('hmzl', '毁灭之蕾', P01_R03_SRCD_L1, 'mm_tp_07', (309, 310))
P01_R03_SP06 = TransportPoint('', '', P01_R03_SRCD_L1, 'mm_tp_09', (840, 352))
P01_R03_SP07 = TransportPoint('', '', P01_R03_SRCD_L1, 'mm_sp_02', (600, 349))

# 空间站黑塔 - 支援舱段
P01_R04_SP01 = TransportPoint('dls', '电力室', P01_R04_ZYCD_L2, 'mm_tp_03', (155, 380))
P01_R04_SP02 = TransportPoint('bjkf', '备件库房', P01_R04_ZYCD_L2, 'mm_tp_03', (424, 206))
P01_R04_SP03 = TransportPoint('yt', '月台', P01_R04_ZYCD_L2, 'mm_tp_03', (778, 370))
P01_R04_SP04 = TransportPoint('chzl', '存护之蕾', P01_R04_ZYCD_L2, 'mm_tp_07', (457, 288), ocr_str='存护')
P01_R04_SP05 = TransportPoint('tkdt', '太空电梯', P01_R04_ZYCD_L2, 'mm_sp_02', (105, 345))

# 雅利洛 - 行政区
P02_R01_SP01 = TransportPoint('hjgjy', '黄金歌剧院', P02_R01_L1, 'mm_tp_03', (603, 374))
P02_R01_SP02 = TransportPoint('zygc', '中央广场', P02_R01_L1, 'mm_tp_03', (487, 806))
P02_R01_SP03 = TransportPoint('gdbg', '歌德宾馆', P02_R01_L1, 'mm_tp_03', (784, 1173))
P02_R01_SP04 = TransportPoint('lswhbwg', '历史文化博物馆', P02_R01_L1, 'mm_tp_05', (395, 771))
P02_R01_SP05 = TransportPoint('cjxy', '城郊雪原', P02_R01_L1, 'mm_sp_02', (485, 370))
P02_R01_SP06 = TransportPoint('bytl', '边缘通路', P02_R01_L1, 'mm_sp_02', (508, 1113))
P02_R01_SP07 = TransportPoint('twjq', '铁卫禁区', P02_R01_L1, 'mm_sp_02', (792, 1259))
P02_R01_SP08 = TransportPoint('shj-s', '售货机-上', P02_R01_L1, 'mm_sp_03', (672, 521), ocr_str='售货机')
P02_R01_SP09 = TransportPoint('ss', '书商', P02_R01_L1, 'mm_sp_03', (641, 705))
P02_R01_SP10 = TransportPoint('mbr', '卖报人', P02_R01_L1, 'mm_sp_03', (610, 806))
P02_R01_SP11 = TransportPoint('xzqsd', '行政区商店', P02_R01_L1, 'mm_sp_03', (639, 906))
P02_R01_SP12 = TransportPoint('shj-x', '售货机-下', P02_R01_L1, 'mm_sp_03', (697, 1187), ocr_str='售货机')
P02_R01_SP13 = TransportPoint('hd-cx', '花店-长夏', P02_R01_L1, 'mm_sp_05', (602, 588), ocr_str='花店')
P02_R01_SP14 = TransportPoint('klbb-s', '克里珀堡-上', P02_R01_L1, 'mm_sp_05', (769, 732), ocr_str='克里珀堡')
P02_R01_SP15 = TransportPoint('klbb-x', '克里珀堡-下', P02_R01_L1, 'mm_sp_05', (769, 878), ocr_str='克里珀堡')
P02_R01_SP16 = TransportPoint('jxw-yd', '机械屋-永动', P02_R01_L1, 'mm_sp_05', (727, 918))
P02_R01_SP17 = TransportPoint('gdbg-rk', '歌德宾馆-入口', P02_R01_L1, 'mm_sp_05', (627, 1152), ocr_str='歌德宾馆')
P02_R01_SP18 = TransportPoint('pyz', '磐岩镇', P02_R01_B1, 'mm_sp_02', (641, 778))
P02_R01_SP19 = TransportPoint('shj-d', '售货机-底', P02_R01_B1, 'mm_sp_03', (516, 864), ocr_str='售货机')

# 雅利洛 - 城郊雪原
P02_R02_SP01 = TransportPoint('cp', '长坡', P02_R02, 'mm_tp_03', (1035, 319))
P02_R02_SP02 = TransportPoint('zld', '着陆点', P02_R02, 'mm_tp_03', (1283, 367))
P02_R02_SP03 = TransportPoint('xlzl', '巡猎之蕾', P02_R02, 'mm_tp_07', (946, 244))
P02_R02_SP04 = TransportPoint('hyzl', '回忆之蕾', P02_R02, 'mm_tp_08', (1098, 391))
P02_R02_SP05 = TransportPoint('xzq', '行政区', P02_R02, 'mm_sp_02', (444, 109))
P02_R02_SP06 = TransportPoint('lk', '玲可', P02_R02, 'mm_sp_03', (1032, 342))

# 雅利洛 - 边缘通路
P02_R03_SP01 = TransportPoint('hcgc', '候车广场', P02_R03, 'mm_tp_03', (598, 832))
P02_R03_SP02 = TransportPoint('xxgc', '休闲广场', P02_R03, 'mm_tp_03', (690, 480))
P02_R03_SP03 = TransportPoint('gdjz', '歌德旧宅', P02_R03, 'mm_tp_03', (811, 259), ocr_str='歌德')
P02_R03_SP04 = TransportPoint('hgzx', '幻光之形', P02_R03, 'mm_tp_06', (450, 840))
P02_R03_SP05 = TransportPoint('frzl', '丰饶之蕾', P02_R03, 'mm_tp_07', (659, 509))
P02_R03_SP06 = TransportPoint('ytzl', '以太之蕾', P02_R03, 'mm_tp_08', (596, 194))

# 雅利洛 - 铁卫禁区
P02_R04_SP01 = TransportPoint('jqgs', '禁区岗哨', P02_R04, 'mm_tp_03', (1162, 576))
P02_R04_SP02 = TransportPoint('jqqx', '禁区前线', P02_R04, 'mm_tp_03', (538, 596))
P02_R04_SP03 = TransportPoint('nysn', '能源枢纽', P02_R04, 'mm_tp_03', (750, 1102))
P02_R04_SP04 = TransportPoint('yhzx', '炎华之形', P02_R04, 'mm_tp_06', (463, 442))
P02_R04_SP05 = TransportPoint('xqzj', '迅拳之径', P02_R04, 'mm_tp_09', (1143, 624))
P02_R04_SP06 = TransportPoint('yyhy', '以眼还眼', P02_R04, 'mm_sp_01', (438, 578))
P02_R04_SP07 = TransportPoint('dbjxq', '冬兵进行曲', P02_R04, 'mm_sp_01', (723, 1073))
P02_R04_SP08 = TransportPoint('cxhl', '残响回廊', P02_R04, 'mm_sp_02', (314, 589))

# 雅利洛 - 残响回廊
P02_R05_SP01 = TransportPoint('zcly', '筑城领域', P02_R05, 'mm_tp_03', (770, 442))
P02_R05_SP02 = TransportPoint('wrgc', '污染广场', P02_R05, 'mm_tp_03', (381, 655))
P02_R05_SP03 = TransportPoint('zzzhs', '作战指挥室', P02_R05, 'mm_tp_03', (495, 856))
P02_R05_SP04 = TransportPoint('gzcqx', '古战场前线', P02_R05, 'mm_tp_03', (570, 1243))
P02_R05_SP05 = TransportPoint('mlzx', '鸣雷之形', P02_R05, 'mm_tp_06', (526, 640))
P02_R05_SP06 = TransportPoint('sjzx', '霜晶之形', P02_R05, 'mm_tp_06', (681, 1231))
P02_R05_SP07 = TransportPoint('pbzj', '漂泊之径', P02_R05, 'mm_tp_09', (654, 242))
P02_R05_SP08 = TransportPoint('twjq', '铁卫禁区', P02_R05, 'mm_sp02', (389, 626))
P02_R05_SP09 = TransportPoint('ydl', '永冬岭', P02_R05, 'mm_sp02', (733, 1280))  # 这里旁边站着一个传送到造物之柱的士兵

# 雅利洛 - 永冬岭
P02_R06_SP01 = TransportPoint('gzc', '古战场', P02_R06, 'mm_tp_03', (366, 776))
P02_R06_SP02 = TransportPoint('zwpt', '造物平台', P02_R06, 'mm_tp_03', (784, 571))
P02_R06_SP03 = TransportPoint('rzzj', '睿治之径', P02_R06, 'mm_tp_09', (585, 663))
P02_R06_SP04 = TransportPoint('cxhl', '残响回廊', P02_R06, 'mm_sp_02', (338, 793))

# 雅利洛 - 造物之柱
P02_R07_SP01 = TransportPoint('zwzz-rk', '造物之柱-入口', P02_R07, 'mm_tp_03', (382, 426), ocr_str='入口')
P02_R07_SP02 = TransportPoint('zwzz-sgc', '造物之柱-施工场', P02_R07, 'mm_tp_03', (660, 616), ocr_str='施工场')
P02_R07_SP03 = TransportPoint('cxhl', '残响回廊', P02_R07, 'mm_sp_02', (313, 346))

# 雅利洛 - 旧武器试验场 # TODO 漏了一个 以太战线终端 的图标
P02_R08_SP01 = TransportPoint('jsqdzx', '决胜庆典中心', P02_R08_L2, 'mm_tp_03', (583, 836))
P02_R08_SP02 = TransportPoint('mdz', '铆钉镇', P02_R08_L2, 'mm_sp_02', (591, 1032))

# 雅利洛 - 磐岩镇
P02_R09_SP01 = TransportPoint('gddfd', '歌德大饭店', P02_R09, 'mm_tp_03', (614, 236))
P02_R09_SP02 = TransportPoint('bjjlb', '搏击俱乐部', P02_R09, 'mm_tp_03', (419, 251))
P02_R09_SP03 = TransportPoint('ntsdzs', '娜塔莎的诊所', P02_R09, 'mm_tp_03', (416, 417))
P02_R09_SP04 = TransportPoint('pyzcjls', '磐岩镇超级联赛', P02_R09, 'mm_tp_10', (358, 262))
P02_R09_SP05 = TransportPoint('', '', P02_R09, 'mm_sp_02', (630, 114))
P02_R09_SP06 = TransportPoint('', '', P02_R09, 'mm_sp_02', (453, 595))
P02_R09_SP07 = TransportPoint('', '', P02_R09, 'mm_sp_03', (707, 458))
P02_R09_SP08 = TransportPoint('', '', P02_R09, 'mm_sp_04', (632, 306))
P02_R09_SP09 = TransportPoint('', '', P02_R09, 'mm_sp_04', (706, 458))
P02_R09_SP10 = TransportPoint('', '', P02_R09, 'mm_sp_05', (688, 222))
P02_R09_SP11 = TransportPoint('', '', P02_R09, 'mm_sp_05', (393, 475))


# 雅利洛 - 大矿区
P02_R10_SP01 = TransportPoint('rk', '入口', P02_R10, 'mm_tp_03', (333, 166))
P02_R10_SP02 = TransportPoint('llzbns', '流浪者避难所', P02_R10, 'mm_tp_03', (778, 349))
P02_R10_SP03 = TransportPoint('fkd', '俯瞰点', P02_R10, 'mm_tp_03', (565, 641))
P02_R10_SP04 = TransportPoint('zkd', '主矿道', P02_R10, 'mm_tp_03', (530, 757))
P02_R10_SP05 = TransportPoint('fmzx', '锋芒之形', P02_R10, 'mm_tp_06', (561, 536))
P02_R10_SP06 = TransportPoint('fzzx', '燔灼之形', P02_R10, 'mm_tp_06', (836, 630))
P02_R10_SP07 = TransportPoint('xwzl', '虚无之蕾', P02_R10, 'mm_tp_07', (295, 243))
P02_R10_SP08 = TransportPoint('czzl', '藏珍之蕾', P02_R10, 'mm_tp_08', (554, 686))
P02_R10_SP09 = TransportPoint('pyz', '磐岩镇', P02_R10, 'mm_sp_02', (351, 144))


# 雅利洛 - 铆钉镇 TODO 判断层数
P02_R11_SP01 = TransportPoint('', '', P02_R11_L1, 'mm_tp_03', (600, 134))
P02_R11_SP02 = TransportPoint('', '', P02_R11_L1, 'mm_tp_03', (465, 297))
P02_R11_SP03 = TransportPoint('', '', P02_R11_L1, 'mm_tp_03', (613, 598))
P02_R11_SP04 = TransportPoint('', '', P02_R11_L1, 'mm_tp_06', (580, 297))
P02_R11_SP05 = TransportPoint('', '', P02_R11_L1, 'mm_tp_07', (609, 531))
P02_R11_SP06 = TransportPoint('', '', P02_R11_L1, 'mm_sp_02', (767, 167))
P02_R11_SP07 = TransportPoint('', '', P02_R11_L1, 'mm_sp_02', (597, 621))


# 雅利洛 - 机械聚落 TODO 判断层数
P02_R12_SP01 = TransportPoint('', '', P02_R12_L1, 'mm_tp_03', (556, 174))
P02_R12_SP02 = TransportPoint('', '', P02_R12_L1, 'mm_tp_03', (554, 506))
P02_R12_SP03 = TransportPoint('', '', P02_R12_L1, 'mm_tp_03', (413, 527))
P02_R12_SP04 = TransportPoint('', '', P02_R12_L1, 'mm_tp_07', (298, 564))

ALL_SP_LIST = [
    P01_R01_SP01, P01_R01_SP02, P01_R01_SP03_HTBGS, P01_R01_SP04, P01_R01_SP04, P01_R01_SP05, P01_R01_SP06,
    P01_R02_SP01_JKS, P01_R02_SP02, P01_R02_SP03, P01_R02_SP04,
    P01_R03_SP01_KZZXW, P01_R03_SP02, P01_R03_SP03, P01_R03_SP04, P01_R03_SP05_HMZL, P01_R03_SP06, P01_R03_SP07,
    P01_R04_SP01, P01_R04_SP02, P01_R04_SP03, P01_R04_SP04, P01_R04_SP05,
    P02_R01_SP01, P02_R01_SP02, P02_R01_SP03, P02_R01_SP04, P02_R01_SP05, P02_R01_SP06, P02_R01_SP07, P02_R01_SP08,
    P02_R01_SP09, P02_R01_SP10,
    P02_R01_SP11, P02_R01_SP12, P02_R01_SP13, P02_R01_SP14, P02_R01_SP15, P02_R01_SP16, P02_R01_SP17, P02_R01_SP18,
    P02_R01_SP19,
    P02_R02_SP01, P02_R02_SP02, P02_R02_SP03, P02_R02_SP04, P02_R02_SP05, P02_R02_SP06,
    P02_R03_SP01, P02_R03_SP02, P02_R03_SP03, P02_R03_SP04, P02_R03_SP05, P02_R03_SP06,
    P02_R04_SP01, P02_R04_SP02, P02_R04_SP03, P02_R04_SP04, P02_R04_SP05, P02_R04_SP06, P02_R04_SP07, P02_R04_SP08,
    P02_R05_SP01, P02_R05_SP02, P02_R05_SP03, P02_R05_SP04, P02_R05_SP05, P02_R05_SP06, P02_R05_SP07, P02_R05_SP08,
    P02_R05_SP09,
    P02_R06_SP01, P02_R06_SP02, P02_R06_SP03, P02_R06_SP04,
    P02_R07_SP01, P02_R07_SP02, P02_R07_SP03,
    P02_R08_SP01, P02_R08_SP02,
    P02_R09_SP01, P02_R09_SP02, P02_R09_SP03, P02_R09_SP04, P02_R09_SP05, P02_R09_SP06, P02_R09_SP07, P02_R09_SP08,
    P02_R09_SP09, P02_R09_SP10,
    P02_R09_SP11,
    P02_R10_SP01, P02_R10_SP02, P02_R10_SP03, P02_R10_SP04, P02_R10_SP05, P02_R10_SP06, P02_R10_SP07, P02_R10_SP08,
    P02_R10_SP09,
    P02_R11_SP01, P02_R11_SP02, P02_R11_SP03, P02_R11_SP04, P02_R11_SP05, P02_R11_SP06, P02_R11_SP07,
    P02_R12_SP01, P02_R12_SP02, P02_R12_SP03, P02_R12_SP04,
]

def get_sp_by_cn(planet_cn: str, region_cn: str, level: int, tp_cn: str) -> TransportPoint:
    for i in ALL_SP_LIST:
        if i.planet.cn != planet_cn:
            continue
        if i.region.cn != region_cn:
            continue
        if i.region.level != level:
            continue
        if i.cn != tp_cn:
            continue
        return i


def region_with_another_floor(region: Region, level: int) -> Region:
    """
    切换层数
    :param region:
    :param level:
    :return:
    """
    return get_region_by_cn(region.cn, region.planet, level)


REGION_2_SP = {
    P01_R01_ZKCD.get_pr_id(): [P01_R01_SP03_HTBGS],
    P01_R02_JZCD.get_pr_id(): [P01_R02_SP01_JKS],
    P01_R03_SRCD_L1.get_pr_id(): [P01_R03_SP01_KZZXW, P01_R03_SP02, P01_R03_SP03, P01_R03_SP04, P01_R03_SP05_HMZL, P01_R03_SP06, P01_R03_SP07],
    P01_R04_ZYCD_L1.get_pr_id(): [P01_R04_SP01, P01_R04_SP02, P01_R04_SP03, P01_R04_SP04, P01_R04_SP05],
    P02_R01_L1.get_pr_id(): [
        P02_R01_SP01, P02_R01_SP02, P02_R01_SP03, P02_R01_SP04, P02_R01_SP05, P02_R01_SP06, P02_R01_SP07, P02_R01_SP08, P02_R01_SP09, P02_R01_SP10,
        P02_R01_SP11, P02_R01_SP12, P02_R01_SP13, P02_R01_SP14, P02_R01_SP15, P02_R01_SP16, P02_R01_SP17, P02_R01_SP18, P02_R01_SP19],
    P02_R02.get_pr_id(): [P02_R02_SP01, P02_R02_SP02, P02_R02_SP03, P02_R02_SP04, P02_R02_SP05, P02_R02_SP06],
    P02_R03.get_pr_id(): [P02_R03_SP01, P02_R03_SP02, P02_R03_SP03, P02_R03_SP04, P02_R03_SP05, P02_R03_SP06],
    P02_R04.get_pr_id(): [P02_R04_SP01, P02_R04_SP02, P02_R04_SP03, P02_R04_SP04, P02_R04_SP05, P02_R04_SP06, P02_R04_SP07, P02_R04_SP08],
    P02_R05.get_pr_id(): [P02_R05_SP01, P02_R05_SP02, P02_R05_SP03, P02_R05_SP04, P02_R05_SP05, P02_R05_SP06, P02_R05_SP07, P02_R05_SP08, P02_R05_SP09],
    P02_R06.get_pr_id(): [P02_R06_SP01, P02_R06_SP02, P02_R06_SP03, P02_R06_SP04],
    P02_R07.get_pr_id(): [P02_R07_SP01, P02_R07_SP02, P02_R07_SP03],
    P02_R08_L2.get_pr_id(): [P02_R08_SP01, P02_R08_SP02],
    P02_R09.get_pr_id(): [P02_R09_SP01, P02_R09_SP02, P02_R09_SP03, P02_R09_SP04, P02_R09_SP05, P02_R09_SP06, P02_R09_SP07, P02_R09_SP08, P02_R09_SP09, P02_R09_SP10,
                          P02_R09_SP11],
    P02_R10.get_pr_id(): [P02_R10_SP01, P02_R10_SP02, P02_R10_SP03, P02_R10_SP04, P02_R10_SP05, P02_R10_SP06, P02_R10_SP07, P02_R10_SP08, P02_R10_SP09],
    P02_R11_L1.get_pr_id(): [P02_R11_SP01, P02_R11_SP02, P02_R11_SP03, P02_R11_SP04, P02_R11_SP05, P02_R11_SP06, P02_R11_SP07],
    P02_R12_L1.get_pr_id(): [P02_R12_SP01, P02_R12_SP02, P02_R12_SP03, P02_R12_SP04]
}


def get_sp_type_in_rect(region: Region, rect: tuple) -> dict:
    """
    获取区域特定矩形内的特殊点 按种类分组
    :param region: 区域
    :param rect: 矩形 为空时返回全部
    :return: 特殊点
    """
    sp_list = REGION_2_SP.get(region.get_pr_id())
    sp_map = {}
    for sp in sp_list:
        if rect is None or cal_utils.in_rect(sp.lm_pos, rect):
            if sp.template_id not in sp_map:
                sp_map[sp.template_id] = []
            sp_map[sp.template_id].append(sp)

    return sp_map
