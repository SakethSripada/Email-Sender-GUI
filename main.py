import smtplib
from tkinter import messagebox, ttk
import tkinter as tk
import threading
import time


class EmailSender:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Email Sender")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.root.geometry("1000x500")

        self.top_label = ttk.Label(self.root, text="Email Sender Bot", font=("Arial", 18))
        self.top_label.pack()
        self.whitespace = tk.Label(self.root, text="")
        self.whitespace.pack()

        self.email_label = ttk.Label(self.root, text="Enter Your Email Address", font=("Arial", 10))
        self.email_label.pack()
        self.user_email = ttk.Entry(self.root, font=("Arial", 18))
        self.user_email.pack()

        self.pass_label = ttk.Label(self.root, text="Enter Your App Password", font=("Arial", 10))
        self.pass_label.pack()
        self.user_pass = ttk.Entry(self.root, font=("Arial", 18))
        self.user_pass.pack()

        self.email_list_label = ttk.Label(self.root, text="Enter List of Recipient Emails Separated By Comma",
                                          font=("Arial", 12))
        self.email_list_label.pack()
        self.email_list = tk.Text(self.root, height="2", font=("Arial", 18))
        self.email_list.pack()

        self.email_content_label = ttk.Label(self.root, text="Enter Content of Email",
                                             font=("Arial", 12))
        self.email_content_label.pack()
        self.email_content = tk.Text(self.root, height="2", font=("Arial", 18))
        self.email_content.pack()

        self.auto_send_label = ttk.Label(self.root, text="How often would you like the email to be automatically sent? "
                                                         "(hours)", font=("Arial", 13))
        self.auto_send_label.pack()
        self.auto_send_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.auto_send_entry.pack()

        self.whitespace3 = ttk.Label(self.root, text="")
        self.whitespace3.pack()

        self.number_emails_label = ttk.Label(self.root, text="How many Emails do you want to send?", font=("Arial", 13))
        self.number_emails_label.pack()
        self.number_of_emails = ttk.Entry(self.root, font=("Arial", 14))
        self.number_of_emails.pack()

        self.whitespace2 = ttk.Label(self.root, text="")
        self.whitespace2.pack()
        self.send_button = ttk.Button(self.root, text="Send", command=self.send_emails)
        self.send_button.pack()

        self.root.mainloop()

    def sort_email_list(self):
        email_text = self.email_list.get("1.0", "end").strip()
        emails = [email.strip() for email in email_text.split(",")]
        sorted_emails = list(set(filter(None, emails)))
        return sorted_emails

    def send_emails(self):
        useremail = self.user_email.get()
        userpass = self.user_pass.get()
        recipients = self.sort_email_list()
        email_content = self.email_content.get("1.0", "end")

        try:
            number_of_emails = int(self.number_of_emails.get())
        except ValueError:
            messagebox.showerror("Please enter a valid number of emails")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(useremail, userpass)
        for i in range(number_of_emails):
            for recipient in recipients:
                server.sendmail(useremail, recipient, email_content)

    def auto_send(self):
        try:
            interval = float(self.auto_send_entry.get())
        except ValueError:
            messagebox.showerror("Please enter a valid number of hours")

        def auto_send_wrapper():
            while True:
                self.send_emails()
                time.sleep(interval*3600)

        thread = threading.Thread(target=auto_send_wrapper)
        thread.daemon = True
        thread.start()


EmailSender()
