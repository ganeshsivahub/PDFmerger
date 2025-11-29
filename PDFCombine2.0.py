import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
from streamlit_sortables import sort_items
import io
from PyPDF2.generic import RectangleObject

# Define common page sizes in points (72 points = 1 inch)
PAGE_SIZES = {
    "A4 (Default)": (595.276, 841.890),  # 210 x 297 mm
    "Letter": (612, 792),  # 8.5 x 11 inches
    "Legal": (612, 1008),  # 8.5 x 14 inches
    "A3": (841.890, 1190.551),  # 297 x 420 mm
    "B5": (498.898, 708.661),  # 176 x 250 mm
}


def merge_pdfs(pdf_files_data, author_name, producer_name, output_page_size_name, output_filename="merged.pdf"):
    """
    Merges multiple PDF files into a single PDF with specified metadata and page size handling.

    Args:
        pdf_files_data (list): A list of file-like objects (bytes data) of PDF files.
        author_name (str): The value to set for the PDF Author property.
        producer_name (str): The value to set for the PDF Producer property.
        output_page_size_name (str): The name of the desired output page size (key from PAGE_SIZES).
        output_filename (str): The name for the merged PDF file.

    Returns:
        bytes: The merged PDF as bytes, or None if an error occurred.
    """
    # Use PyPDF2's PdfWriter
    merger = PdfWriter()

    # 1. SET DOCUMENT PROPERTIES
    merger.add_metadata({
        "/Author": author_name,
        "/Producer": producer_name,
    })

    # Get the selected page size in points (width, height)
    output_width, output_height = PAGE_SIZES.get(output_page_size_name, PAGE_SIZES["A4 (Default)"])

    # Set the default page size (page box) for the writer object
    default_page_size = RectangleObject([0, 0, output_width, output_height])

    for pdf_data in pdf_files_data:
        try:
            # Prepare data for PdfReader
            pdf_buffer = io.BytesIO(pdf_data)
            reader = PdfReader(pdf_buffer)

            # Iterate through all pages of the current PDF
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]

                # Apply the default size (CropBox/MediaBox) to the page
                page.mediabox = default_page_size
                page.cropbox = default_page_size

                # NOTE: Use merger.add_page(page) for PyPDF2 v3.x and later
                merger.add_page(page)

        except Exception as e:
            st.error(f"Error processing a PDF file: {e}. Please ensure it's a valid PDF.")
            return None

    # Write the merged PDF to a BytesIO object
    output_pdf_buffer = io.BytesIO()
    merger.write(output_pdf_buffer)
    merger.close()
    output_pdf_buffer.seek(0)
    return output_pdf_buffer.getvalue()


# --- STREAMLIT APP LAYOUT ---

st.set_page_config(
    page_title="PDF Merger",
    page_icon="📄",
    layout="centered"
)

st.title("PDF Merger App")
st.markdown("Drag and drop your PDF files, reorder them, and click 'Merge'!")

# State to store uploaded files and their order
if 'uploaded_files_info' not in st.session_state:
    st.session_state.uploaded_files_info = []

# File uploader with drag and drop
uploaded_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True,
    key="pdf_uploader",
    help="Drag and drop PDF files here, or click to browse."
)

# Process newly uploaded files
if uploaded_files:
    # Filter out files that are already in session_state to avoid duplicates
    existing_file_names = {info['name'] for info in st.session_state.uploaded_files_info}
    new_files_to_add = []
    for file in uploaded_files:
        # Check if file has already been stored (by name is sufficient for this context)
        if file.name not in existing_file_names:
            # Store the original file object's data
            new_files_to_add.append({'name': file.name, 'data': file.getvalue()})

    if new_files_to_add:
        st.session_state.uploaded_files_info.extend(new_files_to_add)
        # Rerun is necessary here to clear the file uploader widget and update the sortable list immediately
        st.rerun()

# --- Configuration Section ---
st.subheader("Configuration")
col_meta, col_size = st.columns(2)

# MODIFIED: Use st.text_input to allow user input for metadata
with col_meta:
    # Set default values for convenience
    user_author = st.text_input("PDF Author", value="Ganesh Sivaraman", help="Sets the PDF's Author property.")
    user_producer = st.text_input("PDF Producer", value="PDF Merger App", help="Sets the PDF's Producer property.")

# Page Size Selection
with col_size:
    selected_page_size = st.selectbox(
        "Output Document Page Size",
        options=list(PAGE_SIZES.keys()),
        index=0,  # Default to A4
        help="Select the default page size for the merged document. This affects how pages of different sizes are displayed."
    )

st.markdown("---")

# --- File Sorting and Merging Section ---

if st.session_state.uploaded_files_info:
    st.subheader("Arrangement of PDF Files")
    st.info("Drag and drop the file names below to reorder them.")

    file_name_to_data = {info['name']: info['data'] for info in st.session_state.uploaded_files_info}
    initial_file_names = [info['name'] for info in st.session_state.uploaded_files_info]

    # Use sort_items with the list of strings
    sorted_file_names = sort_items(initial_file_names, key="pdf_sorter")

    # Reconstruct the ordered list of file data based on the sorted file names
    reordered_files_data = [file_name_to_data[name] for name in sorted_file_names]

    # Display the current order
    st.write("Current merge order:")
    for i, name in enumerate(sorted_file_names):
        st.write(f"{i + 1}. **{name}**")

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Merge PDFs", type="primary"):
            if len(reordered_files_data) < 2:
                st.warning("Please upload at least two PDF files to merge.")
            else:
                with st.spinner("Merging PDFs..."):
                    # MODIFIED: Pass the user_author and user_producer variables
                    merged_pdf_bytes = merge_pdfs(
                        reordered_files_data,
                        user_author,  # Passed user input
                        user_producer,  # Passed user input
                        selected_page_size
                    )

                    if merged_pdf_bytes:
                        st.success("PDFs merged successfully!")
                        st.download_button(
                            label="Download Merged PDF",
                            data=merged_pdf_bytes,
                            file_name="merged_document.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("Failed to merge PDFs. Please check the uploaded files.")
    with col2:
        if st.button("Clear All Files"):
            st.session_state.uploaded_files_info = []
            st.success("All files cleared.")
            st.rerun()

else:
    st.info("Upload PDF files to get started!")

st.markdown("---")
st.markdown("Built with ❤️ by Ganesh.")