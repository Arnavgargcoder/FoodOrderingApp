import tkinter as tk
from tkinter import messagebox
from database import fetch_all


class CustomerOrders:

    def __init__(self, parent, user):

        self.parent = parent
        self.user = user
        self.orders = []

        self.build_page()
        self.load_orders()

    # =========================================================
    # BUILD PAGE
    # =========================================================

    def build_page(self):

        self.page = tk.Frame(
            self.parent,
            bg="#F4F6F8"
        )

        self.page.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            self.page,
            bg="#8B0000",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="My Orders",
            font=("Arial", 25, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            header,
            text="Your order history",
            font=("Arial", 12),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="right",
            padx=30
        )

        # =====================================================
        # TOOLBAR
        # =====================================================

        toolbar = tk.Frame(
            self.page,
            bg="#F4F6F8",
            height=60
        )

        toolbar.pack(
            fill="x",
            padx=25,
            pady=(10, 0)
        )

        toolbar.pack_propagate(False)

        self.count_label = tk.Label(
            toolbar,
            text="Loading orders...",
            font=("Arial", 13, "bold"),
            bg="#F4F6F8",
            fg="#333333"
        )

        self.count_label.pack(
            side="left",
            pady=10
        )

        tk.Button(
            toolbar,
            text="Refresh",
            font=("Arial", 11, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.load_orders
        ).pack(
            side="right",
            ipadx=15,
            ipady=6
        )

        # =====================================================
        # SCROLL AREA
        # =====================================================

        area = tk.Frame(
            self.page,
            bg="#F4F6F8"
        )

        area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 20)
        )

        self.canvas = tk.Canvas(
            area,
            bg="#F4F6F8",
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar = tk.Scrollbar(
            area,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
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
            self.resize_canvas_window
        )

        # Touchpad / mouse wheel
        # Bind only once to the page. Binding every child causes
        # one touchpad gesture to be processed multiple times.
        self.bind_touchpad_scroll()

        # Remove the top-level bindings when this page is destroyed.
        self.page.bind(
            "<Destroy>",
            self.on_page_destroy,
            add="+"
        )

    def on_page_destroy(self, event=None):

        try:
            if event is not None and event.widget != self.page:
                return
            self.unbind_touchpad_scroll()
        except tk.TclError:
            pass

    # =========================================================
    # LOAD ORDERS
    # =========================================================

    def load_orders(self):

        self.count_label.config(
            text="Loading orders..."
        )

        # Force the UI to update before database operation.
        self.page.update_idletasks()

        query = """
            SELECT
                id,
                order_date,
                subtotal,
                gst,
                discount,
                total,
                payment_method,
                status
            FROM orders
            WHERE user_id = %s
            ORDER BY order_date DESC, id DESC
        """

        try:

            user_id = self.user.get("id")

            if not user_id:

                self.show_error(
                    "Customer ID is missing. Please login again."
                )

                return

            self.orders = fetch_all(
                query,
                (user_id,)
            )

            self.count_label.config(
                text=f"Total Orders: {len(self.orders)}"
            )

            self.display_orders()

        except Exception as e:

            self.count_label.config(
                text="Unable to load orders"
            )

            self.show_error(
                f"Unable to load your orders.\n\n{e}"
            )

    # =========================================================
    # DISPLAY ORDERS
    # =========================================================

    def display_orders(self):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.orders:

            self.show_empty()

            return

        for order in self.orders:

            self.create_order_card(
                order
            )

        # IMPORTANT:
        # Order cards are created AFTER the initial touchpad
        # bindings. Add the custom scroll bind tag again so
        # dynamically-created cards, labels and buttons also
        # receive touchpad events.
        try:
            self.add_scroll_bind_tag(
                self.list_frame
            )
        except tk.TclError:
            pass

        self.canvas.yview_moveto(0)

        self.update_scroll_region()

    # =========================================================
    # EMPTY ORDERS
    # =========================================================

    def show_empty(self):

        card = tk.Frame(
            self.list_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.pack(
            fill="x",
            padx=10,
            pady=20
        )

        tk.Label(
            card,
            text="No Orders Yet",
            font=("Arial", 25, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            pady=(55, 10)
        )

        tk.Label(
            card,
            text="Your orders will appear here after you place an order.",
            font=("Arial", 12),
            bg="white",
            fg="#777777"
        ).pack(
            pady=(0, 55)
        )

    # =========================================================
    # ORDER CARD
    # =========================================================

    def create_order_card(self, order):

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
            pady=(18, 8)
        )

        order_id = order.get("id", "")

        tk.Label(
            top,
            text=f"Order #{order_id}",
            font=("Arial", 18, "bold"),
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
        # DATE / PAYMENT
        # =====================================================

        info = tk.Frame(
            card,
            bg="white"
        )

        info.pack(
            fill="x",
            padx=20,
            pady=3
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
            font=("Arial", 11),
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
                        "Not Available"
                    )
                    or "Not Available"
                )
            ),
            font=("Arial", 11),
            bg="white",
            fg="#666666"
        ).pack(
            side="right"
        )

        # =====================================================
        # ITEMS
        # =====================================================

        items = self.get_items(
            order_id
        )

        items_box = tk.Frame(
            card,
            bg="#F8F8F8",
            bd=1,
            relief="solid"
        )

        items_box.pack(
            fill="x",
            padx=20,
            pady=12
        )

        if not items:

            tk.Label(
                items_box,
                text="No item details available.",
                font=("Arial", 11),
                bg="#F8F8F8",
                fg="#777777"
            ).pack(
                anchor="w",
                padx=15,
                pady=15
            )

        else:

            for item in items:

                row = tk.Frame(
                    items_box,
                    bg="#F8F8F8"
                )

                row.pack(
                    fill="x",
                    padx=12,
                    pady=7
                )

                food_name = (
                    item.get(
                        "food_name"
                    )
                    or "Food"
                )

                try:
                    quantity = int(
                        item.get(
                            "quantity",
                            1
                        )
                    )
                except:
                    quantity = 1

                try:
                    price = float(
                        item.get(
                            "price",
                            0
                        )
                    )
                except:
                    price = 0

                item_total = (
                    price * quantity
                )

                tk.Label(
                    row,
                    text=food_name,
                    font=("Arial", 11),
                    bg="#F8F8F8",
                    fg="#333333",
                    anchor="w"
                ).pack(
                    side="left",
                    fill="x",
                    expand=True
                )

                tk.Label(
                    row,
                    text=f"Qty: {quantity}",
                    font=("Arial", 10),
                    bg="#F8F8F8",
                    fg="#555555",
                    width=9
                ).pack(
                    side="left"
                )

                tk.Label(
                    row,
                    text=f"₹{item_total:.2f}",
                    font=("Arial", 11, "bold"),
                    bg="#F8F8F8",
                    fg="#222222",
                    width=13,
                    anchor="e"
                ).pack(
                    side="right"
                )

        # =====================================================
        # TOTAL
        # =====================================================

        total_row = tk.Frame(
            card,
            bg="white"
        )

        total_row.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
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
            total_row,
            text=(
                f"Subtotal: ₹{subtotal:.2f}   "
                f"GST: ₹{gst:.2f}   "
                f"Discount: ₹{discount:.2f}"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        ).pack(
            side="left"
        )

        tk.Label(
            total_row,
            text=f"Total: ₹{total:.2f}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#8B0000"
        ).pack(
            side="right"
        )

        # =====================================================
        # DETAILS BUTTON
        # =====================================================

        tk.Button(
            card,
            text="View Order Details",
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda o=order:
                self.show_details(o)
        ).pack(
            anchor="e",
            padx=20,
            pady=(0, 18),
            ipadx=10,
            ipady=6
        )

    # =========================================================
    # GET ITEMS
    # =========================================================

    def get_items(self, order_id):

        query = """
            SELECT
                oi.id,
                oi.order_id,
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

            return fetch_all(
                query,
                (order_id,)
            )

        except Exception as e:

            print(
                "Order item error:",
                e
            )

            return []

    # =========================================================
    # ORDER DETAILS
    # =========================================================

    def show_details(self, order):

        order_id = order.get(
            "id"
        )

        items = self.get_items(
            order_id
        )

        window = tk.Toplevel(
            self.parent.winfo_toplevel()
        )

        window.title(
            f"Order #{order_id}"
        )

        window.state(
            "zoomed"
        )

        window.configure(
            bg="#F4F6F8"
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            window,
            bg="#8B0000",
            height=70
        )

        header.pack(
            fill="x"
        )

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
            command=window.destroy
        ).pack(
            side="right",
            padx=25,
            ipadx=15,
            ipady=6
        )

        # =====================================================
        # DETAILS
        # =====================================================

        body = tk.Frame(
            window,
            bg="#F4F6F8"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        details = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        details.pack(
            fill="x",
            pady=(0, 15)
        )

        self.detail_row(
            details,
            "Order ID",
            str(order.get("id", ""))
        )

        self.detail_row(
            details,
            "Order Date",
            self.format_date(
                order.get("order_date")
            )
        )

        self.detail_row(
            details,
            "Status",
            str(
                order.get(
                    "status",
                    "Pending"
                )
                or "Pending"
            )
        )

        self.detail_row(
            details,
            "Payment",
            str(
                order.get(
                    "payment_method",
                    ""
                )
                or ""
            )
        )

        # =====================================================
        # ITEM LIST
        # =====================================================

        items_card = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        items_card.pack(
            fill="both",
            expand=True,
            pady=(0, 15)
        )

        tk.Label(
            items_card,
            text="Order Items",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        list_area = tk.Frame(
            items_card,
            bg="white"
        )

        list_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        item_canvas = tk.Canvas(
            list_area,
            bg="white",
            highlightthickness=0
        )

        item_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        item_scroll = tk.Scrollbar(
            list_area,
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
                    scrollregion=item_canvas.bbox("all")
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

        if not items:

            tk.Label(
                item_frame,
                text="No items found.",
                font=("Arial", 12),
                bg="white",
                fg="#777777"
            ).pack(
                pady=30
            )

        for item in items:

            name = (
                item.get(
                    "food_name"
                )
                or "Food"
            )

            quantity = int(
                item.get(
                    "quantity",
                    1
                )
            )

            price = self.to_float(
                item.get(
                    "price"
                )
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
                text=name,
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
                text=f"Quantity: {quantity}",
                font=("Arial", 11),
                bg="#F8F8F8",
                fg="#555555"
            ).pack(
                side="left",
                padx=20
            )

            tk.Label(
                row,
                text=f"₹{price:.2f}",
                font=("Arial", 12, "bold"),
                bg="#F8F8F8",
                fg="#222222"
            ).pack(
                side="right",
                padx=15
            )

        # =====================================================
        # PRICE
        # =====================================================

        price_card = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )

        price_card.pack(
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
            price_card,
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
            price_card,
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
            pady=8
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 11, "bold"),
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
    # STATUS COLOR
    # =========================================================

    def status_color(
        self,
        status
    ):

        status = str(
            status
        ).lower()

        if status == "pending":
            return "#E67E22"

        if status == "confirmed":
            return "#2980B9"

        if status == "preparing":
            return "#8E44AD"

        if status == "out for delivery":
            return "#16A085"

        if status == "delivered":
            return "#228B22"

        if status == "cancelled":
            return "#C0392B"

        return "#555555"

    # =========================================================
    # DATE FORMAT
    # =========================================================

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

    # =========================================================
    # FLOAT
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

    # =========================================================
    # TOUCHPAD SCROLL
    # =========================================================

    def bind_touchpad_scroll(self):

        try:

            # A custom bind tag is more reliable than binding
            # directly to every child widget.
            self.scroll_bind_tag = "CustomerOrdersScroll"

            self.scroll_target = (
                self.parent.winfo_toplevel()
            )

            self.scroll_target.bind_class(
                self.scroll_bind_tag,
                "<MouseWheel>",
                self.mouse_scroll
            )

            self.scroll_target.bind_class(
                self.scroll_bind_tag,
                "<Button-4>",
                self.mouse_scroll
            )

            self.scroll_target.bind_class(
                self.scroll_bind_tag,
                "<Button-5>",
                self.mouse_scroll
            )

            self.add_scroll_bind_tag(
                self.page
            )

        except tk.TclError:
            pass

    def add_scroll_bind_tag(
        self,
        widget
    ):

        try:

            tags = list(
                widget.bindtags()
            )

            if self.scroll_bind_tag not in tags:

                # Put the custom tag after the widget's own
                # bindings but before the toplevel bindings.
                if len(tags) > 1:
                    tags.insert(
                        1,
                        self.scroll_bind_tag
                    )
                else:
                    tags.append(
                        self.scroll_bind_tag
                    )

                widget.bindtags(
                    tuple(tags)
                )

            for child in widget.winfo_children():

                self.add_scroll_bind_tag(
                    child
                )

        except tk.TclError:
            pass

    def mouse_scroll(
        self,
        event
    ):

        try:

            if not self.canvas.winfo_exists():
                return

            # Windows precision touchpad / mouse
            delta = getattr(
                event,
                "delta",
                0
            )

            if delta > 0:

                # Precision touchpad / Windows mouse
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

            # Linux
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

        # Do not return "break".
        # Other widgets can still receive their normal events.

    def unbind_touchpad_scroll(self):

        try:

            if hasattr(
                self,
                "scroll_target"
            ):

                self.scroll_target.unbind_class(
                    self.scroll_bind_tag,
                    "<MouseWheel>"
                )

                self.scroll_target.unbind_class(
                    self.scroll_bind_tag,
                    "<Button-4>"
                )

                self.scroll_target.unbind_class(
                    self.scroll_bind_tag,
                    "<Button-5>"
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

    # =========================================================
    # CANVAS WIDTH
    # =========================================================

    def resize_canvas_window(
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
    # ERROR
    # =========================================================

    def show_error(
        self,
        message
    ):

        try:

            messagebox.showerror(
                "My Orders",
                message,
                parent=self.parent.winfo_toplevel()
            )

        except tk.TclError:

            messagebox.showerror(
                "My Orders",
                message
            )
