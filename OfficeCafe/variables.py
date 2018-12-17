"""
All static variables used in the system

Author: Himanshu Shankar (https://himanshus.com)
"""

GRAM = "G"
KILOGRAM = "KG"
PLATE = "PLT"
LITRE = "L"
MILLILITRE = "ML"
METER = "M"
KILOMETER = "KM"
MILLIMETER = "MM"
GLASS = "GLS"

UOM_CHOICES = (
    (GRAM, "Grams"),
    (KILOGRAM, "Kilo Grams"),
    (PLATE, "Plates"),
    (LITRE, "Litres"),
    (MILLILITRE, "Milli Litres"),
    (METER, "Meters"),
    (KILOMETER, "Kilo Meters"),
    (MILLIMETER, "Milli Meters"),
    (GLASS, "Glasses"),
)

NEW = "N"
ACCEPTED = "A"
REJECTED = "RJ"
CANCELLED = "C"
READY = "R"
PICKED_UP = "P"
OUT_FOR_DELIVERY = "O"
DELIVERED = "D"

STATUS_CHOICES = (
    (NEW, "New"),
    (ACCEPTED, "Accepted"),
    (REJECTED, "Rejected"),
    (CANCELLED, "Cancelled"),
    (READY, "Ready"),
    (PICKED_UP, "Picked Up"),
    (OUT_FOR_DELIVERY, "Out for Delivery"),
    (DELIVERED, "Delivered"),
)
