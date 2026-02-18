from fastapi import FastAPI
import database.db

import models.client_model
import models.role_model
import models.services_model
import models.user_model
import app.models.vehicle_services_model
import app.models.vehicle_model

from api.v1.role import role

app=FastAPI(
    title="Carwash system control",
    description="System for creating, storing information and selling a car wash"
)

database.db.Base.metadata.create_all(bind=database.db.engine)