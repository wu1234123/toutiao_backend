from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


class HistoryNewsItemResponse(BaseModel):
    history_id: int = Field(..., alias="historyId")
    history_time: datetime = Field(..., alias="historyTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class HistoryListResponse(BaseModel):
    list: list[dict]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
