from tkinter.tix import IMAGE
import streamlit as st 
from PIL import Image
import base64


option = st.sidebar.selectbox("Doc Upload/Download", ('upload', 'download'))

st.header(option)

if option == 'upload':
    st.title("Upload + Receipt")
    uploaded_file = st.file_uploader("Choose an image...", type="jpeg")
    if uploaded_file is not None:
        image = Image.open(uploaded_file) 
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        with open('Receipt.jpeg', "rb") as file : 
            btn = st.download_button(
                label='Download',
                data=file, 
                file_name="receipt.png",
                mime="image/png"
            )
    
    # else:
    #     print (Hello")
    # with open(image) as file:
    #     btn = st.download_button(
    #         label = "Dowload receipt",
    #         data = file, 
    #         file_name = "receipt.png",
    #         mime="image/png"
    #     )


if option == 'download': 
    st.title("Hello")
#     with open(image) as file:
#         btn = st.download_button(
#             label = "Dowload receipt",
#             data = file, 
#             file_name = "receipt.png",
#             mime="image/png"
#         )
