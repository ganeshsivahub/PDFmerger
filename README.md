# 📄 PDF Merger App

An interactive, web-based tool built with Streamlit and PyPDF2 for easily merging multiple PDF files, rearranging their order, and configuring the output document properties.

## ✨ Features

* **Drag-and-Drop Interface:** Easily upload multiple PDF files.
* **Reordering:** Drag and drop file names to instantly set the merge order using the integrated sorting feature.
* **Metadata Configuration:** Sets fixed Author and Producer metadata for the output file.
* **Page Size Standardization:** Select from common paper sizes (A4, Letter, Legal, etc.) to standardize the dimensions of the final merged document. Pages are forced to this boundary (cropping or padding as necessary).
* **In-Memory Processing:** Files are processed using `io.BytesIO` for efficiency and security, without relying on disk storage.

## 🚀 How to Use It (Deployed Version)

If you are using the deployed version (e.g., on Streamlit Community Cloud):

1.  **Upload Files:** Click the "Upload PDF files" box or drag your PDF documents onto it.
2.  **Arrange Order:** Use the drag-and-drop interface under the "Arrangement of PDF Files" section to define the sequence in which the documents will be merged.
3.  **Configure Output:** Select the desired **Output Document Page Size** (A4 is the default).
4.  **Merge:** Click the primary **"Merge PDFs"** button.
5.  **Download:** Once the process is complete, click **"Download Merged PDF"**.

## 🛠️ Installation and Local Setup

To run this application on your local machine, follow these steps:

### Prerequisites

* Python 3.8+

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ganeshsivahub/PDFmerger.git
    cd your-repo-name
    ```

2.  **Install Dependencies:**
    The necessary libraries are listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App:**
    Start the Streamlit server:
    ```bash
    streamlit run PDFCombine2.0.py
    ```
    The application will open in your web browser at `http://localhost:8501`.

## 📦 Key Dependencies

* `streamlit`: For building the web application interface.
* `PyPDF2`: For handling PDF manipulation (reading, merging, writing).
* `streamlit-sortables`: For the drag-and-drop file reordering widget.

## ✍️ Author

Built with ❤️ by **Ganesh Sivaraman**.

## 🤝 Contributing

Contributions are welcome! If you find a bug or have a suggestion for an enhancement (like password protection or page range selection), please open an issue or submit a pull request.

---
