# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields
from src.models import user


class Customer(db.Model):
    __tablename__ = 'customer'
    __table_args__ = {'schema': 'vg_store'}

    customer_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('vg_store.user.user_id'))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='Customer.user_id == User.user_id', backref='customers')

    # Constructor
    def __init__(self, user_id=None, name=None, address=None, phone=None, status=None):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.phone = phone
        self.status = status


# Schema for serialization
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested("UserSchema")
    class Meta:
        model = Customer
        include_fk = True
        load_instance = True
    
    # customer_id = fields.Int(dump_only=True)
    # user_id = fields.Int()
    # name = fields.Str(required=True)
    # address = fields.Str()
    # phone = fields.Str()
    # status = fields.Int()
    # created_at = fields.DateTime(dump_only=True)
    # record_status = fields.Int(dump_only=True)
