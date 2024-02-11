from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the vision model
model = genai.GenerativeModel("gemini-pro-vision")


# Get response from model
def get_response(input, invoice, prompt):

    response = model.generate_content([input, invoice[0], prompt])

    return response.text

# Convert the file to bytes to show in streamlit
def input_image_processing(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Start with streamlit app
st.set_page_config(page_title="Invoice Details Extractor")

st.header("Invoice Detail Extractor")
input = st.text_input("Input Prompt: ", key="input")
upload_file = st.file_uploader("Upload the invoice image",
                                 type=["jpg","jpeg","png"])


image=""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Invoice.", use_column_width=True)


run_button = st.button("Run (Fetch Details)")


# Design the prompt
input_prompt = """
        You are an expert in understanding the contents of invoices.
        You will receive invoices as input images and 
        you will answer the questions related to the invoice input image.
        """


if run_button:
    image_data = input_image_processing(upload_file)
    response = get_response(input_prompt, image_data, input)

    st.header("Details:")
    st.write(response)
