import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import platform 

ERROR_EMPTY_PATH = "Select a PFX file."
ERROR_EMPTY_PASSWORD = "Enter the password."
ERROR_OPENSSL_NOT_INSTALLED = "OpenSSL is not installed. Please install OpenSSL and try again."
ERROR_TITLE = "Error"

def clear_screen():
    system = platform.system()
    subprocess.run('cls' if system == 'Windows' else 'clear', shell=True)

def is_openssl_installed():
    try:
        subprocess.run(['openssl', 'version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def convert_pfx_to_crt_and_key():
    if not is_openssl_installed():
        messagebox.showerror(ERROR_TITLE, ERROR_OPENSSL_NOT_INSTALLED)
        return
    if not entry_pfx.get() or not entry_password.get():
        messagebox.showerror(ERROR_TITLE, ERROR_EMPTY_PATH if not entry_pfx.get() else ERROR_EMPTY_PASSWORD)
        return
        
    try:
        pfx_file = entry_pfx.get()
        password = entry_password.get()

        clear_screen()
        ler_pfx = f'openssl pkcs12 -in {pfx_file} -clcerts -nokeys -passin pass:{password} -legacy | openssl x509 -noout -subject -nameopt sep_multiline'
        result = subprocess.run(ler_pfx, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result.stdout.replace("subject=", "Certificate Data:") + "\n")

        if result.returncode == 0:
            print(result.stdout.replace("subject=", "Certificate Data:"))
            print('Starting the certificate conversion.\n')
            
            cert_folder = os.path.dirname(pfx_file)
            os.makedirs(cert_folder, exist_ok=True)
            
            public_crypted_key_path = os.path.join(cert_folder, 'public-crypted.key')
            certificate_path = os.path.join(cert_folder, 'certificate.crt')
            private_key_path = os.path.join(cert_folder, 'private_key.key')
            
            subprocess.run(['openssl', 'pkcs12', '-in', pfx_file, '-nocerts', '-out', public_crypted_key_path, '-passin', f'pass:{password}', '-legacy', '-passout', f'pass:{password}'])
            subprocess.run(['openssl', 'pkcs12', '-in', pfx_file, '-clcerts', '-nokeys', '-out', certificate_path, '-passin', f'pass:{password}', '-legacy'])
            subprocess.run(['openssl', 'rsa', '-in', public_crypted_key_path, '-out', private_key_path, '-passin', f'pass:{password}'])
            os.remove(public_crypted_key_path)
            
            if export_public_key.get():
                public_key_der_path = os.path.join(cert_folder, 'public_key.der')
                subprocess.run(['openssl', 'x509', '-in', certificate_path, '-outform', 'der', '-out', public_key_der_path])
                public_key_base64_path = os.path.join(cert_folder, 'public_key_base64.txt')
                subprocess.run(['openssl', 'base64', '-in', public_key_der_path, '-out', public_key_base64_path])
                #os.remove(public_key_der_path)
                result_text.insert(tk.END, f'Public Key (Base64): {public_key_base64_path}\n')

            print('Conversion completed successfully!\n')
            messagebox.showinfo("Success", "Conversion completed successfully!")
            result_text.insert(tk.END, f'Crt File: {certificate_path}\n')
            result_text.insert(tk.END, f'Key File: {private_key_path}\n')
        else:
            print("Error:")
            print(result.stderr)
            error_message = f"Error: {result.stderr}"
            messagebox.showerror(ERROR_TITLE, error_message)
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result.stderr)
            
    except Exception as e:
        print(f"Error: {e}")
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error during conversion.\n")
        result_text.config(state=tk.DISABLED)

def browse_file():
    file_path = filedialog.askopenfilename(title="Select the PFX file.", filetypes=[("PFX Files", "*.pfx")])
    entry_pfx.delete(0, tk.END)
    entry_pfx.insert(0, file_path)

def clear_result_text():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

window = tk.Tk()
window.title("PFX to CRT and Private Key Converter")

frame_input = tk.Frame(window)
frame_input.pack(padx=10, pady=10)

label_pfx = tk.Label(frame_input, text="Path of the PFX file:")
label_pfx.grid(row=0, column=0, padx=(0, 5), pady=10, sticky=tk.W)

entry_pfx = tk.Entry(frame_input, width=65)
entry_pfx.grid(row=0, column=1, padx=(0, 5), pady=10)

button_browse = tk.Button(frame_input, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, pady=10)

label_password = tk.Label(frame_input, text="Password:")
label_password.grid(row=1, column=0, padx=(0, 5), pady=10, sticky=tk.W)

entry_password = tk.Entry(frame_input, width=40, show="*")
entry_password.grid(row=1, column=1, pady=10)

export_public_key = tk.BooleanVar()
check_export_public_key = ttk.Checkbutton(frame_input, text="Export Public Key", variable=export_public_key)
check_export_public_key.grid(row=1, column=2, pady=10)

button_convert = tk.Button(window, text="Convert", command=convert_pfx_to_crt_and_key)
button_convert.pack(pady=10)

button_clear_result = tk.Button(window, text="Clear Result", command=clear_result_text)
button_clear_result.pack(pady=10)

result_text = tk.Text(window, height=10, width=100, state=tk.DISABLED)
result_text.pack(padx=10, pady=10)

window_width = 820
window_height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)

window.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

window.update_idletasks()

window.mainloop()