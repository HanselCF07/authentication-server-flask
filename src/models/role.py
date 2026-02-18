# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields


class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'schema': 'vg_store'}

    role_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    # Constructor
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

# schema for serialization
class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True