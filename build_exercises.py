#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build docs/exercises.html — a filterable Traditional-Chinese exercise library
from yuhonas/free-exercise-db (873 exercises, Unlicense).

  python3 build_exercises.py

Design:
- Exercise NAMES are translated EN->ZH-Hant at BUILD TIME by a compositional
  phrase dictionary (below). The resulting id->中文名 map is baked into the page
  and is the human-reviewable correction layer (backlog E1.2: LLM 初翻 + 教練校對).
- Exercise DATA (exercises.json) and IMAGES are fetched at RUNTIME from the
  jsDelivr CDN, so the repo stays light and the page is always self-updating.
- Data is cached locally in .exercises-cache.json so the build runs offline.
"""
import json, os, re, urllib.request
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, ".exercises-cache.json")
SRC = "https://cdn.jsdelivr.net/gh/yuhonas/free-exercise-db@main/dist/exercises.json"

if os.path.exists(CACHE):
    d = json.load(open(CACHE, encoding="utf-8"))
else:
    print("fetching", SRC)
    with urllib.request.urlopen(SRC) as r:
        d = json.loads(r.read().decode("utf-8"))
    json.dump(d, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
d.sort(key=lambda e: e["name"].lower())

# Phrase dictionary — MULTI-WORD keys matched greedily before single words.
# order within a name is preserved by Chinese, so concatenation reads naturally.
PHRASES = {
    # press family (must beat standalone 'press')
    "bench press": "臥推", "shoulder press": "肩推", "overhead press": "過頭推",
    "leg press": "腿推", "chest press": "胸推", "military press": "軍式推舉",
    "push press": "借力推", "floor press": "地板臥推", "incline press": "上斜推",
    "decline press": "下斜推", "shoulder push press": "借力肩推",
    # raise family
    "lateral raise": "側平舉", "front raise": "前平舉", "calf raise": "提踵",
    "leg raise": "抬腿", "rear delt raise": "後三角舉", "shoulder raise": "聳肩",
    "hip raise": "抬髖", "side lateral raise": "側平舉",
    # curl family
    "preacher curl": "牧師彎舉", "hammer curl": "錘式彎舉", "leg curl": "腿後彎舉",
    "bicep curl": "二頭彎舉", "biceps curl": "二頭彎舉", "wrist curl": "腕彎舉",
    "concentration curl": "集中彎舉", "spider curl": "蜘蛛彎舉", "drag curl": "拖曳彎舉",
    # olympic / power
    "power clean": "爆發上膊", "hang clean": "懸垂上膊", "clean and jerk": "挺舉",
    "clean and press": "上膊推舉", "power snatch": "爆發抓舉", "hang snatch": "懸垂抓舉",
    "muscle snatch": "肌肉抓舉", "push jerk": "借力挺舉", "split jerk": "分腿挺舉",
    # squat / hinge
    "front squat": "前蹲舉", "back squat": "後蹲舉", "split squat": "分腿蹲",
    "goblet squat": "高腳杯蹲", "overhead squat": "過頭蹲", "box squat": "箱式蹲",
    "good morning": "早安式體前屈", "romanian deadlift": "羅馬尼亞硬舉",
    "stiff leg deadlift": "直腿硬舉", "sumo deadlift": "相撲硬舉",
    # rows / pulls
    "upright row": "直立划船", "bent over row": "俯身划船", "seated row": "坐姿划船",
    "lat pulldown": "闊背下拉", "pulldown": "下拉", "pull-up": "引體向上",
    "pull up": "引體向上", "chin-up": "反手引體", "chin up": "反手引體",
    "push-up": "伏地挺身", "push up": "伏地挺身", "sit-up": "仰臥起坐",
    "sit up": "仰臥起坐", "pull-over": "仰臥上拉", "face pull": "臉拉",
    # triceps / chest accessory
    "triceps extension": "三頭伸展", "tricep extension": "三頭伸展",
    "triceps pushdown": "三頭下壓", "tricep pushdown": "三頭下壓",
    "triceps dip": "三頭撐體", "skull crusher": "仰臥臂屈伸",
    "close-grip bench press": "窄握臥推", "cable crossover": "滑輪夾胸",
    "chest fly": "胸部飛鳥", "chest flyes": "胸部飛鳥", "rear delt fly": "後三角飛鳥",
    # legs
    "leg extension": "腿伸展", "calf press": "提踵推", "hip thrust": "臀推",
    "glute bridge": "臀橋", "hip bridge": "臀橋", "step-up": "登階", "step up": "登階",
    "wall sit": "靠牆深蹲", "box jump": "跳箱",
    # core
    "russian twist": "俄羅斯轉體", "leg raises": "抬腿", "knee raise": "提膝",
    "mountain climber": "登山者", "flutter kick": "打水踢", "v-up": "V字捲腹",
    "back extension": "背部伸展", "hyperextension": "背部伸展",
    # equipment phrases
    "medicine ball": "藥球", "exercise ball": "健身球", "stability ball": "抗力球",
    "swiss ball": "瑞士球", "bosu ball": "BOSU球", "ez bar": "EZ槓", "e-z bar": "EZ槓",
    "e-z curl bar": "EZ彎舉槓", "smith machine": "史密斯機", "body only": "徒手",
    "foam roll": "滾筒", "foam roller": "滾筒", "battle ropes": "戰繩",
    # grips / modifiers phrases
    "close-grip": "窄握", "close grip": "窄握", "wide-grip": "寬握", "wide grip": "寬握",
    "one-arm": "單臂", "one arm": "單臂", "two-arm": "雙臂", "two arm": "雙臂",
    "single-arm": "單臂", "single-leg": "單腿", "single leg": "單腿",
    "bent-over": "俯身", "bent over": "俯身", "palms-up": "掌心向上",
    "palms-down": "掌心向下", "reverse grip": "反握", "neutral grip": "中立握",
    "behind the neck": "頸後", "behind neck": "頸後", "behind the back": "背後",
    # patched from miss-list
    "straight-arm": "直臂", "straight arm": "直臂", "bent-arm": "屈臂",
    "low-pulley": "低滑輪", "high-pulley": "高滑輪", "two-dumbbell": "雙啞鈴",
    "stiff-legged": "直腿", "ez-bar": "EZ槓", "v-bar": "V槓",
    "external rotation": "外旋", "internal rotation": "內旋",
    "around the world": "繞環", "around-the-world": "繞環", "around the worlds": "繞環",
    "pull-in": "收腿", "pull in": "收腿", "v-up": "V字捲腹", "v-ups": "V字捲腹",
    "ankle on the knee": "踝置於膝", "turkish get-up": "土耳其起立",
    "good mornings": "早安式體前屈",
}

WORDS = {
    # movements
    "press": "推", "curl": "彎舉", "curls": "彎舉", "squat": "深蹲", "squats": "深蹲",
    "raise": "舉", "raises": "舉", "row": "划船", "rows": "划船", "extension": "伸展",
    "deadlift": "硬舉", "crunch": "捲腹", "crunches": "捲腹", "fly": "飛鳥",
    "flye": "飛鳥", "flyes": "飛鳥", "lunge": "弓步", "lunges": "弓步",
    "pulldown": "下拉", "pullover": "仰臥上拉", "pushdown": "下壓", "shrug": "聳肩",
    "shrugs": "聳肩", "clean": "上膊", "snatch": "抓舉", "jerk": "挺舉",
    "thruster": "推舉", "dip": "撐體", "dips": "撐體", "bridge": "橋式",
    "plank": "棒式", "twist": "轉體", "rotation": "旋轉", "rotations": "旋轉",
    "stretch": "伸展", "jump": "跳", "jumps": "跳", "throw": "拋擲", "carry": "負重行走",
    "pull": "拉", "push": "推", "thrust": "推", "kick": "踢", "kicks": "踢",
    "swing": "擺盪", "swings": "擺盪", "circles": "繞環", "chop": "劈砍",
    "walk": "行走", "walking": "行走", "step": "登階", "hop": "跳", "hops": "跳",
    "pushup": "伏地挺身", "pushups": "伏地挺身", "situp": "仰臥起坐", "situps": "仰臥起坐",
    "pullup": "引體向上", "pullups": "引體向上", "chinup": "反手引體",
    "burpee": "波比", "burpees": "波比", "muscle-up": "暴力上槓",
    # equipment
    "barbell": "槓鈴", "dumbbell": "啞鈴", "dumbbells": "啞鈴", "cable": "滑輪",
    "cables": "滑輪", "kettlebell": "壺鈴", "kettlebells": "壺鈴", "machine": "機械",
    "smith": "史密斯", "band": "彈力帶", "bands": "彈力帶", "ball": "球",
    "plate": "槓片", "rope": "繩", "sled": "雪橇", "bar": "槓", "chains": "鐵鏈",
    "weighted": "負重", "lever": "槓桿", "leverage": "槓桿", "trap": "斜方槓",
    # modifiers / posture
    "incline": "上斜", "decline": "下斜", "standing": "站姿", "seated": "坐姿",
    "lying": "仰臥", "kneeling": "跪姿", "reverse": "反向", "alternating": "交替",
    "alternate": "交替", "overhead": "過頭", "front": "前", "rear": "後",
    "side": "側", "lateral": "側", "high": "高", "low": "低", "wide": "寬",
    "narrow": "窄", "split": "分腿", "hang": "懸垂", "hanging": "懸垂",
    "behind": "背後", "preacher": "牧師", "hammer": "錘式", "wall": "靠牆",
    "box": "箱", "floor": "地板", "decline": "下斜", "close": "窄", "single": "單",
    "double": "雙", "bent": "俯身", "power": "爆發", "explosive": "爆發",
    "isometric": "等長", "static": "靜態", "dynamic": "動態", "assisted": "輔助",
    "negative": "離心", "partial": "局部", "full": "全程", "deficit": "墊高",
    "elevated": "墊高", "suspended": "懸吊", "banded": "彈力帶",
    # body parts
    "triceps": "三頭", "tricep": "三頭", "biceps": "二頭", "bicep": "二頭",
    "chest": "胸", "shoulder": "肩", "shoulders": "肩", "leg": "腿", "legs": "腿",
    "calf": "小腿", "calves": "小腿", "hamstring": "腿後", "hamstrings": "腿後",
    "glute": "臀", "glutes": "臀", "hip": "髖", "hips": "髖", "wrist": "手腕",
    "wrists": "手腕", "neck": "頸", "back": "背", "quad": "股四頭", "quads": "股四頭",
    "ab": "腹", "abs": "腹", "abdominal": "腹", "abdominals": "腹", "core": "核心",
    "forearm": "前臂", "forearms": "前臂", "delt": "三角肌", "delts": "三角肌",
    "lat": "闊背", "lats": "闊背", "trap": "斜方肌", "traps": "斜方肌",
    "oblique": "腹斜", "obliques": "腹斜", "knee": "膝", "knees": "膝",
    "ankle": "踝", "thigh": "大腿", "spine": "脊椎", "arm": "手臂", "arms": "手臂",
    "head": "頭", "body": "身體", "hand": "手", "hands": "手", "foot": "腳",
    # connectors / fillers
    "with": "加", "to": "至", "and": "與", "from": "從", "over": "過", "on": "於",
    "the": "", "a": "", "of": "", "in": "", "for": "", "your": "", "an": "",
    "or": "或", "up": "上", "down": "下", "out": "外", "off": "離",
    # misc common
    "good": "早安", "morning": "式", "rope": "繩", "rope": "繩",
    "around": "繞", "world": "世界", "around-the-world": "繞環",
    "scissor": "剪式", "scissors": "剪式", "bicycle": "腳踏車", "frog": "青蛙",
    "donkey": "驢式", "superman": "超人", "bird": "鳥", "dog": "狗",
    "cat": "貓", "cobra": "眼鏡蛇", "child": "嬰兒", "pigeon": "鴿式",
    "windmill": "風車", "halo": "光環繞環", "clean": "上膊", "snatch": "抓舉",
    "get-up": "起身", "turkish": "土耳其", "farmers": "農夫", "farmer's": "農夫",
    "zercher": "澤奇", "jefferson": "傑佛遜", "hack": "哈克", "sissy": "西西里",
    "pistol": "手槍式", "cossack": "哥薩克", "curtsy": "屈膝禮", "bulgarian": "保加利亞",
    # patched from miss-list
    "bench": "臥推凳", "stance": "站距", "grip": "握法", "groin": "鼠蹊",
    "balance": "平衡", "long": "長", "lift": "上舉", "flat": "平", "pulley": "滑輪",
    "linear": "直線", "against": "對抗", "sprint": "衝刺", "bodyweight": "徒手",
    "cross": "交叉", "chair": "椅", "chin": "下巴", "blocks": "墊塊", "block": "墊塊",
    "prone": "俯臥", "supine": "仰臥", "external": "外", "internal": "內",
    "deltoid": "三角肌", "backward": "後向", "forward": "前向", "drag": "拖曳",
    "through": "穿過", "rollout": "推輪", "medium": "中", "bend": "彎",
    "ups": "次", "response": "反應", "butt": "臀", "attachment": "握把",
    "iron": "鐵", "lower": "下", "upper": "上", "crossover": "交叉", "depth": "深度",
    "flexor": "屈肌", "kickback": "後踢", "treadmill": "跑步機", "pass": "傳遞",
    "drill": "訓練", "resistance": "阻力", "rack": "架", "speed": "速度",
    "straight": "直", "roller": "滾輪", "bike": "單車", "bicycling": "踩單車",
    "touchers": "觸碰", "bound": "跳躍", "crawl": "爬行", "palms": "掌心",
    "diagonal": "對角", "heel": "腳跟", "heels": "腳跟", "toe": "腳尖", "toes": "腳尖",
    "adductor": "內收肌", "adductions": "內收", "adduction": "內收",
    "abduction": "外展", "abductions": "外展", "tibialis": "脛前肌",
    "renegade": "叛逆", "windmill": "風車", "axle": "粗槓", "atlas": "阿特拉斯",
    "stone": "石", "stones": "石", "trainer": "訓練器", "board": "板",
    "air": "空氣", "fours": "四肢", "all": "全", "advanced": "進階",
    "arnold": "阿諾", "worlds": "世界", "apart": "分開", "anterior": "前側",
    "posterior": "後側", "rotator": "旋轉肌", "cuff": "袖", "scapular": "肩胛",
    "tuck": "收", "raise": "舉", "decline": "下斜", "leverage": "槓桿",
    "wheel": "輪", "rolling": "滾動", "seated": "坐姿", "incline": "上斜",
    "front": "前", "weighted": "負重", "elbow": "肘", "elbows": "肘",
    "extended": "伸展", "flexion": "屈曲", "elevation": "上抬", "depression": "下沉",
    "decline": "下斜", "tate": "泰特", "spell": "拼字", "caster": "投擲",
    "alternating": "交替", "single": "單", "double": "雙", "isometric": "等長",
    "smr": "肌筋膜放鬆", "self": "自我", "myofascial": "肌筋膜", "release": "放鬆",
    # patched batch 2 (long tail)
    "one": "單", "stationary": "原地", "mid": "中", "bends": "彎", "bend": "彎",
    "position": "姿勢", "multiple": "多", "presses": "推", "flip": "翻轉",
    "twists": "轉體", "quick": "快速", "chain": "鐵鏈", "handle": "握把",
    "concentration": "集中", "dead": "靜止", "leap": "躍", "version": "版本",
    "facing": "面向", "cone": "三角錐", "hurdle": "跨欄", "chins": "反手引體",
    "chin": "反手引體", "ham": "腿後", "below": "下方", "hug": "抱",
    "hyperextensions": "背部伸展", "extensions": "伸展", "inner": "內側",
    "inverted": "反向", "exercise": "運動", "jackknife": "折刀", "load": "負荷",
    "one-legged": "單腿", "style": "式", "muscle": "肌肉", "parallel": "平行",
    "landmine": "槓桿臂", "jammer": "推舉臂", "face": "臉", "t-bar": "T槓",
    "middle": "中部", "olympic": "奧林匹克", "slam": "砸", "open": "開",
    "palm": "掌心", "laterals": "側舉", "pallof": "Pallof", "pelvic": "骨盆",
    "tilt": "傾斜", "plyo": "增強式", "feet": "腳", "rickshaw": "人力車",
    "pulldowns": "下拉", "running": "跑", "harness": "牽引帶", "stride": "跨步",
    "stiff": "僵直", "upright": "直立", "zottman": "佐特曼", "bradford": "布拉福",
    "rocky": "洛基", "car": "汽車", "guillotine": "斷頭台", "battling": "戰",
    "ropes": "繩", "bear": "熊", "drags": "拖曳", "powerlifting": "健力",
    "bottoms-up": "底朝上", "bottoms": "底", "skip": "跳繩", "butterfly": "蝴蝶",
    "deadlifts": "硬舉", "judo": "柔道", "russian": "俄羅斯", "drivers": "驅動",
    "carioca": "卡里奧卡", "catch": "接", "tate": "泰特", "spell": "拼字",
    "row": "划船", "rear": "後", "kneeling": "跪姿", "seated": "坐姿",
    "decline": "下斜", "incline": "上斜", "rotation": "旋轉", "extension": "伸展",
    "pushup": "伏地挺身", "abdominal": "腹", "leg": "腿", "raise": "舉",
    "hip": "髖", "flexion": "屈曲", "pec": "胸", "pecs": "胸", "deck": "夾胸機",
    "weighted": "負重", "alternating": "交替", "side": "側", "lateral": "側",
    # patched batch 3
    "pose": "式", "child's": "嬰兒", "downward": "下", "dog": "犬", "cobra": "眼鏡蛇",
    "cuban": "古巴", "crucifix": "十字", "cocoons": "蜷縮", "bug": "蟲", "dead-bug": "死蟲",
    "drop": "落下", "pronation": "旋前", "supination": "旋後", "scaption": "肩胛面舉",
    "pronated": "旋前", "supinated": "旋後", "skullcrusher": "仰臥臂屈伸",
    "elliptical": "橢圓機", "range": "範圍", "fast": "快速", "skipping": "跳繩",
    "finger": "手指", "flutter": "拍動", "freehand": "徒手", "two": "雙",
    "sternum": "胸骨", "pins": "插銷", "gorilla": "大猩猩", "run": "跑",
    "point": "點", "bell": "鈴", "clock": "時鐘", "circus": "馬戲",
    "dancer's": "舞者", "cuban": "古巴", "sit-ups": "仰臥起坐", "intermediate": "進階",
    "scissor": "剪", "frog": "青蛙", "spider": "蜘蛛", "scorpion": "蠍式",
    "around": "繞", "world": "環", "world's": "世界", "wide": "寬", "narrow": "窄",
    "decline": "下斜", "isometric": "等長", "tempo": "節奏", "pause": "暫停",
    "banded": "彈力帶", "cluster": "集群", "drop-set": "遞減組", "giant": "巨人",
    "complex": "複合", "circuit": "循環", "ladder": "階梯", "tabata": "Tabata",
}

ALLKEYS = dict(WORDS)
# split phrase dict by word count for the matcher
PHRASE_BY_LEN = {}
for k, v in PHRASES.items():
    n = len(k.split())
    PHRASE_BY_LEN.setdefault(n, {})[k] = v
MAXW = max(PHRASE_BY_LEN) if PHRASE_BY_LEN else 1


def split_tokens(name):
    # keep hyphenated dictionary entries intact by treating raw words; lower for lookup
    # tokens split on whitespace; punctuation like () , / handled separately
    name = name.replace("(", " ( ").replace(")", " ) ").replace(",", " , ").replace("/", " / ")
    return [t for t in name.split() if t]


def translate(name):
    toks = split_tokens(name)
    out = []
    miss = []
    i = 0
    n = len(toks)
    while i < n:
        matched = False
        # try longest phrase window first (incl. single-token phrases like 'one-arm')
        for w in range(min(MAXW, n - i), 0, -1):
            key = " ".join(toks[i:i + w]).lower()
            if key in PHRASES:
                out.append(PHRASES[key]); i += w; matched = True; break
        if matched:
            continue
        raw = toks[i]
        low = raw.lower().strip(".'")
        if low in WORDS:
            out.append(WORDS[low])
        elif "-" in low and all(p in WORDS or p in PHRASES for p in low.split("-") if p):
            out.append("".join(PHRASES.get(p, WORDS.get(p, "")) for p in low.split("-") if p))
        elif raw in "()/,":
            out.append({"(": "（", ")": "）", "/": "/", ",": "、"}[raw])
        elif re.fullmatch(r"[0-9/.°-]+", raw):
            out.append(raw)  # numbers like 3/4, 45-degree
        else:
            out.append(raw)   # graceful fallback: keep English inline
            miss.append(low)
        i += 1
    return "".join(out), miss


def read_page_template():
    return PAGE_TEMPLATE


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Noki 動作庫 — 873 個訓練動作</title>
<style>
:root{
  --accent:#14b8a6; --accent-d:#0d9488; --ink:#0f172a; --muted:#64748b;
  --bg:#f6f8fa; --card:#ffffff; --line:#e2e8f0; --sidebar:#0f172a; --chip:#f1f5f9;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Microsoft JhengHei","Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}

/* password gate */
#gate{position:fixed;inset:0;z-index:1000;background:linear-gradient(135deg,#0f172a,#134e4a);display:flex;align-items:center;justify-content:center;padding:24px}
#gate .card{background:var(--card);border-radius:18px;padding:40px 34px;max-width:380px;width:100%;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.35)}
#gate .logo{font-size:30px;font-weight:800}
#gate .logo span{color:var(--accent)}
#gate p{color:var(--muted);margin:.4em 0 1.4em;font-size:14px}
#gate input{width:100%;padding:13px 15px;font-size:18px;text-align:center;letter-spacing:.3em;border:1.5px solid var(--line);border-radius:11px;outline:none}
#gate input:focus{border-color:var(--accent)}
#gate button{margin-top:14px;width:100%;padding:13px;font-size:16px;font-weight:700;color:#fff;background:var(--accent);border:none;border-radius:11px;cursor:pointer}
#gate .err{color:#e11d48;font-size:13px;height:18px;margin-top:10px}

#app{display:none}
header.top{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:14px 22px}
.top-row{display:flex;align-items:center;gap:16px;flex-wrap:wrap;max-width:1280px;margin:0 auto}
.brand{font-size:20px;font-weight:800;white-space:nowrap}
.brand span{color:var(--accent)}
.brand small{font-weight:600;color:var(--muted);font-size:13px;margin-left:6px}
.search{flex:1;min-width:200px;position:relative}
.search input{width:100%;padding:10px 14px 10px 38px;font-size:15px;border:1.5px solid var(--line);border-radius:10px;outline:none;background:var(--bg)}
.search input:focus{border-color:var(--accent);background:#fff}
.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:17px;height:17px;fill:var(--muted)}
.count{font-size:13px;color:var(--muted);white-space:nowrap}
.count b{color:var(--accent-d);font-size:15px}

.wrap{display:flex;max-width:1280px;margin:0 auto;gap:22px;padding:20px 22px 70px;align-items:flex-start}
aside.filters{width:236px;flex-shrink:0;position:sticky;top:78px}
.fgroup{margin-bottom:18px}
.fgroup h4{margin:0 0 8px;font-size:13px;color:var(--muted);font-weight:700;display:flex;justify-content:space-between;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12.5px;padding:5px 10px;border:1px solid var(--line);border-radius:999px;background:var(--chip);cursor:pointer;user-select:none;transition:.12s;color:#334155}
.chip:hover{border-color:var(--accent)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.chip .n{opacity:.6;font-size:11px;margin-left:3px}
.clearbtn{font-size:12px;color:var(--accent-d);background:none;border:none;cursor:pointer;padding:0}
.clearbtn:disabled{color:var(--muted);opacity:.5;cursor:default}

main.results{flex:1;min-width:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(208px,1fr));gap:16px}
.exc{background:var(--card);border:1px solid var(--line);border-radius:13px;overflow:hidden;cursor:pointer;transition:.14s;display:flex;flex-direction:column}
.exc:hover{border-color:var(--accent);box-shadow:0 8px 22px rgba(20,184,166,.13);transform:translateY(-2px)}
.exc .ph{aspect-ratio:5/4;background:#eef2f6 url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="%23cbd5e1"><path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM8.5 13.5l2.5 3 3.5-4.5 4.5 6H5l3.5-4.5z"/></svg>') center/40px no-repeat;position:relative;overflow:hidden}
.exc .ph img{width:100%;height:100%;object-fit:cover;display:block}
.exc .body{padding:11px 13px 13px;display:flex;flex-direction:column;gap:7px;flex:1}
.exc .zh{font-weight:700;font-size:14.5px;line-height:1.35}
.exc .en{font-size:11.5px;color:var(--muted);margin-top:-3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.exc .tags{display:flex;flex-wrap:wrap;gap:4px;margin-top:auto}
.tg{font-size:11px;padding:2px 7px;border-radius:6px;background:var(--chip);color:#475569}
.tg.lv{background:#ecfeff;color:#0e7490}
.empty{text-align:center;color:var(--muted);padding:80px 20px}

/* modal */
#modal{position:fixed;inset:0;z-index:200;background:rgba(15,23,42,.72);display:none;align-items:center;justify-content:center;padding:24px}
#modal .box{background:#fff;border-radius:16px;max-width:760px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 30px 80px rgba(0,0,0,.4)}
#modal .mhead{padding:22px 26px 14px;border-bottom:1px solid var(--line);position:relative}
#modal .mhead h2{margin:0;font-size:22px}
#modal .mhead .men{color:var(--muted);font-size:14px;margin-top:3px}
#modal .x{position:absolute;top:18px;right:20px;font-size:26px;line-height:1;color:var(--muted);background:none;border:none;cursor:pointer}
#modal .imgs{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:18px 26px}
#modal .imgs img{width:100%;border-radius:10px;background:#eef2f6;aspect-ratio:5/4;object-fit:cover}
#modal .meta{display:flex;flex-wrap:wrap;gap:8px;padding:0 26px 14px}
#modal .meta .tg{font-size:12.5px;padding:4px 10px}
#modal .sec{padding:4px 26px 8px}
#modal .sec h3{font-size:14px;color:var(--muted);margin:10px 0 6px}
#modal ol{margin:0;padding-left:20px}
#modal ol li{font-size:13.5px;margin-bottom:7px;color:#334155}
#modal .yt{display:inline-flex;align-items:center;gap:8px;margin:8px 26px 24px;padding:11px 18px;background:#ff0000;color:#fff;font-weight:700;font-size:14px;border-radius:10px;text-decoration:none}
#modal .yt:hover{background:#d70000}
#modal .yt svg{width:20px;height:20px;fill:#fff}
.note{font-size:12px;color:var(--muted);padding:10px 26px 22px}

@media(max-width:780px){
  .wrap{flex-direction:column;padding:14px}
  aside.filters{width:100%;position:static}
  .fgroup .chips{max-height:none}
  #modal .imgs{grid-template-columns:1fr}
}
</style>
</head>
<body>

<div id="gate">
  <form class="card" id="gate-form">
    <div class="logo">No<span>ki</span></div>
    <p>動作庫 · 請輸入存取密碼</p>
    <input id="pw" type="password" inputmode="numeric" autocomplete="off" placeholder="••••" autofocus>
    <button type="submit">進入</button>
    <div class="err" id="err"></div>
  </form>
</div>

<div id="app">
  <header class="top">
    <div class="top-row">
      <div class="brand">No<span>ki</span> 動作庫<small>free-exercise-db · 繁中</small></div>
      <div class="search">
        <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14z"/></svg>
        <input id="q" type="search" placeholder="搜尋動作（中文或英文）…" autocomplete="off">
      </div>
      <div class="count"><b id="cnt">0</b> / __TOTAL__ 個動作</div>
    </div>
  </header>

  <div class="wrap">
    <aside class="filters" id="filters"></aside>
    <main class="results">
      <div class="grid" id="grid"></div>
      <div class="empty" id="empty" hidden>沒有符合條件的動作，試試放寬篩選。</div>
    </main>
  </div>
</div>

<div id="modal"><div class="box" id="mbox"></div></div>

<script>
var NAMES=__NAMES__, FILTERS=__FILTERS__, LABELS=__LABELS__;
var CDN="https://cdn.jsdelivr.net/gh/yuhonas/free-exercise-db@main/exercises/";
var DIM={category:"類別",muscle:"主要部位",equipment:"器材",level:"難度",force:"發力",mechanic:"類型"};
var DATA=[], state={q:"",category:[],muscle:[],equipment:[],level:[],force:[],mechanic:[]};

/* ---- gate ---- */
var gate=document.getElementById('gate'),app=document.getElementById('app');
if(sessionStorage.getItem('noki_ok')==='1'){enter();}
document.getElementById('gate-form').addEventListener('submit',function(e){
  e.preventDefault();
  if(document.getElementById('pw').value.trim()==='555'){sessionStorage.setItem('noki_ok','1');enter();}
  else{document.getElementById('err').textContent='密碼錯誤，請再試一次';document.getElementById('pw').value='';}
});
function enter(){gate.style.display='none';app.style.display='block';if(!DATA.length)load();}

/* ---- data ---- */
function load(){
  var url="https://cdn.jsdelivr.net/gh/yuhonas/free-exercise-db@main/dist/exercises.json";
  fetch(url).then(function(r){return r.json();}).then(function(j){
    DATA=j.map(function(e){return {
      id:e.id, en:e.name, zh:NAMES[e.id]||e.name,
      category:e.category, level:e.level, force:e.force, mechanic:e.mechanic,
      equipment:e.equipment, muscles:e.primaryMuscles||[], sec:e.secondaryMuscles||[],
      instructions:e.instructions||[], images:e.images||[]
    };});
    buildFilters(); apply();
  }).catch(function(){
    document.getElementById('grid').innerHTML='<div class="empty">資料載入失敗，請檢查網路連線後重新整理。</div>';
  });
}

function L(dim,key){return (LABELS[dim]&&LABELS[dim][key])||key;}

/* ---- filters ui ---- */
function buildFilters(){
  var host=document.getElementById('filters'),h='';
  h+='<div class="fgroup"><h4>篩選 <button class="clearbtn" id="clr" disabled>清除全部</button></h4></div>';
  Object.keys(DIM).forEach(function(dim){
    var rows=FILTERS[dim]||[];
    h+='<div class="fgroup"><h4>'+DIM[dim]+'</h4><div class="chips">';
    rows.forEach(function(r){
      h+='<span class="chip" data-dim="'+dim+'" data-key="'+enc(r[0])+'">'+r[1]+'<span class="n">'+r[2]+'</span></span>';
    });
    h+='</div></div>';
  });
  host.innerHTML=h;
  host.querySelectorAll('.chip').forEach(function(c){
    c.addEventListener('click',function(){toggle(c.dataset.dim,c.dataset.key,c);});
  });
  document.getElementById('clr').addEventListener('click',clearAll);
}
function enc(s){return s.replace(/"/g,'&quot;');}
function toggle(dim,key,el){
  var a=state[dim],i=a.indexOf(key);
  if(i<0){a.push(key);el.classList.add('on');}else{a.splice(i,1);el.classList.remove('on');}
  apply();
}
function clearAll(){
  Object.keys(DIM).forEach(function(d){state[d]=[];});
  document.querySelectorAll('.chip.on').forEach(function(c){c.classList.remove('on');});
  apply();
}

/* ---- search ---- */
var qbox=document.getElementById('q'),qt;
qbox.addEventListener('input',function(){clearTimeout(qt);qt=setTimeout(function(){state.q=qbox.value.trim().toLowerCase();apply();},120);});

/* ---- apply + render ---- */
function apply(){
  var q=state.q;
  var out=DATA.filter(function(e){
    if(q && e.en.toLowerCase().indexOf(q)<0 && e.zh.toLowerCase().indexOf(q)<0) return false;
    if(state.category.length && state.category.indexOf(e.category)<0) return false;
    if(state.equipment.length && state.equipment.indexOf(e.equipment)<0) return false;
    if(state.level.length && state.level.indexOf(e.level)<0) return false;
    if(state.force.length && state.force.indexOf(e.force)<0) return false;
    if(state.mechanic.length && state.mechanic.indexOf(e.mechanic)<0) return false;
    if(state.muscle.length && !state.muscle.some(function(m){return e.muscles.indexOf(m)>=0;})) return false;
    return true;
  });
  render(out);
  document.getElementById('cnt').textContent=out.length;
  var any=Object.keys(DIM).some(function(d){return state[d].length;})||q;
  var clr=document.getElementById('clr'); if(clr) clr.disabled=!any;
}
function render(list){
  var grid=document.getElementById('grid'),empty=document.getElementById('empty');
  if(!list.length){grid.innerHTML='';empty.hidden=false;return;}
  empty.hidden=true;
  var h=list.map(function(e){
    var img=e.images[0]?'<img loading="lazy" src="'+CDN+e.images[0]+'" alt="">':'';
    var tags='';
    if(e.equipment) tags+='<span class="tg">'+L('equipment',e.equipment)+'</span>';
    if(e.muscles[0]) tags+='<span class="tg">'+L('muscle',e.muscles[0])+'</span>';
    if(e.level) tags+='<span class="tg lv">'+L('level',e.level)+'</span>';
    return '<article class="exc" data-id="'+e.id+'"><div class="ph">'+img+'</div>'+
      '<div class="body"><div class="zh">'+e.zh+'</div><div class="en">'+e.en+'</div>'+
      '<div class="tags">'+tags+'</div></div></article>';
  }).join('');
  grid.innerHTML=h;
  grid.querySelectorAll('.exc').forEach(function(c){
    c.addEventListener('click',function(){openModal(c.dataset.id);});
  });
}

/* ---- modal ---- */
var modal=document.getElementById('modal'),mbox=document.getElementById('mbox');
function openModal(id){
  var e=DATA.find(function(x){return x.id===id;}); if(!e)return;
  var imgs=e.images.map(function(p){return '<img loading="lazy" src="'+CDN+p+'" alt="">';}).join('');
  var meta='';
  if(e.category) meta+='<span class="tg">'+L('category',e.category)+'</span>';
  if(e.equipment) meta+='<span class="tg">'+L('equipment',e.equipment)+'</span>';
  if(e.level) meta+='<span class="tg lv">'+L('level',e.level)+'</span>';
  if(e.force) meta+='<span class="tg">發力：'+L('force',e.force)+'</span>';
  if(e.mechanic) meta+='<span class="tg">'+L('mechanic',e.mechanic)+'</span>';
  e.muscles.forEach(function(m){meta+='<span class="tg">'+L('muscle',m)+'</span>';});
  var steps=e.instructions.map(function(s){return '<li>'+esc(s)+'</li>';}).join('');
  var yt="https://www.youtube.com/results?search_query="+encodeURIComponent(e.en+" exercise form");
  mbox.innerHTML=
    '<div class="mhead"><button class="x" id="mx">&times;</button>'+
      '<h2>'+e.zh+'</h2><div class="men">'+e.en+'</div></div>'+
    (imgs?'<div class="imgs">'+imgs+'</div>':'')+
    '<div class="meta">'+meta+'</div>'+
    (steps?'<div class="sec"><h3>步驟說明（原文）</h3><ol>'+steps+'</ol></div>':'')+
    '<a class="yt" href="'+yt+'" target="_blank" rel="noopener">'+
      '<svg viewBox="0 0 24 24"><path d="M23 12s0-3.2-.4-4.7a2.5 2.5 0 0 0-1.8-1.8C19.3 5 12 5 12 5s-7.3 0-8.8.5A2.5 2.5 0 0 0 1.4 7.3C1 8.8 1 12 1 12s0 3.2.4 4.7a2.5 2.5 0 0 0 1.8 1.8C4.7 19 12 19 12 19s7.3 0 8.8-.5a2.5 2.5 0 0 0 1.8-1.8C23 15.2 23 12 23 12zM9.8 15.3V8.7l6.2 3.3-6.2 3.3z"/></svg>'+
      'YouTube 看動作示範</a>'+
    '<div class="note">示範影片為 YouTube 即時搜尋結果（資料庫本身僅含實拍圖、無影片）。</div>';
  document.getElementById('mx').addEventListener('click',closeModal);
  modal.style.display='flex';
}
function closeModal(){modal.style.display='none';mbox.innerHTML='';}
modal.addEventListener('click',function(e){if(e.target===modal)closeModal();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Filter-dimension label dictionaries (Traditional Chinese)
# ---------------------------------------------------------------------------
CAT = {
    "strength": "力量訓練", "stretching": "伸展", "plyometrics": "增強式",
    "powerlifting": "健力", "olympic weightlifting": "奧林匹克舉重",
    "strongman": "大力士", "cardio": "有氧",
}
LEVEL = {"beginner": "初級", "intermediate": "中級", "expert": "高級"}
FORCE = {"pull": "拉", "push": "推", "static": "靜態"}
MECH = {"compound": "複合動作", "isolation": "孤立動作"}
EQUIP = {
    "barbell": "槓鈴", "dumbbell": "啞鈴", "body only": "徒手", "cable": "滑輪",
    "machine": "機械", "kettlebells": "壺鈴", "bands": "彈力帶",
    "medicine ball": "藥球", "exercise ball": "健身球", "foam roll": "滾筒",
    "e-z curl bar": "EZ彎舉槓", "other": "其他",
}
MUSCLE = {
    "quadriceps": "股四頭肌", "shoulders": "肩部", "abdominals": "腹肌",
    "chest": "胸部", "hamstrings": "腿後肌", "triceps": "三頭肌",
    "biceps": "二頭肌", "lats": "闊背肌", "middle back": "中背部",
    "calves": "小腿", "lower back": "下背部", "forearms": "前臂",
    "glutes": "臀肌", "traps": "斜方肌", "adductors": "內收肌",
    "neck": "頸部", "abductors": "外展肌",
}

# ---------------------------------------------------------------------------
# Build the id->中文名 map and measure coverage
# ---------------------------------------------------------------------------
NAMES = {}
full_ok = 0
all_miss = Counter()
for e in d:
    zh, miss = translate(e["name"])
    NAMES[e["id"]] = zh
    if miss:
        for m in miss:
            all_miss[m] += 1
    else:
        full_ok += 1


def facet(field, labelmap, multi=False):
    c = Counter()
    for e in d:
        v = e.get(field)
        vals = (v or []) if multi else ([v] if v else [])
        for x in vals:
            c[x] += 1
    return [[k, labelmap.get(k, k), n] for k, n in c.most_common() if k]


FILTERS = {
    "category": facet("category", CAT),
    "muscle": facet("primaryMuscles", MUSCLE, multi=True),
    "equipment": facet("equipment", EQUIP),
    "level": facet("level", LEVEL),
    "force": facet("force", FORCE),
    "mechanic": facet("mechanic", MECH),
}
LABELS = {"category": CAT, "muscle": MUSCLE, "equipment": EQUIP,
          "level": LEVEL, "force": FORCE, "mechanic": MECH}

NAMES_JSON = json.dumps(NAMES, ensure_ascii=False, separators=(",", ":"))
FILTERS_JSON = json.dumps(FILTERS, ensure_ascii=False, separators=(",", ":"))
LABELS_JSON = json.dumps(LABELS, ensure_ascii=False, separators=(",", ":"))

PAGE = read_page_template()
out = (PAGE
       .replace("__NAMES__", NAMES_JSON)
       .replace("__FILTERS__", FILTERS_JSON)
       .replace("__LABELS__", LABELS_JSON)
       .replace("__TOTAL__", str(len(d)))
       .replace("__COVERAGE__", str(100 * full_ok // len(d))))

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "exercises.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)

print("Built docs/exercises.html")
print(f"  exercises: {len(d)}")
print(f"  name translation full-coverage: {full_ok}/{len(d)} ({100*full_ok//len(d)}%)")
print(f"  remaining distinct miss tokens: {len(all_miss)} (degrade to inline EN)")
