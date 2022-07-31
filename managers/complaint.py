from db import db
from models import ComplaintModel, RoleType, TransactionModel
from services.wise import WiseService
import os
import uuid

from constants import TEMP_FILE_FOLDER
from models.enums import State
from services.s3 import S3Service
from helpers.photo_decode_helper import decode_photo

wise_service = WiseService()
s3 = S3Service()


class ComplaintManager:
    @staticmethod
    def get_complaints(user):
        if user.role == RoleType.complainer:
            return ComplaintModel.query.filter_by(complainer_id=user.id).all()
        return ComplaintModel.query.all()

    @staticmethod
    def create(data, user):
        """
        Decode the base64 encoded photo,
        uploads it to s3 and set the photo url to
        the s3 generated url.
        Flushes the row
        """
        data["complainer_id"] = user.id
        encoded_photo = data.pop("photo")
        extension = data.pop("photo_extension")
        name = f"{str(uuid.uuid4())}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}")
        decode_photo(path, encoded_photo)
        url = s3.upload_photo(path, name, extension)
        data["photo_url"] = url
        os.remove(path)

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
