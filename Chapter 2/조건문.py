# if 조건:
    # 조건이 참일 때 실행되는 코드
    # ...

# 조건문 활용 예시
# 숫자를 입력받아 양수 여부를 출력
number = int(input("숫자를 입력하세요: "))
# if 조건문
if number > 0:
    print("입력한 숫자는 양수입니다.")

score = int(input("점수를 입력하세요: "))
# 다중 조건문
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'
print(f"학점: {grade}")

# 중첩 조건문 예제
x = 10
y = 20
if x > 0:
    if y > 0:
        print("x와 y는 양수입니다.")
    else:
        print("x는 양수이고, y는 음수 또는 0입니다.")
else:
    print("x는 음수 또는 0입니다.")

# 복합 조건문
age = 25
is_student = True
if age >= 18 and is_student:
    print("성인 학생입니다.")
else:
    print("성인이거나 학생이 아닙니다.")

# 삼항 연산자를 활용한 한줄짜리 if문
number = 15
result = "짝수" if number % 2 == 0 else "홀수"
print(result)
