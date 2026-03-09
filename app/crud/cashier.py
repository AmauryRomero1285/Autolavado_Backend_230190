from sqlalchemy.orm import Session, aliased
from app.models.user import User
from app.models.services import Service
from app.models.vehicle import Vehicle
from app.models.vehicle_service import VehicleService
from app.models.client import Client as ClientModel

def get_cashier_report_by_id(db: Session, vs_id: int):
    # Alias para los trabajadores (lavador y cajero) y el usuario final (cliente)
    Washer = aliased(User)
    Casher = aliased(User)
    ClientOwner = aliased(User)

    return db.query(
        VehicleService.id,
        Washer.first_name.label("nombre-lavador"),
        Casher.first_name.label("nombre-cajero"),
        Service.name.label("nombre-servicio"),
        Service.description.label("descripcion"),
        VehicleService.status.label("status"),
        VehicleService.service_price.label("service-price"),
        VehicleService.discount.label("discount"),
        VehicleService.total_price.label("total-price"),
        VehicleService.scheduled_at.label("scheduled-at"), 
        VehicleService.started_at.label("started-at"),
        VehicleService.finished_at.label("finished-at"),
        Vehicle.license_plate.label("license-plate"),
        Vehicle.brand.label("marca"),
        Vehicle.model.label("modelo"),
        Vehicle.color.label("color"),
        # Nombre del cliente obtenido a través del vehículo
        ClientOwner.first_name.label("nombre-cliente"),
        VehicleService.notes.label("notes")
    ).select_from(VehicleService)\
     .outerjoin(Washer, VehicleService.employee_washer_id == Washer.id)\
     .outerjoin(Casher, VehicleService.employee_casher_id == Casher.id)\
     .outerjoin(Service, VehicleService.service_id == Service.id)\
     .outerjoin(Vehicle, VehicleService.vehicle_id == Vehicle.id)\
     .outerjoin(ClientModel, Vehicle.client_id == ClientModel.id) \
     .outerjoin(ClientOwner, Vehicle.client_id == ClientOwner.id) \
     .filter(VehicleService.id == vs_id)\
     .first()
