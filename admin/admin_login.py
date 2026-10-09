import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from database import fetch_one


class AdminLogin:

    def __init__(self, parent):

        self.parent = parent

        # ==========================================
        # WINDOW
        # ==========================================

        self.window = tk.Toplevel(parent)

        self.window.title("Admin Login")
        self.window.state("zoomed")
        self.window.configure(bg="white")

        # Keep image reference
        self.admin_icon = None

        self.create_ui()

    # ==========================================
    # CREATE UI
    # ==========================================

    def create_ui(self):

        # ==========================================
        # MAIN FRAME
        # ==========================================

        main_frame = tk.Frame(
            self.window,
            bg="white"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # LOGIN BOX
        # ==========================================

        login_box = tk.Frame(
            main_frame,
            bg="white",
            width=450,
            height=520
        )

        login_box.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        login_box.pack_propagate(False)

        # ==========================================
        # ADMIN ICON
        # ==========================================

        icon_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            ),
            "assets",
            "icons",
            "admin.png"
        )

        try:

            icon = Image.open(icon_path)

            icon = icon.resize(
                (70, 70),
                Image.Resampling.LANCZOS
            )

            self.admin_icon = ImageTk.PhotoImage(icon)

            icon_label = tk.Label(
                login_box,
                image=self.admin_icon,
                bg="white"
            )

            icon_label.pack(
                pady=(20, 10)
            )

        except Exception as e:

            print("Admin icon could not be loaded:", e)

        # ==========================================
        # TITLE
        # ==========================================

        title = tk.Label(
            login_box,
            text="Admin Login",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#222222"
        )

        title.pack(
            pady=10
        )

        # ==========================================
        # EMAIL LABEL
        # ==========================================

        email_label = tk.Label(
            login_box,
            text="Email",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        )

        email_label.pack(
            anchor="w",
            padx=40,
            pady=(15, 5)
        )

        # ==========================================
        # EMAIL ENTRY
        # ==========================================

        self.email_entry = tk.Entry(
            login_box,
            font=("Arial", 13),
            width=35,
            relief="solid",
            bd=1
        )

        self.email_entry.pack(
            padx=40,
            ipady=8
        )

        # ==========================================
        # PASSWORD LABEL
        # ==========================================

        password_label = tk.Label(
            login_box,
            text="Password",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        )

        password_label.pack(
            anchor="w",
            padx=40,
            pady=(15, 5)
        )

        # ==========================================
        # PASSWORD ENTRY
        # ==========================================

        self.password_entry = tk.Entry(
            login_box,
            font=("Arial", 13),
            width=35,
            show="*",
            relief="solid",
            bd=1
        )

        self.password_entry.pack(
            padx=40,
            ipady=8
        )

        # ==========================================
        # LOGIN BUTTON
        # ==========================================

        login_button = tk.Button(
            login_box,
            text="Login",
            font=("Arial", 13, "bold"),
            width=28,
            height=2,
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login
        )

        login_button.pack(
            pady=30
        )

        # ==========================================
        # ENTER KEY
        # ==========================================

        self.window.bind(
            "<Return>",
            lambda event: self.login()
        )

        # ==========================================
        # FOCUS EMAIL
        # ==========================================

        self.email_entry.focus_set()

    # ==========================================
    # ADMIN LOGIN
    # ==========================================

    def login(self):

        email = self.email_entry.get().strip()

        password = self.password_entry.get().strip()

        # ==========================================
        # VALIDATION
        # ==========================================

        if email == "":

            messagebox.showwarning(
                "Required",
                "Please enter admin email.",
                parent=self.window
            )

            self.email_entry.focus_set()

            return

        if password == "":

            messagebox.showwarning(
                "Required",
                "Please enter admin password.",
                parent=self.window
            )

            self.password_entry.focus_set()

            return

        # ==========================================
        # CHECK ADMIN DATABASE
        # ==========================================

        query = """
            SELECT
                id,
                name,
                email
            FROM admin
            WHERE email = %s
            AND password = %s
        """

        admin = fetch_one(
            query,
            (email, password)
        )

        # ==========================================
        # LOGIN SUCCESS
        # ==========================================

        if admin:

            messagebox.showinfo(
                "Login Successful",
                "Welcome Admin",
                parent=self.window
            )

            # Close login window
            self.window.destroy()

            # Open Admin Dashboard
            from admin.dashboard import AdminDashboard

            AdminDashboard(
                self.parent,
                admin
            )

        # ==========================================
        # LOGIN FAILED
        # ==========================================

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid admin email or password.",
                parent=self.window
            )

            self.password_entry.delete(
                0,
                tk.END
            )

            self.password_entry.focus_set()


# ==========================================
# TEST WINDOW
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title("Food Ordering App")

    root.state("zoomed")

    AdminLogin(root)

    root.mainloop()
