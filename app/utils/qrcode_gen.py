"""QR code generation"""
import qrcode
import io
import base64
from typing import Optional
from app.config import Config

def generate_qr_code(url: str) -> str:
    """Generate QR code as base64-encoded PNG"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{Config.QR_CODE_ERROR_CORRECTION}'),
        box_size=Config.QR_CODE_SIZE,
        border=Config.QR_CODE_BORDER,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

