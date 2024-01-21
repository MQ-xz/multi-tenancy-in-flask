import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context
from sqlalchemy import engine_from_config, text
from sqlalchemy.pool import NullPool

from src.models.public import Shop

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions["migrate"].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions["migrate"].db.engine


def get_engine_url():
    try:
        return (
            get_engine()
            .url.render_as_string(hide_password=False)
            .replace("%", "%%")
        )
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option("sqlalchemy.url", get_engine_url())
target_db = current_app.extensions["migrate"].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# list of tenants
tenants = [tenant.id for tenant in Shop.query.all()]
# for initial migration we just use test schema
tenants = ["test"]


def get_metadata():
    if hasattr(target_db, "metadatas"):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Updated migration script for handling schema based multi-tenancy

    ref:
     - https://alembic.sqlalchemy.org/en/latest/cookbook.html#rudimental-schema-level-multi-tenancy-for-postgresql-databases # noqa
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )

    with connectable.connect() as connection:
        for tenant in tenants:
            logger.info(f"Migrating tenant: {tenant}")
            # set search path on the connection, which ensures that
            # PostgreSQL will emit all CREATE / ALTER / DROP statements
            # in terms of this schema by default
            connection.execute(text(f'SET search_path TO "{tenant}"'))
            # in SQLAlchemy v2+ the search path change needs to be committed
            # connection.commit()

            # make use of non-supported SQLAlchemy attribute to ensure
            # the dialect reflects tables in terms of the current tenant name
            connection.dialect.default_schema_name = tenant

            context.configure(
                connection=connection,
                target_metadata=get_metadata(),
            )

            with context.begin_transaction():
                context.run_migrations()

            # for checking migrate or upgrade is running
            if getattr(config.cmd_opts, "autogenerate", False):
                break


if context.is_offline_mode():
    # run_migrations_offline()
    # avoid running migrations offline since we have multiple schemas and names are taken from db
    raise Exception("Offline migrations are not supported.")
else:
    run_migrations_online()
