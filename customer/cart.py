import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from config import GST_RATE


class CustomerCart:

    def __init__(self, parent, user, cart):
        self.parent = parent
        self.user = user
        self.cart = cart

        self.cart_images = []

        self.project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.create_ui()
        self.display_cart()

    # =========================================================
    # CREATE UI
    # =========================================================

    def create_ui(self):

        self.main_frame = tk.Frame(
            self.parent,
            bg="#F4F6F8"
        )
        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            self.main_frame,
            bg="#8B0000",
            height=70
        )
        header.pack(
            fill="x"
        )
        header.pack_propagate(False)

        tk.Label(
            header,
            text="My Cart",
            font=("Arial", 24, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=30
        )

        self.item_count_label = tk.Label(
            header,
            text="0 Items",
            font=("Arial", 12),
            bg="#8B0000",
            fg="white"
        )
        self.item_count_label.pack(
            side="right",
            padx=30
        )

        # -----------------------------------------------------
        # MAIN CONTENT
        # -----------------------------------------------------

        content = tk.Frame(
            self.main_frame,
            bg="#F4F6F8"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # -----------------------------------------------------
        # LEFT SIDE - CART ITEMS
        # -----------------------------------------------------

        left_frame = tk.Frame(
            content,
            bg="#F4F6F8"
        )
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        tk.Label(
            left_frame,
            text="Cart Items",
            font=("Arial", 20, "bold"),
            bg="#F4F6F8",
            fg="#222222"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        # Scrollable cart area

        cart_container = tk.Frame(
            left_frame,
            bg="white",
            bd=1,
            relief="solid"
        )
        cart_container.pack(
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            cart_container,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            cart_container,
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

        self.cart_frame = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.cart_frame,
            anchor="nw"
        )

        self.cart_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        # Touchpad / mouse scrolling
        # Bind scrolling to the whole cart area so it works
        # even when the pointer is over labels, buttons, images,
        # or other child widgets.

        self.setup_touchpad_scroll()

        # -----------------------------------------------------
        # RIGHT SIDE - ORDER SUMMARY
        # -----------------------------------------------------

        right_frame = tk.Frame(
            content,
            bg="white",
            width=330,
            bd=1,
            relief="solid"
        )
        right_frame.pack(
            side="right",
            fill="y"
        )
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame,
            text="Order Summary",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 25)
        )

        # Subtotal

        subtotal_row = tk.Frame(
            right_frame,
            bg="white"
        )
        subtotal_row.pack(
            fill="x",
            padx=25,
            pady=8
        )

        tk.Label(
            subtotal_row,
            text="Subtotal",
            font=("Arial", 12),
            bg="white",
            fg="#555555"
        ).pack(
            side="left"
        )

        self.subtotal_label = tk.Label(
            subtotal_row,
            text="₹0.00",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#222222"
        )
        self.subtotal_label.pack(
            side="right"
        )

        # GST

        gst_row = tk.Frame(
            right_frame,
            bg="white"
        )
        gst_row.pack(
            fill="x",
            padx=25,
            pady=8
        )

        tk.Label(
            gst_row,
            text=f"GST ({GST_RATE}%)",
            font=("Arial", 12),
            bg="white",
            fg="#555555"
        ).pack(
            side="left"
        )

        self.gst_label = tk.Label(
            gst_row,
            text="₹0.00",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#222222"
        )
        self.gst_label.pack(
            side="right"
        )

        # Separator

        tk.Frame(
            right_frame,
            bg="#DDDDDD",
            height=1
        ).pack(
            fill="x",
            padx=25,
            pady=15
        )

        # Total

        total_row = tk.Frame(
            right_frame,
            bg="white"
        )
        total_row.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            total_row,
            text="Total",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            side="left"
        )

        self.total_label = tk.Label(
            total_row,
            text="₹0.00",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#8B0000"
        )
        self.total_label.pack(
            side="right"
        )

        # -----------------------------------------------------
        # CHECKOUT BUTTON
        # -----------------------------------------------------

        self.checkout_button = tk.Button(
            right_frame,
            text="Proceed to Checkout",
            font=("Arial", 12, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.checkout
        )
        self.checkout_button.pack(
            fill="x",
            padx=25,
            pady=(30, 10),
            ipady=12
        )

        # -----------------------------------------------------
        # CLEAR CART BUTTON
        # -----------------------------------------------------

        self.clear_button = tk.Button(
            right_frame,
            text="Clear Cart",
            font=("Arial", 12, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_cart
        )
        self.clear_button.pack(
            fill="x",
            padx=25,
            pady=5,
            ipady=10
        )

    # =========================================================
    # DISPLAY CART
    # =========================================================

    def display_cart(self):

        if not self.cart_frame.winfo_exists():
            return

        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        self.cart_images.clear()

        if not self.cart:

            empty_frame = tk.Frame(
                self.cart_frame,
                bg="white"
            )
            empty_frame.pack(
                fill="both",
                expand=True,
                padx=30,
                pady=100
            )

            tk.Label(
                empty_frame,
                text="Your cart is empty",
                font=("Arial", 24, "bold"),
                bg="white",
                fg="#333333"
            ).pack(
                pady=10
            )

            tk.Label(
                empty_frame,
                text="Add food items from the menu.",
                font=("Arial", 13),
                bg="white",
                fg="#777777"
            ).pack(
                pady=5
            )

            self.update_summary()
            return

        for index, item in enumerate(self.cart):

            self.create_cart_item(
                item,
                index
            )

        self.update_summary()

    # =========================================================
    # CREATE CART ITEM
    # =========================================================

    def create_cart_item(self, item, index):

        item_frame = tk.Frame(
            self.cart_frame,
            bg="white",
            height=120
        )

        item_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        item_frame.pack_propagate(False)

        # -----------------------------------------------------
        # IMAGE
        # -----------------------------------------------------

        image_frame = tk.Frame(
            item_frame,
            bg="#F4F4F4",
            width=100,
            height=100
        )

        image_frame.pack(
            side="left",
            padx=(5, 15),
            pady=10
        )

        image_frame.pack_propagate(False)

        image_value = item.get("image")

        image_loaded = False

        if image_value:
            image_value = str(image_value).strip()

            filename = os.path.basename(image_value)

            # Try the same common locations used by the Menu page.
            possible_paths = [
                image_value,

                os.path.join(
                    self.project_root,
                    image_value
                ),

                os.path.join(
                    self.project_root,
                    "assets",
                    "food",
                    filename
                ),

                os.path.join(
                    self.project_root,
                    "assets",
                    filename
                ),

                os.path.join(
                    self.project_root,
                    "food",
                    filename
                )
            ]

            image_path = None

            for path in possible_paths:
                try:
                    path = os.path.normpath(path)

                    if os.path.isfile(path):
                        image_path = path
                        break

                except Exception:
                    continue

            if image_path:
                try:
                    image = Image.open(image_path)
                    image = image.convert("RGB")

                    image.thumbnail(
                        (90, 90),
                        Image.Resampling.LANCZOS
                    )

                    photo = ImageTk.PhotoImage(image)

                    # Keep a strong reference so Tkinter does not
                    # garbage-collect the image.
                    self.cart_images.append(photo)

                    tk.Label(
                        image_frame,
                        image=photo,
                        bg="#F4F4F4"
                    ).pack(
                        expand=True
                    )

                    image_loaded = True

                except Exception as e:
                    print(
                        "Cart image error:",
                        image_path,
                        e
                    )

            else:
                print(
                    "Cart image not found:",
                    image_value
                )

        if not image_loaded:
            tk.Label(
                image_frame,
                text="No Image",
                font=("Arial", 10),
                bg="#F4F4F4",
                fg="#777777"
            ).pack(
                expand=True
            )

        # -----------------------------------------------------
        # FOOD DETAILS
        # -----------------------------------------------------

        details_frame = tk.Frame(
            item_frame,
            bg="white"
        )

        details_frame.pack(
            side="left",
            fill="both",
            expand=True,
            pady=10
        )

        tk.Label(
            details_frame,
            text=item.get(
                "food_name",
                "Food"
            ),
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        price = float(
            item.get(
                "price",
                0
            )
        )

        tk.Label(
            details_frame,
            text=f"₹{price:.2f} per item",
            font=("Arial", 11),
            bg="white",
            fg="#777777"
        ).pack(
            anchor="w"
        )

        quantity = int(
            item.get(
                "quantity",
                1
            )
        )

        item_total = price * quantity

        tk.Label(
            details_frame,
            text=f"Item Total: ₹{item_total:.2f}",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#8B0000"
        ).pack(
            anchor="w",
            pady=5
        )

        # -----------------------------------------------------
        # QUANTITY CONTROLS
        # -----------------------------------------------------

        quantity_frame = tk.Frame(
            item_frame,
            bg="white"
        )

        quantity_frame.pack(
            side="right",
            padx=25,
            pady=10
        )

        tk.Label(
            quantity_frame,
            text="Quantity",
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack(
            pady=(0, 5)
        )

        controls = tk.Frame(
            quantity_frame,
            bg="white"
        )

        controls.pack()

        tk.Button(
            controls,
            text="-",
            font=("Arial", 13, "bold"),
            width=3,
            bg="#EEEEEE",
            fg="#222222",
            activebackground="#DDDDDD",
            relief="flat",
            cursor="hand2",
            command=lambda i=index:
                self.decrease_quantity(i)
        ).pack(
            side="left"
        )

        tk.Label(
            controls,
            text=str(quantity),
            font=("Arial", 12, "bold"),
            width=5,
            bg="white",
            fg="#222222"
        ).pack(
            side="left"
        )

        tk.Button(
            controls,
            text="+",
            font=("Arial", 13, "bold"),
            width=3,
            bg="#EEEEEE",
            fg="#222222",
            activebackground="#DDDDDD",
            relief="flat",
            cursor="hand2",
            command=lambda i=index:
                self.increase_quantity(i)
        ).pack(
            side="left"
        )

        # -----------------------------------------------------
        # REMOVE BUTTON
        # -----------------------------------------------------

        tk.Button(
            quantity_frame,
            text="Remove",
            font=("Arial", 10, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda i=index:
                self.remove_item(i)
        ).pack(
            pady=(10, 0),
            ipadx=8,
            ipady=4
        )

        # Separator

        if index < len(self.cart) - 1:

            tk.Frame(
                self.cart_frame,
                bg="#EEEEEE",
                height=1
            ).pack(
                fill="x",
                padx=15
            )

    # =========================================================
    # INCREASE QUANTITY
    # =========================================================

    def increase_quantity(self, index):

        if index < 0 or index >= len(self.cart):
            return

        self.cart[index]["quantity"] = (
            int(
                self.cart[index].get(
                    "quantity",
                    1
                )
            ) + 1
        )

        self.display_cart()

    # =========================================================
    # DECREASE QUANTITY
    # =========================================================

    def decrease_quantity(self, index):

        if index < 0 or index >= len(self.cart):
            return

        quantity = int(
            self.cart[index].get(
                "quantity",
                1
            )
        )

        if quantity > 1:

            self.cart[index]["quantity"] = (
                quantity - 1
            )

        else:

            answer = messagebox.askyesno(
                "Remove Item",
                "Quantity is 1. Remove this item from the cart?",
                parent=self.parent
            )

            if answer:
                self.cart.pop(index)

        self.display_cart()

    # =========================================================
    # REMOVE ITEM
    # =========================================================

    def remove_item(self, index):

        if index < 0 or index >= len(self.cart):
            return

        food_name = self.cart[index].get(
            "food_name",
            "this item"
        )

        answer = messagebox.askyesno(
            "Remove Item",
            f"Remove {food_name} from the cart?",
            parent=self.parent
        )

        if not answer:
            return

        self.cart.pop(index)

        self.display_cart()

    # =========================================================
    # CLEAR CART
    # =========================================================

    def clear_cart(self):

        if not self.cart:
            return

        answer = messagebox.askyesno(
            "Clear Cart",
            "Are you sure you want to clear the entire cart?",
            parent=self.parent
        )

        if not answer:
            return

        self.cart.clear()

        self.display_cart()

    # =========================================================
    # UPDATE SUMMARY
    # =========================================================

    def update_summary(self):

        subtotal = 0

        total_items = 0

        for item in self.cart:

            price = float(
                item.get(
                    "price",
                    0
                )
            )

            quantity = int(
                item.get(
                    "quantity",
                    1
                )
            )

            subtotal += price * quantity

            total_items += quantity

        gst = subtotal * (
            float(GST_RATE) / 100
        )

        total = subtotal + gst

        self.subtotal_label.config(
            text=f"₹{subtotal:.2f}"
        )

        self.gst_label.config(
            text=f"₹{gst:.2f}"
        )

        self.total_label.config(
            text=f"₹{total:.2f}"
        )

        self.item_count_label.config(
            text=f"{total_items} Items"
        )

        if self.cart:

            self.checkout_button.config(
                state="normal",
                bg="#8B0000"
            )

            self.clear_button.config(
                state="normal"
            )

        else:

            self.checkout_button.config(
                state="disabled",
                bg="#AAAAAA"
            )

            self.clear_button.config(
                state="disabled"
            )

    # =========================================================
    # CHECKOUT
    # =========================================================

    def checkout(self):

        try:
            if hasattr(self, "scroll_window"):
                self.scroll_window.unbind(
                    "<MouseWheel>"
                )
                self.scroll_window.unbind(
                    "<Button-4>"
                )
                self.scroll_window.unbind(
                    "<Button-5>"
                )
        except tk.TclError:
            pass

        if not self.cart:

            messagebox.showwarning(
                "Empty Cart",
                "Please add at least one food item.",
                parent=self.parent
            )

            return

        from customer.checkout import CustomerCheckout

        for widget in self.parent.winfo_children():

            try:
                widget.destroy()

            except tk.TclError:
                pass

        CustomerCheckout(
            self.parent,
            self.user,
            self.cart
        )

    # =========================================================
    # TOUCHPAD / MOUSE SCROLL SETUP
    # =========================================================

    def setup_touchpad_scroll(self):

        try:
            # Bind to the top-level as well.
            self.scroll_window = self.parent.winfo_toplevel()

            self.scroll_window.bind(
                "<MouseWheel>",
                self.mouse_scroll,
                add="+"
            )

            self.scroll_window.bind(
                "<Button-4>",
                self.mouse_scroll,
                add="+"
            )

            self.scroll_window.bind(
                "<Button-5>",
                self.mouse_scroll,
                add="+"
            )

            # Most importantly, bind every widget inside
            # the cart area. This fixes touchpad scrolling
            # when the pointer is over a child widget.
            self.bind_scroll_recursive(
                self.main_frame
            )

        except tk.TclError:
            pass

    def bind_scroll_recursive(self, widget):

        try:
            widget.bind(
                "<MouseWheel>",
                self.mouse_scroll,
                add="+"
            )

            widget.bind(
                "<Button-4>",
                self.mouse_scroll,
                add="+"
            )

            widget.bind(
                "<Button-5>",
                self.mouse_scroll,
                add="+"
            )

            for child in widget.winfo_children():
                self.bind_scroll_recursive(child)

        except tk.TclError:
            pass

    # =========================================================
    # SCROLL REGION
    # =========================================================

    def update_scroll_region(self, event=None):

        try:

            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )

        except tk.TclError:

            pass

    # =========================================================
    # CANVAS WIDTH
    # =========================================================

    def update_canvas_width(self, event):

        try:

            self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )

        except tk.TclError:

            pass

    # =========================================================
    # MOUSE SCROLL
    # =========================================================

    def mouse_scroll(self, event):

        try:

            if self.canvas is None:
                return

            if not self.canvas.winfo_exists():
                return

            if event.num == 4:
                self.canvas.yview_scroll(
                    -3,
                    "units"
                )

            elif event.num == 5:
                self.canvas.yview_scroll(
                    3,
                    "units"
                )

            elif event.delta > 0:
                self.canvas.yview_scroll(
                    -3,
                    "units"
                )

            elif event.delta < 0:
                self.canvas.yview_scroll(
                    3,
                    "units"
                )

        except tk.TclError:
            pass
