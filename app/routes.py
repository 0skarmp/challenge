from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import Contact
from app.db import db
from app.schemas import ContactSchema

contacts_bp = Blueprint('contacts', __name__)
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


# GET ALL CONTACTS
@contacts_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """
    List contacts with pagination and optional email filter
    ---
    tags:
      - Contacts
    parameters:
      - name: page
        in: query
        type: integer
        required: false
      - name: limit
        in: query
        type: integer
        required: false
      - name: email
        in: query
        type: string
        required: false
    responses:
      200:
        description: List of contacts
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    email = request.args.get('email')

    query = Contact.query

    if email:
        query = query.filter(Contact.email.contains(email))

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "total": pagination.total,
        "page": page,
        "limit": limit,
        "data": contacts_schema.dump(pagination.items)
    })


# GET CONTACT BY ID
@contacts_bp.route('/contacts/<int:id>', methods=['GET'])
def get_contactById(id):
    """
    Get contact by ID
    ---
    tags:
      - Contacts
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Contact found
      404:
        description: Contact not found
    """
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    return jsonify(contact_schema.dump(contact))


# CREATE CONTACT
@contacts_bp.route("/contacts", methods=["POST"])
def create_contact():
    """
    Create a new contact
    ---
    tags:
      - Contacts
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - lastname
            - email
          properties:
            name:
              type: string
            lastname:
              type: string
            email:
              type: string
            address:
              type: string
            reference_address:
              type: string
            phone_number:
              type: string
    responses:
      201:
        description: Contact created
      400:
        description: Validation error
      409:
        description: Email already exists
    """
    data = request.json

    errors = contact_schema.validate(data)
    if errors:
        return errors, 400

    contact = Contact(**data)

    try:
        db.session.add(contact)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already exists"}, 409

    return contact_schema.dump(contact), 201


# UPDATE CONTACT
@contacts_bp.route("/contacts/<int:id>", methods=["PUT"])
def update_contact(id):
    """
    Update a contact
    ---
    tags:
      - Contacts
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            lastname:
              type: string
            email:
              type: string
            address:
              type: string
            reference_address:
              type: string
            phone_number:
              type: string
    responses:
      200:
        description: Contact updated
      404:
        description: Contact not found
      409:
        description: Email already exists
    """
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404

    data = request.json

    errors = contact_schema.validate(data)
    if errors:
        return errors, 400

    for key, value in data.items():
        setattr(contact, key, value)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already exists"}, 409

    return contact_schema.dump(contact)



# DELETE CONTACT
@contacts_bp.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    """
    Delete a contact
    ---
    tags:
      - Contacts
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Contact deleted
      404:
        description: Contact not found
    """
    contact = Contact.query.get(id)
    if not contact:
        return {"error": "Contact not found"}, 404

    db.session.delete(contact)
    db.session.commit()

    return {"message": "Deleted successfully"}