import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def convert_to_pdf(docx_path: Path) -> Path | None:
    output_dir = docx_path.parent
    
    # PDF ni "forma" sifatida emas, oddiy hujjat sifatida eksport qilish
    # Bu matnlarning surilib ketishini oldini oladi
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf:writer_pdf_Export:{\"ExportFormFields\":false}",
        "--outdir",
        str(output_dir),
        str(docx_path),
    ]
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            timeout=120,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info(f"LibreOffice output: {result.stdout.decode()}")
    except Exception as e:
        logger.error(f"PDF conversion failed: {e}")
        return None

    pdf_path = output_dir / (docx_path.stem + ".pdf")
    if pdf_path.exists():
        return pdf_path
    logger.error(f"PDF not found at {pdf_path}")
    return None
