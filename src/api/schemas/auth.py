from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator


class UserSchema(BaseModel):
    username: str = Field(
        BeforeValidator(lambda v: v.lower().strip()),
        min_length=6,
        max_length=25,
        pattern=r"^[a-zA-Z0-9_]+$",
    )


class UserCredentialsSchema(UserSchema):
    password: str = Field(
        BeforeValidator(lambda v: v.strip()),
        min_length=8,
        max_length=200,
        pattern=r"^[A-Za-z\d@$!%*?&]+$",
    )
