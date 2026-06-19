import requests
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import ClassicalWord

load_dotenv()

API_KEY = os.getenv("OURMALSAM_API_KEY")

def fetch_word(query: str, search_query: str = None):
    url = "https://opendict.korean.go.kr/api/search"
    params = {
        "key": API_KEY,
        "q": search_query or query,
        "req_type": "json",
        "part": "word",
        "num": 100,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"API 오류: {response.status_code}")
        return []

    data = response.json()
    items = data.get("channel", {}).get("item", [])
    return [item for item in items if item.get("word") == query]

# (고전어, 검색어, 시대, 카테고리, 뜻필터키워드, 현대어)
WORD_LIST = [
    ("금일", None, "조선전기", "일상어", "이날", "오늘"),
    ("서찰", None, "조선전기", "일상어", "편지", "편지"),
    ("벗", None, "조선전기", "관계어", "친하게", "친구"),
    ("시장하다", "시장하다", "조선전기", "일상어", "배가", "배고프다"),
    ("울적하다", "울적하다", "조선전기", "감정어", "마음", "우울하다"),
    ("착잡하다", "착잡하다", "조선전기", "감정어", "뒤섞", "착잡하다"),
    ("설운하다", "설운하다", "조선전기", "감정어", None, "서운하다"),
    ("가람", None, "조선전기", "자연어", "강", "강"),
    ("나래", None, "조선전기", "자연어", None, "날개"),
    ("미쁘다", None, "조선전기", "감정어", "믿음", "믿음직하다"),
]

def seed_words():
    db: Session = SessionLocal()

    for query, search_query, era, category, keyword, modern_word in WORD_LIST:
        print(f"검색 중: {query}")
        items = fetch_word(query, search_query)

        if not items:
            print(f"  결과 없음: {query}")
            continue

        selected = None
        if keyword:
            for item in items:
                senses = item.get("sense", [])
                meaning = senses[0].get("definition", "") if senses else ""
                if keyword in meaning:
                    selected = item
                    break

        if not selected:
            selected = items[0]

        word = selected.get("word", "")
        senses = selected.get("sense", [])
        meaning = senses[0].get("definition", "") if senses else ""

        if not word or not meaning:
            print(f"  뜻 없음: {query}")
            continue

        exists = db.query(ClassicalWord).filter(ClassicalWord.word == word).first()
        if exists:
            print(f"  이미 존재: {word}")
            continue

        new_word = ClassicalWord(
            word=word,
            era=era,
            category=category,
            modern_word=modern_word,
            modern_meaning=meaning,
        )
        db.add(new_word)
        print(f"  추가됨: {word} ({modern_word}) - {meaning}")

    db.commit()
    db.close()
    print("\n완료!")

MANUAL_WORDS = [
    {
        "word": "시장하다",
        "modern_word": "배고프다",
        "era": "조선전기",
        "category": "일상어",
        "modern_meaning": "배가 고프다.",
        "classical_meaning": "배가 고픔을 이르는 옛 표현.",
        "example_sentence": "시장하니 주린 배를 달랠 음식을 들일까 하노라.",
    },
    {
        "word": "울적하다",
        "modern_word": "우울하다",
        "era": "조선전기",
        "category": "감정어",
        "modern_meaning": "마음이 답답하고 쓸쓸하다.",
        "classical_meaning": "불평불만이 쌓여 마음이 무거운 상태.",
        "example_sentence": "금일 과거에서 낭패를 보니 마음이 울적하도다.",
    },
    {
        "word": "착잡하다",
        "modern_word": "착잡하다",
        "era": "조선전기",
        "category": "감정어",
        "modern_meaning": "갈피를 잡을 수 없이 뒤섞여 어수선하다.",
        "classical_meaning": "여러 감정이 뒤엉켜 정리되지 않는 상태.",
        "example_sentence": "시험이 뜻대로 되지 아니하여 마음이 심히 착잡하도다.",
    },
    {
        "word": "설운하다",
        "modern_word": "서운하다",
        "era": "조선전기",
        "category": "감정어",
        "modern_meaning": "섭섭하고 서운한 감정을 느끼다.",
        "classical_meaning": "이별이나 아쉬움으로 인해 마음이 허전하고 슬픈 상태.",
        "example_sentence": "그대와 이별하니 마음이 설운하도다.",
    },
]

def seed_manual_words():
    db: Session = SessionLocal()

    for data in MANUAL_WORDS:
        exists = db.query(ClassicalWord).filter(ClassicalWord.word == data["word"]).first()
        if exists:
            print(f"  이미 존재: {data['word']}")
            continue

        new_word = ClassicalWord(
            word=data["word"],
            era=data["era"],
            category=data["category"],
            modern_word=data.get("modern_word"),
            modern_meaning=data["modern_meaning"],
            classical_meaning=data.get("classical_meaning"),
            example_sentence=data.get("example_sentence"),
        )
        db.add(new_word)
        print(f"  추가됨: {data['word']} ({data.get('modern_word')}) - {data['modern_meaning']}")

    db.commit()
    db.close()
    print("\n수동 데이터 완료!")

if __name__ == "__main__":
    seed_words()
    seed_manual_words()
