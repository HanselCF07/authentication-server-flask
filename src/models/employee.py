# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields
from src.models import user


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = {'schema': 'vg_store'}

    employee_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('vg_store.user.user_id'))
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))    
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='Employee.user_id == User.user_id', backref='employees')

    # Constructor
    def __init__(self, user_id=None, name=None, position=None, status=None):
        self.user_id = user_id
        self.name = name
        self.position = position
        self.status = status


# Schema for serialization
class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested("UserSchema")
    class Meta:
        model = Employee
        include_fk = True
        load_instance = True

    # employee_id = fields.Int(dump_only=True)
    # user_id = fields.Int()
    # name = fields.Str(required=True)
    # position = fields.Str()
    # status = fields.Int()
    # created_at = fields.DateTime(dump_only=True)
    # record_status = fields.Int(dump_only=True)