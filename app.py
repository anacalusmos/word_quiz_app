import streamlit as st
from auth import login_user, register_user
from ui_guide import show_guide
from file_manager import get_user_files, save_wordlist, load_combined_wordlist
from quiz_generator import generate_quiz

# 페이지 설정
st.set_page_config(page_title="단어시험 웹앱", layout="wide")
st.title("📘 단어 시험 생성기")

# ✅ 세션 상태 초기화 (팝업 설명서 관련)
if "show_guide" not in st.session_state:
    st.session_state.show_guide = False  # 로그인 시에만 표시되도록 기본값 False
if "guide_dismissed" not in st.session_state:
    st.session_state.guide_dismissed = False
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

# 로그인 및 회원가입 탭
login_tab, register_tab = st.sidebar.tabs(["🔐 로그인", "📝 회원가입"])
user = None
name = None
authenticator = None

with login_tab:
    authenticator, user, name = login_user()

    if user:
        st.session_state.just_logged_in = True
        if authenticator.logout("🔓 로그아웃", "sidebar"):
            st.experimental_rerun()

with register_tab:
    register_user()

# 메인 영역: 로그인된 사용자만 접근
if user:
    # 주제명 입력
    subject = st.sidebar.text_input("단어시험 주제 (예: 동물학, 토익 등)")
    user_folder = "user_data"

    # 설명서 팝업
    if st.session_state.just_logged_in:
        st.session_state.show_guide = True
        st.session_state.just_logged_in = False
    show_guide()

    # 좌우 레이아웃
    left_col, right_col = st.columns([1.6, 1])
    with left_col:
        st.subheader("🆕 새 단어장 만들기")
        with st.expander("📁 단어장 직접 추가 입력", expanded=False):
            new_filename = st.text_input("새 단어장 이름 (확장자 없이)", key="filename_1")
            new_words = st.text_area("새 단어쌍 입력", height=150, key="new_words_area")
            if st.button("💾 새 단어장 저장"):
                save_wordlist(subject, new_filename, new_words, user_folder)

        st.subheader("📚 단어장 선택하기")
        selected_files = st.multiselect("원하는 단어장을 선택하세요:", get_user_files(subject, user_folder))
        if st.button("📚 선택한 단어장으로 시험지 만들기"):
            load_combined_wordlist(selected_files, subject, user_folder)

    with right_col:
        generate_quiz(selected_files)
else:
    st.info("🔒 로그인 후 사용해주세요.")
