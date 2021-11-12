from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    rentals = db.relationship("Rental", back_populates="customer", lazy=True)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at
        }



    def to_dict_with_rentals(self):
        result = []
        for rental in self.rentals:
            if rental.checked_in == None:
                result.append( {
                    "release_date": rental.video.release_date,
                    "title": rental.video.title,
                    "due_date": rental.due_date
                })
        return result 