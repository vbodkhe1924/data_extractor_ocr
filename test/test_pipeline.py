# tests/test_pipeline.py
import pytest
from app.models.pipeline import InvoicePipeline

@pytest.fixture
def pipeline():
    return InvoicePipeline()

def test_pipeline_process(pipeline):
    with open("tests/sample_invoice.png", "rb") as f:
        content = f.read()
    result = pipeline.process_document(content, "sample_invoice.png")
    assert "document_id" in result
    assert "extracted_data" in result
    assert "raw_text" in result