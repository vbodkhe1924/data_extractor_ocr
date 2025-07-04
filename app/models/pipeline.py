# app/models/pipeline.py
import logging
from app.services.ocr import OCRProcessor
from app.services.nlp import NLPProcessor
from app.services.validation import Validator
from app.storage.database import Database

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InvoicePipeline:
    def __init__(self):
        """
        Initialize the InvoicePipeline with OCR, NLP, validation, and database components.
        """
        self.ocr = OCRProcessor()
        self.nlp = NLPProcessor()
        self.validator = Validator()
        self.db = Database()
        
    def process_document(self, content: bytes, filename: str) -> dict:
        """
        Process an uploaded document (PDF or image) to extract invoice data.
        
        Args:
            content (bytes): The binary content of the uploaded file.
            filename (str): The name of the uploaded file.
            
        Returns:
            dict: A dictionary containing the document ID, extracted data, and raw text.
        """
        logger.debug(f"Processing file: {filename}")
        text = self.ocr.extract_text(content)
        logger.debug(f"Raw OCR text: {text}")
        entities = self.nlp.extract_entities(text)
        logger.debug(f"Extracted entities: {entities}")
        validated_data = self.validator.validate(entities)
        doc_id = self.db.store(validated_data, filename)
        return {
            "document_id": doc_id,
            "extracted_data": validated_data,
            "raw_text": text
        }
