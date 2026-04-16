from django.core.mail import EmailMessage
from django.template.defaultfilters import title
from .models import Document


def document_email_subject(document: Document) -> str:
    label = title(document.document_type.replace("_", " "))
    return f"Selorya {label} {document.document_number}"


def document_email_body(document: Document) -> str:
    return (
        f"Hello {document.recipient.full_name},\n\n"
        f"your document {document.document_number} is ready.\n"
        f"Document type: {document.document_type}\n"
        f"Order ID: {document.order.id}\n\n"
        f"Best regards,\n"
        f"Selorya"
    )


def send_document_email(document: Document):
    email = EmailMessage(
        subject=document_email_subject(document),
        body=document_email_body(document),
        to=[document.recipient.email],
    )
    if document.file:
        document.file.open("rb")
        email.attach(
            filename=document.file.name.split("/")[-1],
            content=document.file.read(),
            mimetype="application/pdf",
        )
        document.file.close()
    email.send(fail_silently=False)
    document.status = "sent"
    document.save(update_fields=["status", "updated_at"])
    return document