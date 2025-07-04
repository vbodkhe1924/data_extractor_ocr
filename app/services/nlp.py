from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

class NLPProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("impira/layoutlm-invoices")
        self.model = AutoModelForTokenClassification.from_pretrained("impira/layoutlm-invoices")
        self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer)
        
    def extract_entities(self, text: str) -> dict:
        entities = self.nlp(text)
        result = {
            "vendor_name": "",
            "invoice_number": "",
            "date": "",
            "total": 0.0,
            "line_items": []
        }
        
        current_item = {}
        for entity in entities:
            if entity["entity"].startswith("B-VENDOR"):
                result["vendor_name"] = entity["word"]
            elif entity["entity"].startswith("B-INVOICE_NUMBER"):
                result["invoice_number"] = entity["word"]
            elif entity["entity"].startswith("B-DATE"):
                result["date"] = entity["word"]
            elif entity["entity"].startswith("B-TOTAL"):
                result["total"] = float(entity["word"].replace("$", ""))
            elif entity["entity"].startswith("B-LINE_ITEM"):
                current_item["description"] = entity["word"]
            elif entity["entity"].startswith("I-QUANTITY"):
                current_item["quantity"] = float(entity["word"])
            elif entity["entity"].startswith("I-UNIT_PRICE"):
                current_item["unit_price"] = float(entity["word"])
                if current_item.get("description") and current_item.get("quantity"):
                    current_item["total"] = current_item["quantity"] * current_item["unit_price"]
                    result["line_items"].append(current_item)
                    current_item = {}
                    
        return result