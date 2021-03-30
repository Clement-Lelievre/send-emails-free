import ezgmail, os
import streamlit as st

st.set_page_config(
    page_title="Free email sender!", # => Quick reference - Streamlit
    page_icon="📧",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

ezgmail.init()

st.markdown("""
    # 📧 Online email sender! 📧

    ## Send emails *including attachments* for free!
""")

subject = st.text_input('Email subject', max_chars=20)
body = st.text_area('Email body', max_chars= 100)

attachments, uploaded_files, attachments_to_send = None, None, None

recipient = st.text_input('Email recipient', max_chars=50)

if st.checkbox('Include attachment(s)?'):
    st.set_option('deprecation.showfileUploaderEncoding', False)
    uploaded_files = st.file_uploader("Choose a file", type=["csv","xls","xlsx","doc","docx","jpg","jpeg","JPG","png","PNG"], accept_multiple_files=True,help="Upload your file(s)")

def preprocess_attachment(file):
    '''saves locally the attached file'''
    with open(os.path.join("app","Attachments", file.name),"wb") as f:
            f.write(file.getbuffer())

if uploaded_files is not None:
    attachments = uploaded_files
    for attachment in attachments:
        filename = attachment.name
        if filename[-3:] in ['jpg','png','JPG','PNG'] or filename[-4:] == "jpeg":
            st.image(attachment, caption='Image ' + str(attachments.index(attachment)+1)+': '+filename,width= 100, use_column_width='always')
        preprocess_attachment(attachment)
    attachments_to_send = []
    for (root,dirs,files) in os.walk(os.path.join("app",'Attachments'), topdown=True):   
        for f in files[-len(attachments):]:  
            attachments_to_send.append(os.path.join("Attachments",f))

if st.button('Send email'):
    if len(subject) * len(body) * len(recipient) != 0:
        try:
            ezgmail.send(recipient, subject, body, attachments_to_send)
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
    for (root,dirs,files) in os.walk('Attachments', topdown=True): 
        for f in files:
            try:
                os.remove(os.path.join("app","Attachments",f))  
            except Exception as e:
                continue
                st.error(e)

code = 'import os; os.system("ls -a")'

st.write(exec(code))








