from db import db
from models import ComplaintModel, RoleType, State


class ComplaintManager:
    @staticmethod
    def get_complaints(user):
        if user.role == RoleType.complainer:
            return ComplaintModel.query.filter_by(complainer_id=user.id).all()
        return ComplaintModel.query.all()

    @staticmethod
    def create(data, user):
        data["complainer_id"] = user.id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        return complaint

    @staticmethod
    def approve(complaint_id):
        ComplaintModel.query.filter_by(id=complaint_id).update({"status": State.approved})

    @staticmethod
    def reject(complaint_id):
        ComplaintModel.query.filter_by(id=complaint_id).update({"status": State.rejected})
