import ezgmail, os
import streamlit as st
from PIL import Image
import base64 
import streamlit.components.v1 as components

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
    }
    div.css-1pq2z0s.etr89bj1 {
    color: white;
    }
    .reportview-container {
        background: url("https://cdn.searchenginejournal.com/wp-content/uploads/2019/01/How-to-Use-Python-to-Analyze-SEO-Data-A-Reference-Guide-1520x800.png")
    }
    </style>
    """,
    unsafe_allow_html=True
)

components.html("""<meta property="og:type" content="website">
    <meta property="og:url" content="https://email2me.herokuapp.com/">
    <meta property="og:title" content="Streamlit">
    <meta property="og:description" content="A demo app that enables to send emails and attachments.">
    <meta property="og:image" content=""> """)

ezgmail.init()

st.markdown("""
    # 📧 Online email sender! 📧

    ## Send emails *including attachments* for free!
""")

subject = st.text_input('Email subject', max_chars=20)
body = st.text_area('Email body', max_chars= 100)

body += '\n\nSent via an app coded by Clement Lelievre (www.linkedin.com/in/clem-data/) here: www.email2me.herokuapp.com/\n' # a little bit of self-advertising

nb = st.slider('Select number of recipients',1,5, help = 'Select how many adresses will receive your message')
recipients = []
for i in range(int(nb)):
    a = st.text_input('Email recipient ' + str(i+1) , max_chars=40)
    recipients.append(str(a))
recipients = [rec for rec in recipients if len(rec)>0]

def save_image(file):
    '''saves locally the attached file. This is necessary to send the attachment (see send method of ezgmail).'''
    with open(file.name,"wb") as f:
        f.write(file.getbuffer())


attachments, uploaded_files, attachments_to_send = None, None, []
#st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_files = st.file_uploader("Choose a file", type=["jpg","jpeg","JPG","png","PNG"], accept_multiple_files=True, help="Upload your file(s) (only images for now)")
attachments = uploaded_files    
for attachment in attachments:
    filename = attachment.name
    attachments_to_send.append(str(filename))
    save_image(attachment)
    st.image(attachment, caption='Image ' + str(attachments.index(attachment)+1)+': '+filename, width= 100, use_column_width='always')
   
    # with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), name),"wb") as f:
    #     f.write(file.getbuffer())    

if st.button('Send email'):
    if len(subject) * len(body) * len(recipients) != 0:
        try:
            for item in recipients:
                if len(attachments_to_send)>0:
                    ezgmail.send(item, subject, body, attachments = attachments_to_send)
                else:
                    ezgmail.send(item, subject, body)
            if len(recipients) == 1:
                st.success('Email sent! 🎉')
                st.balloons()
            elif len(recipients) > 1:
                st.success(str(len(recipients)) + ' emails sent! 🎉')
                st.balloons()
            body += '\n\nRecipient list:\n'
            for item in recipients:
                body += '\n' + item
            ezgmail.send('clement.lelievre91@gmail.com' ,subject , body, attachments=attachments_to_send) # controlling what is being sent to whom for security purposes           
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










