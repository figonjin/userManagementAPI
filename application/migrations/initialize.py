import requests
import sqlalchemy as sa

from application.extensions import db
from application.models.user import User, Address, Geolocation, Company


def seed_db():
    r = requests.get("https://jsonplaceholder.typicode.com/users")
    json_data = None

    if r.status_code == 200:
        json_data = r.json()


    # TODO: Add Company
    if json_data is not None:
        for item in json_data:
            query = sa.select(User).filter_by(username=item["username"])
            result = db.session.execute(query)
            user = result.fetchone()
            address_data = item["address"]
            geo_data = address_data["geo"]
            if geo_data:
                geo = Geolocation(lat=geo_data["lat"], lng=geo_data["lng"])
            else:
                geo = None
            if address_data:
                address = Address(suite=address_data["suite"],
                                  street=address_data["street"],
                                  city=address_data["city"],
                                  zipcode=address_data["zipcode"],
                                  geo=geo)
            else:
                address = None
            company_data = item["company"]
            if company_data:
                company = Company(name=company_data["name"],
                                  catchPhrase=company_data["catchPhrase"],
                                  bs=company_data["bs"])
            else:
                company = None
            if user is None:
                user = User(
                    name=item["name"],
                    username=item["username"],
                    email=item["email"],
                    address=address,
                    phone=item["phone"],
                    website=item["website"],
                    company=company
                )
                db.session.add(user)
        db.session.commit()
