import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

USER_FILE = "users.yaml"

def login_user():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            credentials = yaml.load(f, Loader=SafeLoader)
    else:
        credentials = {"usernames": {}}

    authenticator = stauth.Authenticate(
        credentials,
        "wordquiz_cookie",
        "auth_key",
        cookie_expiry_days=1
    )

    name, auth_status, username = authenticator.login("로그인", st.sidebar)

    if auth_status is False:
        st.error("❌ 유저명이나 비밀번호가 잘못되었습니다.")
        return authenticator, None, None
    elif auth_status is None:
        st.warning("🔒 로그인 정보를 입력해주세요.")
        return authenticator, None, None
    else:
        st.sidebar.success(f"✅ 환영합니다, {name}님!")
        return authenticator, username, name


def register_user():
    st.subheader("📝 신규 사용자 등록")
    new_username = st.text_input("사용자 ID")
    new_name = st.text_input("이름")
    new_password = st.text_input("비밀번호", type="password")
    confirm_password = st.text_input("비밀번호 확인", type="password")

    if st.button("✅ 회원가입"):
        if not new_username.strip() or not new_name.strip() or not new_password.strip() or not confirm_password.strip():
            st.warning("❗ 모든 항목을 입력해주세요.")
            return

        if new_password != confirm_password:
            st.warning("❗ 비밀번호가 일치하지 않습니다.")
            return

        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f:
                credentials = yaml.load(f, Loader=SafeLoader)
        else:
            credentials = {"usernames": {}}

        if new_username in credentials["usernames"]:
            st.error("❌ 이미 존재하는 사용자 ID입니다.")
            return

        hashed_pw = stauth.Hasher([new_password]).generate()[0]
        credentials["usernames"][new_username] = {
            "name": new_name,
            "password": hashed_pw
        }

        with open(USER_FILE, "w", encoding="utf-8") as f:
            yaml.dump(credentials, f)

        st.success("🎉 회원가입이 완료되었습니다! 로그인 탭에서 로그인하세요.")
