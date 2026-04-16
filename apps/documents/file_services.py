from django.core.files.base import ContentFile
from .pdf import build_document_pdf


def document_file_name(document) -> str:
    return f"{document.document_number}.pdf"


def attach_pdf_to_document(document):
    pdf_bytes = build_document_pdf(document)
    file_name = document_file_name(document)
    document.file.save(file_name, ContentFile(pdf_bytes), save=False)
    document.save(update_fields=["file", "updated_at"])
    return document