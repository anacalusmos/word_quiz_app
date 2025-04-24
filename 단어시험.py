import streamlit as st
import os
import random

# 상태 초기화
def init_session():
    if "show_guide" not in st.session_state:
        st.session_state.show_guide = True
init_session()

# 📘 페이지 타이틀
st.set_page_config(page_title="단어시험 웹앱", layout="wide")
st.title("📘 단어 시험 생성기")

# 안내 팝업
if st.session_state.show_guide:
    with st.expander("📘 단어시험 웹앱 사용 설명서 (자동 안내)", expanded=True):
        st.markdown("""
### 🧑‍🏫 단어장 사용 방법

---

**1️⃣ 단어자료 준비하기**  
✅ PPT 스크린샷을 찍고 ChatGPT에게 다음과 같이 요청하세요:  
`이 이미지를 \"영단어 / 뜻\" 형식으로 바꿔줘.`  
- 예시: `metaphysis / 발허리의, 중족골의`

✅ 메모장에 직접 작성 가능  
```
apple / 사과  
give up / 포기하다  
```

> 📌 **형식**: 슬래시(`/`)로 구분, 뜻에 쉼표는 자유롭게 사용 가능

---

**2️⃣ .txt 파일로 저장하기**  
- 파일명: toeic.txt  
- 인코딩: UTF-8  
- 이 앱이 있는 폴더에 저장

**3️⃣ 웹앱에서 사용하기**  
- 단어장 선택 후 📥 불러오기  
- 📝 문제 생성으로 시험 시작!
""")

        col1, col2 = st.columns([8, 2])
        with col1:
            st.caption("팝업을 닫으면 다시 보이지 않아요. 필요하면 아래 버튼으로 다시 열 수 있어요.")
        with col2:
            if st.button("🔄 다시 보기"):
                st.session_state.show_guide = True
                st.rerun()
    st.session_state.show_guide = False

# 📂 단어장 파일 목록
@st.cache_data
def get_word_files():
    return [f for f in os.listdir() if f.endswith(".txt")]

# 좌우 분할 레이아웃
left_col, right_col = st.columns([2, 1])
with left_col:
    st.subheader("📚 단어장 선택하기")
    selected_files = st.multiselect("원하는 단어장을 선택하세요:", get_word_files())
    if st.button("📚 선택한 단어장 합치기"):
        combined_pairs = []
        for file in selected_files:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                combined_pairs.extend([line.strip() for line in lines if line.strip()])
        combined_pairs = list(dict.fromkeys(combined_pairs))
        st.session_state.combined = combined_pairs

    st.subheader("🆕 새 단어장 만들기")
    with st.expander("📁 단어장 직접 추가 입력", expanded=False):
        new_filename = st.text_input("새 단어장 이름 (확장자 없이)")
        new_words = st.text_area("새 단어쌍 입력", height=150)
        if st.button("💾 새 단어장 저장"):
            if new_filename.strip():
                full_filename = new_filename.strip() + ".txt"
                with open(full_filename, "w", encoding="utf-8") as f:
                    f.write(new_words.strip())
                st.success(f"'{full_filename}' 파일로 저장되었습니다.")
                st.rerun()

with right_col:
    st.subheader("📝 단어시험 문제 출력")

    quiz_mode = st.radio(
        "문제 출제 방식 선택:",
        ["영어 → 뜻 (뜻 빈칸)", "뜻 → 영어 (영어 빈칸)", "랜덤 혼합"],
        index=2
    )

    combined_pairs = st.session_state.get("combined", [])
    if combined_pairs:
        word_pairs = []
        for line in combined_pairs:
            parts = line.split("/", maxsplit=1)
            if len(parts) == 2:
                eng = parts[0].strip()
                kor = parts[1].strip()
                word_pairs.append((eng, kor))

        random.shuffle(word_pairs)
        output = ""
        for i, (eng, kor) in enumerate(word_pairs, start=1):
            if quiz_mode == "영어 → 뜻 (뜻 빈칸)":
                q = f"{i}. {eng} : ________"
            elif quiz_mode == "뜻 → 영어 (영어 빈칸)":
                q = f"{i}. ________ : {kor}"
            else:
                if random.choice([True, False]):
                    q = f"{i}. {eng} : ________"
                else:
                    q = f"{i}. ________ : {kor}"
            st.markdown(q)
            output += q + "\n"

        st.download_button("📄 누적 문제 다운로드", output, file_name="merged_quiz.txt", mime="text/plain")
    else:
        st.info("📌 왼쪽에서 단어장을 불러오거나 합쳐주세요!")

