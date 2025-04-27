import streamlit as st

def show_guide():
    # 초기화
    if "show_guide" not in st.session_state:
        st.session_state.show_guide = False
    if "guide_dismissed" not in st.session_state:
        st.session_state.guide_dismissed = False

    # 안내 팝업 표시
    if st.session_state.show_guide:
        with st.expander("📘 단어시험 웹앱 사용 설명서 ", expanded=True):
            st.markdown("""
### 🧑‍🏫 단어장 사용 방법

**1️⃣ 단어자료 준비하기**  
✅ PPT 스크린샷을 찍고 ChatGPT에게 다음과 같이 요청하세요:  
이 이미지를 "영단어 / 뜻" 형식으로 바꿔줘.  
- 예시: metaphysis / 발허리의, 중족골의

✅ 메모장에 직접 작성 가능  
apple / 사과  
give up / 포기하다

> 📌 **형식**: 슬래시(/)로 구분, 뜻에 쉼표는 자유롭게 사용 가능

**2️⃣ .txt 파일로 저장하기**  
- 파일명: toeic.txt  
- 인코딩: UTF-8  
- 이 앱이 있는 폴더에 저장

**3️⃣ 웹앱에서 사용하기**  
- 단어장 선택 후 📥 불러오기  
- 📝 문제 생성으로 시험 시작!
            """)