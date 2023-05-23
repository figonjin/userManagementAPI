import sqlalchemy as sa
import json

from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from markupsafe import Markup
from flask import jsonify
from geopy.geocoders import Nominatim

from application.utils.assorted import validate_fields, validate_input

from application.models.user import User, Address, Geolocation, Company

mandatory_user_fields = ["name", "username", "email", "phone"]
mandatory_address_fields = ["street", "city", "zipcode"]


def create_user_data(data):
    missing_fields = validate_fields(data, mandatory_user_fields)
    if missing_fields:
        missing_fields_str = ", ".join(missing_fields)
        return f"The following user fields are mandatory {missing_fields_str}"

    name = Markup.escape(data.get("name"))
    username = Markup.escape(data.get("username"))
    email = Markup.escape(data.get("email"))
    phone = Markup.escape(data.get("phone"))
    website = Markup.escape(data.get("website"))
    company_data = data.get("company")
    address_data = data.get("address")

    user = User(name=name, username=username, email=email, phone=phone)
    if website is not None or website != "":
        user.website = website

    if address_data is not None and address_data != "":
        mandatory_fields = validate_fields(address_data, mandatory_address_fields)
        if not mandatory_fields:
            street = Markup.escape(address_data["street"])
            city = Markup.escape(address_data["city"])
            zipcode = Markup.escape(address_data["zipcode"])
            address = Address(street=street,
                              city=city,
                              zipcode=zipcode)
            if "suite" in address_data:
                address.suite = Markup.escape(address_data["suite"])
            geolocator = Nominatim(user_agent="my_geocoder")
            location = geolocator.geocode(f"{street}, {city}")
            address.geo = Geolocation(lat=location.latitude if location else -1,
                                      lng=location.longitude if location else -1)
            user.address = address
        else:
            missing_fields_str = ", ".join(mandatory_fields)
            return f"The following address fields are mandatory {missing_fields_str}"

    if company_data is not None and company_data != "":
        mandatory_fields = validate_fields(company_data, ["name"])
        if not mandatory_fields:
            name = Markup.escape(company_data["name"])
            company = Company(name=name)
            if "catchPhrase" in company_data:
                company.catchPhrase = Markup.escape(company_data["catchPhrase"])
            if "bs" in company_data:
                company.bs = Markup.escape(company_data["bs"])
            user.company = company
        else:
            missing_fields_str = ", ".join(mandatory_fields)
            return f"The following company fields are mandatory {missing_fields_str}"

    return user


class UserService:

    def __init__(self, db):
        self.db = db

    def user_list(self, param=None):
        allowed_parameters = ["name"]
        param = Markup.escape(param)
        query = self.db.session.execute(sa.select(User).order_by(
            getattr(User, param) if param and param in allowed_parameters else User.id
        ))
        users = [row for row in query.scalars()]
        user_data = []
        for user in users:
            address_data = None
            if user.address:
                geo_data = None
                if user.address.geo:
                    geo_data = {
                        'lat': user.address.geo.lat,
                        'lng': user.address.geo.lng
                    }
                address_data = {
                    'street': user.address.street,
                    'suite': user.address.suite,
                    'city': user.address.city,
                    'zipcode': user.address.zipcode,
                    'geo': geo_data
                }
            company_data = None
            if user.company:
                company_data = {
                    'name': user.company.name,
                    'catchPhrase': user.company.catchPhrase,
                    'bs': user.company.bs
                }
            user_dict = {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'address': address_data,
                'phone': user.phone,
                'website': user.website,
                'company': company_data
            }
            user_data.append(user_dict)
        json_data = json.dumps(user_data)
        return json_data

    def user_by_id(self, uid):
        user = self.db.get_or_404(User, uid)
        geo_data = None
        if user.address.geo:
            geo_data = {
                'lat': user.address.geo.lat,
                'lng': user.address.geo.lng
            }
        address_data = None
        if user.address:
            address_data = {
                'street': user.address.street,
                'suite': user.address.suite,
                'city': user.address.city,
                'zipcode': user.address.zipcode,
                'geo': geo_data
            }
        company_data = None
        if user.company:
            company_data = {
                'name': user.company.name,
                'catchPhrase': user.company.catchPhrase,
                'bs': user.company.bs
            }
        user_dict = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'address': address_data,
            'phone': user.phone,
            'website': user.website,
            'company': company_data
        }
        return json.dumps(user_dict)

    def create_user(self, user_data):
        if isinstance(user_data, dict):
            data = create_user_data(user_data)
            if isinstance(data, User):
                self.db.session.add(data)
            else:
                return jsonify({"message": f"Failed to create entries with the following error\n{data}"}),\
                    400

        elif isinstance(user_data, list):
            users = []
            for i in user_data:
                data = create_user_data(i)
                if isinstance(data, User):
                    users.append(data)
                else:
                    return jsonify({"message": f"Failed to create entries with the following error\n{data}"}), \
                        400
            self.db.session.add_all(users)

        else:
            return jsonify({"message": f"Failed to create entries with the following error\n"
                                       f"Unknown Data Format"}),\
                400
        try:
            self.db.session.commit()
        except IntegrityError:
            return jsonify({"message": "One of the entries already exists"}), 400
        return jsonify({"message": "Entries successfully created"}), 201

    def delete_user(self, uid):
        try:
            user = self.db.session.query(User).get(uid)
            self.db.session.delete(user)
            self.db.session.commit()
            return jsonify({"message": "User successfully deleted"}), 200
        except UnmappedInstanceError:
            return jsonify({"message": f"User {uid} does not exist"}), 404

    def modify_user(self, uid, data):
        user = self.db.get_or_404(User, uid)

        user.name = Markup.escape(validate_input(user.name, data.get("name")))
        user.username = Markup.escape(validate_input(user.username, data.get("username")))
        user.email = Markup.escape(validate_input(user.email, data.get("email")))
        user.phone = Markup.escape(validate_input(user.phone, data.get("phone")))
        user.website = Markup.escape(validate_input(user.website, data.get("website")))

        address_data = data.get("address")
        company_data = data.get("company")

        if address_data is not None and address_data != "":
            mandatory_fields = validate_fields(address_data, mandatory_address_fields)
            if not mandatory_fields:
                street = Markup.escape(address_data["street"])
                city = Markup.escape(address_data["city"])
                zipcode = Markup.escape(address_data["zipcode"])
                address = Address(street=street,
                                  city=city,
                                  zipcode=zipcode)
                if "suite" in address_data:
                    address.suite = Markup.escape(address_data["suite"])
                if "geo" in address_data:
                    # TODO: Implement geocoding
                    pass
                user.address = address
            else:
                missing_fields_str = ", ".join(mandatory_fields)
                return jsonify({"message":
                                f"The following address fields are mandatory {missing_fields_str}"}), 400

            if company_data is not None and company_data != "":
                mandatory_fields = validate_fields(company_data, ["name"])
                if not mandatory_fields:
                    name = Markup.escape(company_data["name"])
                    company = Company(name=name)
                    if "catchPhrase" in company_data:
                        company.catchPhrase = Markup.escape(company_data["catchPhrase"])
                    if "bs" in company_data:
                        company.bs = Markup.escape(company_data["bs"])
                    user.company = company
                else:
                    missing_fields_str = ", ".join(mandatory_fields)
                    return jsonify({"message":
                                    f"The following company fields are mandatory {missing_fields_str}"}), 400

        self.db.session.commit()
        return jsonify({"message": f"User {uid} updated successfully"}), 200