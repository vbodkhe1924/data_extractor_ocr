# app/services/validation.py
from datetime import datetime

class Validator:
    def validate(self, data: dict) -> dict:
        # Validate date format
        try:
            datetime.strptime(data["date"], "%Y-%m-%d")
        except ValueError:
            data["date"] = datetime.now().strftime("%Y-%m-%d")
            
        # Validate total
        calculated_total = sum(item["total"] for item in data["line_items"])
        if abs(calculated_total - data["total"]) > 0.01:
            data["validation_errors"] = ["Total mismatch"]
            
        # Validate required fields
        required = ["vendor_name", "invoice_number", "date"]
        for field in required:
            if not data.get(field):
                data["validation_errors"] = data.get("validation_errors", []) + [f"Missing {field}"]
                
        return data