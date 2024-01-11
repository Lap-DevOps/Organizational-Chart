from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from api.app.database import Base

db = SQLAlchemy(model_class=Base)
# migrate = Migrate(db)
bcrypt = Bcrypt()
