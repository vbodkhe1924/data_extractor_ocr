# app/services/ocr.py
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image, ImageEnhance
import io

class OCRProcessor:
    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")
        
    def extract_text(self, content: bytes) -> str:
        image = Image.open(io.BytesIO(content)).convert("RGB")
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # Increase contrast
        image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)  # Upscale
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return text

# app/services/ocr.py
# import pytesseract
# from PIL import Image
# import io

# class OCRProcessor:
#     def __init__(self):
#         pytesseract.pytesseract.tesseract_cmd = r'"C:\Users\vbodk\tesseract_ocr\tesseract.exe"'  # Adjust path

#     def extract_text(self, content: bytes) -> str:
#         image = Image.open(io.BytesIO(content)).convert("RGB")
#         text = pytesseract.image_to_string(image)
#         return text