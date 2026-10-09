import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil

from database import fetch_all, fetch_one, execute_query


class ManageFood:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Manage Food")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.icons = {}
        self.food_rows = []
        self.categories = []

        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.food_folder = os.path.join(
            self.base_dir,
            "assets",
            "food"
        )

        os.makedirs(
            self.food_folder,
            exist_ok=True
        )

        self.create_ui()

        self.load_categories()
        self.load_food()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_ui(self):

        # ---------------- HEADER ----------------

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
            text="Food Management",
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#20242A"
        ).pack(
            side="left",
            padx=30
        )

        tk.Button(
            header,
            text="Close",
            font=("Arial", 10, "bold"),
            bg="#F2F2F2",
            fg="#333333",
            activebackground="#E5E5E5",
            relief="flat",
            cursor="hand2",
            command=self.close_window
        ).pack(
            side="right",
            padx=30,
            ipadx=15,
            ipady=7
        )

        # ---------------- MAIN ----------------

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

        tk.Label(
            main,
            text="Manage Food",
            font=("Arial", 30, "bold"),
            bg="#F4F6F8",
            fg="#20242A"
        ).pack(
            anchor="w"
        )

        tk.Label(
            main,
            text="Add, edit and manage food items",
            font=("Arial", 11),
            bg="#F4F6F8",
            fg="#777777"
        ).pack(
            anchor="w",
            pady=(5, 20)
        )

        self.create_statistics(main)

        self.create_search_bar(main)

        self.create_food_table(main)

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

        self.total_value = self.create_stat_card(
            frame,
            "Total Food",
            "0",
            "add.png",
            "#E8F0FF"
        )

        self.available_value = self.create_stat_card(
            frame,
            "Available",
            "0",
            "add.png",
            "#EAF8F0"
        )

        self.unavailable_value = self.create_stat_card(
            frame,
            "Unavailable",
            "0",
            "delete.png",
            "#FDECEC"
        )

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
            height=105
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
            width=55,
            height=55
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

            icon_label = tk.Label(
                icon_box,
                image=icon,
                bg=icon_bg
            )

            icon_label.place(
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
            fg="#777777"
        ).pack(
            anchor="w"
        )

        value_label = tk.Label(
            text_frame,
            text=value,
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#222222"
        )

        value_label.pack(
            anchor="w",
            pady=(3, 0)
        )

        return value_label

    # =========================================================
    # SEARCH BAR
    # =========================================================

    def create_search_bar(self, parent):

        frame = tk.Frame(
            parent,
            bg="white",
            height=70
        )

        frame.pack(
            fill="x",
            pady=(0, 15)
        )

        frame.pack_propagate(False)

        search_icon = self.load_icon(
            "search.png",
            (22, 22)
        )

        if search_icon:

            tk.Label(
                frame,
                image=search_icon,
                bg="white"
            ).pack(
                side="left",
                padx=(20, 8)
            )

        tk.Label(
            frame,
            text="Search",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#444444"
        ).pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            frame,
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
            self.search_food
        )

        tk.Button(
            frame,
            text="Refresh",
            font=("Arial", 10, "bold"),
            bg="#F1F1F1",
            fg="#333333",
            relief="flat",
            cursor="hand2",
            command=self.load_food
        ).pack(
            side="right",
            padx=5,
            ipadx=10,
            ipady=7
        )

        tk.Button(
            frame,
            text="Add Food",
            font=("Arial", 10, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.add_food
        ).pack(
            side="right",
            padx=(5, 20),
            ipadx=12,
            ipady=7
        )

    # =========================================================
    # FOOD TABLE
    # =========================================================

    def create_food_table(self, parent):

        outer = tk.Frame(
            parent,
            bg="white"
        )

        outer.pack(
            fill="both",
            expand=True
        )

        # ---------------- TABLE HEADER ----------------

        header = tk.Frame(
            outer,
            bg="#20242A",
            height=50
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        columns = [
            "ID",
            "Image",
            "Food Name",
            "Category",
            "Description",
            "Price",
            "Status",
            "Action"
        ]

        for i in range(8):

            header.grid_columnconfigure(
                i,
                weight=1
            )

        for i, column in enumerate(columns):

            tk.Label(
                header,
                text=column,
                font=("Arial", 10, "bold"),
                bg="#20242A",
                fg="white",
                anchor="w"
            ).grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=10
            )

        # ---------------- TABLE BODY ----------------

        table_area = tk.Frame(
            outer,
            bg="white"
        )

        table_area.pack(
            fill="both",
            expand=True
        )

        self.table_canvas = tk.Canvas(
            table_area,
            bg="white",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            table_area,
            orient="vertical",
            command=self.table_canvas.yview
        )

        self.table_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.table_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table_frame = tk.Frame(
            self.table_canvas,
            bg="white"
        )

        self.table_window = self.table_canvas.create_window(
            (0, 0),
            window=self.table_frame,
            anchor="nw"
        )

        self.table_frame.bind(
            "<Configure>",
            lambda event:
            self.table_canvas.configure(
                scrollregion=
                self.table_canvas.bbox("all")
            )
        )

        self.table_canvas.bind(
            "<Configure>",
            lambda event:
            self.table_canvas.itemconfig(
                self.table_window,
                width=event.width
            )
        )

        # Touchpad + mouse wheel scrolling for the food table
        self.bind_touchpad_scroll(self.window, self.table_canvas)

    # =========================================================
    # LOAD CATEGORIES
    # =========================================================

    def load_categories(self):

        try:

            self.categories = fetch_all(
                """
                SELECT
                    id,
                    category_name
                FROM categories
                ORDER BY category_name
                """
            )

        except Exception as e:

            self.categories = []

            print(
                "Category error:",
                e
            )

    # =========================================================
    # LOAD FOOD
    # =========================================================

    def load_food(self):

        try:

            self.food_rows = fetch_all(
                """
                SELECT
                    f.id,
                    f.food_name,
                    f.description,
                    f.price,
                    f.image,
                    f.available,
                    f.category_id,
                    c.category_name
                FROM foods f
                INNER JOIN categories c
                    ON f.category_id = c.id
                ORDER BY f.id DESC
                """
            )

            self.display_food(
                self.food_rows
            )

            self.update_statistics()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to load food.\n\n" + str(e),
                parent=self.window
            )

    # =========================================================
    # DISPLAY FOOD
    # =========================================================

    def display_food(self, foods):

        for widget in self.table_frame.winfo_children():

            widget.destroy()

        if not foods:

            tk.Label(
                self.table_frame,
                text="No food items found",
                font=("Arial", 12),
                bg="white",
                fg="#888888"
            ).pack(
                pady=50
            )

            return

        for index, food in enumerate(foods):

            self.create_food_row(
                food,
                index
            )

    # =========================================================
    # CREATE FOOD ROW
    # =========================================================

    def create_food_row(
        self,
        food,
        index
    ):

        bg = (
            "white"
            if index % 2 == 0
            else "#F8F9FA"
        )

        row = tk.Frame(
            self.table_frame,
            bg=bg,
            height=70
        )

        row.pack(
            fill="x"
        )

        row.pack_propagate(False)

        for i in range(8):

            row.grid_columnconfigure(
                i,
                weight=1
            )

        self.add_cell(
            row,
            0,
            food["id"],
            bg
        )

        # IMAGE

        image_frame = tk.Frame(
            row,
            bg=bg
        )

        image_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        image = self.get_food_image(
            food.get("image")
        )

        if image:

            label = tk.Label(
                image_frame,
                image=image,
                bg=bg
            )

            label.pack(
                pady=7
            )

            label.image = image

        else:

            tk.Label(
                image_frame,
                text="No Image",
                font=("Arial", 8),
                bg=bg,
                fg="#999999"
            ).pack(
                pady=25
            )

        # NAME

        self.add_cell(
            row,
            2,
            food["food_name"],
            bg
        )

        # CATEGORY

        self.add_cell(
            row,
            3,
            food["category_name"],
            bg
        )

        # DESCRIPTION

        description = food.get(
            "description"
        ) or "-"

        description = str(
            description
        )

        if len(description) > 25:

            description = (
                description[:25]
                + "..."
            )

        self.add_cell(
            row,
            4,
            description,
            bg
        )

        # PRICE

        try:

            price = float(
                food["price"]
            )

            price_text = (
                "₹ "
                + format(
                    price,
                    ",.2f"
                )
            )

        except Exception:

            price_text = str(
                food["price"]
            )

        self.add_cell(
            row,
            5,
            price_text,
            bg
        )

        # STATUS

        status_frame = tk.Frame(
            row,
            bg=bg
        )

        status_frame.grid(
            row=0,
            column=6,
            sticky="nsew"
        )

        if food["available"]:

            status = "Available"
            status_bg = "#EAF8F0"
            status_fg = "#218838"

        else:

            status = "Unavailable"
            status_bg = "#FDECEC"
            status_fg = "#C0392B"

        tk.Label(
            status_frame,
            text=status,
            font=("Arial", 9, "bold"),
            bg=status_bg,
            fg=status_fg
        ).pack(
            padx=8,
            pady=22
        )

        # ACTION

        action = tk.Frame(
            row,
            bg=bg
        )

        action.grid(
            row=0,
            column=7,
            sticky="nsew"
        )

        tk.Button(
            action,
            text="Edit",
            font=("Arial", 9, "bold"),
            bg="#E8F0FF",
            fg="#1769AA",
            relief="flat",
            cursor="hand2",
            command=lambda f=food:
            self.edit_food(f)
        ).pack(
            side="left",
            padx=3,
            pady=20
        )

        tk.Button(
            action,
            text="Delete",
            font=("Arial", 9, "bold"),
            bg="#FDECEC",
            fg="#C0392B",
            relief="flat",
            cursor="hand2",
            command=lambda fid=food["id"]:
            self.delete_food(fid)
        ).pack(
            side="left",
            padx=3,
            pady=20
        )

    # =========================================================
    # CELL
    # =========================================================

    def add_cell(
        self,
        parent,
        column,
        value,
        bg
    ):

        tk.Label(
            parent,
            text=str(value),
            font=("Arial", 10),
            bg=bg,
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

    def search_food(self, event=None):

        search = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if not search:

            self.display_food(
                self.food_rows
            )

            return

        filtered = []

        for food in self.food_rows:

            values = [
                str(
                    food.get(
                        "food_name",
                        ""
                    )
                ),
                str(
                    food.get(
                        "category_name",
                        ""
                    )
                ),
                str(
                    food.get(
                        "description",
                        ""
                    )
                )
            ]

            if any(
                search in value.lower()
                for value in values
            ):

                filtered.append(
                    food
                )

        self.display_food(
            filtered
        )

    # =========================================================
    # ADD FOOD
    # =========================================================

    def add_food(self):

        self.open_food_form(
            "Add Food"
        )

    # =========================================================
    # EDIT FOOD
    # =========================================================

    def edit_food(self, food):

        self.open_food_form(
            "Edit Food",
            food
        )

    # =========================================================
    # FOOD FORM
    # =========================================================

    def open_food_form(
        self,
        title,
        food=None
    ):

        form_window = tk.Toplevel(
            self.window
        )

        form_window.title(
            title
        )

        form_window.state(
            "zoomed"
        )

        form_window.configure(
            bg="#F4F6F8"
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            form_window,
            bg="#8B0000",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#8B0000",
            fg="white"
        ).pack(
            side="left",
            padx=40
        )

        tk.Button(
            header,
            text="Close",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#8B0000",
            activebackground="#EEEEEE",
            relief="flat",
            cursor="hand2",
            command=form_window.destroy
        ).pack(
            side="right",
            padx=40,
            ipadx=15,
            ipady=7
        )

        # =====================================================
        # FIXED BOTTOM BUTTON AREA
        # =====================================================

        bottom = tk.Frame(
            form_window,
            bg="white",
            height=85
        )

        bottom.pack(
            side="bottom",
            fill="x"
        )

        bottom.pack_propagate(False)

        # =====================================================
        # SCROLLABLE FORM AREA
        # =====================================================

        body = tk.Frame(
            form_window,
            bg="#F4F6F8"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        canvas = tk.Canvas(
            body,
            bg="#F4F6F8",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            body,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        card = tk.Frame(
            canvas,
            bg="white"
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=card,
            anchor="n"
        )

        # =====================================================
        # SCROLL REGION
        # =====================================================

        def update_scroll(event=None):

            canvas.configure(
                scrollregion=
                canvas.bbox("all")
            )

        card.bind(
            "<Configure>",
            update_scroll
        )

        # =====================================================
        # CARD WIDTH
        # =====================================================

        def resize_card(event):

            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            resize_card
        )

        # =====================================================
        # FOOD NAME
        # =====================================================

        self.form_label(
            card,
            "Food Name"
        )

        name_entry = tk.Entry(
            card,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        name_entry.pack(
            fill="x",
            padx=60,
            ipady=8
        )

        if food:

            name_entry.insert(
                0,
                food.get(
                    "food_name",
                    ""
                )
            )

        # =====================================================
        # CATEGORY
        # =====================================================

        self.form_label(
            card,
            "Category"
        )

        category_values = []
        category_map = {}

        for category in self.categories:

            category_values.append(
                category["category_name"]
            )

            category_map[
                category["category_name"]
            ] = category["id"]

        category_var = tk.StringVar()

        if food:

            category_var.set(
                food.get(
                    "category_name",
                    ""
                )
            )

        elif category_values:

            category_var.set(
                category_values[0]
            )

        category_menu = tk.OptionMenu(
            card,
            category_var,
            *category_values
        )

        category_menu.config(
            font=("Arial", 11),
            bg="white",
            fg="#333333",
            relief="solid",
            bd=1,
            anchor="w"
        )

        category_menu.pack(
            fill="x",
            padx=60,
            ipady=4
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        self.form_label(
            card,
            "Description"
        )

        description_text = tk.Text(
            card,
            font=("Arial", 11),
            height=4,
            relief="solid",
            bd=1
        )

        description_text.pack(
            fill="x",
            padx=60
        )

        if food:

            description_text.insert(
                "1.0",
                food.get(
                    "description",
                    ""
                )
            )

        # =====================================================
        # PRICE
        # =====================================================

        self.form_label(
            card,
            "Price"
        )

        price_entry = tk.Entry(
            card,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        price_entry.pack(
            fill="x",
            padx=60,
            ipady=8
        )

        if food:

            price_entry.insert(
                0,
                str(
                    food.get(
                        "price",
                        ""
                    )
                )
            )

        # =====================================================
        # IMAGE
        # =====================================================

        self.form_label(
            card,
            "Food Image"
        )

        image_frame = tk.Frame(
            card,
            bg="white"
        )

        image_frame.pack(
            fill="x",
            padx=60
        )

        image_entry = tk.Entry(
            image_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        image_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        if food:

            image_entry.insert(
                0,
                food.get(
                    "image",
                    ""
                ) or ""
            )

        tk.Button(
            image_frame,
            text="Browse",
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            relief="flat",
            cursor="hand2",
            command=lambda:
            self.browse_image(
                image_entry,
                form_window
            )
        ).pack(
            side="right",
            padx=(10, 0),
            ipadx=12,
            ipady=7
        )

        # =====================================================
        # IMAGE PREVIEW
        # =====================================================

        preview_frame = tk.Frame(
            card,
            bg="white",
            height=100
        )

        preview_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        preview_frame.pack_propagate(False)

        preview_label = tk.Label(
            preview_frame,
            text="No image selected",
            font=("Arial", 9),
            bg="white",
            fg="#999999"
        )

        preview_label.pack(
            pady=10
        )

        if food and food.get("image"):

            self.show_preview(
                food["image"],
                preview_label
            )

        # =====================================================
        # AVAILABLE
        # =====================================================

        available_var = tk.BooleanVar(
            value=True
        )

        if food:

            available_var.set(
                bool(
                    food.get(
                        "available",
                        1
                    )
                )
            )

        tk.Checkbutton(
            card,
            text="Food is available",
            variable=available_var,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#333333",
            activebackground="white",
            selectcolor="white"
        ).pack(
            anchor="w",
            padx=60,
            pady=(5, 30)
        )

        # =====================================================
        # FIXED ADD / UPDATE BUTTON
        # =====================================================

        button_text = (
            "Update Food"
            if food
            else
            "Add Food"
        )

        tk.Button(
            bottom,
            text=button_text,
            font=("Arial", 12, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda:
            self.save_food(
                form_window,
                food,
                name_entry,
                category_var,
                category_map,
                description_text,
                price_entry,
                image_entry,
                available_var
            )
        ).pack(
            pady=15,
            ipadx=55,
            ipady=9
        )

        # =====================================================
        # TOUCHPAD + MOUSE SCROLLING
        # =====================================================

        self.bind_touchpad_scroll(form_window, canvas)

        # =====================================================
        # KEYBOARD
        # =====================================================

        form_window.bind(
            "<Escape>",
            lambda event:
            form_window.destroy()
        )

        name_entry.focus_set()

    # =========================================================
    # TOUCHPAD / MOUSE SCROLLING
    # =========================================================

    def bind_touchpad_scroll(self, window, canvas):

        # Precision touchpads can send very small MouseWheel delta values.
        # Accumulate them until they equal one normal wheel step.
        state = {"remainder": 0}

        def mousewheel(event):

            try:
                delta = event.delta

                if delta == 0:
                    return "break"

                state["remainder"] += delta

                units = int(state["remainder"] / 120)

                if units != 0:
                    canvas.yview_scroll(-units, "units")
                    state["remainder"] -= units * 120

                return "break"

            except tk.TclError:
                return "break"

        def scroll_up(event):
            try:
                canvas.yview_scroll(-1, "units")
            except tk.TclError:
                pass
            return "break"

        def scroll_down(event):
            try:
                canvas.yview_scroll(1, "units")
            except tk.TclError:
                pass
            return "break"

        # Bind on the Toplevel, not only on the Canvas.
        # This makes scrolling work even when the pointer is over an Entry,
        # Text, Button, Label, OptionMenu, image, etc.
        window.bind("<MouseWheel>", mousewheel, add="+")
        window.bind("<Button-4>", scroll_up, add="+")
        window.bind("<Button-5>", scroll_down, add="+")

        # Shift + wheel for horizontal scrolling if ever needed.
        def horizontal_scroll(event):
            try:
                delta = event.delta
                state["remainder"] += delta
                units = int(state["remainder"] / 120)
                if units != 0:
                    canvas.xview_scroll(-units, "units")
                    state["remainder"] -= units * 120
            except tk.TclError:
                pass
            return "break"

        window.bind("<Shift-MouseWheel>", horizontal_scroll, add="+")

    # =========================================================
    # FORM LABEL
    # =========================================================

    def form_label(
        self,
        parent,
        text
    ):

        tk.Label(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#444444"
        ).pack(
            anchor="w",
            padx=60,
            pady=(15, 5)
        )

    # =========================================================
    # BROWSE IMAGE
    # =========================================================

    def browse_image(
        self,
        entry,
        parent
    ):

        path = filedialog.askopenfilename(
            parent=parent,
            title="Select Food Image",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg *.webp"
                )
            ]
        )

        if not path:
            return

        try:

            filename = os.path.basename(
                path
            )

            destination = os.path.join(
                self.food_folder,
                filename
            )

            if os.path.abspath(path) != os.path.abspath(
                destination
            ):

                shutil.copy2(
                    path,
                    destination
                )

            entry.delete(
                0,
                tk.END
            )

            entry.insert(
                0,
                filename
            )

        except Exception as e:

            messagebox.showerror(
                "Image Error",
                "Unable to copy image.\n\n"
                + str(e),
                parent=parent
            )

    # =========================================================
    # IMAGE PREVIEW
    # =========================================================

    def show_preview(
        self,
        filename,
        label
    ):

        if not filename:
            return

        filename = os.path.basename(
            str(filename)
        )

        path = os.path.join(
            self.food_folder,
            filename
        )

        if not os.path.exists(path):
            return

        try:

            image = Image.open(
                path
            )

            image.thumbnail(
                (80, 80),
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            label.config(
                image=photo,
                text=""
            )

            label.image = photo

        except Exception as e:

            print(
                "Preview error:",
                e
            )

    # =========================================================
    # SAVE FOOD
    # =========================================================

    def save_food(
        self,
        form_window,
        food,
        name_entry,
        category_var,
        category_map,
        description_text,
        price_entry,
        image_entry,
        available_var
    ):

        name = name_entry.get().strip()

        category_name = (
            category_var
            .get()
            .strip()
        )

        description = (
            description_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )

        price_text = (
            price_entry
            .get()
            .strip()
        )

        image = (
            image_entry
            .get()
            .strip()
        )

        available = (
            1
            if available_var.get()
            else 0
        )

        # ---------------- VALIDATION ----------------

        if not name:

            messagebox.showwarning(
                "Required",
                "Please enter food name.",
                parent=form_window
            )

            name_entry.focus_set()
            return

        if category_name not in category_map:

            messagebox.showwarning(
                "Required",
                "Please select a category.",
                parent=form_window
            )

            return

        if not price_text:

            messagebox.showwarning(
                "Required",
                "Please enter food price.",
                parent=form_window
            )

            price_entry.focus_set()
            return

        try:

            price = float(
                price_text
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Price",
                "Please enter a valid numeric price.",
                parent=form_window
            )

            price_entry.focus_set()
            return

        if price < 0:

            messagebox.showwarning(
                "Invalid Price",
                "Price cannot be negative.",
                parent=form_window
            )

            return

        category_id = category_map[
            category_name
        ]

        if image:

            image = os.path.basename(
                image
            )

        else:

            image = None

        # ---------------- DATABASE ----------------

        try:

            if food:

                execute_query(
                    """
                    UPDATE foods
                    SET
                        category_id = %s,
                        food_name = %s,
                        description = %s,
                        price = %s,
                        image = %s,
                        available = %s
                    WHERE id = %s
                    """,
                    (
                        category_id,
                        name,
                        description,
                        price,
                        image,
                        available,
                        food["id"]
                    )
                )

                messagebox.showinfo(
                    "Success",
                    "Food updated successfully.",
                    parent=form_window
                )

            else:

                execute_query(
                    """
                    INSERT INTO foods
                    (
                        category_id,
                        food_name,
                        description,
                        price,
                        image,
                        available
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        category_id,
                        name,
                        description,
                        price,
                        image,
                        available
                    )
                )

                messagebox.showinfo(
                    "Success",
                    "Food added successfully.",
                    parent=form_window
                )

            form_window.destroy()

            self.load_food()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Unable to save food.\n\n"
                + str(e),
                parent=form_window
            )

    # =========================================================
    # DELETE FOOD
    # =========================================================

    def delete_food(
        self,
        food_id
    ):

        food = fetch_one(
            """
            SELECT food_name
            FROM foods
            WHERE id = %s
            """,
            (food_id,)
        )

        if not food:

            messagebox.showerror(
                "Error",
                "Food item not found.",
                parent=self.window
            )

            return

        confirm = messagebox.askyesno(
            "Delete Food",
            "Are you sure you want to delete:\n\n"
            + food["food_name"]
            + "\n\nThis action cannot be undone.",
            parent=self.window
        )

        if not confirm:
            return

        try:

            execute_query(
                """
                DELETE FROM foods
                WHERE id = %s
                """,
                (food_id,)
            )

            messagebox.showinfo(
                "Success",
                "Food deleted successfully.",
                parent=self.window
            )

            self.load_food()

        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                "Unable to delete food.\n\n"
                + str(e),
                parent=self.window
            )

    # =========================================================
    # STATISTICS UPDATE
    # =========================================================

    def update_statistics(self):

        total = len(
            self.food_rows
        )

        available = 0
        unavailable = 0

        for food in self.food_rows:

            if food["available"]:

                available += 1

            else:

                unavailable += 1

        self.total_value.config(
            text=str(total)
        )

        self.available_value.config(
            text=str(available)
        )

        self.unavailable_value.config(
            text=str(unavailable)
        )

    # =========================================================
    # FOOD IMAGE
    # =========================================================

    def get_food_image(
        self,
        image_name
    ):

        if not image_name:
            return None

        filename = os.path.basename(
            str(image_name)
        )

        path = os.path.join(
            self.food_folder,
            filename
        )

        if not os.path.exists(path):
            return None

        try:

            image = Image.open(
                path
            )

            image.thumbnail(
                (50, 50),
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            self.icons[
                "food_" + filename
            ] = photo

            return photo

        except Exception as e:

            print(
                "Food image error:",
                e
            )

            return None

    # =========================================================
    # ICON
    # =========================================================

    def load_icon(
        self,
        filename,
        size
    ):

        path = os.path.join(
            self.base_dir,
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
                "Icon error:",
                filename,
                e
            )

            return None

    # =========================================================
    # CLOSE
    # =========================================================

    def close_window(self):

        try:

            self.window.destroy()

        except tk.TclError:

            pass


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Food Ordering App"
    )

    root.state(
        "zoomed"
    )

    ManageFood(
        root
    )

    root.mainloop()
