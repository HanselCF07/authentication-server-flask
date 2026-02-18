# coding: utf-8
from src import db, ma
from marshmallow import Schema, fields


class Profile(db.Model):
    __tablename__ = 'profile'
    __table_args__ = {'schema': 'vg_store'}

    profile_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    record_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    # Constructor
    def __init__(self, name, description=None):
        self.name = name
        self.description = description


    # Example usage get all profiles with pagination and sorting
    def get_all_profiles(order_by='created_at', desc=True, limit=None, offset=None):
        try:
            query = Profile.query.filter_by(record_status=1)

            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            
            query = query.order_by(getattr(Profile, order_by).desc() if desc else getattr(Profile, order_by).asc())
            profiles = query.all()
            return ProfileSchema(many=True).dump(profiles)
        except Exception as e:
            print(f"Error fetching profiles")
            raise e

    # Example usage get profile by id
    def get_profile_by_id(profile_id):
        try:
            profile = Profile.query.get(profile_id)
            if profile:
                return ProfileSchema().dump(profile)
            return None
        except Exception as e:
            print(f"Error fetching profile")
            raise e

    # Example usage create profile
    def create_profile(name, description=None):
        try:
            new_profile = Profile(name=name, description=description)
            db.session.add(new_profile)
            db.session.flush()
            return ProfileSchema().dump(new_profile) # .only('profile_id', 'name', 'description', 'created_at')
        except Exception as e:
            print(f"Error creating profile")
            raise e

    # Example usage Bulk create profiles
    def bulk_create_profiles(profiles_data):
        try:
            new_profiles = [Profile(name=data['name'], description=data.get('description')) for data in profiles_data]
            db.session.bulk_save_objects(new_profiles)
            db.session.flush()
            return ProfileSchema(many=True).dump(new_profiles)
        except Exception as e:
            print(f"Error bulk creating profiles")
            raise e

    # Example usage update profile
    def update_profile(profile_id, name=None, description=None):
        try:
            profile = Profile.query.get(profile_id)
            if not profile:
                return None
            if name and profile.name != name:
                profile.name = name
            if description and profile.description != description:
                profile.description = description
            db.session.flush()
            return ProfileSchema().dump(profile)
        except Exception as e:
            print(f"Error updating profile")
            raise e

    # Example usage session bulk update mappings profiles
    def bulk_update_profiles(profiles_data):
        try:
            db.session.bulk_update_mappings(Profile, profiles_data)
            db.session.flush()
            return True
        except Exception as e:
            print(f"Error bulk updating profiles")
            raise e

    # Example usage delete profile
    def delete_profile(profile_id):
        try:
            profile = Profile.query.get(profile_id)
            if not profile:
                return False
            db.session.delete(profile)
            db.session.flush()
            return True
        except Exception as e:
            print(f"Error deleting profile")
            raise e


# schema for serialization
class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True


# Schema for deserialization
class ProfileCreateSchema(Schema):
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(dump_only=True)
    record_status = fields.Integer(dump_only=True)

