from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)
from app.repositories.shipment import ShipmentRepository
from app.schemas.shipment import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentRead,
    ShipmentList,
)


class ShipmentService:
    def __init__(self, db: AsyncSession):
        self.shipment_repo = ShipmentRepository(db)

    async def create_shipment(self, shipment_data: ShipmentCreate) -> ShipmentRead:
        # Перевіряємо, чи вже існує відправлення з таким номером
        existing = await self.shipment_repo.find_one(
            tracking_number=shipment_data.tracking_number
        )
        if existing:
            raise ConflictException("Shipment with this tracking number already exists")

        new_shipment = await self.shipment_repo.add_one(shipment_data.model_dump())
        return ShipmentRead.model_validate(new_shipment)

    async def get_shipments(self, skip: int = 0, limit: int = 10) -> ShipmentList:
        total = await self.shipment_repo.count_all()
        page = (skip // limit) + 1
        shipments = await self.shipment_repo.find_all(skip=skip, limit=limit)
        return ShipmentList(
            items=[ShipmentRead.model_validate(s) for s in shipments],
            total=total,
            page=page,
            per_page=limit,
        )

    async def get_shipment(self, shipment_id: int) -> ShipmentRead:
        shipment = await self.shipment_repo.find_one(id=shipment_id)
        if not shipment:
            raise NotFoundException(f"Shipment with id {shipment_id} not found")
        return ShipmentRead.model_validate(shipment)

    async def update_shipment(
        self, shipment_id: int, shipment_data: ShipmentUpdate
    ) -> ShipmentRead:
        shipment = await self.get_shipment(shipment_id)

        update_data = shipment_data.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestException("No valid fields provided for update")

        updated_shipment = await self.shipment_repo.edit_one(shipment_id, update_data)
        return ShipmentRead.model_validate(updated_shipment)

    async def delete_shipment(self, shipment_id: int) -> ShipmentRead:
        shipment = await self.get_shipment(shipment_id)
        deleted_shipment = await self.shipment_repo.delete_one(shipment_id)
        return ShipmentRead.model_validate(deleted_shipment)

    async def update_status(self, shipment_id: int, status: str) -> ShipmentRead:
        shipment = await self.get_shipment(shipment_id)
        updated_shipment = await self.shipment_repo.edit_one(
            shipment_id, {"status": status, "updated_at": datetime.utcnow()}
        )
        return ShipmentRead.model_validate(updated_shipment)
