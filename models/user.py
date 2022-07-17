from db import db
from models.enums import RoleType


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)


class ComplainerModel(BaseUserModel):
    __tablename__ = 'complainer'

    complaints = db.relationship('ComplaintModel', backref='complaints', lazy='dynamic')
    role = db.Column(
        db.Enum(RoleType),
        default=RoleType.complainer,
        nullable=False
    )


class ApproverModel(BaseUserModel):
    __tablename__ = 'approver'

    certificate = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum(RoleType),
        default=RoleType.approver,
        nullable=False
    )


class AdministratorModel(BaseUserModel):
    __tablename__ = 'administrator'

    role = db.Column(
        db.Enum(RoleType),
        default=RoleType.admin,
        nullable=False
    )
