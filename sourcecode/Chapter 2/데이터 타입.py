# 정수형 변수 선언
age = 25
count = -10

# 실수형 변수 선언
height = 175.5
pi = 3.141592

# 문자열 변수 선언
name = "Alice"
message = 'Hello, Python!'

# 문자열 슬라이싱
message = "Hello, Python!"
print(message[7]) # P
print(message[1:5]) # ello

# 문자열 연결
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name) # John Doe

#문자열 메서드
# 문자열을 대문자로 변환
sentence = "Python is a powerful programming language."
upper_sentence = sentence.upper()
print(upper_sentence)

# lower 메서드를 사용하여 문자열을 소문자로 변환
lower_sentence = sentence.lower()
print(lower_sentence)

# split 메서드를 사용하여 공백을 기준으로 문자열을 분리
words = sentence.split()
print(words)

# True/False 직접 할당한 boolean 변수
is_sunny = True
is_raining = False

# 비교 연산자를 사용한 예시
age = 25
is_adult = age >= 18
print(is_adult)