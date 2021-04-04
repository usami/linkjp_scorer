from enum import Enum


class Category(Enum):
    AIRPORT = 'airport'
    CITY = 'city'
    COMPANY = 'company'
    COMPOUND = 'compound'
    CONFERENCE = 'conference'
    LAKE = 'lake'
    PERSON = 'person'

    def __str__(self):
        return self.value

def set(category):
    if category == Category.AIRPORT:
        return ["別名", "旧称", "国", "所在地", "母都市", "近隣空港", "運営者", "名前の謂れ",
                "名称由来人物の地位職業名"]
    elif category == Category.CITY:
        return ["別名", "旧称", "種類", "国", "国内位置", "所在地", "合併市区町村", "温泉・鉱泉", "首長",
                "地形", "観光地", "恒例行事", "特産品", "産業", "地名の謂れ", "友好市区町村", "鉄道会社"]
    elif category == Category.COMPANY:
        return ["別名", "過去の社名", "種類", "業界", "事業内容", "起源", "業界内地位・規模", "創業時の事業",
                "創業国", "創業地", "本拠地国", "本拠地", "創業者", "代表者", "取扱商品", "商品名",
                "子会社・合弁会社", "買収・合併した会社", "主要株主", "コーポレートスローガン"]
    elif category == Category.COMPOUND:
        return ["別称", "種類", "商標名", "原材料", "生成化合物", "製造方法", "用途", "特性"]
    elif category == Category.CONFERENCE:
        return ["別名", "旧称・前身", "後継会議", "種類", "国", "開催地", "開催施設", "分野", "議題",
                "採択した事項", "採択した法令・条約", "賞", "議会", "構成する会議", "議長", "参加国", "参加者",
                "参加組織", "参加資格", "開催・運営", "地位・規模", "名前の謂れ"]
    elif category == Category.LAKE:
        return ["別名", "種類", "国", "国内位置", "所在地", "湖岸の地域区分", "構成する湖沼", "流入・流出河川",
                "島", "水質（淡水・汽水）", "観光地", "橋・トンネル", "公園", "産業", "動物", "植物",
                "成因", "名前の謂れ"]
    elif category == Category.PERSON:
        return ["別名", "国籍", "地位職業", "所属組織", "学歴", "生誕地", "居住地", "没地", "死因",
                "作品", "受賞歴", "参加イベント", "師匠", "両親", "家族"]
