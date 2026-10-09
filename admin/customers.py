import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from database import fetch_all, fetch_one, execute_query


class Customers:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Customers")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.icons = {}
        self.customers = []

        self.create_ui()
        self.load_customers()

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_ui(self):

        self.create_header()

        main = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        # =====================================================
        # TITLE
        # =====================================================

        tk.Label(
            main,
            text="Customers",
            font=("Arial", 28, "bold"),
            bg="#F4F6F8",
            fg="#20242A"
        ).pack(
            anchor="w"
        )

        tk.Label(
            main,
            text="Manage registered customers",
            font=("Arial", 11),
            bg="#F4F6F8",
            fg="#7B818A"
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        # =====================================================
        # STATISTICS
        # =====================================================

        self.create_statistics(main)

        # =====================================================
        # SEARCH
        # =====================================================

        self.create_search(main)

        # =====================================================
        # CUSTOMER TABLE
        # =====================================================

        self.create_table(main)

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.window,
            bg="white",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="Customer Management",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            side="left",
            padx=30
        )

        close_icon = self.load_icon(
            "close.png",
            (20, 20)
        )

        close_button = tk.Button(
            header,
            text="Close",
            image=close_icon,
            compound="left",
            font=("Arial", 10, "bold"),
            bg="#F5F5F5",
            fg="#555555",
            relief="flat",
            cursor="hand2",
            command=self.window.destroy
        )

        close_button.pack(
            side="right",
            padx=30,
            ipadx=10,
            ipady=7
        )

    # =========================================================
    # STATISTICS
    # =========================================================

    def create_statistics(self, parent):

        frame = tk.Frame(
            parent,
            bg="#F4F6F8"
        )

        frame.pack(
            fill="x",
            pady=(0, 20)
        )

        total = self.get_total_customers()

        self.create_stat_card(
            frame,
            "Total Customers",
            total,
            "user.png",
            "#E8F0FF"
        )

        self.create_stat_card(
            frame,
            "Active Customers",
            total,
            "user.png",
            "#EAF8F0"
        )

        self.create_stat_card(
            frame,
            "Customer Records",
            total,
            "search.png",
            "#FFF3E6"
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
            height=110
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
            width=52,
            height=52
        )

        icon_box.pack(
            side="left",
            padx=20
        )

        icon_box.pack_propagate(False)

        icon = self.load_icon(
            icon_name,
            (28, 28)
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

        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#7C828A"
        ).pack(
            side="left",
            anchor="n",
            pady=(28, 0)
        )

        tk.Label(
            card,
            text=str(value),
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#222222"
        ).place(
            relx=0.34,
            rely=0.58,
            anchor="w"
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def create_search(self, parent):

        search_frame = tk.Frame(
            parent,
            bg="white",
            height=70
        )

        search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        search_frame.pack_propagate(False)

        icon = self.load_icon(
            "search.png",
            (22, 22)
        )

        if icon:

            tk.Label(
                search_frame,
                image=icon,
                bg="white"
            ).pack(
                side="left",
                padx=(20, 8)
            )

        tk.Label(
            search_frame,
            text="Search",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#444444"
        ).pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            ipady=8
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_customers
        )

        tk.Button(
            search_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.load_customers
        ).pack(
            side="right",
            padx=20,
            ipadx=12,
            ipady=7
        )

    # =========================================================
    # TABLE
    # =========================================================

    def create_table(self, parent):

        outer = tk.Frame(
            parent,
            bg="white"
        )

        outer.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            outer,
            bg="#20242A",
            height=50
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        headers = [
            "ID",
            "Name",
            "Email",
            "Phone",
            "Address",
            "Joined",
            "Action"
        ]

        for column in range(7):

            header.grid_columnconfigure(
                column,
                weight=1
            )

        for column, text in enumerate(headers):

            tk.Label(
                header,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#20242A",
                fg="white",
                anchor="w"
            ).grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=10
            )

        # -----------------------------------------------------
        # SCROLL AREA
        # -----------------------------------------------------

        table_area = tk.Frame(
            outer,
            bg="white"
        )

        table_area.pack(
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            table_area,
            bg="white",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            table_area,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table_frame = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.table_frame,
            anchor="nw"
        )

        self.table_frame.bind(
            "<Configure>",
            self.update_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_table
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

    # =========================================================
    # RESIZE TABLE
    # =========================================================

    def resize_table(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # =========================================================
    # UPDATE SCROLL
    # =========================================================

    def update_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # =========================================================
    # LOAD CUSTOMERS
    # =========================================================

    def load_customers(self):

        try:

            query = """
                SELECT
                    id,
                    name,
                    email,
                    phone,
                    address,
                    created_at
                FROM users
                ORDER BY id DESC
            """

            self.customers = fetch_all(
                query
            )

            print(
                "Customers loaded:",
                self.customers
            )

            self.display_customers(
                self.customers
            )

        except Exception as e:

            print(
                "Customer loading error:",
                e
            )

            messagebox.showerror(
                "Database Error",
                f"Unable to load customers.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # DISPLAY CUSTOMERS
    # =========================================================

    def display_customers(
        self,
        customers
    ):

        for widget in self.table_frame.winfo_children():

            widget.destroy()

        if not customers:

            empty = tk.Frame(
                self.table_frame,
                bg="white",
                height=100
            )

            empty.pack(
                fill="x"
            )

            empty.pack_propagate(False)

            tk.Label(
                empty,
                text="No customers found",
                font=("Arial", 12),
                bg="white",
                fg="#888888"
            ).place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            self.update_scroll()

            return

        for index, customer in enumerate(
            customers
        ):

            self.create_customer_row(
                customer,
                index
            )

        self.update_scroll()

    # =========================================================
    # CUSTOMER ROW
    # =========================================================

    def create_customer_row(
        self,
        customer,
        index
    ):

        background = (
            "white"
            if index % 2 == 0
            else "#F8F9FA"
        )

        row = tk.Frame(
            self.table_frame,
            bg=background,
            height=60
        )

        row.pack(
            fill="x"
        )

        row.pack_propagate(False)

        # Seven equal columns

        for column in range(7):

            row.grid_columnconfigure(
                column,
                weight=1
            )

        customer_id = customer.get(
            "id",
            ""
        )

        name = customer.get(
            "name",
            ""
        )

        email = customer.get(
            "email",
            ""
        )

        phone = customer.get(
            "phone",
            ""
        )

        address = customer.get(
            "address",
            ""
        )

        created_at = customer.get(
            "created_at",
            ""
        )

        if created_at:

            created_at = str(
                created_at
            )[:16]

        # -----------------------------------------------------
        # ID
        # -----------------------------------------------------

        self.add_cell(
            row,
            0,
            customer_id,
            background
        )

        # -----------------------------------------------------
        # NAME
        # -----------------------------------------------------

        self.add_cell(
            row,
            1,
            name,
            background
        )

        # -----------------------------------------------------
        # EMAIL
        # -----------------------------------------------------

        self.add_cell(
            row,
            2,
            email,
            background
        )

        # -----------------------------------------------------
        # PHONE
        # -----------------------------------------------------

        self.add_cell(
            row,
            3,
            phone,
            background
        )

        # -----------------------------------------------------
        # ADDRESS
        # -----------------------------------------------------

        self.add_cell(
            row,
            4,
            address if address else "-",
            background
        )

        # -----------------------------------------------------
        # JOINED
        # -----------------------------------------------------

        self.add_cell(
            row,
            5,
            created_at if created_at else "-",
            background
        )

        # -----------------------------------------------------
        # ACTION
        # -----------------------------------------------------

        action_frame = tk.Frame(
            row,
            bg=background
        )

        action_frame.grid(
            row=0,
            column=6,
            sticky="nsew"
        )

        tk.Button(
            action_frame,
            text="View",
            font=("Arial", 9, "bold"),
            bg="#E8F0FF",
            fg="#1769AA",
            activebackground="#D6E6FF",
            relief="flat",
            cursor="hand2",
            command=lambda c=customer:
            self.view_customer(c)
        ).pack(
            side="left",
            padx=4,
            pady=13
        )

        tk.Button(
            action_frame,
            text="Delete",
            font=("Arial", 9, "bold"),
            bg="#FDECEC",
            fg="#C0392B",
            activebackground="#F8D7D4",
            relief="flat",
            cursor="hand2",
            command=lambda cid=customer_id:
            self.delete_customer(cid)
        ).pack(
            side="left",
            padx=4,
            pady=13
        )

    # =========================================================
    # TABLE CELL
    # =========================================================

    def add_cell(
        self,
        parent,
        column,
        value,
        background
    ):

        tk.Label(
            parent,
            text=str(value),
            font=("Arial", 10),
            bg=background,
            fg="#333333",
            anchor="w"
        ).grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=10
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def search_customers(
        self,
        event=None
    ):

        text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if text == "":

            self.display_customers(
                self.customers
            )

            return

        filtered = []

        for customer in self.customers:

            name = str(
                customer.get(
                    "name",
                    ""
                )
            ).lower()

            email = str(
                customer.get(
                    "email",
                    ""
                )
            ).lower()

            phone = str(
                customer.get(
                    "phone",
                    ""
                )
            ).lower()

            address = str(
                customer.get(
                    "address",
                    ""
                )
            ).lower()

            if (
                text in name
                or text in email
                or text in phone
                or text in address
            ):

                filtered.append(
                    customer
                )

        self.display_customers(
            filtered
        )

    # =========================================================
    # VIEW CUSTOMER
    # =========================================================

    def view_customer(self, customer):

      window = tk.Toplevel(self.window)

      window.title("Customer Details")
      window.state("zoomed")
      window.configure(bg="#F4F6F8")

      # =========================================================
      # HEADER
      # =========================================================

      header = tk.Frame(
          window,
          bg="#8B0000",
          height=75
      )

      header.pack(fill="x")
      header.pack_propagate(False)

      tk.Label(
          header,
          text="Customer Details",
          font=("Arial", 23, "bold"),
          bg="#8B0000",
          fg="white"
      ).pack(
          side="left",
          padx=30
      )

      tk.Button(
          header,
          text="Close",
          font=("Arial", 10, "bold"),
          bg="white",
          fg="#8B0000",
          activebackground="#F5F5F5",
          relief="flat",
          cursor="hand2",
          command=window.destroy
      ).pack(
          side="right",
          padx=30,
          ipadx=15,
          ipady=7
      )

      # =========================================================
      # CENTER AREA
      # =========================================================

      center = tk.Frame(
          window,
          bg="#F4F6F8"
      )

      center.pack(
          fill="both",
          expand=True,
          padx=30,
          pady=30
      )

      # =========================================================
      # CUSTOMER CARD
      # =========================================================

      card = tk.Frame(
          center,
          bg="white"
      )

      card.place(
          relx=0.5,
          rely=0.5,
          anchor="center",
          relwidth=0.65
      )

      # =========================================================
      # USER ICON
      # =========================================================

      icon = self.load_icon(
          "user.png",
          (60, 60)
      )

      if icon:

          icon_label = tk.Label(
              card,
              image=icon,
              bg="white"
          )

          icon_label.pack(
              pady=(30, 10)
          )

          # Keep reference
          card.customer_icon = icon

      # =========================================================
      # CUSTOMER NAME
      # =========================================================

      tk.Label(
          card,
          text=str(
              customer.get(
                  "name",
                  "Customer"
              )
          ),
          font=("Arial", 25, "bold"),
          bg="white",
          fg="#222222"
      ).pack(
          pady=(0, 5)
      )

      # =========================================================
      # SUBTITLE
      # =========================================================

      tk.Label(
          card,
          text="Customer Information",
          font=("Arial", 11),
          bg="white",
          fg="#888888"
      ).pack(
          pady=(0, 20)
      )

      # =========================================================
      # DETAILS
      # =========================================================

      details = [
          (
              "Customer ID",
              customer.get("id", "-")
          ),
          (
              "Full Name",
              customer.get("name", "-")
          ),
          (
              "Email Address",
              customer.get("email", "-")
          ),
          (
              "Phone Number",
              customer.get("phone", "-")
          ),
          (
              "Address",
              customer.get("address", "-")
          ),
          (
              "Created At",
              customer.get("created_at", "-")
          )
      ]

      for title, value in details:

          row = tk.Frame(
              card,
              bg="white"
          )

          row.pack(
              fill="x",
              padx=100,
              pady=5
          )

          tk.Label(
              row,
              text=title,
              font=("Arial", 11, "bold"),
              bg="white",
              fg="#555555",
              width=20,
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
      # CLOSE BUTTON
      # =========================================================

      tk.Button(
          card,
          text="Close",
          font=("Arial", 11, "bold"),
          bg="#8B0000",
          fg="white",
          activebackground="#660000",
          activeforeground="white",
          relief="flat",
          cursor="hand2",
          command=window.destroy
      ).pack(
          pady=(20, 30),
          ipadx=35,
          ipady=8
      )

      # =========================================================
      # UPDATE CARD HEIGHT AFTER CONTENT IS CREATED
      # =========================================================

      window.update_idletasks()

      card_height = card.winfo_reqheight()

      card.place_configure(
          rely=0.5,
          relheight=None,
          height=card_height
      )

    # =========================================================
    # DELETE CUSTOMER
    # =========================================================

    def delete_customer(
        self,
        customer_id
    ):

        customer = fetch_one(
            """
            SELECT
                name,
                email
            FROM users
            WHERE id = %s
            """,
            (customer_id,)
        )

        if not customer:

            messagebox.showerror(
                "Error",
                "Customer not found.",
                parent=self.window
            )

            return

        confirm = messagebox.askyesno(
            "Delete Customer",
            (
                "Are you sure you want to delete this customer?\n\n"
                f"Name: {customer['name']}\n"
                f"Email: {customer['email']}\n\n"
                "This action cannot be undone."
            ),
            parent=self.window
        )

        if not confirm:

            return

        try:

            execute_query(
                """
                DELETE FROM users
                WHERE id = %s
                """,
                (customer_id,)
            )

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully.",
                parent=self.window
            )

            self.load_customers()

        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                f"Unable to delete customer.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # CUSTOMER COUNT
    # =========================================================

    def get_total_customers(self):

        try:

            result = fetch_one(
                """
                SELECT COUNT(*) AS total
                FROM users
                """
            )

            if result:

                return int(
                    result["total"]
                )

        except Exception as e:

            print(
                "Customer count error:",
                e
            )

        return 0

    # =========================================================
    # MOUSE SCROLL
    # =========================================================

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(
            int(
                -1 * (event.delta / 120)
            ),
            "units"
        )

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

            image = Image.open(
                path
            )

            image = image.resize(
                size,
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            self.icons[
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
# TEST
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Food Ordering App"
    )

    root.state("zoomed")

    Customers(root)

    root.mainloop()

