from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.model import Address
from app.modules.users.schema import AddressCreate, AddressUpdate


class AddressService:
    @staticmethod
    async def create(db: AsyncSession, user_id: str, data: AddressCreate) -> Address:
        """Create a new address for a user."""
        # If setting as default, unset others
        if data.is_default:
            result = await db.execute(
                select(Address).where(Address.user_id == user_id)
            )
            for addr in result.scalars().all():
                addr.is_default = False

        address = Address(user_id=user_id, **data.model_dump())
        db.add(address)
        await db.commit()
        await db.refresh(address)
        return address

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: str) -> list[Address]:
        """Get all addresses for a user."""
        result = await db.execute(
            select(Address).where(Address.user_id == user_id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, address_id: str, user_id: str) -> Address:
        """Get an address by ID and verify it belongs to the user."""
        result = await db.execute(select(Address).where(Address.id == address_id))
        address = result.scalar_one_or_none()
        if not address or address.user_id != user_id:
            raise ValueError("Address not found")
        return address

    @staticmethod
    async def update(
        db: AsyncSession, address_id: str, user_id: str, data: AddressUpdate
    ) -> Address:
        """Update an address."""
        address = await AddressService.get_by_id(db, address_id, user_id)

        # If setting as default, unset others
        if data.is_default:
            result = await db.execute(
                select(Address).where(Address.user_id == user_id)
            )
            for addr in result.scalars().all():
                addr.is_default = False

        # Update fields
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(address, field, value)

        await db.commit()
        await db.refresh(address)
        return address

    @staticmethod
    async def delete(db: AsyncSession, address_id: str, user_id: str) -> None:
        """Delete an address."""
        address = await AddressService.get_by_id(db, address_id, user_id)
        await db.delete(address)
        await db.commit()
