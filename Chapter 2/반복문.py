# for 요소 in 시퀀스:
#     # 반복 실행할 코드
#     # ...

# for 반복문 예시
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 리스트 컴프리헨션
numbers = [1, 2, 3, 4, 5]
squared_numbers = [num ** 2 for num in numbers]
print(squared_numbers)

# range 함수의 이용
for number in range(1, 5):
    print(number)

# for 반복문의 활용1
numbers = [1, 2, 3, 4, 5]
sum_result = 0
for number in numbers:
    sum_result += number
print(sum_result)

# for 반복문의 활용2
numbers = [10, 25, 30, 15, 40, 50]
# 20보다 큰 숫자만 출력
for number in numbers:
    if number > 20:
        print(number)

# for 반복문의 활용3
numbers = [10, 20, 30, 40, 50]
# 30 이상의 숫자가 나오면 종료
for number in numbers:
    if number >= 30:
        break
    print(number)

# while 반복문의 기본 구조
# while 조건:
#     # 조건이 참일 동안 실행되는 코드
#     # ...

# while 반복문 예시1
count = 0
while count < 5:
    print(f"현재 카운터 값: {count}")
    count += 1

# while 반복문 예시2
while True:
    user_input = input("종료하려면 'exit'을 입력하세요: ")
         
    if user_input.lower() == "exit":
        break
    print(f"사용자 입력: {user_input}")
