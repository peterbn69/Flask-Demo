from app.extensions import db


class ItemModel(db.Model):
    __tablename__ = "items"
    __table_args__ = (db.UniqueConstraint("store_id", "name"),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")

    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
