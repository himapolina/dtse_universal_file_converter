import streamlit as st
import os
from markitdown import MarkItDown
import io
import zipfile

# Define allowed file types and max file size
ALLOWED_FILE_TYPES = [
    "pdf", "pptx", "docx", "xlsx", "jpg", "jpeg", "png", "mp3"
]
MAX_FILE_SIZE_MB = 25  # Set a reasonable limit for web apps

# Set a title for the Streamlit app
st.title("Docs to Markdown Converter")

# Main user instructions
st.markdown("### 📄 Drag, drop, and convert your files to Markdown text.")

# File uploader widget for user input
uploaded_files = st.file_uploader(
    "Upload your files here", 
    type=ALLOWED_FILE_TYPES, 
    accept_multiple_files=True
)

if uploaded_files:
    # Check for large files and provide a warning
    large_files = [f.name for f in uploaded_files if f.size > MAX_FILE_SIZE_MB * 1024 * 1024]
    if large_files:
        st.warning(f"The following files are larger than the recommended {MAX_FILE_SIZE_MB}MB limit: {', '.join(large_files)}. Processing may be slow or fail.")

    # Show a spinner while processing
    with st.spinner("Converting..."):
        # Initialize the MarkItDown converter
        converter = MarkitDown()
        
        # Initialize a list to hold the converted text from all files
        full_text_list = []
        
        # Process each uploaded file
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Check if the file type is supported
            if file_extension not in ALLOWED_FILE_TYPES:
                st.error(f"Unsupported file type: **{file_extension}**. Please upload a supported file.")
                continue

            # Read the file's content into a BytesIO object
            file_content = io.BytesIO(uploaded_file.read())
            
            try:
                # Use the MarkItDown converter to convert the file
                converted_doc = converter.convert(file_content, file_extension=file_extension)
                full_text_list.append(f"# {uploaded_file.name}\n\n{converted_doc.text_content}\n\n---")
                
            except Exception as e:
                st.error(f"**Conversion failed for '{uploaded_file.name}'**: {e}")
                
    if full_text_list:
        # Join all converted text into a single string
        full_text = "\n\n".join(full_text_list)
        
        # Add a download button for the final markdown file
        st.download_button(
            label="Download Converted File",
            data=full_text,
            file_name="converted_document.md",
            mime="text/markdown"
        )
        
        # Add an expandable section to show the rendered Markdown
        with st.expander("Rendered Preview"):
            st.markdown(full_text)
