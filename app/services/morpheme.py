from kiwipiepy import Kiwi

kiwi = Kiwi()

TARGET_TAGS = {"NNG", "NNP", "VV", "VA"}  # 일반명사, 고유명사, 동사, 형용사


def extract_keywords(text: str) -> list[str]:
    result = kiwi.analyze(text)
    tokens = result[0][0]  # 가장 확률 높은 분석 결과

    keywords = []
    for token in tokens:
        if token.tag in TARGET_TAGS:
            keywords.append(token.form)

    return list(dict.fromkeys(keywords))  # 순서 유지하며 중복 제거
