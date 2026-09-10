from datetime import datetime

from sqlalchemy import select, func,delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_news_history(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    # 浏览历史存在 (user_id, news_id) 唯一约束，重复浏览时刷新浏览时间而不是再次插入
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()

    if history is not None:
        history.view_time = datetime.now()
        await db.commit()
        await db.refresh(history)
        return history

    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_news_history(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    count_query = select(func.count()).select_from(History).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size

    query = (
        select(News, History.view_time.label("history_time"), History.id.label("history_id"))
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset).limit(page_size)
    )

    result = await db.execute(query)
    rows = result.all()
    return rows, total

async def remove_news_history(
        db:AsyncSession,
        user_id:int,
        news_id:int
):
    stmt=delete(History).where(History.user_id==user_id,History.news_id==news_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount>0

async def remove_all_history(
        db:AsyncSession,
        user_id:int
):
    stmt=delete(History).where(History.user_id==user_id)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0