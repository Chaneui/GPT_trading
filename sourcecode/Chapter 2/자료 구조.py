# 리스트 생성
my_list = [1, 2, 3, "four", 5.0, 6, 'eight']

# 리스트 인덱싱
print(my_list[0])
print(my_list[3])

# 리스트 슬라이싱1
print(my_list[1:4]) #[2, 3, 'four']

# 리스트 슬라이싱2
print(my_list[2:-2]) #[3, 'four', 5.0]

# 리스트 슬라이싱3
print(my_list[3:])

# 리스트 슬라이싱4
print(my_list[1::2])  

# 덧셈, 두 개의 리스트를 합쳐 새로운 리스트 생성
list1 = [1, 2, 3]
list2 = [4, 5, 6]
result = list1 + list2
print(result)

# 곱셈, 리스트를 반복하여 새로운 리스트를 생성
list = [1, 2, 3]
print(list * 3)

# append, 리스트의 끝에 새로운 요소 추가
my_list = [1, 2, 3]
my_list.append(4)
print(my_list)

# pop, 지정된 인덱스의 요소 제거 후 반환, 
my_list = [1, 2, 3]
popped_value = my_list.pop(1)
print(popped_value)
print(my_list)

#sort, 리스트 정렬
my_list = [3, 1, 4, 1, 5, 9, 2]
my_list.sort()
print(my_list)

# 튜플 생성
my_tuple = (1, 2, 3, "four", 5.0)
print(my_tuple)

# 튜플의 불변성 예시 (에러 발생)
# my_tuple[0] = 0

# 딕셔너리 생성
my_dict = {'name': 'John', 'age': 25, 'city': 'New York'}

# 딕셔너리의 요소에 접근
print(my_dict['name'])
print(my_dict['age'])

# 딕셔너리 값 변경
my_dict['age'] = 26
# 딕셔너리에 새로운 요소 추가
my_dict['gender'] = 'Male'
# 딕셔너리의 키-값 쌍 출력
print(my_dict)

# del, 딕셔너리 요소 삭제
my_dict = {'name':'John', 'age': 25, 'city': 'New York'}
del my_dict['city']
print(my_dict)

# keys, 딕셔너리의 모든 키 출력
keys = my_dict.keys()
print(keys)
# values, 딕셔너리의 모든 값 출력
values = my_dict.values()
print(values)

# pop, 지정된 키에 해당하는 값을 제거 후 반환
my_dict = {'name': 'John', 'age': 25, 'city': 'New York'}
removed_value = my_dict.pop('age')
print(removed_value)
print(my_dict)

# update, 다른 딕셔너리나, 키:값 쌍으로 현 딕셔너리 업데이트
my_dict = {'name': 'John', 'age': 25, 'city': 'New York'}
new_data = {'age': 26, 'gender': 'Male'}
my_dict.update(new_data)
print(my_dict)

# 집합 생성
my_set = {1, 2, 2, 3, 3, 4, 5, 5}
print(my_set)

# 집합 연산: 합집합, 교집합, 차집합
set1 = {1, 2, 3, 4, 5}
set2 = {3, 4, 5, 6, 7}

union_set = set1 | set2
intersection_set = set1 & set2
difference_set = set1 - set2

print(union_set)
print(intersection_set)
print(difference_set)

# add, 집합에 새로운 원소 추가
my_set = {1, 2, 3}
my_set.add(4)
print(my_set)

# remove, 집합에서 특정 원소 제거
my_set = {1, 2, 3, 4}
my_set.remove(3)
print(my_set)

# issubset, 한 집합이 다른 집합의 부분집합인지 확인
set1 = {1, 2, 3}
set2 = {1, 2}
is_subset = set2.issubset(set1)
print(is_subset)
