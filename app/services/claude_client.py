import os
import re
import json
import anthropic
from anthropic.types import MessageParam

client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))


async def convert_to_classical(text: str, substitutions: dict[str, str]) -> dict:
    """현대 문장을 조선시대 말투로 변환하고 강조 단어 목록 반환"""
    sub_text = json.dumps(substitutions, ensure_ascii=False) if substitutions else "없음"

    prompt = f"""다음 현대 한국어 문장을 조선시대·고전 문체 스타일로 변환해줘.

현대 문장: {text}
참고할 단어 치환 목록: {sub_text}

규칙:
- 단순 단어 치환이 아니라 문장 전체의 분위기와 말투를 바꿔줘
- 자연스럽고 읽기 좋게 다듬어줘
- highlighted_words는 변환된 문장에서 옛 표현만 포함해줘
- position은 변환된 문장에서 해당 단어의 시작·끝 인덱스 (문자 기준)

반드시 아래 JSON 형식으로만 응답해줘:
{{
  "converted_text": "변환된 문장",
  "highlighted_words": [
    {{"word": "고전어", "modern": "현대어", "position": [시작인덱스, 끝인덱스]}}
  ]
}}"""

    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[MessageParam(role="user", content=prompt)],
    )

    raw = message.content[0].text
    # 마크다운 코드블럭(```json ... ```) 제거
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
    return json.loads(cleaned)
