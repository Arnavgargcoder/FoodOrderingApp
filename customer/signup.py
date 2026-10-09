import tkinter as tk
from tkinter import messagebox

from database import fetch_one, execute_query


class CustomerSignup:

    def __init__(self, parent):

        self.parent = parent

        # Hide main window while signup is open
        self.parent.withdraw()

        self.window = tk.Toplevel(parent)
        self.window.title("Create Account")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.create_ui()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =========================================================
    # CREATE UI
    # =========================================================

    def create_ui(self):

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            self.window,
            bg="#8B0000",
            height=75
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Food Ordering App",
            font=("Arial", 24, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=30
        )

        tk.Button(
            header,
            text="Back",
            font=("Arial", 11, "bold"),
            bg="#660000",
            fg="white",
            activebackground="#500000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.close_window
        ).pack(
            side="right",
            padx=25,
            ipadx=18,
            ipady=8
        )

        # =====================================================
        # MAIN AREA
        # =====================================================

        main = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        main.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # SIGNUP CARD
        # =====================================================

        card = tk.Frame(
            main,
            bg="white",
            width=650,
            height=700
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        # =====================================================
        # TITLE
        # =====================================================

        tk.Label(
            card,
            text="Create Account",
            font=("Arial", 30, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            card,
            text="Register to start ordering food",
            font=("Arial", 12),
            bg="white",
            fg="#777777"
        ).pack(
            pady=(0, 20)
        )

        # =====================================================
        # FORM
        # =====================================================

        form = tk.Frame(
            card,
            bg="white"
        )

        form.pack(
            fill="x",
            padx=55
        )

        # =====================================================
        # NAME
        # =====================================================

        tk.Label(
            form,
            text="Full Name",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.name_entry = tk.Entry(
            form,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.name_entry.pack(
            fill="x",
            ipady=8
        )

        # =====================================================
        # EMAIL
        # =====================================================

        tk.Label(
            form,
            text="Email",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        self.email_entry = tk.Entry(
            form,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.email_entry.pack(
            fill="x",
            ipady=8
        )

        # =====================================================
        # PHONE
        # =====================================================

        tk.Label(
            form,
            text="Phone Number",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        self.phone_entry = tk.Entry(
            form,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.phone_entry.pack(
            fill="x",
            ipady=8
        )

        self.phone_entry.insert(
            0,
            "+91 "
        )

        self.phone_entry.bind(
            "<KeyRelease>",
            self.phone_validation
        )

        # =====================================================
        # ADDRESS
        # =====================================================

        tk.Label(
            form,
            text="Address",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        self.address_entry = tk.Entry(
            form,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.address_entry.pack(
            fill="x",
            ipady=8
        )

        # =====================================================
        # PASSWORD
        # =====================================================

        tk.Label(
            form,
            text="Password",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        password_frame = tk.Frame(
            form,
            bg="white"
        )

        password_frame.pack(
            fill="x"
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            show="*",
            relief="solid",
            bd=1
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        self.password_button = tk.Button(
            password_frame,
            text="Show",
            font=("Arial", 10, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.toggle_password
        )

        self.password_button.pack(
            side="right",
            padx=(5, 0),
            ipady=8,
            ipadx=8
        )

        # =====================================================
        # CONFIRM PASSWORD
        # =====================================================

        tk.Label(
            form,
            text="Confirm Password",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        self.confirm_entry = tk.Entry(
            form,
            font=("Arial", 12),
            show="*",
            relief="solid",
            bd=1
        )

        self.confirm_entry.pack(
            fill="x",
            ipady=8
        )

        # =====================================================
        # CREATE ACCOUNT
        # =====================================================

        tk.Button(
            card,
            text="Create Account",
            font=("Arial", 13, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.create_account
        ).pack(
            fill="x",
            padx=55,
            pady=(25, 10),
            ipady=10
        )

        # =====================================================
        # LOGIN
        # =====================================================

        tk.Button(
            card,
            text="Already have an account? Login",
            font=("Arial", 11),
            bg="white",
            fg="#8B0000",
            activebackground="white",
            activeforeground="#660000",
            relief="flat",
            cursor="hand2",
            command=self.open_login
        ).pack(
            pady=5
        )

        self.name_entry.focus_set()

        # Enter key
        self.window.bind(
            "<Return>",
            lambda event: self.create_account()
        )

    # =========================================================
    # PHONE VALIDATION
    # =========================================================

    def phone_validation(self, event=None):

        value = self.phone_entry.get()

        if not value.startswith("+91 "):

            digits = ""

            for char in value:

                if char.isdigit():
                    digits += char

            digits = digits[:10]

            self.phone_entry.delete(
                0,
                tk.END
            )

            self.phone_entry.insert(
                0,
                "+91 " + digits
            )

            return

        number = value[4:]

        digits = ""

        for char in number:

            if char.isdigit():
                digits += char

        digits = digits[:10]

        new_value = "+91 " + digits

        if value != new_value:

            self.phone_entry.delete(
                0,
                tk.END
            )

            self.phone_entry.insert(
                0,
                new_value
            )

    # =========================================================
    # TOGGLE PASSWORD
    # =========================================================

    def toggle_password(self):

        if self.password_entry.cget("show") == "*":

            self.password_entry.config(
                show=""
            )

            self.password_button.config(
                text="Hide"
            )

        else:

            self.password_entry.config(
                show="*"
            )

            self.password_button.config(
                text="Show"
            )

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    def create_account(self):

        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()

        # =====================================================
        # NAME
        # =====================================================

        if not name:

            messagebox.showwarning(
                "Required",
                "Please enter your name.",
                parent=self.window
            )

            self.name_entry.focus_set()
            return

        # =====================================================
        # EMAIL
        # =====================================================

        if not email:

            messagebox.showwarning(
                "Required",
                "Please enter your email.",
                parent=self.window
            )

            self.email_entry.focus_set()
            return

        if not email.lower().endswith("@gmail.com"):

            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid Gmail address.",
                parent=self.window
            )

            self.email_entry.focus_set()
            return

        # =====================================================
        # PHONE
        # =====================================================

        if not phone.startswith("+91 "):

            messagebox.showwarning(
                "Invalid Phone",
                "Please enter a valid Indian phone number.",
                parent=self.window
            )

            self.phone_entry.focus_set()
            return

        phone_number = phone[4:]

        if len(phone_number) != 10:

            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain exactly 10 digits.",
                parent=self.window
            )

            self.phone_entry.focus_set()
            return

        if not phone_number.isdigit():

            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain only digits.",
                parent=self.window
            )

            self.phone_entry.focus_set()
            return

        # =====================================================
        # ADDRESS
        # =====================================================

        if not address:

            messagebox.showwarning(
                "Required",
                "Please enter your address.",
                parent=self.window
            )

            self.address_entry.focus_set()
            return

        # =====================================================
        # PASSWORD
        # =====================================================

        if not password:

            messagebox.showwarning(
                "Required",
                "Please enter a password.",
                parent=self.window
            )

            self.password_entry.focus_set()
            return

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters.",
                parent=self.window
            )

            self.password_entry.focus_set()
            return

        # =====================================================
        # CONFIRM PASSWORD
        # =====================================================

        if not confirm_password:

            messagebox.showwarning(
                "Required",
                "Please confirm your password.",
                parent=self.window
            )

            self.confirm_entry.focus_set()
            return

        if password != confirm_password:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match.",
                parent=self.window
            )

            self.confirm_entry.focus_set()
            return

        # =====================================================
        # DATABASE
        # =====================================================

        try:

            # Check email

            existing_email = fetch_one(
                """
                SELECT id
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            if existing_email:

                messagebox.showwarning(
                    "Already Registered",
                    "This email is already registered.",
                    parent=self.window
                )

                self.email_entry.focus_set()
                return

            # Check phone

            existing_phone = fetch_one(
                """
                SELECT id
                FROM users
                WHERE phone = %s
                """,
                (phone_number,)
            )

            if existing_phone:

                messagebox.showwarning(
                    "Already Registered",
                    "This phone number is already registered.",
                    parent=self.window
                )

                self.phone_entry.focus_set()
                return

            # Insert customer

            query = """
                INSERT INTO users
                (
                    name,
                    email,
                    phone,
                    password,
                    address
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            execute_query(
                query,
                (
                    name,
                    email,
                    phone_number,
                    password,
                    address
                )
            )

            # =================================================
            # SUCCESS
            # =================================================

            messagebox.showinfo(
                "Account Created",
                "Your account has been created successfully.",
                parent=self.window
            )

            # Close signup window
            self.window.destroy()

            # Show MAIN WINDOW
            self.parent.deiconify()
            self.parent.state("zoomed")
            self.parent.lift()
            self.parent.focus_force()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to create account.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # OPEN LOGIN
    # =========================================================

    def open_login(self):

        self.window.destroy()

        self.parent.deiconify()
        self.parent.state("zoomed")

        from customer.login import CustomerLogin

        CustomerLogin(self.parent)

    # =========================================================
    # CLOSE
    # =========================================================

    def close_window(self):

        try:
            self.window.destroy()
        except tk.TclError:
            pass

        self.parent.deiconify()
        self.parent.state("zoomed")
        self.parent.lift()
        self.parent.focus_force()


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title("Food Ordering App")
    root.state("zoomed")
    root.configure(bg="white")

    CustomerSignup(root)

    root.mainloop()
