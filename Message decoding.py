import tkinter as tk
from tkinter import scrolledtext, messagebox, font

def generate_keys():
    length = 1
    while True:
        for i in range(2**length):
            key_str = bin(i)[2:].zfill(length)
            if '0' in key_str: yield key_str
        length += 1

def decode_message(header, message):
    key_map = {}
    key_gen = generate_keys()
    for char in header: key_map[next(key_gen)] = char
    decoded_message = ''
    message = message.replace('\n', '')
    while message:
        segment_length = int(message[:3], 2)
        message = message[3:]
        termination_sequence = '1' * segment_length
        while not message.startswith(termination_sequence):
            decoded_message += key_map[message[:segment_length]]
            message = message[segment_length:]
        message = message[segment_length:]
        if message.startswith('000'): break
    return decoded_message

def decode_and_display():
    output_text.delete("1.0", tk.END)
    decoded = decode_message(header_entry.get(), message_text.get("1.0", tk.END))
    output_text.insert(tk.END, decoded)
    output_text.tag_add("bold", "1.0", "end")
    output_text.tag_config("bold", font=bold_font)
    messagebox.showinfo("Success", "Successfully Decoded!")

root = tk.Tk()
root.title("Binary Decoder")
root.configure(bg="pink")

bold_font = font.Font(weight="bold")

tk.Label(root, text="Enter Header:", bg="yellow", fg="black").pack()
header_entry = tk.Entry(root, width=50)
header_entry.pack()

tk.Label(root, text="Enter Message:", bg="orange", fg="black").pack()
message_text = scrolledtext.ScrolledText(root, width=50, height=10, bg="white")
message_text.pack()

tk.Button(root, text="Decode", command=decode_and_display, bg="green", fg="brown").pack()

tk.Label(root, text="Decoded Message:", bg="light grey", fg="black").pack()
output_text = scrolledtext.ScrolledText(root, width=50, height=5, bg="light blue")
output_text.pack()

root.mainloop()