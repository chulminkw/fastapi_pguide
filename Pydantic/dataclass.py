from pydantic import BaseModel, ValidationError
from typing import List, Optional
import json

# Pydantic Model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None 

user = User(id=10, name="test_name", 
            email="tname@example.com", 
            age=40)

# 일반 클래스 선언
class UserClass:
    def __init__(self, id: int, name: str, 
                 email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"id: {self.id}, name: {self.name}"
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, 
                 email: {self.email}, age: {self.age}"

userobj = UserClass(10, 'test_name', 
                    'tname@example.com', 40)

print("userobj:", userobj, userobj.id)

# Pydantic Model 객체화. 
# User(10, 'test_name', 'tname@example.com', 40) 하지 않도록 유의
user = User(id=10, name="test_name", email="tname@example.com", age=40)
print("user:", user, user.id)

# dict keyword argument(kwargs)로 Pydantic Model 객체화
user_from_dict = User(**{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40})
print("user_from_dict:", user_from_dict, user_from_dict.id)

# json 문자열 기반 Pydantic Model 객체화. 
json_string = '{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40}'
json_dict = json.loads(json_string)
#print("json_dict type:", type(json_dict))
user_from_json = User(**json_dict)
print("user_from_json:", user_from_json, user_from_json.id)

# Pydantic Model의 상속
class AdvancedUser(User):
    advanced_level: int

#AdvancedUser(10, 'test_name', 'tname@example.com', 40, 10) 하지 않도록 유의
adv_user = AdvancedUser(id=10, name="test_name", email="tname@example.com", age=40, advanced_level=9)
print("adv_user:", adv_user)


# 내포된(Nested 된 Json) 데이터 기반 Pydantic Model 생성. 
class Address(BaseModel):
    street: str
    city: str

class UserNested(BaseModel):
    name: str
    age: int
    address: Address

# 내포된 Json 문자열에서 생성. 
json_string_nested = '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}'
json_dict_nested = json.loads(json_string_nested)

user_nested_01 = UserNested(**json_dict_nested)
print("user_nested_01:", user_nested_01, user_nested_01.address, user_nested_01.address.city)

# 인자로 전달 시 Nested 된 값을 dict 형태로 전달하여 생성.
user_nested_02 = UserNested(
    name="test_name", age=40, address = {"street": "123 Main St", "city": "Anytown"}
)
print("user_nested_02:", user_nested_02, user_nested_02.address, user_nested_02.address.city)

# python 기반으로 pydantic serialization
user_dump_01 = user.model_dump()
print(user_dump_01, type(user_dump_01))

# json 문자열 기반으로 pydantic serialization
user_dump_02 = user.model_dump_json()
print(user_dump_02, type(user_dump_02))
