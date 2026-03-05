# api/v1/cashier.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from app.schemas.cashier import CashierDetail
from app.crud.cashier import get_cashier_report_by_id
# Importamos la dependencia de seguridad si quieres que solo el staff acceda
from app.api.v1.deps import get_current_staff 

router = APIRouter(prefix="/cashier", tags=["cashier"])

@router.get("/{service_id}", response_model=CashierDetail)
def get_payment_detail(
    service_id: int, 
    db: Session = Depends(get_db),
    # Descomenta la siguiente línea si quieres proteger la ruta:
    # current_user: dict = Depends(get_current_staff)
):
    """
    Obtiene el reporte detallado para cobro (JOIN de múltiples tablas).
    Muestra precios, descuentos, datos del vehículo, cliente y empleados.
    """
    detail = get_cashier_report_by_id(db, vs_id=service_id)
    
    if not detail:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró información de cobro para el ID de servicio: {service_id}"
        )
        
    return detail
