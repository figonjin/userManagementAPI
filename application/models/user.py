import json
import sqlalchemy as sa

from application.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    username = sa.Column(sa.String(20), nullable=False, unique=True)
    email = sa.Column(sa.String(100), nullable=False, unique=True)
    address_id = sa.Column(sa.Integer, sa.ForeignKey("addresses.id"), nullable=True)
    address = db.relationship("Address", backref="users")
    phone = sa.Column(sa.String(10), nullable=False, unique=True)
    website = sa.Column(sa.String(100))
    company_id = sa.Column(sa.Integer, sa.ForeignKey("companies.id"), nullable=True)
    company = db.relationship("Company", backref="users")

    def __repr__(self):
        return f"<User {self.id}: {self.name} ({self.email}, {self.phone}, " \
               f"{self.website}), {self.address}, {self.company}"


class Address(db.Model):
    __tablename__ = "addresses"

    id = sa.Column(sa.Integer, primary_key=True)
    street = sa.Column(sa.String(100), nullable=False)
    suite = sa.Column(sa.String(100))
    city = sa.Column(sa.String(100), nullable=False)
    zipcode = sa.Column(sa.String(10))
    geo_id = sa.Column(sa.Integer, sa.ForeignKey("geolocations.id"), nullable=True)
    geo = db.relationship("Geolocation", backref="addresses")

    def __repr__(self):
        return f"<Address {self.id}: {self.suite} - {self.street}, {self.city}, {self.zipcode}, {self.geo}>"


class Geolocation(db.Model):
    __tablename__ = "geolocations"

    id = sa.Column(sa.Integer, primary_key=True)
    lat = sa.Column(sa.String(100))
    lng = sa.Column(sa.String(100))

    def __repr__(self):
        return f"<Geolocation {self.id}: {self.lat} {self.lng}>"


class Company(db.Model):
    __tablename__ = "companies"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    catchPhrase = sa.Column(sa.String(100))
    bs = sa.Column(sa.String(100))

    def __repr__(self):
        return f"<Company {self.id}: {self.name}, {self.catchPhrase}, {self.bs}>"
