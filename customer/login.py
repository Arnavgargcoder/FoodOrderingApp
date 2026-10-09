import tkinter as tk
from tkinter import messagebox

from database import fetch_one


class CustomerLogin:

    def __init__(self, parent):

        self.parent = parent

        # Hide main window
        self.parent.withdraw()

        self.window = tk.Toplevel(parent)
        self.window.title("Customer Login")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.create_ui()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =========================================================
    # UI
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
        # LOGIN CARD
        # =====================================================

        card = tk.Frame(
            main,
            bg="white",
            width=500,
            height=500
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
            text="Customer Login",
            font=("Arial", 30, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            pady=(45, 5)
        )

        tk.Label(
            card,
            text="Login to continue ordering food",
            font=("Arial", 12),
            bg="white",
            fg="#777777"
        ).pack(
            pady=(0, 30)
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
            pady=(0, 6)
        )

        self.email_entry = tk.Entry(
            form,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.email_entry.pack(
            fill="x",
            ipady=9
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
            pady=(18, 6)
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
            ipady=9
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
            ipady=9,
            ipadx=8
        )

        # =====================================================
        # LOGIN BUTTON
        # =====================================================

        tk.Button(
            card,
            text="Login",
            font=("Arial", 13, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.login
        ).pack(
            fill="x",
            padx=55,
            pady=(30, 12),
            ipady=10
        )

        # =====================================================
        # CREATE ACCOUNT
        # =====================================================

        tk.Button(
            card,
            text="Create New Account",
            font=("Arial", 11),
            bg="white",
            fg="#8B0000",
            activebackground="white",
            activeforeground="#660000",
            relief="flat",
            cursor="hand2",
            command=self.open_signup
        ).pack(
            pady=5
        )

        # =====================================================
        # ENTER KEY
        # =====================================================

        self.window.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.email_entry.focus_set()

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
    # LOGIN
    # =========================================================

    def login(self):

        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        # =====================================================
        # VALIDATION
        # =====================================================

        if not email:

            messagebox.showwarning(
                "Required",
                "Please enter your email.",
                parent=self.window
            )

            self.email_entry.focus_set()
            return

        if not password:

            messagebox.showwarning(
                "Required",
                "Please enter your password.",
                parent=self.window
            )

            self.password_entry.focus_set()
            return

        # =====================================================
        # DATABASE LOGIN
        # =====================================================

        try:

            query = """
                SELECT
                    id,
                    name,
                    email,
                    phone,
                    address
                FROM users
                WHERE email = %s
                AND password = %s
            """

            user = fetch_one(
                query,
                (
                    email,
                    password
                )
            )

            if user:

                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome, {user['name']}!",
                    parent=self.window
                )

                # Close login
                self.window.destroy()

                # Open customer home
                from customer.home import CustomerHome

                CustomerHome(
                    self.parent,
                    user
                )

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid email or password.",
                    parent=self.window
                )

                self.password_entry.delete(
                    0,
                    tk.END
                )

                self.password_entry.focus_set()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to login.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # OPEN SIGNUP
    # =========================================================

    def open_signup(self):

        self.window.destroy()

        from customer.signup import CustomerSignup

        CustomerSignup(
            self.parent
        )

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

    CustomerLogin(root)

    root.mainloop()
