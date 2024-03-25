from models.users import User
from extensions import ma
from marshmallow.fields import String
from marshmallow import ValidationError, validates_schema, validate

# This Schema for Returing the user
class UserSchema(ma.SQLAlchemyAutoSchema):

    name = String(required=True, validate=[validate.Length(min=3, max=100)], error_messages={
        "required": "The name is required",
        "invalid": "The name is invalid and needs to be a string",
    })
    email = String(required=True, validate=[validate.Email()])

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")

        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")

    class Meta:
        model = User
        load_instance = True # Load the instance of the model : Use for update
        exclude = ["_password"]
        
# This Schema for Creating the user
class UserCreateSchema(UserSchema):
    password = String(
        required=True,
        validate=[validate.Regexp(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$", error="The password need to be at least 8 characters long, and have at least 1 of each of the following: lowercase letter, uppercase letter, special character, number.")],)