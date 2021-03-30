import ezgmail, os
import streamlit as st
from PIL import Image
import base64 

st.set_page_config(
    page_title="Free email sender!", # => Quick reference - Streamlit
    page_icon="📧",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

st.markdown(
    """
    <style>
    h1 {
    color: white;
    }
    h2 {
    color: white;
    }
    label.css-145kmo2.effi0qh0 {
    color: white;
    }
    div.row-widget stCheckbox {
    color: white;
    } 
    .reportview-container {
        background: url("https://www.agari.com/wp-content/uploads/2019/06/python-code.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)

ezgmail.init()

st.markdown("""
    # 📧 Online email sender! 📧

    ## Send emails *including attachments* for free!
""")

subject = st.text_input('Email subject', max_chars=20)
body = st.text_area('Email body', max_chars= 100)

body += '\n\nSent via an app coded by Clement Lelievre.\nLinkedin: www.linkedin.com/in/clem-data/'

attachments, uploaded_files, attachments_to_send = None, None, None

recipient = st.text_input('Email recipient', max_chars=40)
if st.checkbox('Add a recipient?'):
    recipient2 = st.text_input('Email recipient 2', max_chars=40)

recipients = [recipient, recipient2]

if st.checkbox('Include attachment(s)?'):
    st.set_option('deprecation.showfileUploaderEncoding', False)
    uploaded_files = st.file_uploader("Choose a file", type=["jpg","jpeg","JPG","png","PNG"], accept_multiple_files=True, help="Upload your file(s) (only images for now)")

#@st.cache
def preprocess_attachment(file):
    '''saves locally the attached file'''
    name = file.name
    file = Image.open(file)
    file = file.save(os.path.join("Attachments",name))
    # with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"Attachments", name),"wb") as f:
    #     f.write(file.getbuffer())
    

if uploaded_files is not None:
    attachments = uploaded_files
    for attachment in attachments:
        filename = attachment.name
        if filename[-3:] in ['jpg','png','JPG','PNG'] or filename[-4:] == "jpeg":
            st.image(attachment, caption='Image ' + str(attachments.index(attachment)+1)+': '+filename,width= 100, use_column_width='always')
        preprocess_attachment(attachment)
    attachments_to_send = []
    for (root,dirs,files) in os.walk(os.path.join(os.path.abspath(os.path.dirname(__file__)),"Attachments"), topdown=True):   
        for f in files[-len(attachments):]:  
            attachments_to_send.append(f)

if st.button('Send email'):
    if len(subject) * len(body) * len(recipient) != 0:
        try:
            ezgmail.send(recipients, subject, body, attachments_to_send)
            print(subject)
            st.success('Email sent! 🎉')
        except Exception as e:
            st.error(f'An error occured: {e}')
    elif len(subject) == 0:
        st.warning('Please type a subject')
    elif len(body) == 0:
        st.warning('Please type a body')
    else:
        st.warning('Please type a recipient')
    # clear the attachments folder for the next email
    # for (root,dirs,files) in os.walk(os.path.join(os.path.abspath(os.path.dirname(__file__)),"Attachments"), topdown=True): 
    #     for f in files:
    #         try:
    #             os.remove(f)
    #         except Exception as e:
    #             continue
    #             st.error(e)










