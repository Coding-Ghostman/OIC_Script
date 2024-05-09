import base64
import json

from flask import Flask, jsonify, request

from split import split_pdf
from table_extractor import table_to_base64

app = Flask(__name__)


@app.route("/api/conneqtion/upload", methods=["POST"])
def upload_file():
    if "file" not in request.json:
        return jsonify({"error": "No file part in JSON payload"})
    try:
        pdf_data = base64.b64decode(request.json["file"])
        extracted_table_base64 = table_to_base64(pdf_data)
        invoice_base64 = split_pdf(pdf_data)
        return {"invoice": invoice_base64, "table": extracted_table_base64}
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
