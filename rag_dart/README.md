# RAG DART

Python 기반의 DART 보고서 수집 및 RAG 시스템입니다.

## 환경 변수

프로젝트 루트에 .env 파일을 생성하고 다음 값을 설정합니다.

```env
DART_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-5
GEMINI_MODEL=gemini-2.5-flash
```

## 설치

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## OpenAI 사용법

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5
```

## Gemini 사용법

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

## 실행

```bash
python build_db.py
python app.py
```
