"""Peewee migrations -- 002_create_user_table.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

from datetime import datetime
import peewee as pw
from peewee_migrate import Migrator

SQL = pw.SQL


def migrate(migrator: Migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    @migrator.create_model
    class User(pw.Model):
        name = pw.TextField(null=False)
        email = pw.TextField(null=False, unique=True)
        password = pw.TextField(null=False)
        is_admin = pw.BooleanField(null=False)
        created_at = pw.DateTimeField(null=False, default=datetime.now())


def rollback(migrator: Migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    migrator.remove_model('user')
