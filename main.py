import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=API_KEY)
MODEL = "gpt-4o"

# Function to grade email
def grade_email(email_from, email_subject, email_body):
    prompt = f"""
    Analyze the following email and grade it based on the following criteria:
    1. CRITERIA 1: 
    2. CRITERIA 1
    3. CRITERIA 3: 
    4. CRITERIA 4:

    Email:
    From: {email_from}
    Subject: {email_subject}
    Body: {email_body}

    Grade the email and explain the reasoning. Reasoning should be on croatian language.
    """
    
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
                    {"role": "system", "content": """
                    You are generating a e-mail grading for a travel agency mail system. Grade in: 

                     1. high priority (only if all criteria are met. Do not classify as high priority if all criteria is not met! If the subject does not contain "request", the mesage can not be classified in high priority.)
                     2. middle priority (if the mail is from top agents, but some of the other criteria is not met. Or the mail fits all criteria, but is not send from top agent)
                     3. low priority (if the mail is not send from top agent and does not fit in one additional criteria)
                     4. spam (classify as spam only if a request have no relations with travel agency buisness whatsoever)
                    Do not assume anything.
                    """},
                    {"role": "user", "content": f"The audio transcription is: {prompt}"},
                ],
      max_tokens=250
    )
    
    return response.choices[0].message.content
# Function to save email to appropriate folder
def save_email(grade, email_from, email_subject, email_body):
    grade_folder = {
        "high priority": "HighPriority",
        "middle priority": "MiddlePriority",
        "low priority": "LowPriority",
        "spam": "Spam"
    }

    # Extract grade from the response
    for key in grade_folder.keys():
        if key in grade.lower():
            folder = grade_folder[key]
            break
    else:
        folder = "Uncategorized"

    # Create the directory if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Create a safe filename using from and subject
    filename_safe = f"{email_from}_{email_subject}".replace(' ', '_').replace('/', '_').replace('\\', '_')
    filename = os.path.join(folder, f"{filename_safe[:100]}.txt")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"From: {email_from}\n")
        file.write(f"Subject: {email_subject}\n")
        file.write(f"Body:\n{email_body}\n")
        file.write(f"Grade: {grade}\n")


# Streamlit UI
st.markdown(
        """
        <style>
            .main {
                background-color: #022b65;
                color: #fffefe;
            }
            .stButton>button {
                background-color: #008CBA;
                color: #fffefe;
            }
            .stFileUploader {
                color: #008CBA;
            }
            .stTextInput {
                background-color: #022b65;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
# Set the title and logo
st.image("image.png", width=300)
st.title("Uniline sustav za rangiranje upita")

st.write("Upišite e-mail upit:")

email_from = st.text_input("From")
email_subject = st.text_input("Subject")
email_body = st.text_area("Body")

if st.button("Rangiraj upit"):
    grade = grade_email(email_from, email_subject, email_body)
    st.write("Rang upita i pojašnjenje:")
    st.write(grade)
    save_email(grade, email_from, email_subject, email_body)
    st.write("Upit uspješno spremljen.")
