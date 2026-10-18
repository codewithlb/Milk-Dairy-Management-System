from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.units import mm


def generate_payment_receipt(
    payment,
    farmer,
    milk_collections,
    filename,
):
    """
    Generate detailed payment receipt.

    The receipt contains every milk collection
    between payment.from_date and payment.to_date.
    """

    # Landscape gives us enough space for all columns.
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    styles = getSampleStyleSheet()

    elements = []

    # ============================================================
    # TITLE
    # ============================================================

    title_style = styles["Title"]
    title_style.fontName = "Helvetica-Bold"
    title_style.fontSize = 20

    elements.append(
        Paragraph(
            "MILK DAIRY PAYMENT RECEIPT",
            title_style,
        )
    )

    elements.append(Spacer(1, 8))

    # ============================================================
    # FARMER / PAYMENT INFORMATION
    # ============================================================

    info_data = [
        [
            "Payment ID",
            str(payment.id),
            "Farmer Name",
            farmer.name,
        ],
        [
            "Farmer ID",
            str(payment.farmer_id),
            "Mobile",
            farmer.mobile or "",
        ],
        [
            "From Date",
            str(payment.from_date),
            "To Date",
            str(payment.to_date),
        ],
        [
            "Status",
            payment.status,
            "Payment Method",
            payment.payment_method or "-",
        ],
        [
            "Payment Date",
            str(payment.payment_date)
            if payment.payment_date
            else "-",
            "",
            "",
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            30 * mm,
            55 * mm,
            35 * mm,
            65 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, -2),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (2, 0),
                    (2, -2),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elements.append(info_table)

    elements.append(Spacer(1, 12))

    # ============================================================
    # MILK COLLECTION DETAILS
    # ============================================================

    elements.append(
        Paragraph(
            "Daily Milk Collection Details",
            styles["Heading2"],
        )
    )

    elements.append(Spacer(1, 5))

    table_data = [
        [
            "Date",
            "Shift",
            "Liters",
            "Fat",
            "SNF",
            "Rate",
            "Amount",
        ]
    ]

    total_liters = 0.0
    total_amount = 0.0

    # Sort collections by date and shift.
    sorted_collections = sorted(
        milk_collections,
        key=lambda x: (
            x.collection_date,
            x.shift or "",
        ),
    )

    for collection in sorted_collections:

        quantity = float(
            collection.quantity or 0
        )

        fat = float(
            collection.fat or 0
        )

        snf = float(
            collection.snf or 0
        )

        rate = float(
            collection.rate or 0
        )

        amount = float(
            collection.amount or 0
        )

        total_liters += quantity
        total_amount += amount

        table_data.append(
            [
                str(collection.collection_date),
                collection.shift or "-",
                f"{quantity:.2f}",
                f"{fat:.2f}",
                f"{snf:.2f}",
                f"₹{rate:.2f}",
                f"₹{amount:.2f}",
            ]
        )

    # ============================================================
    # TOTAL ROW
    # ============================================================

    table_data.append(
        [
            "",
            "TOTAL",
            f"{total_liters:.2f}",
            "",
            "",
            "",
            f"₹{total_amount:.2f}",
        ]
    )

    collection_table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            40 * mm,
            30 * mm,
            28 * mm,
            25 * mm,
            25 * mm,
            30 * mm,
            35 * mm,
        ],
    )

    collection_table.setStyle(
        TableStyle(
            [
                # Header
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    9,
                ),

                # Body
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    8,
                ),

                # Grid
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                # Alignment
                (
                    "ALIGN",
                    (2, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (1, -1),
                    "CENTER",
                ),

                # Total
                (
                    "BACKGROUND",
                    (0, -1),
                    (-1, -1),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, -1),
                    (-1, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, -1),
                    (-1, -1),
                    9,
                ),

                # Padding
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elements.append(collection_table)

    elements.append(Spacer(1, 15))

    # ============================================================
    # PAYMENT SUMMARY
    # ============================================================

    calculated_rate = 0

    if total_liters > 0:
        calculated_rate = (
            total_amount / total_liters
        )

    summary_data = [
        [
            "Total Milk",
            f"{total_liters:.2f} Liters",
        ],
        [
            "Average Rate",
            f"₹{calculated_rate:.2f}",
        ],
        [
            "Total Payment",
            f"₹{total_amount:.2f}",
        ],
        [
            "Payment Status",
            payment.status,
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            50 * mm,
            60 * mm,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (1, 0),
                    (1, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elements.append(summary_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "This is a computer-generated payment receipt.",
            styles["Normal"],
        )
    )

    # ============================================================
    # BUILD PDF
    # ============================================================

    doc.build(elements)