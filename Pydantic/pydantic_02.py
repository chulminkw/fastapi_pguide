from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    # 문자열->숫자값 자동 파싱을 허용하지 않을 경우 Strict 모드로 설정. 
    #model_config = ConfigDict(strict=True)

    id: int
    name: str
    email: str
    addresses: List[Address]
    age: int | None = None # Optional[int] = None
    #개별 속성에 Strict 모드 설정 시 Field나 Annotated 이용. None 적용 시 Optional
    #age: int = Field(None, strict=True)
    #age: Annotated[int, Strict()] = None

#Pydantic Model 객체화 시 자동으로 검증 수행 수행하고, 검증 오류 시 ValidationError raise 
try:
    user = User(
        id=123,
        name="John Doe",
        email="john.doe@example.com",
        addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}],
        age="29" # 문자열 값을 자동으로 int 로 파싱함.
    )
    print(user)
except ValidationError as e:
    print("validation error happened")
    print(e)

