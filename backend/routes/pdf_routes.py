from flask import Blueprint, request, jsonify
import os

pdf_bp = Blueprint("pdf_bp", __name__)

# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "uploads",
    "pdfs"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# UPLOAD PDF ROUTE
# ==========================================

@pdf_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():

    try:

        # Check file exists
        if "file" not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        # Empty filename
        if file.filename == "":

            return jsonify({
                "error": "Empty filename"
            }), 400

        # Only allow PDF
        if not file.filename.endswith(".pdf"):

            return jsonify({
                "error": "Only PDF files allowed"
            }), 400

        # Save file
        save_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(save_path)

        print(f"\nPDF Saved: {save_path}\n")

        return jsonify({
            "message": "PDF uploaded successfully",
            "filename": file.filename
        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500