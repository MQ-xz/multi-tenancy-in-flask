"""Database related functions"""
from os import popen
from sqlalchemy import text
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import InternalError
from sqlalchemy.orm import sessionmaker, scoped_session

from src.extensions import db


class Database:
    """used for managing tenant databases related operations"""

    def __init__(self, tenant: str) -> None:
        self.schema = str(tenant)

    def get_engine(self):
        """create new schema engine"""
        return db.engine.execution_options(
            schema_translate_map={None: self.schema}
        )

    def get_session(self):
        """To get session of tenant/public database schema for quick use

        returns:
            session: session of tenant/public database schema
        """
        return scoped_session(
            sessionmaker(bind=self.get_engine(), expire_on_commit=True)
        )

    def create_schema(self):
        """create new database schema, mostly used on tenant creation"""
        try:
            db.session.execute(CreateSchema(self.schema))
            db.session.commit()
        except InternalError:
            db.session.rollback()
            db.session.close()

    def create_tables(self):
        """create tables in for schema"""
        db.metadata.create_all(self.get_engine())

    def switch_schema(self):
        """switch between tenant/public database schema"""
        db.session.execute(f'set search_path to "{self.schema}"')
        db.session.commit()

    def migrate_tenant_schema(self):
        """migrate tenant database schema for new tenant"""
        # Get the current revision for a database.
        # NOTE: using popen may have a minor performance impact on the application
        # you can store it in a different table in public schema and use it from there
        # may be a faster approach
        last_revision = popen("flask db heads -d migrations/tenant").read()
        last_revision = last_revision.splitlines()[-1].split(" ")[0]

        # creating revision table in tenant schema
        session = self.get_session()
        session.execute(
            text(
                f'CREATE TABLE "{self.schema}".alembic_version (version_num '
                "VARCHAR(32) NOT NULL)"
            )
        )
        session.commit()

        # Insert last revision to alembic_version table
        session.execute(
            text(
                f'INSERT INTO "{self.schema}".alembic_version (version_num) '
                "VALUES (:version)"
            ),
            {"version": last_revision},
        )
        session.commit()
        session.close()

    def create_tenant_schema(self):
        """create tenant used for creating new schema and its tables"""
        self.create_schema()
        self.create_tables()
        self.migrate_tenant_schema()
