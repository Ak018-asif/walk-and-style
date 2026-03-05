from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.users.model import Address


class AddressService:
    @staticmethod
    async def create(db: AsyncSession, user_id: str, data: Address) -> Address:
        # if default unset others
        if data.is_default:
            result = await db.execute(select(Address).where(Address.user_id == user_id))
            for addr in result.scalars().all():
                addr.is_default = False
        address = Address(user_id=user_id, **data.model_dump())
        db.add(address)
        await db.commit()
        await db.refresh(address)
        return address

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: str) -> list[Address]:
        result = await db.execute(select(Address).where(Address.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, address_id: str, user_id: str) -> Address:
        result = await db.execute(select(Address).where(Address.id == address_id))
        address = result.scalar_one_or_none()
        if not address or address.user_id != user_id:
            raise ValueError("Address not found for user")
        return address

    @staticmethod
    async def update(db: AsyncSession, address_id: str, user_id: str, data: dict) -> Address:
        address = await AddressService.get_by_id(db, address_id, user_id)
        if data.get("is_default"):
            result = await db.execute(select(Address).where(Address.user_id == user_id))
            for addr in result.scalars().all():
                addr.is_default = False
        for key, value in data.items():
            if value is not None:
                setattr(address, key, value)
        await db.commit()
        await db.refresh(address)
        return address

    @staticmethod
    async def delete(db: AsyncSession, address_id: str, user_id: str) -> None:
        address = await AddressService.get_by_id(db, address_id, user_id)
        await db.delete(address)
        await db.commit()
