# 사용자 정의 함수의 기본 구조
def function_name(parameters):
    # 함수 내용
    # ...
    return result # 함수의 결과값 (생략 가능)

# 사용자 정의 함수의 정의와 호출 예시1
def add_numbers(x, y):
    return x + y
print(add_numbers(3, 5))

# 사용자 정의 함수의 정의와 호출 예시2
def square(x=2):
    return x ** 2
result = square()
print(result) 
result = square(4)
print(result) 

# 사용자 정의 함수의 정의와 호출 예시3
def calculate(x, y):
    sum_result = x + y
    product_result = x * y
    return sum_result, product_result
sum_result, product_result = calculate(3, 4)
print(f"Sum: {sum_result}, Product: {product_result}")

# 람다함수의 정의와 호출 예시
multiply = lambda x, y: x * y
result = multiply(4, 6)
print(result)

# 파이썬 내장 함수 len, type
my_list = [1, 2, 3, 4, 5]
length = len(my_list)
print(length)

value = 42
value_type = type(value)
print(value_type)

# 파이썬 내장 함수 sum, round
numbers = [1, 2, 3, 4, 5]
sum_result = sum(numbers)
print(sum_result)

value = 3.14159
rounded_value = round(value, 2)
print(rounded_value)

# 파이썬 내장 함수 str
number = 42
number_str = str(number)
print(type(number_str))

# 은행 클래스 예시
class Bank:
    def __init__(self, balance=0):
        self.balance = balance
    def deposit(self, amount):
        """예금 메서드"""
        self.balance += amount # 속성
        return f"{amount}원이 예금되었습니다. 현재 잔액: {self.balance}원"
    def withdraw(self, amount):
        """인출 메서드"""
        if amount <= self.balance:
            self.balance -= amount
            return f"{amount}원이 인출되었습니다. 현재 잔액: {self.balance}원"
        else:
            return "잔액이 부족합니다."
    def loan(self, amount):
        """대출 메서드"""
        self.balance += amount
        return f"{amount}원이 대출되었습니다. 현재 잔액: {self.balance}원"
    
my_bank = Bank(1000) # my_bank 인스턴스

print(my_bank.deposit(2000))
print(my_bank.withdraw(1500))
print(my_bank.loan(3000))

# 모듈 생성 및 사용
import my_module
result = my_module.greet("Alice")
print(result)
value = my_module.square(4)
print(value)

# 파이썬 표준 라이브러리 모듈
import math
result = math.sqrt(25)
print(result)

import os
files_in_directory = os.listdir()
print(files_in_directory)

from datetime import datetime
current_time = datetime.now()
print(current_time)