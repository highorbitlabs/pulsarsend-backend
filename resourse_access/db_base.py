# Import all the models, so that Base has them before being
# imported by Alembic
from .db_base_class import Base
from .models.user_models import UserDB
