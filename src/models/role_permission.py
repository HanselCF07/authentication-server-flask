# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields
from src.models import role


class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    __table_args__ = {'schema': 'vg_store'}

    role_permission_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    role_id = db.Column(db.ForeignKey('vg_store.role.role_id'))
    permission = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    role = db.relationship('Role', primaryjoin='RolePermission.role_id == Role.role_id', backref='role_permissions')

    # Constructor
    def __init__(self, role_id=None, permission=None):
        self.role_id = role_id
        self.permission = permission


# Schema for serialization
class RolePermissionSchema(ma.SQLAlchemyAutoSchema):
    role = ma.Nested("RoleSchema")
    class Meta:
        model = RolePermission
        include_fk = True
        load_instance = True
    
    # role_permission_id = fields.Int(dump_only=True)
    # role_id = fields.Int()
    # permission = fields.Str(required=True)
    # created_at = fields.DateTime(dump_only=True)
    # record_status = fields.Int(dump_only=True)
    # role = fields.Nested("RoleSchema", dump_only=True)

