from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_document_pdf(document) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60
    lines = [
        "Selorya",
        "",
        f"Document Type: {document.document_type}",
        f"Document Number: {document.document_number}",
        f"Issue Date: {document.issue_date}",
        f"Status: {document.status}",
        "",
        f"Recipient: {document.recipient.full_name}",
        f"Recipient Email: {document.recipient.email}",
        "",
        f"Order ID: {document.order.id}",
        f"Order Status: {document.order.status}",
        f"Currency: {document.order.currency}",
        f"Subtotal: {document.order.subtotal}",
        f"Total Amount: {document.order.total_amount}",
        "",
        "Notes:",
        document.notes or "-",
    ]

    for line in lines:
        pdf.drawString(60, y, str(line))
        y -= 20
        if y < 60:
            pdf.showPage()
            y = height - 60

    pdf.save()
    value = buffer.getvalue()
    buffer.close()
    return value