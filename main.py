import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os
import io
import openpyxl
import smtplib
from email.message import EmailMessage

df = pd.DataFrame({
    "Name": ["Anna", "Bence", "Csilla"],
    "Score": [90, 85, 92]
})

st.title("Corvinus Karrier Fesztivál Állások")

# Email input
email = st.text_input("Add meg az egyetemi email címedet (@stud.uni-corvinus.hu):")

# Checkbox
agree = st.checkbox("Elfogadom a Felhasználási Feltételeket")

# Regex validation
valid_email = re.match(r"^[A-Za-z0-9._%+-]+@stud\.uni-corvinus\.hu$", email)

# Log file name
log_file = os.path.join(os.path.dirname(__file__), "email_log.txt")

EMAIL_USER = st.secrets["EMAIL_USER"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]

def send_email_log(user_email):
    msg = EmailMessage()
    msg['Subject'] = "Új Excel letöltés – Corvinus App"
    msg['From'] = "kovalikdberci@gmail.com"  # replace with your logging email
    msg['To'] = "kovalikdberci@gmail.com"    # could be same as From
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg.set_content(f"Letöltés történt:\n\nEmail: {user_email}\nIdőpont: {now}")

    # Connect and send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    print('message sent successfully')


excel_path = os.path.join(os.path.dirname(__file__), "munkalehetosegek_.xlsx")
# Main logic
if valid_email and agree:
    st.success("✅ Mostmár letöltheted az excelt!")

    with open(excel_path, "rb") as f:
        excel_bytes = f.read()

    download_clicked = st.download_button(
        label="📥 Excel letöltése",
        data=excel_bytes,
        file_name="osztondij_kalkulator.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    if download_clicked:
        send_email_log(email)
        st.info("📑 Az email címed rögzítésre került a letöltéshez.")
else:
    st.info("A letöltéshez érvényes email cím és a feltételek elfogadása szükséges.")
