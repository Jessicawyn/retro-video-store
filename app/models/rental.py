from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import timedelta

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

    def get_videos_checked_out(self):
        return len([rental for rental in self.customer.rentals if rental.checked_in == None])

    def to_dict(self):
        result = {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": self.get_videos_checked_out(),
                "available_inventory": self.get_available_inventory(),
        }
        return result
    
    def overdue_to_dict(self):
        result = {
            "video_id": self.video_id,
            "title": self.video.title,
            "customer_id": self.customer_id,
            "name": self.customer.name,
            "postal_code": self.customer.postal_code,
            "checkout_date": self.due_date - timedelta(7),
            "due_date": self.due_date
        }
        
        return result


  
