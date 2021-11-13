from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    rentals = db.relationship("Rental", back_populates="video", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    def to_dict_with_rentals(self):
        result = []
        for rental in self.rentals:
            if rental.checked_in == None:
                result.append({
                    "due_date": rental.due_date,
                    "name": rental.customer.name,
                    "phone": rental.customer.phone,
                    "postal_code": rental.customer.postal_code 
                })
        return result

