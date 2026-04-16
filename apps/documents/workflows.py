from .emails import send_document_email


def generate_and_send_document(document):
    return send_document_email(document)