import io
import os

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

# PDFファイルのパス
pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.pdf")

# 抽出後テキスト
text = ""

# PDFファイルからテキストを抽出
with open(pdf_path, "rb") as file:
    # PDFリソースマネージャーを作成
    resource_manager = PDFResourceManager()

    # テキスト抽出用のバッファを作成
    text_buffer = io.StringIO()
    converter = TextConverter(resource_manager, text_buffer, laparams=LAParams())

    # PDFページインタープリタを作成
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    # 3ページ分のテキストを抽出
    for page in PDFPage.get_pages(file, maxpages=3, check_extractable=False):
        page_interpreter.process_page(page)
        text += text_buffer.getvalue()
        text_buffer.truncate(0)
        text_buffer.seek(0)

    # リソースを解放
    converter.close()
    text_buffer.close()
print(text)
