import io
import PyPDF2
import streamlit as st


def merge_pdfs(pdfs):
    merger = PyPDF2.PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    return merged_pdf


def extract_pages(pdf, pages):
    reader = PyPDF2.PdfReader(pdf)
    writer = PyPDF2.PdfWriter()
    page_ranges = (x.split("-") for x in pages.split(","))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    for p in range_list:
        # Subtract 1 to deal with 0 index
        writer.add_page(reader.pages[p - 1])
    extracted_pdf = io.BytesIO()
    writer.write(extracted_pdf)
    return extracted_pdf


st.title("PDF Manipulation")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 1:
        if st.button("Merge PDFs"):
            merged_pdf = merge_pdfs(uploaded_files)
            st.download_button(label="Download Merged PDF", data=merged_pdf.getvalue(), file_name="merged.pdf", mime="application/pdf")
    else:
        pdf = uploaded_files[0]
        st.write(f"Total Pages: {len(PyPDF2.PdfReader(pdf).pages)}")
        pages = st.text_input("Please enter pages to extract (e.g. 1-3, 5, 7)")
        if st.button("Extract Pages"):
            extracted_pdf = extract_pages(pdf, pages)
            st.download_button(label="Download Extracted Pages", data=extracted_pdf.getvalue(), file_name="extracted.pdf", mime="application/pdf")
