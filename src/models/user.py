# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields
from src.models import profile, role, user_status


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'vg_store'}

    user_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_public_key = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    user_status_id = db.Column(db.ForeignKey('vg_store.user_status.status_id'))
    role_id = db.Column(db.ForeignKey('vg_store.role.role_id'))
    profile_id = db.Column(db.ForeignKey('vg_store.profile.profile_id'))
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    profile = db.relationship('Profile', primaryjoin='User.profile_id == Profile.profile_id', backref='users')
    role = db.relationship('Role', primaryjoin='User.role_id == Role.role_id', backref='users')
    user_status = db.relationship('UserStatus', primaryjoin='User.user_status_id == UserStatus.status_id', backref='users')

    # Constructor
    def __init__(self, user_public_key=None, username=None, password=None, email=None, user_status_id=None, role_id=None, profile_id=None):
        self.user_public_key = user_public_key
        self.username = username
        self.password = password
        self.email = email
        self.user_status_id = user_status_id
        self.role_id = role_id
        self.profile_id = profile_id


# Schema for serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    profile = ma.Nested('ProfileSchema', only=['profile_id', 'name'])
    role = ma.Nested('RoleSchema', only=['role_id', 'name'])
    user_status = ma.Nested('UserStatusSchema', only=['status_id', 'name'])
    class Meta:
        model = User
        include_fk = True
        load_instance = True
    
    # user_id = fields.Int(dump_only=True)
    # user_public_key = fields.Str(dump_only=True)
    # username = fields.Str(required=True)
    # email = fields.Email(required=True)
    # password = fields.Str(load_only=True, required=True)
    # user_status_id = fields.Int()
    # role_id = fields.Int()
    # profile_id = fields.Int()
    # created_at = fields.DateTime(dump_only=True)
    # record_status = fields.Int(dump_only=True)


class UserCustomerCreateSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)


