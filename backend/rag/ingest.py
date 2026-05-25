from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PDF_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "uploads",
    "pdfs"
)

PDF_FOLDER = os.path.abspath(PDF_FOLDER)


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=300,
        chunk_overlap=80,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    chunks = splitter.split_text(text)

    return chunks


def process_all_pdfs():

    all_chunks = []

    print("PDF Folder:", PDF_FOLDER)

    for filename in os.listdir(PDF_FOLDER):

        if filename.endswith(".pdf"):

            pdf_path = os.path.join(
                PDF_FOLDER,
                filename
            )

            print(f"Processing: {filename}")

            text = extract_text_from_pdf(pdf_path)

            chunks = chunk_text(text)

            all_chunks.extend(chunks)

    return all_chunks


if __name__ == "__main__":

    chunks = process_all_pdfs()

    print("\nTotal Chunks:", len(chunks))