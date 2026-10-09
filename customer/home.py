import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class CustomerHome:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user

        # Shared cart for Menu and Cart
        self.cart = []

        self.window = tk.Toplevel(parent)
        self.window.title("Customer Home")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.logo_image = None

        self.create_ui()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.logout
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

        logo_path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            ),
            "assets",
            "logo.png"
        )

        try:

            logo = Image.open(logo_path)

            logo.thumbnail(
                (55, 55),
                Image.Resampling.LANCZOS
            )

            self.logo_image = ImageTk.PhotoImage(logo)

            tk.Label(
                header,
                image=self.logo_image,
                bg="#8B0000"
            ).pack(
                side="left",
                padx=(25, 10)
            )

        except Exception as e:

            print(
                "Logo could not be loaded:",
                e
            )

        tk.Label(
            header,
            text="Food Ordering App",
            font=("Arial", 23, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left"
        )

        tk.Label(
            header,
            text=f"Welcome, {self.user['name']}",
            font=("Arial", 12, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="right",
            padx=30
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar = tk.Frame(
            self.window,
            bg="#222222",
            width=240
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="CUSTOMER PANEL",
            font=("Arial", 15, "bold"),
            bg="#222222",
            fg="white"
        ).pack(
            pady=(30, 25)
        )

        self.create_sidebar_button(
            sidebar,
            "Home",
            self.show_home
        )

        self.create_sidebar_button(
            sidebar,
            "Menu",
            self.show_menu
        )

        self.create_sidebar_button(
            sidebar,
            "Cart",
            self.show_cart
        )

        self.create_sidebar_button(
            sidebar,
            "My Orders",
            self.show_orders
        )

        self.create_sidebar_button(
            sidebar,
            "Profile",
            self.show_profile
        )

        # Spacer
        tk.Frame(
            sidebar,
            bg="#222222"
        ).pack(
            fill="both",
            expand=True
        )

        # Logout
        tk.Button(
            sidebar,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.logout
        ).pack(
            fill="x",
            padx=15,
            pady=20,
            ipady=10
        )

        # =====================================================
        # CONTENT AREA
        # =====================================================

        self.content = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        self.show_home()

    # =========================================================
    # SIDEBAR BUTTON
    # =========================================================

    def create_sidebar_button(
        self,
        parent,
        text,
        command
    ):

        tk.Button(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=25,
            command=command
        ).pack(
            fill="x",
            padx=15,
            pady=5,
            ipady=10
        )

    # =========================================================
    # HOME
    # =========================================================

    def show_home(self):

        self.clear_content()

        tk.Label(
            self.content,
            text=f"Welcome, {self.user['name']}",
            font=("Arial", 32, "bold"),
            bg="#F4F6F8",
            fg="#222222"
        ).pack(
            pady=(55, 5)
        )

        tk.Label(
            self.content,
            text="What would you like to order today?",
            font=("Arial", 15),
            bg="#F4F6F8",
            fg="#666666"
        ).pack(
            pady=(0, 40)
        )

        cards = tk.Frame(
            self.content,
            bg="#F4F6F8"
        )

        cards.pack(
            fill="x",
            padx=50
        )

        self.create_home_card(
            cards,
            "Browse Menu",
            "Explore our food menu",
            self.show_menu
        )

        self.create_home_card(
            cards,
            "My Cart",
            "View items added to cart",
            self.show_cart
        )

        self.create_home_card(
            cards,
            "My Orders",
            "View your previous orders",
            self.show_orders
        )

        tk.Button(
            self.content,
            text="Order Now",
            font=("Arial", 14, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.show_menu
        ).pack(
            pady=45,
            ipadx=50,
            ipady=12
        )

    # =========================================================
    # HOME CARD
    # =========================================================

    def create_home_card(
        self,
        parent,
        title,
        description,
        command
    ):

        card = tk.Frame(
            parent,
            bg="white",
            height=180
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            pady=(35, 10)
        )

        tk.Label(
            card,
            text=description,
            font=("Arial", 11),
            bg="white",
            fg="#777777"
        ).pack()

        tk.Button(
            card,
            text="Open",
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=command
        ).pack(
            pady=20,
            ipadx=15,
            ipady=5
        )

    # =========================================================
    # MENU
    # =========================================================

    def show_menu(self):

        self.clear_content()

        from customer.menu import CustomerMenu

        CustomerMenu(
            self.content,
            self.user,
            self.cart
        )

    # =========================================================
    # CART
    # =========================================================

    def show_cart(self):

        self.clear_content()

        from customer.cart import CustomerCart

        CustomerCart(
            self.content,
            self.user,
            self.cart
        )

    # =========================================================
    # ORDERS
    # =========================================================

    def show_orders(self):

        self.clear_content()

        from customer.orders import CustomerOrders

        CustomerOrders(
            self.content,
            self.user
        )

    # =========================================================
    # PROFILE
    # =========================================================

    def show_profile(self):

        self.clear_content()

        tk.Label(
            self.content,
            text="My Profile",
            font=("Arial", 30, "bold"),
            bg="#F4F6F8",
            fg="#222222"
        ).pack(
            pady=(50, 30)
        )

        profile = tk.Frame(
            self.content,
            bg="white",
            width=600,
            height=400
        )

        profile.place(
            relx=0.5,
            rely=0.52,
            anchor="center"
        )

        profile.pack_propagate(False)

        self.create_profile_row(
            profile,
            "Name",
            self.user.get("name", "")
        )

        self.create_profile_row(
            profile,
            "Email",
            self.user.get("email", "")
        )

        self.create_profile_row(
            profile,
            "Phone",
            self.user.get("phone", "")
        )

        self.create_profile_row(
            profile,
            "Address",
            self.user.get("address", "")
        )

    # =========================================================
    # PROFILE ROW
    # =========================================================

    def create_profile_row(
        self,
        parent,
        label,
        value
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=45,
            pady=12
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#555555",
            width=12,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=str(value),
            font=("Arial", 11),
            bg="white",
            fg="#222222",
            anchor="w"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.window
        )

        if not answer:
            return

        try:

            self.window.destroy()

        except tk.TclError:
            pass

        self.parent.deiconify()
        self.parent.state("zoomed")
        self.parent.lift()
        self.parent.focus_force()
