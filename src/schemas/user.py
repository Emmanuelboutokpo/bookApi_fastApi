from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class User(BaseModel):
    username : Annotated[str, Field(description="The username of the user", min_length=3, max_length=50)]
    first_name : Annotated[str, Field(description="The first name of the user", min_length=1, max_length=50)]
    last_name : Annotated[str, Field(description="The last name of the user", min_length=1, max_length=50)]
    email : EmailStr
    password : Annotated[str, Field(description="The password of the user", min_length=6, max_length=72)]



class UserLogin(BaseModel):
    email : EmailStr
    password : Annotated[str, Field(description="The password of the user", min_length=6, max_length=72)]