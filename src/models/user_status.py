# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields


class UserStatus(db.Model):
    __tablename__ = 'user_status'
    __table_args__ = {'schema': 'vg_store'}

    status_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    # Constructor
    def __init__(self, name, description=None):
        self.name = name
        self.description = description


#Schema for serialization
class UserStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserStatus
        load_instance = True
