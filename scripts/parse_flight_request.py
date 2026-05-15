#!/usr/bin/env python3
"""
从自然语言中提取航班搜索参数，输出结构化 JSON。
主要供 Claude 在 Workflow 2 中调用，理解用户意图并回传给 build_ita_search.py。

用法: python parse_flight_request.py "<自然语言请求>"
输出: JSON，包含可能缺失的字段（值为 null），让 Claude 知道还需要向用户追问什么。
"""

import sys
import json
import re
from datetime import datetime, timedelta

# ── 机场关键词匹配（与 build_ita_search.py 保持同步）──────────────
CITY_PATTERNS = {
    r'上海|shanghai|pvg|sha': ('上海', 'PVG'),
    r'浦东|pudong': ('上海浦东', 'PVG'),
    r'虹桥|hongqiao': ('上海虹桥', 'SHA'),
    r'北京|beijing|pek|pkx': ('北京', 'PEK'),
    r'广州|guangzhou|can': ('广州', 'CAN'),
    r'深圳|shenzhen|szx': ('深圳', 'SZX'),
    r'成都|chengdu|ctu': ('成都', 'CTU'),
    r'杭州|hangzhou|hgh': ('杭州', 'HGH'),
    r'武汉|wuhan|wuh': ('武汉', 'WUH'),
    r'重庆|chongqing|ckg': ('重庆', 'CKG'),
    r'洛杉矶|los angeles|lax': ('洛杉矶', 'LAX'),
    r'纽约|new york|nyc|jfk|ewr': ('纽约', 'JFK'),
    r'旧金山|san francisco|sfo': ('旧金山', 'SFO'),
    r'西雅图|seattle|sea': ('西雅图', 'SEA'),
    r'芝加哥|chicago|ord': ('芝加哥', 'ORD'),
    r'波士顿|boston|bos': ('波士顿', 'BOS'),
    r'华盛顿|washington|dc|iad': ('华盛顿', 'IAD'),
    r'伦敦|london|lhr': ('伦敦', 'LHR'),
    r'巴黎|paris|cdg': ('巴黎', 'CDG'),
    r'法兰克福|frankfurt|fra': ('法兰克福', 'FRA'),
    r'东京|tokyo|nrt|hnd': ('东京', 'NRT'),
    r'首尔|seoul|icn': ('首尔', 'ICN'),
    r'香港|hong kong|hkg': ('香港', 'HKG'),
    r'新加坡|singapore|sin': ('新加坡', 'SIN'),
    r'悉尼|sydney|syd': ('悉尼', 'SYD'),
}

CABIN_PATTERNS = {
    r'头等|first class|first|f\b': 'first',
    r'商务|business|biz|j\b|c\b': 'business',
    r'超级经济|premium economy|premium|超经|pe\b|w\b': 'premium_economy',
    r'经济|economy|coach|廉价': 'economy',
}

DATE_PATTERNS = [
    (r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', '%Y-%m-%d'),
    (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', '%m/%d/%Y'),
    (r'(\d{4})(\d{2})(\d{2})', '%Y%m%d'),
]

# 中文日期，如 "6月15号"、"6月15日"、"6/15"（当年）
CHINESE_DATE_RE = re.compile(r'(\d{1,2})月(\d{1,2})[号日]?')

PASSENGER_PATTERN = re.compile(
    r'(\d+)\s*(?:人|位|名|个人|passengers?|adults?|pax)', re.IGNORECASE
)


def extract_cities(text: str):
    found = []
    text_lower = text.lower()
    for pattern, (name, iata) in CITY_PATTERNS.items():
        if re.search(pattern, text_lower):
            found.append({'name': name, 'iata': iata, 'matched_pattern': pattern})
    return found


def extract_dates(text: str):
    dates = []
    current_year = datetime.now().year

    for pattern, _ in DATE_PATTERNS:
        for m in re.finditer(pattern, text):
            raw = m.group(0)
            parts = re.split(r'[/-]', raw)
            if len(parts) == 3:
                try:
                    if len(parts[0]) == 4:
                        d = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                    else:
                        d = datetime(int(parts[2]), int(parts[0]), int(parts[1]))
                    dates.append(d.strftime('%Y-%m-%d'))
                except ValueError:
                    pass

    # 中文日期：6月15号 → 当年或明年（若已过则推明年）
    for m in CHINESE_DATE_RE.finditer(text):
        month, day = int(m.group(1)), int(m.group(2))
        try:
            d = datetime(current_year, month, day)
            if d < datetime.now():
                d = datetime(current_year + 1, month, day)
            dates.append(d.strftime('%Y-%m-%d'))
        except ValueError:
            pass

    return list(dict.fromkeys(dates))  # 去重保序


def extract_cabin(text: str):
    text_lower = text.lower()
    for pattern, cabin in CABIN_PATTERNS.items():
        if re.search(pattern, text_lower):
            return cabin
    return None


def extract_passengers(text: str):
    m = PASSENGER_PATTERN.search(text)
    if m:
        return int(m.group(1))
    return None


def is_round_trip(text: str) -> bool | None:
    text_lower = text.lower()
    if re.search(r'往返|round.?trip|来回|return', text_lower):
        return True
    if re.search(r'单程|one.?way|单向', text_lower):
        return False
    return None  # 需要追问


def parse(text: str) -> dict:
    cities = extract_cities(text)
    dates = extract_dates(text)
    cabin = extract_cabin(text)
    pax = extract_passengers(text)
    rt = is_round_trip(text)

    result = {
        'origin': cities[0] if len(cities) >= 1 else None,
        'destination': cities[1] if len(cities) >= 2 else None,
        'depart_date': dates[0] if len(dates) >= 1 else None,
        'return_date': dates[1] if len(dates) >= 2 else None,
        'cabin': cabin or 'economy',
        'adults': pax or 1,
        'trip_type': 'round_trip' if rt else ('one_way' if rt is False else None),
        'ambiguous': [],
        'missing': [],
    }

    # 标注缺失 / 模糊字段
    if result['origin'] is None:
        result['missing'].append('出发地')
    if result['destination'] is None:
        result['missing'].append('目的地')
    if result['depart_date'] is None:
        result['missing'].append('出发日期')
    if result['trip_type'] is None:
        result['ambiguous'].append('行程类型（单程/往返？）')
    if result['trip_type'] == 'round_trip' and result['return_date'] is None:
        result['missing'].append('回程日期')
    if len(cities) > 2:
        result['ambiguous'].append(f'识别到超过2个城市: {[c["name"] for c in cities]}，请确认出发地和目的地')

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python parse_flight_request.py \"<用户请求>\"")
        sys.exit(1)

    text = ' '.join(sys.argv[1:])
    result = parse(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
