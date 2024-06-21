from pydantic import BaseModel


class Newsletters(BaseModel):
    group_name: str
    group_id: int
    mailing_times: str
    text: str
    status: bool