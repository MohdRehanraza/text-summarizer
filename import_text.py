import tkinter as tk
from tkinter import filedialog, messagebox
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure required NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# --- Summarization Function ---
def summarize_text(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = {}
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = {}

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = sum(sentenceValue.values())
    if len(sentenceValue) == 0:
        return "No significant content to summarize."

    average = int(sumValues / len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] > (1.2 * average):
            summary += " " + sentence

    return summary.strip() or "No summary generated."

# --- Button Commands ---
def generate_summary():
    input_text = input_text_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Needed", "Please enter some text to summarize.")
        return

    summary = summarize_text(input_text)
    output_text_box.delete("1.0", tk.END)
    output_text_box.insert(tk.END, summary)

def save_summary():
    summary = output_text_box.get("1.0", tk.END).strip()
    if not summary:
        messagebox.showwarning("Nothing to Save", "There is no summary to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(summary)
            messagebox.showinfo("Success", f"Summary saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save summary:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("800x600")

# Input Text Box
tk.Label(root, text="Input Text:").pack()
input_text_box = tk.Text(root, height=12, wrap=tk.WORD)
input_text_box.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

summarize_button = tk.Button(button_frame, text="Generate Summary", command=generate_summary)
summarize_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(button_frame, text="Save Summary", command=save_summary)
save_button.pack(side=tk.LEFT, padx=10)

# Output Text Box
tk.Label(root, text="Summary:").pack()
output_text_box = tk.Text(root, height=10, wrap=tk.WORD, bg="#f0f0f0")
output_text_box.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Run GUI
root.mainloop()
