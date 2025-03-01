import streamlit as st
from PIL import Image
import io

# Custom CSS to enhance the UI and add a footer watermark
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-container {
        padding: 20px;
    }
    .title {
        text-align: center;
        font-size: 3em;
        color: #333;
        margin-bottom: 10px;
    }
    .subheader {
        text-align: center;
        font-size: 1.5em;
        color: #555;
        margin-bottom: 30px;
    }
    .footer {
        position: fixed;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        font-size: 12px;
        color: #888;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main UI layout with a unique header
with st.container():
    st.markdown("<div class='title'>Image Metadata Remover</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>Upload an image to remove its metadata (EXIF, etc.)</div>", unsafe_allow_html=True)

    # File uploader widget for images
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image
        original_image = Image.open(uploaded_file)
        
        # Display the original image using the updated parameter
        st.image(original_image, caption="Original Image", use_container_width=True)
        
        # Remove metadata by re-creating the image from its pixel data
        image_data = list(original_image.getdata())
        clean_image = Image.new(original_image.mode, original_image.size)
        clean_image.putdata(image_data)
        
        st.success("Metadata has been removed from the image!")
        
        # Prepare the image for download
        img_byte_arr = io.BytesIO()
        # Use the same format as the uploaded file (default to PNG if not available)
        format = original_image.format if original_image.format else "PNG"
        clean_image.save(img_byte_arr, format=format)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Provide a download button for the cleaned image
        st.download_button(
            label="Download Image without Metadata",
            data=img_byte_arr,
            file_name=f"clean_image.{format.lower()}",
            mime=f"image/{format.lower()}"
        )

# Footer watermark displayed at the bottom center of the app
st.markdown("<div class='footer'>Voyagers~ Creative I'm / We are</div>", unsafe_allow_html=True)
