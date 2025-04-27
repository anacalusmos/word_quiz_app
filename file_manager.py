import os
import streamlit as st

def get_user_files(subject, user_folder):
    if not subject:
        return []
    folder_path = os.path.join(user_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return [f for f in os.listdir(folder_path) if f.startswith(f"{subject}_") and f.endswith(".txt")]

def save_wordlist(subject, filename, words, user_folder):
    if not subject or not filename or not words:
        st.warning("❗ 주제, 파일명, 단어쌍을 모두 입력해주세요.")
        return
    folder_path = os.path.join(user_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    full_filename = f"{subject}_{filename}.txt"
    with open(os.path.join(folder_path, full_filename), "w", encoding="utf-8") as f:
        f.write(words.strip())
    st.success(f"'{full_filename}' 파일로 저장되었습니다. 새로고침 후 불러올 수 있어요!")
    st.experimental_rerun()

def load_combined_wordlist(selected_files, subject, user_folder):
    combined_words = []
    for filename in selected_files:
        with open(os.path.join(user_folder, filename), "r", encoding="utf-8") as f:
            combined_words.append(f.read())
    combined_text = "\n".join(combined_words)
    st.session_state["combined_words"] = combined_text
    st.success(f"총 {len(selected_files)}개의 단어장을 합쳤습니다!")
