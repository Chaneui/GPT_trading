import streamlit as st

# 사이드바에 텍스트 입력 위젯 추가
user_name = st.sidebar.text_input('이름을 입력해 주세요:')

# 사이드바에 슬라이더 추가
user_age = st.sidebar.slider('나이:', 0, 100, 25)

# 사이드바에 버튼 추가
submit_button = st.sidebar.button('제출')

# 버튼이 클릭되면 메인 페이지에 사용자 정보 표시
if submit_button:
    st.write(f'안녕하세요, {user_name}님!')
    st.write(f'당신의 나이는 {user_age}살입니다.')
    

# 2개의 컬럼 생성
col1, col2 = st.columns(2)

# 첫 번째 컬럼에 콘텐츠 배치
with col1:
    st.header("첫 번째 컬럼")
    st.image("image1.jpg")

# 두 번째 컬럼에 콘텐츠 배치
with col2:
    st.header("두 번째 컬럼")
    st.image("image2.jpg")
    
# 탭 컨테이너 생성
tab1, tab2 = st.tabs(["탭 1", "탭 2"])

# 첫 번째 탭에 콘텐츠 추가
with tab1:
    st.header("이것은 첫 번째 탭입니다")
    st.write("여기에는 첫 번째 탭의 콘텐츠가 표시됩니다.")

# 두 번째 탭에 콘텐츠 추가
with tab2:
    st.header("이것은 두 번째 탭입니다")
    st.write("여기에는 두 번째 탭의 콘텐츠가 표시됩니다.")