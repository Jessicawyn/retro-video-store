from app import db
from app.models.video import Video
from app.models.customer import Customer

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime, nullable = False)
    checked_in = db.Column(db.DateTime, nullable = True)
    customer = db.relationship("Customer", back_populates="rentals")
    video = db.relationship("Video", back_populates="rentals")

    
    def get_available_inventory(self):
        return self.video.total_inventory - len([rental for rental in self.video.rentals if rental.checked_in == None])

    def to_dict(self):
        result = {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": len([rental for rental in self.customer.rentals if rental.checked_in == None]),
                "available_inventory": self.get_available_inventory(),
        }
        return result
    
    def customer_list_to_dict(self):
        return {
            "due_date": self.due_date,
            "name": self.customer.name,
            "phone": self.customer.phone,
            "postal_code": self.customer.postal_code          
        }
    
    def movie_list_to_dict(self):
        return {
            "release_date": self.video.release_date,
            "title": self.video.title,
            "due_date": self.due_date
        }