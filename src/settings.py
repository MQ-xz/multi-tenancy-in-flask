"""Few settings for the project"""


# NOTE: since this is a demo project, I'm just hardcoding the
# database URI. it is not a good practice to do so.
SQLALCHEMY_DATABASE_URI = (
    "postgresql://postgres:postgres@localhost:5432/postgres"
)
SQLALCHEMY_BINDS = {"public": SQLALCHEMY_DATABASE_URI}

JWT_SECRET_KEY = "super-secret"  # change this
