import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from database import fetch_one, fetch_all


class AdminDashboard:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user

        self.window = tk.Toplevel(parent)
        self.window.title("Admin Dashboard")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.icon_images = {}

        self.create_ui()

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_ui(self):

        self.create_sidebar()
        self.create_main_area()
        self.dashboard()

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.window,
            bg="#171A1F",
            width=250
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # -----------------------------------------------------
        # LOGO
        # -----------------------------------------------------

        logo_frame = tk.Frame(
            self.sidebar,
            bg="#171A1F",
            height=100
        )

        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

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

            logo = logo.resize(
                (55, 55),
                Image.Resampling.LANCZOS
            )

            self.icon_images["logo"] = ImageTk.PhotoImage(logo)

            tk.Label(
                logo_frame,
                image=self.icon_images["logo"],
                bg="#171A1F"
            ).pack(
                side="left",
                padx=(20, 10)
            )

        except Exception as e:

            print("Logo could not be loaded:", e)

        tk.Label(
            logo_frame,
            text="FOOD\nADMIN",
            font=("Arial", 15, "bold"),
            bg="#171A1F",
            fg="white",
            justify="left"
        ).pack(
            side="left"
        )

        # -----------------------------------------------------
        # ADMIN PROFILE
        # -----------------------------------------------------

        profile = tk.Frame(
            self.sidebar,
            bg="#20242A",
            height=90
        )

        profile.pack(
            fill="x",
            padx=12,
            pady=(10, 20)
        )

        profile.pack_propagate(False)

        admin_icon = self.load_icon(
            "admin.png",
            (40, 40)
        )

        if admin_icon:

            tk.Label(
                profile,
                image=admin_icon,
                bg="#20242A"
            ).pack(
                side="left",
                padx=10
            )

        profile_text = tk.Frame(
            profile,
            bg="#20242A"
        )

        profile_text.pack(
            side="left"
        )

        tk.Label(
            profile_text,
            text=self.user.get(
                "name",
                "Administrator"
            ),
            font=("Arial", 11, "bold"),
            bg="#20242A",
            fg="white"
        ).pack(
            anchor="w"
        )

        tk.Label(
            profile_text,
            text="Administrator",
            font=("Arial", 9),
            bg="#20242A",
            fg="#AEB4BC"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # -----------------------------------------------------
        # MENU TITLE
        # -----------------------------------------------------

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            bg="#171A1F",
            fg="#707780"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # MENU BUTTONS
        # -----------------------------------------------------

        self.create_sidebar_button(
            "Dashboard",
            "home.png",
            self.dashboard
        )

        self.create_sidebar_button(
            "Manage Food",
            "add.png",
            self.manage_food
        )

        self.create_sidebar_button(
            "Categories",
            "edit.png",
            self.manage_categories
        )

        self.create_sidebar_button(
            "Orders",
            "orders.png",
            self.manage_orders
        )

        self.create_sidebar_button(
            "Customers",
            "user.png",
            self.customers
        )

        # -----------------------------------------------------
        # LOGOUT
        # -----------------------------------------------------

        logout_frame = tk.Frame(
            self.sidebar,
            bg="#171A1F"
        )

        logout_frame.pack(
            side="bottom",
            fill="x",
            pady=15
        )

        self.create_sidebar_button(
            "Logout",
            "logout.png",
            self.logout,
            logout_frame
        )

    # =========================================================
    # SIDEBAR BUTTON
    # =========================================================

    def create_sidebar_button(
        self,
        text,
        icon_name,
        command,
        parent=None
    ):

        if parent is None:
            parent = self.sidebar

        button_frame = tk.Frame(
            parent,
            bg="#171A1F",
            height=52
        )

        button_frame.pack(
            fill="x",
            padx=12,
            pady=3
        )

        button_frame.pack_propagate(False)

        icon = self.load_icon(
            icon_name,
            (22, 22)
        )

        button = tk.Button(
            button_frame,
            text="  " + text,
            image=icon,
            compound="left",
            font=("Arial", 11, "bold"),
            bg="#171A1F",
            fg="#D8DCE1",
            activebackground="#8B0000",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=15,
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="both",
            expand=True
        )

        if icon:

            self.icon_images[
                "sidebar_" + text
            ] = icon

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):

        self.main_area = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_topbar()

        self.content = tk.Frame(
            self.main_area,
            bg="#F4F6F8"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

    # =========================================================
    # TOP BAR
    # =========================================================

    def create_topbar(self):

        topbar = tk.Frame(
            self.main_area,
            bg="white",
            height=75
        )

        topbar.pack(
            fill="x"
        )

        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="Admin Panel",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            side="left",
            padx=30
        )

        right_frame = tk.Frame(
            topbar,
            bg="white"
        )

        right_frame.pack(
            side="right",
            padx=30
        )

        tk.Label(
            right_frame,
            text=self.user.get(
                "email",
                "admin@gmail.com"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack(
            side="left",
            padx=15
        )

        logout_icon = self.load_icon(
            "logout.png",
            (20, 20)
        )

        logout_button = tk.Button(
            right_frame,
            text="Logout",
            image=logout_icon,
            compound="left",
            font=("Arial", 10, "bold"),
            bg="#F5F5F5",
            fg="#555555",
            activebackground="#EEEEEE",
            relief="flat",
            cursor="hand2",
            command=self.logout
        )

        logout_button.pack(
            side="left",
            padx=5,
            ipady=7,
            ipadx=10
        )

        if logout_icon:

            self.icon_images[
                "top_logout"
            ] = logout_icon

    # =========================================================
    # DASHBOARD
    # =========================================================

    def dashboard(self):

        self.clear_content()

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title_frame = tk.Frame(
            self.content,
            bg="#F4F6F8"
        )

        title_frame.pack(
            fill="x"
        )

        tk.Label(
            title_frame,
            text="Dashboard",
            font=("Arial", 28, "bold"),
            bg="#F4F6F8",
            fg="#20242A"
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Overview of your food ordering business",
            font=("Arial", 11),
            bg="#F4F6F8",
            fg="#7B818A"
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        # -----------------------------------------------------
        # STATISTICS
        # -----------------------------------------------------

        stats_frame = tk.Frame(
            self.content,
            bg="#F4F6F8"
        )

        stats_frame.pack(
            fill="x"
        )

        customer_count = self.get_count(
            "SELECT COUNT(*) AS total FROM users"
        )

        food_count = self.get_count(
            "SELECT COUNT(*) AS total FROM foods"
        )

        order_count = self.get_count(
            "SELECT COUNT(*) AS total FROM orders"
        )

        revenue = self.get_revenue()

        self.create_stat_card(
            stats_frame,
            "Total Customers",
            str(customer_count),
            "user.png",
            "#E8F0FF"
        )

        self.create_stat_card(
            stats_frame,
            "Total Food Items",
            str(food_count),
            "add.png",
            "#EAF8F0"
        )

        self.create_stat_card(
            stats_frame,
            "Total Orders",
            str(order_count),
            "orders.png",
            "#FFF3E6"
        )

        self.create_stat_card(
            stats_frame,
            "Total Revenue",
            "₹ " + format(
                revenue,
                ",.2f"
            ),
            "home.png",
            "#F3EAFE"
        )

        # -----------------------------------------------------
        # DYNAMIC CENTER AREA
        # -----------------------------------------------------

        middle_frame = tk.Frame(
            self.content,
            bg="#F4F6F8"
        )

        middle_frame.pack(
            fill="both",
            expand=True,
            pady=(25, 15)
        )

        self.create_order_overview(
            middle_frame
        )

        self.create_food_availability(
            middle_frame
        )

        # -----------------------------------------------------
        # RECENT ORDERS
        # -----------------------------------------------------

        self.create_recent_orders(
            self.content
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        icon_name,
        icon_bg
    ):

        card = tk.Frame(
            parent,
            bg="white",
            height=135
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        card.pack_propagate(False)

        icon_box = tk.Frame(
            card,
            bg=icon_bg,
            width=60,
            height=60
        )

        icon_box.pack(
            side="left",
            padx=20
        )

        icon_box.pack_propagate(False)

        icon = self.load_icon(
            icon_name,
            (32, 32)
        )

        if icon:

            tk.Label(
                icon_box,
                image=icon,
                bg=icon_bg
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

        text_frame = tk.Frame(
            card,
            bg="white"
        )

        text_frame.pack(
            side="left"
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#7C828A"
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text=value,
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    # =========================================================
    # ORDER OVERVIEW
    # =========================================================

    def create_order_overview(self, parent):

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        tk.Label(
            frame,
            text="Order Overview",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            frame,
            text="Current order status",
            font=("Arial", 10),
            bg="white",
            fg="#888888"
        ).pack(
            anchor="w",
            padx=20
        )

        status_data = self.get_order_status()

        statuses = [
            ("Pending", "#F39C12"),
            ("Preparing", "#3498DB"),
            ("Completed", "#27AE60"),
            ("Cancelled", "#E74C3C")
        ]

        total_orders = sum(
            status_data.values()
        )

        for status, color in statuses:

            count = status_data.get(
                status,
                0
            )

            row = tk.Frame(
                frame,
                bg="white"
            )

            row.pack(
                fill="x",
                padx=25,
                pady=9
            )

            tk.Label(
                row,
                text=status,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#444444",
                width=14,
                anchor="w"
            ).pack(
                side="left"
            )

            bar_background = tk.Frame(
                row,
                bg="#EEEEEE",
                height=12
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True,
                padx=10
            )

            bar_background.pack_propagate(False)

            if total_orders > 0:

                percentage = (
                    count / total_orders
                )

                bar = tk.Frame(
                    bar_background,
                    bg=color
                )

                bar.place(
                    relx=0,
                    rely=0,
                    relheight=1,
                    relwidth=percentage
                )

            else:

                bar = tk.Frame(
                    bar_background,
                    bg=color,
                    width=2
                )

                bar.pack(
                    side="left",
                    fill="y"
                )

            tk.Label(
                row,
                text=str(count),
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#333333",
                width=5
            ).pack(
                side="right"
            )

    # =========================================================
    # FOOD AVAILABILITY
    # =========================================================

    def create_food_availability(self, parent):

        frame = tk.Frame(
            parent,
            bg="white",
            width=350
        )

        frame.pack(
            side="right",
            fill="y"
        )

        frame.pack_propagate(False)

        tk.Label(
            frame,
            text="Food Availability",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            frame,
            text="Current menu status",
            font=("Arial", 10),
            bg="white",
            fg="#888888"
        ).pack(
            anchor="w",
            padx=20
        )

        available = self.get_count(
            """
            SELECT COUNT(*) AS total
            FROM foods
            WHERE available = TRUE
            """
        )

        unavailable = self.get_count(
            """
            SELECT COUNT(*) AS total
            FROM foods
            WHERE available = FALSE
            """
        )

        total = available + unavailable

        self.availability_item(
            frame,
            "Available",
            available,
            "#27AE60"
        )

        self.availability_item(
            frame,
            "Unavailable",
            unavailable,
            "#E74C3C"
        )

        tk.Label(
            frame,
            text=f"Total Food Items: {total}",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#555555"
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

    # =========================================================
    # AVAILABILITY ITEM
    # =========================================================

    def availability_item(
        self,
        parent,
        title,
        count,
        color
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(22, 5)
        )

        indicator = tk.Frame(
            row,
            bg=color,
            width=15,
            height=15
        )

        indicator.pack(
            side="left"
        )

        indicator.pack_propagate(False)

        tk.Label(
            row,
            text=title,
            font=("Arial", 11),
            bg="white",
            fg="#555555"
        ).pack(
            side="left",
            padx=10
        )

        tk.Label(
            row,
            text=str(count),
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            side="right"
        )

    # =========================================================
    # RECENT ORDERS
    # =========================================================

    def create_recent_orders(self, parent):

        # IMPORTANT:
        # No fixed height here.
        # The frame will automatically expand according
        # to the number of rows.

        frame = tk.Frame(
            parent,
            bg="white"
        )

        frame.pack(
            fill="x"
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title_frame = tk.Frame(
            frame,
            bg="white"
        )

        title_frame.pack(
            fill="x"
        )

        tk.Label(
            title_frame,
            text="Recent Orders",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            side="left",
            padx=20,
            pady=18
        )

        # -----------------------------------------------------
        # TABLE HEADER
        # -----------------------------------------------------

        header_frame = tk.Frame(
            frame,
            bg="#F7F8FA"
        )

        header_frame.pack(
            fill="x",
            padx=15
        )

        headers = [
            "Order ID",
            "Customer",
            "Date",
            "Total",
            "Status"
        ]

        for header in headers:

            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 10, "bold"),
                bg="#F7F8FA",
                fg="#666666",
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=8,
                pady=10
            )

        # -----------------------------------------------------
        # DATA
        # -----------------------------------------------------

        orders = self.get_recent_orders()

        if not orders:

            empty_frame = tk.Frame(
                frame,
                bg="white",
                height=70
            )

            empty_frame.pack(
                fill="x"
            )

            empty_frame.pack_propagate(False)

            tk.Label(
                empty_frame,
                text="No orders available",
                font=("Arial", 11),
                bg="white",
                fg="#888888"
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            return

        for order in orders:

            row = tk.Frame(
                frame,
                bg="white"
            )

            row.pack(
                fill="x",
                padx=15
            )

            order_date = order.get(
                "order_date",
                ""
            )

            if order_date:

                order_date = str(
                    order_date
                )[:16]

            values = [
                "#" + str(
                    order["id"]
                ),

                order["customer"],

                order_date,

                "₹ " + format(
                    float(order["total"]),
                    ",.2f"
                ),

                order["status"]
            ]

            for value in values:

                tk.Label(
                    row,
                    text=value,
                    font=("Arial", 10),
                    bg="white",
                    fg="#333333",
                    anchor="w"
                ).pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=8,
                    pady=9
                )

    # =========================================================
    # DATABASE - COUNT
    # =========================================================

    def get_count(self, query):

        try:

            result = fetch_one(query)

            if result:

                return int(
                    result["total"]
                )

        except Exception as e:

            print(
                "Database error:",
                e
            )

        return 0

    # =========================================================
    # DATABASE - REVENUE
    # =========================================================

    def get_revenue(self):

        try:

            query = """
                SELECT
                    COALESCE(
                        SUM(total),
                        0
                    ) AS revenue
                FROM orders
            """

            result = fetch_one(query)

            if result:

                return float(
                    result["revenue"]
                )

        except Exception as e:

            print(
                "Revenue error:",
                e
            )

        return 0.0

    # =========================================================
    # DATABASE - ORDER STATUS
    # =========================================================

    def get_order_status(self):

        status_data = {}

        try:

            query = """
                SELECT
                    status,
                    COUNT(*) AS total
                FROM orders
                GROUP BY status
            """

            rows = fetch_all(query)

            for row in rows:

                status = row["status"]

                if status:

                    # Make database values consistent
                    status = str(
                        status
                    ).strip().capitalize()

                    status_data[
                        status
                    ] = int(
                        row["total"]
                    )

        except Exception as e:

            print(
                "Order status error:",
                e
            )

        return status_data

    # =========================================================
    # DATABASE - RECENT ORDERS
    # =========================================================

    def get_recent_orders(self):

        try:

            query = """
                SELECT
                    o.id,
                    u.name AS customer,
                    o.order_date,
                    o.total,
                    o.status
                FROM orders o
                JOIN users u
                    ON o.user_id = u.id
                ORDER BY o.id DESC
                LIMIT 6
            """

            return fetch_all(query)

        except Exception as e:

            print(
                "Recent orders error:",
                e
            )

        return []

    # =========================================================
    # MANAGE FOOD
    # =========================================================

    def manage_food(self):

        try:

            from admin.manage_food import ManageFood

            ManageFood(
                self.window
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open Manage Food.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # MANAGE CATEGORIES
    # =========================================================

    def manage_categories(self):

        try:

            from admin.manage_categories import ManageCategories

            ManageCategories(
                self.window
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open Categories.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # MANAGE ORDERS
    # =========================================================

    def manage_orders(self):

        try:

            from admin.manage_orders import ManageOrders

            ManageOrders(
                self.window
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open Orders.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # CUSTOMERS
    # =========================================================

    def customers(self):

        try:

            from admin.customers import Customers

            Customers(
                self.window
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open Customers.\n\n{e}",
                parent=self.window
            )

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

      # Close dashboard
      self.window.destroy()

      # Reopen the original main.py window
      self.parent.deiconify()
      self.parent.state("zoomed")
      self.parent.lift()
      self.parent.focus_force()
    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()

    # =========================================================
    # LOAD ICON
    # =========================================================

    def load_icon(
        self,
        filename,
        size
    ):

        path = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            ),
            "assets",
            "icons",
            filename
        )

        try:

            image = Image.open(path)

            image = image.resize(
                size,
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            self.icon_images[
                filename + str(size)
            ] = photo

            return photo

        except Exception as e:

            print(
                f"Icon could not be loaded: {filename}",
                e
            )

            return None


# =============================================================
# TESTING
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Food Ordering App"
    )

    root.state("zoomed")

    test_user = {
        "id": 1,
        "name": "Administrator",
        "email": "admin@gmail.com"
    }

    AdminDashboard(
        root,
        test_user
    )

    root.mainloop()
