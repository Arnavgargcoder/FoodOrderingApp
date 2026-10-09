import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import fetch_all
import os


class CustomerMenu:

    def __init__(self, parent, user, cart):

        self.parent = parent
        self.user = user
        self.cart = cart

        self.foods = []
        self.filtered_foods = []

        self.food_images = []

        self.current_category = "All"

        self.canvas = None
        self.food_frame = None
        self.canvas_window = None
        self.scroll_window = None

        self.category_canvas = None
        self.category_frame = None
        self.category_window = None
        self.category_scrollbar = None

        self.create_ui()
        self.load_foods()

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

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            self.main_frame,
            bg="#8B0000",
            height=70
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Food Menu",
            font=("Arial", 24, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=30
        )

        self.cart_button = tk.Button(
            header,
            text="Cart (0)",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#8B0000",
            activebackground="#EEEEEE",
            activeforeground="#8B0000",
            relief="flat",
            cursor="hand2",
            command=self.open_cart
        )

        self.cart_button.pack(
            side="right",
            padx=30,
            ipadx=15,
            ipady=7
        )

        # =====================================================
        # SEARCH
        # =====================================================

        search_frame = tk.Frame(
            self.main_frame,
            bg="#F4F6F8"
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        tk.Label(
            search_frame,
            text="Search Food",
            font=("Arial", 12, "bold"),
            bg="#F4F6F8",
            fg="#333333"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=35,
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="left",
            ipady=7
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_food
        )

        tk.Button(
            search_frame,
            text="Clear",
            font=("Arial", 11, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_search
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=6
        )

        # =====================================================
        # CATEGORY SECTION
        # =====================================================

        category_outer = tk.Frame(
            self.main_frame,
            bg="#F4F6F8"
        )

        category_outer.pack(
            fill="x",
            padx=25,
            pady=(5, 15)
        )

        tk.Label(
            category_outer,
            text="Categories",
            font=("Arial", 12, "bold"),
            bg="#F4F6F8",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        category_container = tk.Frame(
            category_outer,
            bg="#F4F6F8"
        )

        category_container.pack(
            fill="x"
        )

        self.category_canvas = tk.Canvas(
            category_container,
            bg="#F4F6F8",
            height=55,
            highlightthickness=0,
            bd=0
        )

        self.category_canvas.pack(
            side="top",
            fill="x",
            expand=True
        )

        self.category_scrollbar = tk.Scrollbar(
            category_container,
            orient="horizontal",
            command=self.category_canvas.xview
        )

        self.category_scrollbar.pack(
            side="bottom",
            fill="x"
        )

        self.category_canvas.configure(
            xscrollcommand=self.category_scrollbar.set
        )

        self.category_frame = tk.Frame(
            self.category_canvas,
            bg="#F4F6F8"
        )

        self.category_window = self.category_canvas.create_window(
            (0, 0),
            window=self.category_frame,
            anchor="nw"
        )

        self.category_frame.bind(
            "<Configure>",
            self.update_category_scroll_region
        )

        self.category_canvas.bind(
            "<Shift-MouseWheel>",
            self.category_horizontal_scroll
        )

        self.category_canvas.bind(
            "<MouseWheel>",
            self.category_horizontal_scroll
        )

        self.category_frame.bind(
            "<Shift-MouseWheel>",
            self.category_horizontal_scroll
        )

        self.category_frame.bind(
            "<MouseWheel>",
            self.category_horizontal_scroll
        )

        # =====================================================
        # FOOD CONTAINER
        # =====================================================

        food_container = tk.Frame(
            self.main_frame,
            bg="#F4F6F8"
        )

        food_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # =====================================================
        # CANVAS
        # =====================================================

        self.canvas = tk.Canvas(
            food_container,
            bg="#F4F6F8",
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =====================================================
        # SCROLLBAR
        # =====================================================

        scrollbar = tk.Scrollbar(
            food_container,
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

        # =====================================================
        # FOOD FRAME
        # =====================================================

        self.food_frame = tk.Frame(
            self.canvas,
            bg="#F4F6F8"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.food_frame,
            anchor="nw"
        )

        self.food_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        # =====================================================
        # TOUCHPAD SCROLL
        # =====================================================

        self.setup_touchpad_scroll()

    # =========================================================
    # TOUCHPAD SCROLL SETUP
    # =========================================================

    def setup_touchpad_scroll(self):

        try:

            self.scroll_window = (
                self.parent.winfo_toplevel()
            )

            self.scroll_window.bind(
                "<MouseWheel>",
                self.on_mousewheel,
                add="+"
            )

            self.scroll_window.bind(
                "<Button-4>",
                self.on_mousewheel,
                add="+"
            )

            self.scroll_window.bind(
                "<Button-5>",
                self.on_mousewheel,
                add="+"
            )

            self.bind_scroll_recursive(
                self.main_frame
            )

        except tk.TclError:
            pass

    # =========================================================
    # BIND SCROLL TO ALL WIDGETS
    # =========================================================

    def bind_scroll_recursive(self, widget):

        try:

            widget.bind(
                "<MouseWheel>",
                self.on_mousewheel,
                add="+"
            )

            widget.bind(
                "<Button-4>",
                self.on_mousewheel,
                add="+"
            )

            widget.bind(
                "<Button-5>",
                self.on_mousewheel,
                add="+"
            )

            for child in widget.winfo_children():

                self.bind_scroll_recursive(
                    child
                )

        except tk.TclError:
            pass

    # =========================================================
    # TOUCHPAD / MOUSE SCROLL
    # =========================================================

    def on_mousewheel(self, event):

        try:

            if self.canvas is None:
                return

            if not self.canvas.winfo_exists():
                return

            if event.delta > 0:

                self.canvas.yview_scroll(
                    -3,
                    "units"
                )

            elif event.delta < 0:

                self.canvas.yview_scroll(
                    3,
                    "units"
                )

            elif event.num == 4:

                self.canvas.yview_scroll(
                    -3,
                    "units"
                )

            elif event.num == 5:

                self.canvas.yview_scroll(
                    3,
                    "units"
                )

        except tk.TclError:
            pass

    # =========================================================
    # LOAD FOOD
    # =========================================================

    def load_foods(self):

        query = """
            SELECT
                f.id,
                f.food_name,
                f.description,
                f.price,
                f.image,
                f.available,
                c.category_name
            FROM foods f
            INNER JOIN categories c
                ON f.category_id = c.id
            WHERE f.available = 1
            ORDER BY c.category_name, f.food_name
        """

        try:

            self.foods = fetch_all(
                query
            )

            print(
                "Available foods loaded:",
                len(self.foods)
            )

            self.create_categories()

            self.filtered_foods = (
                self.foods.copy()
            )

            self.display_foods()

            self.update_cart_count()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load food menu.\n\n{e}",
                parent=self.parent
            )

    # =========================================================
    # CREATE CATEGORIES
    # =========================================================

    def create_categories(self):

        # Remove old category buttons

        for widget in (
            self.category_frame.winfo_children()
        ):

            widget.destroy()

        # Always show All

        self.create_category_button(
            "All"
        )

        categories = []

        # Since load_foods() only loads available food,
        # every category found here has at least one
        # available food item.

        for food in self.foods:

            category = food.get(
                "category_name"
            )

            if not category:
                continue

            if category not in categories:

                categories.append(
                    category
                )

        # Create only categories containing food

        for category in categories:

            self.create_category_button(
                category
            )

    # =========================================================
    # CATEGORY BUTTON
    # =========================================================

    def create_category_button(
        self,
        category
    ):

        button = tk.Button(
            self.category_frame,
            text=category,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333",
            activebackground="#8B0000",
            activeforeground="white",
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda c=category:
                self.filter_category(c)
        )

        button.pack(
            side="left",
            padx=(0, 10),
            pady=5,
            ipadx=15,
            ipady=6
        )

        button.bind(
            "<Shift-MouseWheel>",
            self.category_horizontal_scroll,
            add="+"
        )

        button.bind(
            "<MouseWheel>",
            self.category_horizontal_scroll,
            add="+"
        )

    # =========================================================
    # CATEGORY HORIZONTAL SCROLL
    # =========================================================

    def category_horizontal_scroll(
        self,
        event
    ):

        try:

            if self.category_canvas is None:
                return

            if not self.category_canvas.winfo_exists():
                return

            if event.delta > 0:

                self.category_canvas.xview_scroll(
                    -3,
                    "units"
                )

            elif event.delta < 0:

                self.category_canvas.xview_scroll(
                    3,
                    "units"
                )

        except tk.TclError:
            pass

    # =========================================================
    # UPDATE CATEGORY SCROLL REGION
    # =========================================================

    def update_category_scroll_region(
        self,
        event=None
    ):

        try:

            if self.category_canvas is None:
                return

            if not self.category_canvas.winfo_exists():
                return

            self.category_canvas.configure(
                scrollregion=self.category_canvas.bbox("all")
            )

        except tk.TclError:
            pass

    # =========================================================
    # FILTER CATEGORY
    # =========================================================

    def filter_category(
        self,
        category
    ):

        self.current_category = category

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        self.filtered_foods = []

        for food in self.foods:

            category_name = (
                food.get(
                    "category_name"
                ) or ""
            )

            food_name = (
                food.get(
                    "food_name"
                ) or ""
            )

            description = (
                food.get(
                    "description"
                ) or ""
            )

            if category != "All":

                if category_name != category:
                    continue

            if search_text:

                if (
                    search_text not in
                    food_name.lower()
                    and
                    search_text not in
                    description.lower()
                    and
                    search_text not in
                    category_name.lower()
                ):
                    continue

            self.filtered_foods.append(
                food
            )

        self.display_foods()

    # =========================================================
    # SEARCH FOOD
    # =========================================================

    def search_food(
        self,
        event=None
    ):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        self.filtered_foods = []

        for food in self.foods:

            food_name = (
                food.get(
                    "food_name"
                ) or ""
            )

            description = (
                food.get(
                    "description"
                ) or ""
            )

            category = (
                food.get(
                    "category_name"
                ) or ""
            )

            if self.current_category != "All":

                if category != self.current_category:
                    continue

            if search_text:

                if (
                    search_text not in
                    food_name.lower()
                    and
                    search_text not in
                    description.lower()
                    and
                    search_text not in
                    category.lower()
                ):
                    continue

            self.filtered_foods.append(
                food
            )

        self.display_foods()

    # =========================================================
    # CLEAR SEARCH
    # =========================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.current_category = "All"

        self.filtered_foods = (
            self.foods.copy()
        )

        self.display_foods()

    # =========================================================
    # DISPLAY FOODS
    # =========================================================

    def display_foods(self):

        if self.food_frame is None:
            return

        for widget in (
            self.food_frame.winfo_children()
        ):

            widget.destroy()

        self.food_images.clear()

        if not self.filtered_foods:

            tk.Label(
                self.food_frame,
                text="No food items found.",
                font=("Arial", 18, "bold"),
                bg="#F4F6F8",
                fg="#555555"
            ).pack(
                pady=80
            )

            self.update_scroll_region()

            return

        # Four columns

        for column in range(4):

            self.food_frame.grid_columnconfigure(
                column,
                weight=1
            )

        for index, food in enumerate(
            self.filtered_foods
        ):

            row = index // 4
            column = index % 4

            self.create_food_card(
                food,
                row,
                column
            )

        self.canvas.yview_moveto(
            0
        )

        self.update_scroll_region()

    # =========================================================
    # CREATE FOOD CARD
    # =========================================================

    def create_food_card(
        self,
        food,
        row,
        column
    ):

        card = tk.Frame(
            self.food_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # =====================================================
        # IMAGE
        # =====================================================

        image_container = tk.Frame(
            card,
            bg="#F4F4F4",
            height=180
        )

        image_container.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        image_container.pack_propagate(
            False
        )

        image_loaded = (
            self.load_food_image(
                food,
                image_container
            )
        )

        if not image_loaded:

            tk.Label(
                image_container,
                text="Image Not Available",
                font=("Arial", 11),
                bg="#F4F4F4",
                fg="#777777"
            ).pack(
                expand=True
            )

        # =====================================================
        # FOOD NAME
        # =====================================================

        tk.Label(
            card,
            text=food.get(
                "food_name",
                "Food"
            ),
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#222222",
            wraplength=220
        ).pack(
            pady=(8, 3)
        )

        # =====================================================
        # CATEGORY
        # =====================================================

        tk.Label(
            card,
            text=(
                food.get(
                    "category_name"
                ) or
                "Uncategorized"
            ),
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#8B0000"
        ).pack(
            pady=2
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        description = (
            food.get(
                "description"
            ) or ""
        )

        tk.Label(
            card,
            text=description,
            font=("Arial", 10),
            bg="white",
            fg="#666666",
            wraplength=230,
            justify="center"
        ).pack(
            padx=10,
            pady=5
        )

        # =====================================================
        # PRICE
        # =====================================================

        try:

            price = float(
                food.get(
                    "price",
                    0
                )
            )

        except:

            price = 0

        tk.Label(
            card,
            text=f"₹{price:.2f}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            pady=5
        )

        # =====================================================
        # AVAILABLE
        # =====================================================

        tk.Label(
            card,
            text="Available",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="green"
        ).pack(
            pady=2
        )

        # =====================================================
        # ADD TO CART
        # =====================================================

        add_button = tk.Button(
            card,
            text="Add to Cart",
            font=("Arial", 11, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda f=food:
                self.add_to_cart(f)
        )

        add_button.pack(
            fill="x",
            padx=15,
            pady=(8, 15),
            ipady=8
        )

        # Make all widgets scrollable

        self.bind_scroll_recursive(
            card
        )

    # =========================================================
    # LOAD FOOD IMAGE
    # =========================================================

    def load_food_image(
        self,
        food,
        parent
    ):

        image_value = food.get(
            "image"
        )

        if not image_value:

            print(
                "No image stored for:",
                food.get(
                    "food_name"
                )
            )

            return False

        image_value = str(
            image_value
        ).strip()

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        filename = os.path.basename(
            image_value
        )

        # Possible image locations

        possible_paths = [

            image_value,

            os.path.join(
                project_root,
                image_value
            ),

            os.path.join(
                project_root,
                "assets",
                "food",
                filename
            ),

            os.path.join(
                project_root,
                "assets",
                filename
            ),

            os.path.join(
                project_root,
                "food",
                filename
            )
        ]

        image_path = None

        for path in possible_paths:

            try:

                path = os.path.normpath(
                    path
                )

                if os.path.isfile(path):

                    image_path = path
                    break

            except Exception:

                continue

        if image_path is None:

            print(
                "IMAGE NOT FOUND:",
                image_value
            )

            print(
                "Food:",
                food.get(
                    "food_name"
                )
            )

            return False

        # =====================================================
        # OPEN IMAGE
        # =====================================================

        try:

            image = Image.open(
                image_path
            )

            image = image.convert(
                "RGB"
            )

            image.thumbnail(
                (220, 165),
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            # Keep image reference

            self.food_images.append(
                photo
            )

            image_label = tk.Label(
                parent,
                image=photo,
                bg="#F4F4F4"
            )

            image_label.pack(
                expand=True
            )

            self.bind_scroll_recursive(
                image_label
            )

            print(
                "Image loaded:",
                image_path
            )

            return True

        except Exception as e:

            print(
                "IMAGE ERROR:",
                image_path
            )

            print(
                e
            )

            return False

    # =========================================================
    # ADD TO CART
    # =========================================================

    def add_to_cart(
        self,
        food
    ):

        food_id = food.get(
            "id"
        )

        # Check if already in cart

        for item in self.cart:

            if item.get(
                "id"
            ) == food_id:

                item["quantity"] = (
                    int(
                        item.get(
                            "quantity",
                            1
                        )
                    ) + 1
                )

                self.update_cart_count()

                messagebox.showinfo(
                    "Cart",
                    f"{food.get('food_name')} quantity updated.",
                    parent=self.parent
                )

                return

        # New cart item

        try:

            price = float(
                food.get(
                    "price",
                    0
                )
            )

        except:

            price = 0

        self.cart.append(
            {
                "id": food.get(
                    "id"
                ),

                "food_name": food.get(
                    "food_name"
                ),

                "price": price,

                "image": food.get(
                    "image"
                ),

                "quantity": 1
            }
        )

        self.update_cart_count()

        messagebox.showinfo(
            "Cart",
            f"{food.get('food_name')} added to cart.",
            parent=self.parent
        )

    # =========================================================
    # UPDATE CART COUNT
    # =========================================================

    def update_cart_count(self):

        total_quantity = 0

        for item in self.cart:

            total_quantity += int(
                item.get(
                    "quantity",
                    1
                )
            )

        self.cart_button.config(
            text=f"Cart ({total_quantity})"
        )

    # =========================================================
    # OPEN CART
    # =========================================================

    def open_cart(self):

        try:

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

        for widget in (
            self.parent.winfo_children()
        ):

            try:

                widget.destroy()

            except tk.TclError:

                pass

        from customer.cart import CustomerCart

        CustomerCart(
            self.parent,
            self.user,
            self.cart
        )

    # =========================================================
    # UPDATE SCROLL REGION
    # =========================================================

    def update_scroll_region(
        self,
        event=None
    ):

        try:

            if self.canvas is None:
                return

            if not self.canvas.winfo_exists():
                return

            self.canvas.configure(
                scrollregion=(
                    self.canvas.bbox("all")
                )
            )

        except tk.TclError:

            pass

    # =========================================================
    # UPDATE CANVAS WIDTH
    # =========================================================

    def update_canvas_width(
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
