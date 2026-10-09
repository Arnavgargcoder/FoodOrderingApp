import tkinter as tk
from PIL import Image, ImageTk

from config import APP_NAME, LOGO_PATH
from admin_sync import sync_admin_data


# ============================================
# SYNC ADMIN EXCEL DATA WITH MYSQL
# ============================================

sync_admin_data()


# ============================================
# MAIN APPLICATION
# ============================================

class FoodOrderingApp:

    def __init__(self, root):

        self.root = root

        self.root.title(APP_NAME)
        self.root.state("zoomed")
        self.root.configure(bg="white")

        self.logo_image = None

        self.create_ui()

    # ========================================
    # CREATE MAIN UI
    # ========================================

    def create_ui(self):

        # ------------------------------------
        # HEADER
        # ------------------------------------

        header = tk.Frame(
            self.root,
            bg="#8B0000",
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # ------------------------------------
        # LOGO
        # ------------------------------------

        try:

            logo = Image.open(LOGO_PATH)

            logo = logo.resize(
                (60, 60),
                Image.Resampling.LANCZOS
            )

            self.logo_image = ImageTk.PhotoImage(logo)

            logo_label = tk.Label(
                header,
                image=self.logo_image,
                bg="#8B0000"
            )

            logo_label.pack(
                side="left",
                padx=20
            )

        except Exception as e:

            print("Logo could not be loaded:", e)

        # ------------------------------------
        # HEADER TITLE
        # ------------------------------------

        title = tk.Label(
            header,
            text="Food Ordering App",
            font=("Arial", 26, "bold"),
            bg="#8B0000",
            fg="white"
        )

        title.pack(
            side="left",
            padx=10
        )

        # ------------------------------------
        # MAIN AREA
        # ------------------------------------

        main_frame = tk.Frame(
            self.root,
            bg="white"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------
        # CENTER BOX
        # ------------------------------------

        box = tk.Frame(
            main_frame,
            bg="white"
        )

        box.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ------------------------------------
        # WELCOME
        # ------------------------------------

        welcome = tk.Label(
            box,
            text="Welcome",
            font=("Arial", 32, "bold"),
            bg="white",
            fg="#222222"
        )

        welcome.pack(
            pady=10
        )

        # ------------------------------------
        # SUBTITLE
        # ------------------------------------

        subtitle = tk.Label(
            box,
            text="Order your favourite food",
            font=("Arial", 16),
            bg="white",
            fg="#666666"
        )

        subtitle.pack(
            pady=10
        )

        # ------------------------------------
        # CUSTOMER LOGIN
        # ------------------------------------

        customer_button = tk.Button(
            box,
            text="Customer Login",
            font=("Arial", 14, "bold"),
            width=25,
            height=2,
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.customer_login
        )

        customer_button.pack(
            pady=8
        )

        # ------------------------------------
        # CREATE ACCOUNT
        # ------------------------------------

        signup_button = tk.Button(
            box,
            text="Create Account",
            font=("Arial", 14, "bold"),
            width=25,
            height=2,
            bg="#444444",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.signup
        )

        signup_button.pack(
            pady=8
        )

        # ------------------------------------
        # ADMIN LOGIN
        # ------------------------------------

        admin_button = tk.Button(
            box,
            text="Admin Login",
            font=("Arial", 14, "bold"),
            width=25,
            height=2,
            bg="#222222",
            fg="white",
            activebackground="#111111",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.admin_login
        )

        admin_button.pack(
            pady=8
        )

        # ------------------------------------
        # FOOTER
        # ------------------------------------

        footer = tk.Label(
            self.root,
            text="Food Ordering App",
            font=("Arial", 10),
            bg="#222222",
            fg="white",
            height=2
        )

        footer.pack(
            fill="x",
            side="bottom"
        )

    # ========================================
    # CUSTOMER LOGIN
    # ========================================

    def customer_login(self):

        from customer.login import CustomerLogin

        CustomerLogin(
            self.root
        )

    # ========================================
    # CUSTOMER SIGNUP
    # ========================================

    def signup(self):

        from customer.signup import CustomerSignup

        CustomerSignup(
            self.root
        )

    # ========================================
    # ADMIN LOGIN
    # ========================================

    def admin_login(self):

        # Hide main window
        self.root.withdraw()

        from admin.admin_login import AdminLogin

        AdminLogin(
            self.root
        )


# ============================================
# START APPLICATION
# ============================================

if __name__ == "__main__":

    root = tk.Tk()

    app = FoodOrderingApp(
        root
    )

    root.mainloop()
