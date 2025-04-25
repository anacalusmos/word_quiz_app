import streamlit as st
import os
import random
from io import BytesIO

# 📘 페이지 타이틀
st.set_page_config(page_title="단어시험 웹앱", layout="wide")

# 상태 초기화
def init_session():
    if "show_guide" not in st.session_state:
        st.session_state.show_guide = not st.session_state.get("guide_dismissed", False)
    if "guide_dismissed" not in st.session_state:
        st.session_state.guide_dismissed = False
init_session()

st.title("📘 단어 시험 생성기")

# 사용자 이름 입력
import streamlit_authenticator as stauth

# 사용자 로그인
st.sidebar.subheader("🔐 로그인")
names = ["민재"]
usernames = ["minjae"]
passwords = ["abc123"]
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "wordquiz_cookie", "auth_key", cookie_expiry_days=1)

name, auth_status, username = authenticator.login("로그인", "sidebar")

if auth_status:
    st.sidebar.success(f"환영합니다, {name}님!")
    subject = st.sidebar.text_input("단어시험 주제 (예: 동물학, 토익 등)")
    user = username
else:
    st.stop()
user_folder = "user_data"
os.makedirs(user_folder, exist_ok=True)

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
            if st.button("👋 다시 보지 않기"):
                st.session_state.show_guide = False
                st.session_state.guide_dismissed = True
                st.rerun()
        with col2:
            if st.button("🔄 다시 보기"):
                st.session_state.show_guide = True
                st.session_state.guide_dismissed = False
                st.rerun()
    st.session_state.show_guide = False

# 📂 사용자별 단어장 파일 목록
def get_user_files():
    if not subject:
        return []
    return [f for f in os.listdir(user_folder) if f.startswith(f"{subject}_") and f.endswith(".txt")]
    return [f for f in os.listdir(user_folder) if f.startswith(f"{user}_") and f.endswith(".txt")]

# 좌우 분할 레이아웃
left_col, right_col = st.columns([1.6, 1])
with left_col:
    st.subheader("🆕 새 단어장 만들기")
    with st.expander("📁 단어장 직접 추가 입력", expanded=False):
        new_filename = st.text_input("새 단어장 이름 (확장자 없이)", key="filename_1")
        new_words = st.text_area("새 단어쌍 입력", height=150, key="new_words_area")
        if st.button("💾 새 단어장 저장"):
            if new_filename.strip() and user:
                full_filename = f"{subject}_{new_filename.strip()}.txt" if subject else f"{new_filename.strip()}.txt"
                with open(os.path.join(user_folder, full_filename), "w", encoding="utf-8") as f:
                    f.write(new_words.strip())
                st.success(f"'{full_filename}' 파일로 저장되었습니다.")
                st.rerun()

    st.subheader("📚 단어장 선택하기")
    selected_files = st.multiselect("원하는 단어장을 선택하세요:", get_user_files())
    if st.button("📚 선택한 단어장으로 시험지 만들기"):
        combined_pairs = []
        for file in selected_files:
            with open(os.path.join(user_folder, file), "r", encoding="utf-8") as f:
                lines = f.readlines()
                combined_pairs.extend([line.strip() for line in lines if line.strip()])
        combined_pairs = list(dict.fromkeys(combined_pairs))
        st.session_state.combined = combined_pairs
        st.session_state.shuffled_word_pairs = None

    st.subheader("📝 단어시험 문제 출력")

    cols_top = st.columns([2, 1])
    with cols_top[0]:
        quiz_mode = st.radio("문제 출제 방식 선택:", ["영어 → 뜻 (뜻 빈칸)", "뜻 → 영어 (영어 빈칸)", "랜덤 혼합"], index=2)

    combined_pairs = st.session_state.get("combined", [])
    if combined_pairs:
        word_pairs = []
        for line in combined_pairs:
            parts = line.split("/", maxsplit=1)
            if len(parts) == 2:
                eng = parts[0].strip()
                kor = parts[1].strip()
                word_pairs.append((eng, kor))

        if "shuffled_word_pairs" not in st.session_state or st.session_state.shuffled_word_pairs is None:
            random.shuffle(word_pairs)
            st.session_state.shuffled_word_pairs = word_pairs.copy()
        else:
            word_pairs = st.session_state.shuffled_word_pairs

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

        st.session_state["output_text"] = output

        answer_output = ""
        for i, (eng, kor) in enumerate(word_pairs, start=1):
            a = f"{i}. {eng} : {kor}"
            answer_output += a + "\n"

        st.session_state["answer_text"] = answer_output

        selected_name = selected_files[0].replace(".txt", "") if selected_files else "merged"

        with cols_top[1]:
            st.download_button("📄 문제 다운로드", st.session_state["output_text"], file_name=f"{selected_name} test.txt", mime="text/plain")
            st.download_button("🟥 정답 다운로드", st.session_state["answer_text"], file_name=f"{selected_name} solution.txt", mime="text/plain")
            if st.button("📋 시험지 복사하기"):
                st.session_state["copy_text"] = st.session_state["output_text"]
                st.success("📋 텍스트가 복사되었습니다! (Ctrl+V로 붙여넣기 하세요)")
    else:
        st.info("📌 왼쪽에서 단어장을 불러오거나 합쳐주세요!")