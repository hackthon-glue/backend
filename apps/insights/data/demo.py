"""Demo data used to seed the insights app."""
from __future__ import annotations

COUNTRIES = [
    {
        "code": "jp",
        "name": "Japan",
        "lat": 36.2048,
        "lng": 138.2529,
        "summary": {
            "headline": "AI協業報道でテック業界が活況",
            "weather": "東京: 18°C、今夜は小雨予想",
            "persona": "落ち着きつつ集中し、世界とイノベーションを模索",
            "moodNarrative": "ロボティクスと量子技術の進展が話題を独占し、雨模様でも都市全体に静かな前向きさが広がった一日。",
            "todaySummary": (
                "Evening showers kept umbrellas open across Tokyo, yet the robotics expo still drew long queues of "
                "students and investors. Quantum labs announced fresh climate-modeling breakthroughs, prompting "
                "manufacturers from Nagoya to book follow-up visits. Neighborhood chatter framed the weather as a "
                "gentle backdrop to a calmly optimistic day of collaboration."
            ),
        },
        "insights": {
            "sentiment": [
                {"label": "Day 1", "score": 62},
                {"label": "Day 2", "score": 65},
                {"label": "Day 3", "score": 59},
                {"label": "Day 4", "score": 68},
                {"label": "Day 5", "score": 71},
                {"label": "Day 6", "score": 74},
                {"label": "Day 7", "score": 69},
            ],
            "weatherTrend": [
                {"label": "Mon", "temperature": 19},
                {"label": "Tue", "temperature": 21},
                {"label": "Wed", "temperature": 18},
                {"label": "Thu", "temperature": 17},
                {"label": "Fri", "temperature": 20},
                {"label": "Sat", "temperature": 22},
                {"label": "Sun", "temperature": 23},
            ],
            "news": [
                {
                    "title": "東京でロボティクス博開幕",
                    "summary": "災害支援や介護を想定した協働型ヒューマノイドが来場者の関心を集めた。",
                    "url": "https://example.com/jp-robotics",
                    "category": "イノベーション",
                    "tone": "celebratory",
                },
                {
                    "title": "スマートエネルギー地区が本格運用",
                    "summary": "ピーク電力を17%削減する予測制御が都内2地区で常時稼働に移行。",
                    "url": "https://example.com/jp-energy",
                    "category": "エネルギー",
                    "tone": "optimistic",
                },
                {
                    "title": "京都の量子研究が気候モデル加速へ",
                    "summary": "高精度の誤り訂正回路が確認され、環境シミュレーション活用が期待される。",
                    "url": "https://example.com/jp-quantum",
                    "category": "研究",
                    "tone": "optimistic",
                },
            ],
            "stats": [
                {"label": "ムード変化率", "value": "↑8pt", "change": "+8", "sentiment": "positive"},
                {"label": "ヘッドライン感情", "value": "ポジティブ", "change": "AI期待感", "sentiment": "positive"},
                {"label": "体感気候", "value": "穏やかで小雨", "change": "やや気温低下", "sentiment": "neutral"},
            ],
            "weatherNow": {
                "condition": "小雨と時折の晴れ間",
                "temperature": 18,
                "feelsLike": 17,
                "humidity": 64,
                "wind": "北東 9 km/h",
                "precipitationChance": 48,
            },
            "alerts": [
                {
                    "type": "交通",
                    "level": "info",
                    "message": "山手線は夜間保守で軽微な遅延が見込まれます。",
                    "recommendedAction": "移動時間に10分の余裕を。",
                },
                {
                    "type": "天候",
                    "level": "watch",
                    "message": "関東では深夜にかけてにわか雨が強まる可能性。",
                    "recommendedAction": "屋外機材は早めに片付けを。",
                },
            ],
        },
    },
    {
        "code": "us",
        "name": "United States",
        "lat": 37.0902,
        "lng": -95.7129,
        "summary": {
            "headline": "サステナ企業が過去最高の資金調達",
            "weather": "ニューヨーク: 11°C、ひんやり快晴",
            "persona": "大胆なサプライチェーン変革を語るエネルギッシュな姿勢",
            "moodNarrative": "明るい青空のもと、グリーン投資のニュースが全国の自信と活動量を押し上げた。",
            "todaySummary": (
                "Coast-to-coast sunshine set the stage for record clean-tech funding announcements, and livestreamed "
                "demo days pulled in peak audiences from venture hubs. Utilities in California and Texas expanded "
                "rooftop storage incentives while Midwest retrofit crews reported steady hiring gains. Conversations "
                "framed the day as quietly bullish, energized by crisp air and clear policy signals."
            ),
        },
        "insights": {
            "sentiment": [
                {"label": "Day 1", "score": 48},
                {"label": "Day 2", "score": 52},
                {"label": "Day 3", "score": 57},
                {"label": "Day 4", "score": 60},
                {"label": "Day 5", "score": 63},
                {"label": "Day 6", "score": 65},
                {"label": "Day 7", "score": 67},
            ],
            "weatherTrend": [
                {"label": "Mon", "temperature": 8},
                {"label": "Tue", "temperature": 6},
                {"label": "Wed", "temperature": 9},
                {"label": "Thu", "temperature": 10},
                {"label": "Fri", "temperature": 12},
                {"label": "Sat", "temperature": 13},
                {"label": "Sun", "temperature": 11},
            ],
            "news": [
                {
                    "title": "住宅用蓄電の導入が第1四半期で倍増",
                    "summary": "カリフォルニアとテキサスで電力会社の共同出資プログラムが拡大。",
                    "url": "https://example.com/us-solar",
                    "category": "エネルギー",
                    "tone": "optimistic",
                },
                {
                    "title": "西海岸港湾で水素回廊の実証",
                    "summary": "ロサンゼルスとシアトルを結ぶ長距離輸送で水素補給網をテスト。",
                    "url": "https://example.com/us-hydrogen",
                    "category": "インフラ",
                    "tone": "cautious",
                },
                {
                    "title": "中西部で建物改修が雇用を創出",
                    "summary": "断熱・省エネ改修により25,000人のグリーンジョブが新設。",
                    "url": "https://example.com/us-retrofit",
                    "category": "雇用",
                    "tone": "celebratory",
                },
            ],
            "stats": [
                {"label": "ムード変化率", "value": "↑19pt", "change": "+19", "sentiment": "positive"},
                {"label": "ヘッドライン感情", "value": "建設的", "change": "資金流入", "sentiment": "positive"},
                {"label": "体感気候", "value": "ひんやり快適", "change": "徐々に暖かく", "sentiment": "positive"},
            ],
            "weatherNow": {
                "condition": "快晴で涼しい風",
                "temperature": 11,
                "feelsLike": 9,
                "humidity": 40,
                "wind": "北西 12 km/h",
                "precipitationChance": 5,
            },
            "alerts": [
                {
                    "type": "大気質",
                    "level": "info",
                    "message": "北東部のAQIは交通量減で中程度を維持。",
                    "recommendedAction": "屋外アクティビティを推奨。",
                }
            ],
        },
    },
    {
        "code": "fr",
        "name": "France",
        "lat": 46.2276,
        "lng": 2.2137,
        "summary": {
            "headline": "パリ気候フォーラムが包摂的炭素政策を討議",
            "weather": "パリ: 15°C、厚い雲と穏やかな風",
            "persona": "エスプレッソを片手に協調を促すビジョナリー",
            "moodNarrative": "曇天の下でも対話が進み、現実的な協調策を模索する落ち着いた空気が漂った。",
            "todaySummary": (
                "Policy delegates and community advocates shared a long afternoon of carbon-pricing negotiations, while "
                "cafés along the Seine closed early to watch river levels. Mobility founders in Lyon and Toulouse highlighted "
                "pilot wins that now attract regional partners. The day felt steady and deliberate, with every conversation "
                "circling back to inclusive climate planning."
            ),
        },
        "insights": {
            "sentiment": [
                {"label": "Day 1", "score": 55},
                {"label": "Day 2", "score": 58},
                {"label": "Day 3", "score": 54},
                {"label": "Day 4", "score": 56},
                {"label": "Day 5", "score": 60},
                {"label": "Day 6", "score": 63},
                {"label": "Day 7", "score": 61},
            ],
            "weatherTrend": [
                {"label": "Mon", "temperature": 13},
                {"label": "Tue", "temperature": 12},
                {"label": "Wed", "temperature": 11},
                {"label": "Thu", "temperature": 12},
                {"label": "Fri", "temperature": 14},
                {"label": "Sat", "temperature": 15},
                {"label": "Sun", "temperature": 16},
            ],
            "news": [
                {
                    "title": "パリ屋上で水耕農園が拡大",
                    "summary": "市内学校向け野菜の30%を地産地消で賄う計画が始動。",
                    "url": "https://example.com/fr-hydroponics",
                    "category": "食料システム",
                    "tone": "optimistic",
                },
                {
                    "title": "大西洋風力回廊が試験段階へ",
                    "summary": "浮体式タービンが安定的な基幹電源化に向けたテストを実施。",
                    "url": "https://example.com/fr-wind",
                    "category": "エネルギー",
                    "tone": "cautious",
                },
                {
                    "title": "AI主導の交通サービスを地方で展開",
                    "summary": "地方都市が需要応答型のEVシャトル導入を加速。",
                    "url": "https://example.com/fr-mobility",
                    "category": "モビリティ",
                    "tone": "optimistic",
                },
            ],
            "stats": [
                {"label": "ムード変化率", "value": "↑8pt", "change": "+8", "sentiment": "positive"},
                {"label": "ヘッドライン感情", "value": "思慮深い", "change": "合意形成", "sentiment": "neutral"},
                {"label": "体感気候", "value": "ひんやり穏やか", "change": "緩やかな昇温", "sentiment": "neutral"},
            ],
            "weatherNow": {
                "condition": "厚い雲と穏やかな風",
                "temperature": 15,
                "feelsLike": 14,
                "humidity": 58,
                "wind": "南西 7 km/h",
                "precipitationChance": 18,
            },
            "alerts": [
                {
                    "type": "河川水位",
                    "level": "watch",
                    "message": "上流の降雨でセーヌ川が今夜12cm上昇予測。",
                    "recommendedAction": "低地の倉庫は状況確認を。",
                }
            ],
        },
    },
]
