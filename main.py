import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os
import io

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

def log_email(email_address):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{now} - {email_address}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

# Main logic
if valid_email and agree:
    st.success("✅ Mostmár letöltheted az excelt!")

    # Always recreate buffer
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        df.to_excel(writer, index=False, sheet_name="Adatok")
    excel_buffer.seek(0)

    # Download button (shows when ready)
    download_clicked = st.download_button(
        label="📥 Excel letöltése",
        data=excel_buffer,
        file_name="osztondij_kalkulator.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    if download_clicked:
        log_email(email)
        st.info("📑 Az email címed rögzítésre került a letöltéshez.")
else:
    st.info("A letöltéshez érvényes email cím és a feltételek elfogadása szükséges.")
