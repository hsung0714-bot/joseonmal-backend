****- 사라진 단어 복원기

  # 1. 목표 (Goal)"
    - 현대 한국어 문장과 옛 한국어 표현을 연결하여, 사람들이 잊혀가는 한국어 문체와 어휘를 쉽고 재미있게 체험할 수 있는 웹 서비스를 만든다.
    - 단순 사전 서비스가 아닌, 현대 문장을 조선시대·고전 문체 스타일로 재해석하여 언어 데이터를 새로운 방식으로 경험하게 한다.
    - 고문헌 및 공공 언어 데이터를 대중 친화적인 형태로 재구성하여 젊은 세대가 자연스럽게 한국어의 역사와 변화를 접할 수 있도록 한다.
    - **비즈니스 목표**
      교육용·체험형 웹 서비스로 시작하여, 향후 국어 교육 플랫폼, 한국어 학습 서비스, 문화·관광 콘텐츠 분야로 확장 가능성을 확보한다.
   
 # 2. 타겟 고객 (Persona)

    - **학생 및 젊은 세대**
        - 평소 신조어와 짧은 표현에 익숙하지만, 색다른 말투나 옛 한국어 감성 콘텐츠에 흥미를 느끼는 사람.
    - **국어·문학에 관심 있는 사용자**
        - 고전 문학과 옛 표현에 관심은 있지만 접근하기 어렵다고 느끼는 사람.
        - 어렵고 딱딱한 고문헌보다 체험형 콘텐츠를 선호하는 사람.
    - 외국인들
        - 대성 → 날봐귀순 → 한국 트로트 과거문화?
    - **한국어 학습자**
        - 한국어의 역사와 다양한 표현 방식을 흥미롭게 배우고 싶은 사용자.

    # 3. 요구사항 / 기능 (Features)

    ## 3-A. 문장 변환 기능

    ### A1. **현대 문장 → 옛 문체 변환**
    
    - 사용자가 현대식 문장을 입력하면 이를 조선시대·고전 문체 스타일로 변환.
    - 단순 단어 치환이 아니라 문장 분위기와 말투까지 함께 재구성.
    
    예시:
    
    - “오늘 시험 망해서 우울함”
        
        → “금일 시험이 뜻대로 되지 아니하여 마음이 심히 착잡하도다.”
        
    - “배고픈데 배달시킬까?”
        
        → “시장하니 주린 배를 달랠 음식을 들일까 하노라."
    
    ### A3. 핵심 단어 하이라이트 → 명확한 단어들만?(like 명사?)
    
    - 변환된 문장에서 옛 표현을 강조 표시.
    - 해당 단어를 클릭하면 의미와 설명 확인 가능.
        - 오늘 시험 망해서 우울함
        - 배고픈데 배달시킬까
        - 시장하니 주린 배를 달랠 음식을 들일까 하노라
    
    예:
    
    - 벗 → 친구
    - 서찰 → 편지
    
    ### B3. 오늘의 사라진 표현
    
    - 메인 화면에서 매일 하나의 옛 표현을 소개.
    - 짧은 설명과 함께 제공.
    
    예:
    > “설운하다”
    > 
    > 
    > 섭섭하고 서운한 감정을 뜻하는 옛 표현
    > 

    # 4. 사용자 스토리 (User Stories)
    
    - **학생**
        - 친구들과 재미로 현대 문장을 조선시대 말투로 바꿔보고 싶다.
        - 고전 문학 표현을 어렵지 않게 접하고 싶다.
    - **국어·문학 관심 사용자**
        - 옛 표현이 실제로 어떻게 사용되었는지 알고 싶다.
        - 현대 한국어와 과거 한국어의 차이를 흥미롭게 경험하고 싶다.
    - **한국어 학습자**
        - 단순 번역이 아니라 한국어 문체의 변화와 분위기를 배우고 싶다.

    ## 데이터
    
    - 한국고전종합DB
    - 국립국어원 언어 자료
    - 옛 사전 및 고문헌 데이터 활용.
    - 문헌 출처를 명확하게 표기하여 신뢰성 확보.

    # 8. MVP 범위
    
    MVP는  **'최소 기능 제품(Minimum Viable Product)'**
    
    우선 출시 기능:
    
    - 현대 문장 입력
    - 조선시대 스타일 문체 변환


사용자 입력: "오늘 시험 망해서 우울함" 
↓
KiWi로 형태소 분석 ← Python 라이브러리 
↓
명사·동사 추출 → 우리말샘 API에 각 단어 검색
↓
치환 가능한 단어 목록 확보 { "오늘": "금일", "우울하다": "착잡하다" } 
↓ 
Claude한테 전달 "이 단어들을 참고해서 문체를 조선시대 말투로 다듬어줘"
↓ 
최종 문장 + highlighted_words 완성


A — AI 변환 파이프라인 (핵심) → 김한성
KiWi로 형태소 분석하고, 우리말샘 API로 단어 치환하고, Claude로 문체 다듬는 것까지 이 세 개를 하나로 연결하는 게 A 담당. 제일 복잡하고 핵심.

* KiWi 설치 및 형태소 분석 코드
* 우리말샘 API 연동 (단어별 고어 검색)
* Claude API 연동 (문체 다듬기)
* `POST /api/convert` 엔드포인트
  B — 사전 API → 안영주
  우리말샘에서 긁어온 데이터로 검색·조회 기능 만드는 것.

* `GET /api/dictionary` (검색, 필터, 페이지네이션)
* `GET /api/dictionary/:id` (단어 상세)
* `GET /api/dictionary/daily` (오늘의 단어 + fallback)
  C — DB 설정 + 데이터 → 조율건
  PostgreSQL 세팅하고 우리말샘에서 단어 데이터 긁어와서 테이블에 넣는 것. 이게 없으면 B가 테스트를 못 하니까 제일 먼저 끝내야 함.

* PostgreSQL 연결 설정
* `classical_words`, `daily_words` 테이블 생성
* 우리말샘 API로 단어 데이터 수집 스크립트
* DB에 데이터 적재
* `GET /health`



문장 변환
POST
/api/convert
현대 문장 → 고어 변환 · Anthropic API 호출
req
original_text string · 1–100자 필수
rate
IP당 10회/분 제한 · 초과 시 429 반환
res 200
converted_text · highlighted_words[]
{
"converted_text": "금일 시험이 뜻대로 되지 아니하여...",
"highlighted_words": [
{ "word": "금일", "modern": "오늘", "position": [0, 2] },
{ "word": "아니하여", "modern": "안 해서", "position": [18, 22] }
]
}
note
결과는 서버 저장 안 함 · 프론트 localStorage 처리
고어 사전
GET
/api/dictionary
단어 목록 검색 · 필터 · 페이지네이션
query
q 검색어 · era 시대 · category 분류 · page · limit (default 20)
res 200
words[] · total · page · totalPages
note
is_active = true 인 단어만 반환
GET
/api/dictionary/:id
단어 상세 조회
res 200
word · era · category · modern_meaning · classical_meaning · example_sentence · source
res 404
단어 없음 · WORD_NOT_FOUND
GET
/api/dictionary/daily
오늘의 단어 · 매 요청마다 DB 직접 조회
res 200
단어 상세 전체 + is_fallback: true/false
fallback
오늘 날짜 단어 없으면 → 가장 최근 등록 단어 반환
note
Redis 없음 · 트래픽 많아지면 그때 캐시 추가 고려
시스템
GET
/health
서버·DB 상태 확인 · 배포·모니터링용
res 200
{ status: "ok", db: "ok", version: "1.0.0" }
res 503
DB 연결 실패 시


classical_words · 단어 사전
classical_words
국립국어원 데이터 최초 1회 수집 후 저장
타입
컬럼명
설명
속성
uuid
id
고유 식별자
PK
varchar
word
옛 단어 (예: 금일)
IDX
enum
era
조선전기·조선후기·고려·삼국
IDX
enum
category
감정어·관계어·일상어·자연어
text
modern_meaning
현대 뜻 (예: 오늘)
text
classical_meaning
고전적 의미·용법 설명
text
example_sentence
예문
varchar
source
출처 (예: 훈몽자회)
boolean
is_active
false = 비공개 · default true
timestamp
created_at
등록일시
classical_words
──── featured as ────▶
daily_words
daily_words · 오늘의 단어 스케줄표
daily_words
날짜별 단어 예약 · 없으면 fallback 처리
타입
컬럼명
설명
속성
uuid
id
고유 식별자
PK
uuid
word_id
classical_words 참조
FK
date
display_date
노출 날짜 · 날짜당 1개만
UK