import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import PyPDF2  # To handle PDF files
import docx    # To handle DOCX files

# Set the API key directly
openai.api_key = "YOUR-API-KEY-HERE"  

# Function to interact with ChatGPT
def chat_gpt_interaction(prompt):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

# Function to score the resume
def resume_score(resume_text, job_description, mandatory_keywords):
    # Construct the prompt
    prompt = f"Based on the job description and the mandatory keywords {mandatory_keywords}, please provide a score for the following resume:\n\n{resume_text}\n\nJob Description:\n{job_description}"

    # Get the ChatGPT response
    response = chat_gpt_interaction(prompt)
    if response:
        try:
            # Attempt to find a numerical score in the response.
            score = float(response)
            return score
        except ValueError:
            # If conversion to float fails, show the response to the user.
            messagebox.showinfo("Response", response)
            return None
    else:
        return None

# Function to handle resume upload
def upload_resume():
    filename = filedialog.askopenfilename()
    if filename:
        if filename.endswith('.pdf'):
            resume_text.delete(1.0, tk.END)
            resume_text.insert(tk.END, extract_text_from_pdf(filename))
        elif filename.endswith('.docx'):
            resume_text.delete(1.0, tk.END)
            resume_text.insert(tk.END, extract_text_from_docx(filename))
        else:
            with open(filename, 'r') as file:
                resume_text.delete(1.0, tk.END)
                resume_text.insert(tk.END, file.read())

# Function to handle job description upload
def upload_job_description():
    filename = filedialog.askopenfilename()
    if filename:
        if filename.endswith('.pdf'):
            job_description_text.delete(1.0, tk.END)
            job_description_text.insert(tk.END, extract_text_from_pdf(filename))
        elif filename.endswith('.docx'):
            job_description_text.delete(1.0, tk.END)
            job_description_text.insert(tk.END, extract_text_from_docx(filename))
        else:
            with open(filename, 'r') as file:
                job_description_text.delete(1.0, tk.END)
                job_description_text.insert(tk.END, file.read())

# Functions to extract text from PDF and DOCX files
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to extract keywords from job description using GPT
def extract_keywords(job_description):
    prompt = f"Extract the mandatory keywords from the following job description:\n\n{job_description}"
    response = chat_gpt_interaction(prompt)
    if response:
        return [keyword.strip() for keyword in response.split(',')]
    else:
        return []

# Function to calculate score
def calculate_score():
    resume = resume_text.get(1.0, tk.END).strip()
    job_description = job_description_text.get(1.0, tk.END).strip()
    
    if resume and job_description:
        mandatory_keywords = extract_keywords(job_description)
        score = resume_score(resume, job_description, mandatory_keywords)
        if score is not None:
            messagebox.showinfo("Score", f"The resume score is: {score}")

# GUI setup
root = tk.Tk()
root.title("Resume Score Calculator")
root.configure(bg="#f0f4f8")

# Style configuration
button_style = {
    "bg": "#4CAF50",
    "fg": "white",
    "font": ("Helvetica", 12),
    "relief": tk.FLAT,
    "borderwidth": 0
}
label_style = {
    "bg": "#f0f4f8",
    "fg": "#333333",
    "font": ("Helvetica", 12, "bold")
}
text_style = {
    "bg": "#ffffff",
    "fg": "#333333",
    "font": ("Helvetica", 10),
    "relief": tk.FLAT,
    "borderwidth": 1
}

# Create and place widgets with round corners
resume_label = tk.Label(root, text="Resume:", **label_style)
resume_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

resume_text = tk.Text(root, height=10, width=50, **text_style)
resume_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")

upload_resume_button = tk.Button(root, text="Upload Resume", command=upload_resume, **button_style)
upload_resume_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")
upload_resume_button.config(font=("Helvetica", 12, "bold"), borderwidth=0, padx=10, pady=5, relief="solid")

job_description_label = tk.Label(root, text="Job Description:", **label_style)
job_description_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

job_description_text = tk.Text(root, height=10, width=50, **text_style)
job_description_text.grid(row=1, column=1, padx=10, pady=5, sticky="w")

upload_job_description_button = tk.Button(root, text="Upload Job Description", command=upload_job_description, **button_style)
upload_job_description_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")
upload_job_description_button.config(font=("Helvetica", 12, "bold"), borderwidth=0, padx=10, pady=5, relief="solid")

calculate_button = tk.Button(root, text="Calculate Score", command=calculate_score, **button_style)
calculate_button.grid(row=3, columnspan=2, padx=10, pady=10)
calculate_button.config(font=("Helvetica", 12, "bold"), borderwidth=0, padx=10, pady=10, relief="solid")

# Apply rounded corners to Text widgets
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

root.mainloop()
