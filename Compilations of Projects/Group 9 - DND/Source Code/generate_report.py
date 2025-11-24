import asyncio
import sys
import nbformat
from nbclient import NotebookClient
import subprocess

# Windows compatibility
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Step 1: Execute the notebook
with open("report.ipynb", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=None, kernel_name="python3")
client.execute()

with open("report.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

# Step 2: Export directly to PDF
subprocess.run([
    sys.executable, "-m", "jupyter", "nbconvert",
    "--to", "webpdf",
    "--allow-chromium-download",
    "--no-input",
    "--WebPDFExporter.embed_images=True",
    "--log-level=ERROR",
    # Separate Chrome args properly
    "--WebPDFExporter.chrome_args=--no-pdf-header-footer",
    "--WebPDFExporter.chrome_args=--print-backgrounds",
    "--WebPDFExporter.chrome_args=--allow-file-access-from-files",
    "--WebPDFExporter.chrome_args=--disable-web-security",
    "report.ipynb"
])
