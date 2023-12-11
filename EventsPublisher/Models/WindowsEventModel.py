from pydantic import BaseModel

class WindowsEventModel(BaseModel):
    UserName: str
    AppName: str
