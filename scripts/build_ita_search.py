#!/usr/bin/env python3
"""
构建 ITA Matrix 搜索链接。
用法: python build_ita_search.py [OPTIONS]

示例:
  python build_ita_search.py --origin PVG --dest LAX --date 2025-06-15
  python build_ita_search.py --origin PVG --dest LAX --date 2025-06-15 --return-date 2025-06-30 --cabin business
  python build_ita_search.py --origin PVG --dest LAX --date 2025-06-15 --passengers 2
"""

import argparse
import base64
import json
import sys
import urllib.parse
from datetime import datetime

BASE_URL = "https://matrix.itasoftware.com/itinerary"

CABIN_MAP = {
    'economy':          'COACH',
    'coach':            'COACH',
    'premium_economy':  'PREMIUM_COACH',
    'premium economy':  'PREMIUM_COACH',
    'pe':               'PREMIUM_COACH',
    'business':         'BUSINESS',
    'biz':              'BUSINESS',
    'first':            'FIRST',
    'first_class':      'FIRST',
}

# 常用城市 → IATA 机场代码
CITY_TO_IATA = {
    # 中国
    '上海':     ['PVG', 'SHA'],
    'shanghai': ['PVG', 'SHA'],
    '北京':     ['PEK', 'PKX'],
    'beijing':  ['PEK', 'PKX'],
    '广州':     ['CAN'],
    'guangzhou':['CAN'],
    '深圳':     ['SZX'],
    'shenzhen': ['SZX'],
    '成都':     ['CTU', 'TFU'],
    'chengdu':  ['CTU', 'TFU'],
    '杭州':     ['HGH'],
    'hangzhou': ['HGH'],
    '武汉':     ['WUH'],
    'wuhan':    ['WUH'],
    '西安':     ['XIY'],
    "xi'an":    ['XIY'],
    '厦门':     ['XMN'],
    'xiamen':   ['XMN'],
    '昆明':     ['KMG'],
    'kunming':  ['KMG'],
    '重庆':     ['CKG'],
    'chongqing':['CKG'],
    # 美国
    '洛杉矶':    ['LAX'],
    'los angeles':['LAX'],
    'la':        ['LAX'],
    '纽约':      ['JFK', 'EWR', 'LGA'],
    'new york':  ['JFK', 'EWR', 'LGA'],
    'nyc':       ['JFK', 'EWR', 'LGA'],
    '旧金山':    ['SFO'],
    'san francisco':['SFO'],
    'sf':        ['SFO'],
    '西雅图':    ['SEA'],
    'seattle':   ['SEA'],
    '芝加哥':    ['ORD', 'MDW'],
    'chicago':   ['ORD', 'MDW'],
    '波士顿':    ['BOS'],
    'boston':    ['BOS'],
    '华盛顿':    ['IAD', 'DCA', 'BWI'],
    'washington':['IAD', 'DCA', 'BWI'],
    'dc':        ['IAD', 'DCA', 'BWI'],
    # 欧洲
    '伦敦':      ['LHR', 'LGW'],
    'london':    ['LHR', 'LGW'],
    '巴黎':      ['CDG', 'ORY'],
    'paris':     ['CDG', 'ORY'],
    '法兰克福':  ['FRA'],
    'frankfurt': ['FRA'],
    '阿姆斯特丹':['AMS'],
    'amsterdam': ['AMS'],
    # 其他
    '东京':      ['NRT', 'HND'],
    'tokyo':     ['NRT', 'HND'],
    '首尔':      ['ICN', 'GMP'],
    'seoul':     ['ICN', 'GMP'],
    '香港':      ['HKG'],
    'hong kong': ['HKG'],
    'hk':        ['HKG'],
    '新加坡':    ['SIN'],
    'singapore': ['SIN'],
    '悉尼':      ['SYD'],
    'sydney':    ['SYD'],
}


def resolve_airport(name: str) -> str:
    """将城市名或机场代码解析为 IATA 代码（优先主机场）。"""
    name = name.strip()
    # 已经是 IATA 代码（3 个 ASCII 字母）
    if len(name) == 3 and name.isascii() and name.isalpha():
        return name.upper()
    key = name.lower()
    if key in CITY_TO_IATA:
        return CITY_TO_IATA[key][0]  # 返回首选机场
    # 部分匹配
    for city, codes in CITY_TO_IATA.items():
        if key in city or city in key:
            return codes[0]
    raise ValueError(f"无法识别机场或城市: {name!r}，请直接使用 IATA 代码（如 PVG, LAX）")


def parse_date(date_str: str) -> str:
    """解析日期，返回 YYYY-MM-DD 格式。"""
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d'):
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    raise ValueError(f"无法解析日期: {date_str!r}，请使用 YYYY-MM-DD 格式")


def build_search_json(
    origin: str,
    destination: str,
    depart_date: str,
    return_date: str | None = None,
    cabin: str = 'economy',
    adults: int = 1,
    children: int = 0,
    infants: int = 0,
) -> dict:
    origin_code = resolve_airport(origin)
    dest_code = resolve_airport(destination)
    depart = parse_date(depart_date)
    cabin_code = CABIN_MAP.get(cabin.lower(), 'COACH')

    slices = [{'origin': origin_code, 'destination': dest_code, 'date': depart}]

    if return_date:
        ret = parse_date(return_date)
        slices.append({'origin': dest_code, 'destination': origin_code, 'date': ret})
        # 确保 JSON 中只有 IATA 代码，不含中文
        for s in slices:
            s['origin'] = s['origin'].upper()
            s['destination'] = s['destination'].upper()
        trip_type = 'round_trip'
    else:
        trip_type = 'one_way'

    payload = {
        'slices': slices,
        'passengers': {
            'adultCount': adults,
            'childCount': children,
            'infantInLapCount': infants,
        },
        'cabin': cabin_code,
        'trips': trip_type,
    }
    return payload


def build_url(payload: dict) -> str:
    json_str = json.dumps(payload, separators=(',', ':'))
    encoded = base64.b64encode(json_str.encode()).decode()
    return f"{BASE_URL}?search={urllib.parse.quote(encoded)}"


def format_summary(payload: dict, url: str) -> str:
    slices = payload['slices']
    pax = payload['passengers']
    cabin_display = {
        'COACH': '经济舱',
        'PREMIUM_COACH': '超级经济舱',
        'BUSINESS': '商务舱',
        'FIRST': '头等舱',
    }.get(payload['cabin'], payload['cabin'])

    trip_display = '往返' if payload['trips'] == 'round_trip' else '单程'

    lines = [
        '',
        '✅ ITA Matrix 搜索链接已生成',
        '─' * 50,
        url,
        '─' * 50,
        '📋 搜索摘要:',
    ]

    for i, s in enumerate(slices, 1):
        label = '  去程' if i == 1 else '  回程'
        lines.append(f"{label}: {s['origin']} → {s['destination']}  ({s['date']})")

    lines.append(f"  行程类型: {trip_display}")
    lines.append(f"  舱位: {cabin_display}")

    pax_parts = []
    if pax['adultCount']:
        pax_parts.append(f"{pax['adultCount']} 成人")
    if pax['childCount']:
        pax_parts.append(f"{pax['childCount']} 儿童")
    if pax['infantInLapCount']:
        pax_parts.append(f"{pax['infantInLapCount']} 婴儿")
    lines.append(f"  旅客: {', '.join(pax_parts)}")
    lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='构建 ITA Matrix 搜索链接')
    parser.add_argument('--origin', '-o', required=True, help='出发地（城市名或 IATA 代码）')
    parser.add_argument('--dest', '-d', required=True, help='目的地（城市名或 IATA 代码）')
    parser.add_argument('--date', required=True, help='出发日期 YYYY-MM-DD')
    parser.add_argument('--return-date', '-r', default=None, help='回程日期 YYYY-MM-DD（留空=单程）')
    parser.add_argument('--cabin', '-c', default='economy',
                        help='舱位: economy / premium_economy / business / first')
    parser.add_argument('--passengers', '-p', type=int, default=1, help='成人人数')
    parser.add_argument('--children', type=int, default=0, help='儿童人数')
    parser.add_argument('--infants', type=int, default=0, help='婴儿人数（坐大腿）')
    parser.add_argument('--json-only', action='store_true', help='只输出 JSON payload')

    args = parser.parse_args()

    try:
        payload = build_search_json(
            origin=args.origin,
            destination=args.dest,
            depart_date=args.date,
            return_date=args.return_date,
            cabin=args.cabin,
            adults=args.passengers,
            children=args.children,
            infants=args.infants,
        )
    except ValueError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json_only:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    url = build_url(payload)
    print(format_summary(payload, url))


if __name__ == '__main__':
    main()
