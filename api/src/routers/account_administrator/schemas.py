from uuid import UUID

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    displayName: str


class UserDisplay(BaseModel):
    id: UUID
    username: str
    displayName: str | None = None

    class Config:
        orm_mode = True


class CertificateBase(BaseModel):
    id: UUID
    publicKey: str

    class Config:
        orm_mode = True


class CertificateDisplay(BaseModel):
    id: UUID
    publicKey: str
    user: UserDisplay

    class Config:
        orm_mode = True
