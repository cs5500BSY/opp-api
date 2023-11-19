from fastapi import FastAPI

import sys
print(sys.path)
sys.path.append("./")

# print(sys.path)

from .models import models
from .db import database
from .routers import auth, admin, example, payment

# application
app = FastAPI()

# sets up database defined in engine
models.Base.metadata.create_all(bind=database.engine)

# Set API endpoints on router
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(example.router)
app.include_router(payment.router)