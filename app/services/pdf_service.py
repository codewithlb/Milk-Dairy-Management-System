from reportlab.pdfgen import canvas


def generate_payment_receipt(payment, farmer, filename):
    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(170, 800, "MILK DAIRY RECEIPT")

    c.setFont("Helvetica", 12)

    y = 750

    # Calculate rate from payment
    rate = 0
    if payment.total_liters:
        rate = payment.total_amount / payment.total_liters

    c.drawString(50, y, f"Farmer Name : {farmer.name}")
    y -= 25

    c.drawString(50, y, f"Mobile : {farmer.mobile}")
    y -= 25

    c.drawString(50, y, f"From Date : {payment.from_date}")
    y -= 25

    c.drawString(50, y, f"To Date : {payment.to_date}")
    y -= 25

    c.drawString(50, y, f"Total Liters : {payment.total_liters}")
    y -= 25

    c.drawString(50, y, f"Rate : ₹{rate:.2f}")
    y -= 25

    c.drawString(50, y, f"Total Amount : ₹{payment.total_amount}")
    y -= 25

    c.drawString(50, y, f"Status : {payment.status}")
    y -= 25

    c.save()