from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    username: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class EventBase(BaseModel):
    app_id: int
    customer_id: int
    instance_id: int
    queue_id: int
    script_id: int
    endpoint: str
    contact_id: Optional[str]   = None
    integration_id: Optional[int]   = None
    severity_id: int
    response_id: int
    url: Optional[str]   = None
    error: Optional[str]   = None
    error_description: Optional[str]   = None
    modality: int

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class CustomerBase(BaseModel):
    customer_id: int
    customer_name: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class InstanceBase(BaseModel):
    cloud_region: str
    service_id: str

class InstanceCreate(InstanceBase):
    pass

class InstanceResponse(InstanceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PlatformBase(BaseModel):
    app_id: str
    name: str

class PlatformCreate(PlatformBase):
    pass

class PlatformResponse(PlatformBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class QueueBase(BaseModel):
    queue_id: str
    queue_name: str

class QueueCreate(QueueBase):
    pass

class QueueResponse(QueueBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class IntegrationBase(BaseModel):
    integration_name: str

class IntegrationCreate(IntegrationBase):
    pass

class IntegrationResponse(IntegrationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SeverityBase(BaseModel):
    severity: str

class SeverityCreate(SeverityBase):
    pass

class SeverityResponse(SeverityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ResponseCodeBase(BaseModel):
    response_code: int
    response_description: str

class ResponseCodeCreate(ResponseCodeBase):
    pass

class ResponseCodeResponse(ResponseCodeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SriptBase(BaseModel):
    script_id: str
    script_type: str
    script_name: str

class SriptCreate(SriptBase):
    pass

class SriptResponse(SriptBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ModalityBase(BaseModel):
    modality: str

class ModalitytCreate(ModalityBase):
    pass

class ModalityResponse(ModalityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True



        