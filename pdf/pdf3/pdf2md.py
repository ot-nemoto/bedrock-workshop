import pymupdf4llm

# PDFファイルのパス
pdf_path='sample.pdf'

# PDFファイルからMarkdownに変換
md_text = pymupdf4llm.to_markdown(pdf_path,pages=range(0,3),margins=(0,0,0,0))

print(md_text)
