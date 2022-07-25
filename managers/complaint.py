from db import db
from models import ComplaintModel, RoleType, State, TransactionModel
from services.wise import WiseService

wise_service = WiseService()


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
        db.session.flush()
        ComplaintManager.issue_transaction(
            data["amount"],
            f"{user.first_name} {user.last_name}",
            user.iban,
            complaint.id,
        )
        return complaint

    @staticmethod
    def approve(complaint_id):
        transaction = TransactionModel.query.filter_by(
            complaint_id=complaint_id
        ).first()
        wise_service.fund_transfer(transaction.transfer_id)
        ComplaintModel.query.filter_by(id=complaint_id).update(
            {"status": State.approved}
        )

    @staticmethod
    def reject(complaint_id):
        transaction = TransactionModel.query.filter_by(
            complaint_id=complaint_id
        ).first()
        wise_service.cancel_transfer(transaction.transfer_id)
        ComplaintModel.query.filter_by(id=complaint_id).update(
            {"status": State.rejected}
        )

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id):
        quote_id = wise_service.create_quote(amount)
        recipient_id = wise_service.create_recipient_account(full_name, iban)
        transfer_id = wise_service.create_transfer(recipient_id, quote_id)
        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": recipient_id,
            "amount": amount,
            "complaint_id": complaint_id,
        }
        transaction = TransactionModel(**data)
        db.session.add(transaction)
        db.session.flush()
