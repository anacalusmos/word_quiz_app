import streamlit as st
import random
import io
import datetime

def generate_quiz(selected_files):
    if "combined_words" not in st.session_state:
        st.info("📋 먼저 단어장을 선택하고 문제를 만들어주세요!")
        return

    lines = st.session_state["combined_words"].strip().split("\n")
    pairs = []
    for line in lines:
        if "/" in line:
            eng, kor = line.split("/", 1)
            pairs.append((eng.strip(), kor.strip()))

    if not pairs:
        st.warning("⚠️ 유효한 단어쌍이 없습니다.")
        return

    st.subheader("🖍️ 문제 생성")

    mode = st.radio("문제 출제 방식 선택", ["영어 → 뜻 (영어 빈칸)", "뜻 → 영어 (영어 빈칸)", "랜덤 혼합"], horizontal=True)

    quiz = []
    answer_sheet = []
    for i, (eng, kor) in enumerate(pairs, start=1):
        q_mode = mode
        if mode == "랜덤 혼합":
            q_mode = random.choice(["영어 → 뜻 (영어 빈칸)", "뜻 → 영어 (영어 빈칸)"])

        if q_mode == "영어 → 뜻 (영어 빈칸)":
            quiz.append(f"{i}. {eng} : (             )")
            answer_sheet.append(f"{i}. {eng} : {kor}")
        else:
            quiz.append(f"{i}. (             ) : {kor}")
            answer_sheet.append(f"{i}. {eng} : {kor}")

    st.text_area("📋 생성된 시험지", "\n".join(quiz), height=300)

    # 다운로드 파일 이름 정하기
    if selected_files and len(selected_files) == 1:
        base_filename = selected_files[0].replace(".txt", "")
    else:
        now = datetime.datetime.now()
        base_filename = now.strftime("%m%d_%H%M")

    # 다운로드 버튼
    quiz_text = "\n".join(quiz)
    st.download_button(
        label="📄 시험지 다운로드",
        data=quiz_text,
        file_name=f"{base_filename}_test.txt",
        mime="text/plain"
    )

    st.download_button(
        label="📄 답안지 다운로드",
        data="\n".join(answer_sheet),
        file_name=f"{base_filename}_solution.txt",
        mime="text/plain"
    )
