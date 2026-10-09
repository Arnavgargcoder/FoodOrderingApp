import tkinter as tk
from tkinter import ttk, messagebox
from database import fetch_all, fetch_one, execute_query


class ManageOrders:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Manage Orders")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.orders = []
        self.filtered_orders = []

        self.canvas = None
        self.list_frame = None
        self.scroll_target = None

        self.create_ui()
        self.load_orders()

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
            text="Manage Orders",
            font=("Arial", 25, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            header,
            text="View and manage customer orders",
            font=("Arial", 12),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=15
        )

        tk.Button(
            header,
            text="Close",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#8B0000",
            activebackground="#EEEEEE",
            activeforeground="#8B0000",
            relief="flat",
            cursor="hand2",
            command=self.close_window
        ).pack(
            side="right",
            padx=25,
            ipadx=15,
            ipady=6
        )

        # =====================================================
        # STATISTICS
        # =====================================================

        stats = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        stats.pack(
            fill="x",
            padx=25,
            pady=(18, 10)
        )

        self.total_value = self.create_stat_card(
            stats,
            "Total Orders"
        )

        self.pending_value = self.create_stat_card(
            stats,
            "Pending"
        )

        self.confirmed_value = self.create_stat_card(
            stats,
            "Confirmed"
        )

        self.preparing_value = self.create_stat_card(
            stats,
            "Preparing"
        )

        self.delivered_value = self.create_stat_card(
            stats,
            "Delivered"
        )

        self.cancelled_value = self.create_stat_card(
            stats,
            "Cancelled"
        )

        # =====================================================
        # FILTER BAR
        # =====================================================

        filter_frame = tk.Frame(
            self.window,
            bg="white",
            bd=1,
            relief="solid"
        )

        filter_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 10)
        )

        tk.Label(
            filter_frame,
            text="Search",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            side="left",
            padx=(15, 8),
            pady=12
        )

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            filter_frame,
            textvariable=self.search_var,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            width=30
        )

        search_entry.pack(
            side="left",
            ipady=7
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.apply_filters()
        )

        tk.Label(
            filter_frame,
            text="Status",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            side="left",
            padx=(25, 8)
        )

        self.status_var = tk.StringVar(
            value="All"
        )

        status_box = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=[
                "All",
                "Pending",
                "Confirmed",
                "Preparing",
                "Out for Delivery",
                "Delivered",
                "Cancelled"
            ],
            state="readonly",
            width=20
        )

        status_box.pack(
            side="left",
            ipady=5
        )

        status_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        tk.Button(
            filter_frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.load_orders
        ).pack(
            side="right",
            padx=15,
            ipadx=15,
            ipady=6
        )

        # =====================================================
        # ORDER LIST
        # =====================================================

        list_area = tk.Frame(
            self.window,
            bg="#F4F6F8"
        )

        list_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        self.canvas = tk.Canvas(
            list_area,
            bg="#F4F6F8",
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            list_area,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.list_frame = tk.Frame(
            self.canvas,
            bg="#F4F6F8"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor="nw"
        )

        self.list_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas
        )

        # Bind touchpad once to the Toplevel.
        self.scroll_target = self.window

        self.scroll_target.bind(
            "<MouseWheel>",
            self.mouse_scroll,
            add="+"
        )

        self.scroll_target.bind(
            "<Button-4>",
            self.mouse_scroll,
            add="+"
        )

        self.scroll_target.bind(
            "<Button-5>",
            self.mouse_scroll,
            add="+"
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        title
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(
            pady=(12, 3)
        )

        value = tk.Label(
            card,
            text="0",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#8B0000"
        )

        value.pack(
            pady=(0, 12)
        )

        return value

    # =========================================================
    # LOAD ORDERS
    # =========================================================

    def load_orders(self):

        query = """
            SELECT
                o.id,
                o.user_id,
                o.order_date,
                o.subtotal,
                o.gst,
                o.discount,
                o.total,
                o.payment_method,
                o.status,
                u.name AS customer_name,
                u.email AS customer_email,
                u.phone AS customer_phone,
                u.address AS customer_address
            FROM orders o
            LEFT JOIN users u
                ON o.user_id = u.id
            ORDER BY o.order_date DESC, o.id DESC
        """

        try:

            self.orders = fetch_all(
                query
            )

            self.update_statistics()
            self.apply_filters()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load orders.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # STATISTICS
    # =========================================================

    def update_statistics(self):

        counts = {
            "Pending": 0,
            "Confirmed": 0,
            "Preparing": 0,
            "Out for Delivery": 0,
            "Delivered": 0,
            "Cancelled": 0
        }

        for order in self.orders:

            status = str(
                order.get(
                    "status",
                    "Pending"
                )
                or "Pending"
            )

            if status in counts:
                counts[status] += 1

        self.total_value.config(
            text=str(len(self.orders))
        )

        self.pending_value.config(
            text=str(counts["Pending"])
        )

        self.confirmed_value.config(
            text=str(counts["Confirmed"])
        )

        self.preparing_value.config(
            text=str(counts["Preparing"])
        )

        self.delivered_value.config(
            text=str(counts["Delivered"])
        )

        self.cancelled_value.config(
            text=str(counts["Cancelled"])
        )

    # =========================================================
    # FILTER
    # =========================================================

    def apply_filters(self):

        search = (
            self.search_var.get()
            .strip()
            .lower()
        )

        selected_status = (
            self.status_var.get()
        )

        self.filtered_orders = []

        for order in self.orders:

            status = str(
                order.get(
                    "status",
                    ""
                )
                or ""
            )

            searchable = " ".join([
                str(order.get("id", "")),
                str(order.get("customer_name", "")),
                str(order.get("customer_email", "")),
                str(order.get("customer_phone", "")),
                str(status)
            ]).lower()

            if search and search not in searchable:
                continue

            if (
                selected_status != "All"
                and status != selected_status
            ):
                continue

            self.filtered_orders.append(
                order
            )

        self.display_orders()

    # =========================================================
    # DISPLAY
    # =========================================================

    def display_orders(self):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.filtered_orders:

            card = tk.Frame(
                self.list_frame,
                bg="white",
                bd=1,
                relief="solid"
            )

            card.pack(
                fill="x",
                padx=10,
                pady=25
            )

            tk.Label(
                card,
                text="No Orders Found",
                font=("Arial", 22, "bold"),
                bg="white",
                fg="#333333"
            ).pack(
                pady=(45, 10)
            )

            tk.Label(
                card,
                text="Try changing the search or status filter.",
                font=("Arial", 11),
                bg="white",
                fg="#777777"
            ).pack(
                pady=(0, 45)
            )

            self.update_scroll_region()

            return

        for order in self.filtered_orders:

            self.create_order_card(
                order
            )

        self.canvas.yview_moveto(0)
        self.update_scroll_region()

    # =========================================================
    # ORDER CARD
    # =========================================================

    def create_order_card(
        self,
        order
    ):

        card = tk.Frame(
            self.list_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        # =====================================================
        # TOP
        # =====================================================

        top = tk.Frame(
            card,
            bg="white"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        tk.Label(
            top,
            text=f"Order #{order.get('id', '')}",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            side="left"
        )

        status = str(
            order.get(
                "status",
                "Pending"
            )
            or "Pending"
        )

        tk.Label(
            top,
            text=status,
            font=("Arial", 10, "bold"),
            bg=self.status_color(status),
            fg="white",
            padx=12,
            pady=5
        ).pack(
            side="right"
        )

        # =====================================================
        # CUSTOMER
        # =====================================================

        customer = tk.Frame(
            card,
            bg="#F8F8F8"
        )

        customer.pack(
            fill="x",
            padx=20,
            pady=8
        )

        customer_text = (
            f"Customer: "
            f"{order.get('customer_name', 'Unknown')}    "
            f"Phone: "
            f"{order.get('customer_phone', '')}    "
            f"Email: "
            f"{order.get('customer_email', '')}"
        )

        tk.Label(
            customer,
            text=customer_text,
            font=("Arial", 10, "bold"),
            bg="#F8F8F8",
            fg="#444444",
            anchor="w"
        ).pack(
            fill="x",
            padx=12,
            pady=10
        )

        # =====================================================
        # ORDER INFO
        # =====================================================

        info = tk.Frame(
            card,
            bg="white"
        )

        info.pack(
            fill="x",
            padx=20,
            pady=4
        )

        tk.Label(
            info,
            text=(
                "Date: "
                +
                self.format_date(
                    order.get("order_date")
                )
            ),
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        ).pack(
            side="left"
        )

        tk.Label(
            info,
            text=(
                "Payment: "
                +
                str(
                    order.get(
                        "payment_method",
                        ""
                    )
                    or ""
                )
            ),
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        ).pack(
            side="right"
        )

        # =====================================================
        # TOTAL
        # =====================================================

        total = self.to_float(
            order.get("total")
        )

        tk.Label(
            info,
            text=f"Total: ₹{total:.2f}",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#8B0000"
        ).pack(
            side="right",
            padx=25
        )

        # =====================================================
        # ACTIONS
        # =====================================================

        actions = tk.Frame(
            card,
            bg="white"
        )

        actions.pack(
            fill="x",
            padx=20,
            pady=(8, 15)
        )

        tk.Button(
            actions,
            text="View Details",
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda o=order:
                self.view_order(o)
        ).pack(
            side="right",
            padx=(8, 0),
            ipadx=10,
            ipady=5
        )

        tk.Button(
            actions,
            text="Update Status",
            font=("Arial", 10, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda o=order:
                self.update_status(o)
        ).pack(
            side="right",
            ipadx=10,
            ipady=5
        )

    # =========================================================
    # VIEW ORDER
    # =========================================================

    def view_order(
        self,
        order
    ):

        order_id = order.get(
            "id"
        )

        items_query = """
            SELECT
                oi.id,
                oi.food_id,
                oi.quantity,
                oi.price,
                f.food_name
            FROM order_items oi
            LEFT JOIN foods f
                ON oi.food_id = f.id
            WHERE oi.order_id = %s
            ORDER BY oi.id ASC
        """

        try:

            items = fetch_all(
                items_query,
                (order_id,)
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load order items.\n\n{e}",
                parent=self.window
            )

            return

        details = tk.Toplevel(
            self.window
        )

        details.title(
            f"Order #{order_id} Details"
        )

        details.state(
            "zoomed"
        )

        details.configure(
            bg="#F4F6F8"
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            details,
            bg="#8B0000",
            height=70
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"Order #{order_id}",
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
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#8B0000",
            relief="flat",
            cursor="hand2",
            command=details.destroy
        ).pack(
            side="right",
            padx=25,
            ipadx=15,
            ipady=6
        )

        body = tk.Frame(
            details,
            bg="#F4F6F8"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        # =====================================================
        # CUSTOMER DETAILS
        # =====================================================

        customer_card = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        customer_card.pack(
            fill="x",
            pady=(0, 15)
        )

        self.detail_row(
            customer_card,
            "Customer",
            str(
                order.get(
                    "customer_name",
                    ""
                )
            )
        )

        self.detail_row(
            customer_card,
            "Phone",
            str(
                order.get(
                    "customer_phone",
                    ""
                )
            )
        )

        self.detail_row(
            customer_card,
            "Email",
            str(
                order.get(
                    "customer_email",
                    ""
                )
            )
        )

        self.detail_row(
            customer_card,
            "Address",
            str(
                order.get(
                    "customer_address",
                    ""
                )
            )
        )

        self.detail_row(
            customer_card,
            "Payment",
            str(
                order.get(
                    "payment_method",
                    ""
                )
            )
        )

        self.detail_row(
            customer_card,
            "Status",
            str(
                order.get(
                    "status",
                    ""
                )
            )
        )

        # =====================================================
        # ITEMS
        # =====================================================

        item_card = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        item_card.pack(
            fill="both",
            expand=True,
            pady=(0, 15)
        )

        tk.Label(
            item_card,
            text="Order Items",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 12)
        )

        item_area = tk.Frame(
            item_card,
            bg="white"
        )

        item_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        item_canvas = tk.Canvas(
            item_area,
            bg="white",
            highlightthickness=0
        )

        item_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        item_scroll = tk.Scrollbar(
            item_area,
            orient="vertical",
            command=item_canvas.yview
        )

        item_scroll.pack(
            side="right",
            fill="y"
        )

        item_canvas.configure(
            yscrollcommand=item_scroll.set
        )

        item_frame = tk.Frame(
            item_canvas,
            bg="white"
        )

        item_window = item_canvas.create_window(
            (0, 0),
            window=item_frame,
            anchor="nw"
        )

        item_frame.bind(
            "<Configure>",
            lambda e:
                item_canvas.configure(
                    scrollregion=item_canvas.bbox(
                        "all"
                    )
                )
        )

        item_canvas.bind(
            "<Configure>",
            lambda e:
                item_canvas.itemconfig(
                    item_window,
                    width=e.width
                )
        )

        for item in items:

            quantity = int(
                item.get(
                    "quantity",
                    1
                )
            )

            price = self.to_float(
                item.get("price")
            )

            row = tk.Frame(
                item_frame,
                bg="#F8F8F8"
            )

            row.pack(
                fill="x",
                pady=5
            )

            tk.Label(
                row,
                text=(
                    item.get(
                        "food_name"
                    )
                    or "Food"
                ),
                font=("Arial", 12, "bold"),
                bg="#F8F8F8",
                fg="#333333",
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=10
            )

            tk.Label(
                row,
                text=f"Qty: {quantity}",
                font=("Arial", 11),
                bg="#F8F8F8",
                fg="#555555"
            ).pack(
                side="left",
                padx=20
            )

            tk.Label(
                row,
                text=f"₹{price * quantity:.2f}",
                font=("Arial", 12, "bold"),
                bg="#F8F8F8",
                fg="#222222"
            ).pack(
                side="right",
                padx=15
            )

        # =====================================================
        # TOTAL
        # =====================================================

        total_card = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        total_card.pack(
            fill="x"
        )

        subtotal = self.to_float(
            order.get("subtotal")
        )

        gst = self.to_float(
            order.get("gst")
        )

        discount = self.to_float(
            order.get("discount")
        )

        total = self.to_float(
            order.get("total")
        )

        tk.Label(
            total_card,
            text=(
                f"Subtotal: ₹{subtotal:.2f}    "
                f"GST: ₹{gst:.2f}    "
                f"Discount: ₹{discount:.2f}"
            ),
            font=("Arial", 11),
            bg="white",
            fg="#555555"
        ).pack(
            side="left",
            padx=25,
            pady=18
        )

        tk.Label(
            total_card,
            text=f"Total: ₹{total:.2f}",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#8B0000"
        ).pack(
            side="right",
            padx=25,
            pady=15
        )

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    def update_status(
        self,
        order
    ):

        order_id = order.get(
            "id"
        )

        dialog = tk.Toplevel(
            self.window
        )

        dialog.title(
            f"Update Order #{order_id}"
        )

        dialog.geometry(
            "420x280"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            bg="white"
        )

        tk.Label(
            dialog,
            text=f"Update Order #{order_id}",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            pady=(30, 20)
        )

        tk.Label(
            dialog,
            text="Order Status",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#444444"
        ).pack(
            pady=(0, 8)
        )

        status_var = tk.StringVar(
            value=str(
                order.get(
                    "status",
                    "Pending"
                )
                or "Pending"
            )
        )

        status_box = ttk.Combobox(
            dialog,
            textvariable=status_var,
            values=[
                "Pending",
                "Confirmed",
                "Preparing",
                "Out for Delivery",
                "Delivered",
                "Cancelled"
            ],
            state="readonly",
            width=25
        )

        status_box.pack(
            ipady=6
        )

        def save_status():

            new_status = status_var.get()

            if not new_status:
                return

            try:

                execute_query(
                    """
                    UPDATE orders
                    SET status = %s
                    WHERE id = %s
                    """,
                    (
                        new_status,
                        order_id
                    )
                )

                order["status"] = new_status

                dialog.destroy()

                self.load_orders()

                messagebox.showinfo(
                    "Order Updated",
                    f"Order #{order_id} status updated to {new_status}.",
                    parent=self.window
                )

            except Exception as e:

                messagebox.showerror(
                    "Update Error",
                    f"Unable to update order status.\n\n{e}",
                    parent=dialog
                )

        tk.Button(
            dialog,
            text="Update Status",
            font=("Arial", 11, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=save_status
        ).pack(
            pady=30,
            ipadx=25,
            ipady=8
        )

        dialog.transient(
            self.window
        )

        dialog.grab_set()

    # =========================================================
    # DETAIL ROW
    # =========================================================

    def detail_row(
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
            padx=25,
            pady=7
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#555555",
            width=18,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            font=("Arial", 10),
            bg="white",
            fg="#222222",
            anchor="w"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # =========================================================
    # TOUCHPAD / MOUSE SCROLL
    # =========================================================

    def mouse_scroll(
        self,
        event
    ):

        try:

            if not self.canvas.winfo_exists():
                return

            delta = getattr(
                event,
                "delta",
                0
            )

            if delta > 0:

                units = max(
                    1,
                    min(
                        5,
                        abs(int(delta / 60))
                    )
                )

                self.canvas.yview_scroll(
                    -units,
                    "units"
                )

            elif delta < 0:

                units = max(
                    1,
                    min(
                        5,
                        abs(int(delta / 60))
                    )
                )

                self.canvas.yview_scroll(
                    units,
                    "units"
                )

            elif getattr(
                event,
                "num",
                None
            ) == 4:

                self.canvas.yview_scroll(
                    -3,
                    "units"
                )

            elif getattr(
                event,
                "num",
                None
            ) == 5:

                self.canvas.yview_scroll(
                    3,
                    "units"
                )

        except tk.TclError:
            pass

    # =========================================================
    # SCROLL REGION
    # =========================================================

    def update_scroll_region(
        self,
        event=None
    ):

        try:

            self.canvas.configure(
                scrollregion=self.canvas.bbox(
                    "all"
                )
            )

        except tk.TclError:
            pass

    def resize_canvas(
        self,
        event
    ):

        try:

            self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )

        except tk.TclError:
            pass

    # =========================================================
    # HELPERS
    # =========================================================

    def to_float(
        self,
        value
    ):

        try:
            return float(
                value or 0
            )
        except:
            return 0.0

    def format_date(
        self,
        value
    ):

        if value is None:
            return "Not Available"

        try:

            if hasattr(
                value,
                "strftime"
            ):

                return value.strftime(
                    "%d %b %Y, %I:%M %p"
                )

        except:
            pass

        return str(
            value
        )

    def status_color(
        self,
        status
    ):

        status = str(
            status
        ).lower()

        colors = {
            "pending": "#E67E22",
            "confirmed": "#2980B9",
            "preparing": "#8E44AD",
            "out for delivery": "#16A085",
            "delivered": "#228B22",
            "cancelled": "#C0392B"
        }

        return colors.get(
            status,
            "#555555"
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def close_window(self):

        try:

            self.window.unbind(
                "<MouseWheel>"
            )

            self.window.unbind(
                "<Button-4>"
            )

            self.window.unbind(
                "<Button-5>"
            )

        except tk.TclError:
            pass

        try:

            self.window.destroy()

        except tk.TclError:
            pass
