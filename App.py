import streamlit as st
import requests
from split import split_pdf
from table_extractor import pdf_to_base64

# Function to call API for invoice extraction
def api_to_invoice(pdf_content, file_name):
    invoice_base64, _ = split_pdf(pdf_content,file_name)

    payload = {
        "FileDetails": [{
            "Base64": invoice_base64,
            "fileName": file_name
        }]
    }

    api_url_invoice = "https://oicdev-bmjnxdnrlvmc-bo.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/AIRLINES_INVOICE_EXTRACTION/1.0/getBulkData"
    username = "VBCS_OIC_DEV_SERVICE_USER"
    password = "Integration@2024 "
    
    response = requests.post(api_url_invoice, json=payload, auth=(username, password))
    return response

# Function to call API for table extraction
def api_to_table_extract(pdf_content):
    table_base64 = pdf_to_base64(pdf_content)

    payload = {
        "FileDetails": {
            "Base64": table_base64
        }
    }

    api_url_table = "https://oicdev-bmjnxdnrlvmc-bo.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/AIRLINES_TABLE_EXTRACTION/1.0/insert_into_table"
    username = "VBCS_OIC_DEV_SERVICE_USER"
    password = "Integration@2024 "
    
    response = requests.post(api_url_table, json=payload, auth=(username, password))
    return response

# Streamlit UI
def main():
    st.title("PDF Processor")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        # Display file details
        print(uploaded_file)
        file_details = {"Filename": uploaded_file.name,"File Size": f"{uploaded_file.size / (1024 * 1024):.2f} MB","File Type": uploaded_file.type}
        st.write(file_details)

        # Run API functions
        if st.button("Run Invoice Extraction API"):
            response = api_to_invoice(uploaded_file.read(), uploaded_file.name)
            if response.status_code == 200:
                st.success("Invoice Extraction API request successful")
            else:
                st.error(f"Invoice Extraction API request failed with status code {response.status_code}")
                st.error(response.text)

        if st.button("Run Table Extraction API"):
            response = api_to_table_extract(uploaded_file.read())
            if response.status_code == 200:
                st.success("Table Extraction API request successful")
            else:
                st.error(f"Table Extraction API request failed with status code {response.status_code}")
                st.error(response.text)

if __name__ == "__main__":
    main()
