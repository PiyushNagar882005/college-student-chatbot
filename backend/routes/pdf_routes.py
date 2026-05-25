from flask import Blueprint, request, jsonify
import os

pdf_bp = Blueprint("pdf_bp", __name__)

UPLOAD_FOLDER = "backend/uploads/pdfs"

# Create folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@pdf_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "Empty filename"
            }), 400

        save_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(save_path)

        return jsonify({
            "message": "PDF uploaded successfully",
            "filename": file.filename
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500