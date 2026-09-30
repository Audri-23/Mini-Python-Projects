import subprocess, sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])

from pypdf import PdfWriter

writer = PdfWriter()

for file in [
    "file1.pdf",
    "file2.pdf",
    "file3.pdf"
]:writer.append(file)

writer.write("merged.pdf")
writer.close()