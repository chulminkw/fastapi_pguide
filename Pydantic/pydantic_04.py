from pydantic import BaseModel, EmailStr, Field

'''
EmailStr: Validate Email Address
https://docs.pydantic.dev/2.8/api/networks/#pydantic.networks.EmailStr
'''

class UserEmail(BaseModel):
    email: EmailStr # 문자열 Email 검증. 
    #email: EmailStr = Field(..., max_length=40) #Field와 함께 사용.
    #email: EmailStr = Field(None, max_length=40, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') 

try:
    user_email = UserEmail(email="user@examples.com")
    print(user_email)
except ValueError as e:
    print(e)

'''
https://docs.pydantic.dev/2.8/api/networks/

1. HttpUrl: http 또는 https만 허용. TLD(top-level domain)와 host명 필요. 최대 크기 2083
- valid: https://www.example.com, http://www.example.com, http://example.com
- invalid: ftp://example.com

2. AnyUrl: http, https, ftp 등 어떤 프로토콜도 다 허용. host 명 필요하며 TLD 필요 없음. 
- valid: http://www.example.com ftp://example.com, ksp://example.com ftp://example
- invalid: ftp//example.com

3. AnyHttpUrl: http 또는 https만 허용, TLD는 필요하지 않고 host명은 필요.
- valid: https://www.example.com, http://www.example.com, http://example.com
- invalid: ftp://example.com

4. FileUrl: 파일 프로토콜만 허용. host 명이 필요하지 않음. 
- valid: file:///path/to/file.txt
'''
from pydantic import HttpUrl, AnyUrl, AnyHttpUrl, FileUrl

class UserResource(BaseModel):
    http_url: HttpUrl
    any_url: AnyUrl
    any_http_url: AnyHttpUrl
    file_url: FileUrl
    
try:
    user_resource = UserResource(
        http_url="https://www.example.com",
        any_url="ftp://example.com",
        any_http_url="http://www.example.com",
        file_url="file:///path/to/file.txt"
    )

    print(user_resource, user_resource.http_url)
except ValueError as e:
    print(f"Validation error: {e}")

# '''
# IP Addresses
# https://docs.pydantic.dev/2.8/api/networks/

# IPvAnyAddress:  IPv4Address or an IPv6Address.

# * valid: 192.168.1.1, 192.168.56.101
# * invalid: 999.999.999.999

# IPvAnyNetwork: IPv4Network or an IPv6Network.
# * valid: 192.168.1.0/24
# * invalid: 192.168.1.0/33

# IPvAnyInterface: IPv4Interface or an IPv6Interface.
# * valid: 192.168.1.1/24
# * invalid: 192.168.1.1/33

# '''
from pydantic import IPvAnyAddress, IPvAnyNetwork, IPvAnyInterface

class Device(BaseModel):
    ip_address: IPvAnyAddress
    network: IPvAnyNetwork
    interface: IPvAnyInterface

# Example usage
try:
    device = Device(
        ip_address="192.168.1.1",
        network="192.168.1.0/24",
        interface="192.168.1.0/24")
    print(device)
except ValueError as e:
    print(e)

# pip install pydantic-extra-types pycountry
# https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/
from pydantic_extra_types.country import CountryAlpha3

class Product(BaseModel):
    made_in: CountryAlpha3

product = Product(made_in="USA")
print(product)
#> made_in='USA'
