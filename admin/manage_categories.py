import tkinter as tk
from tkinter import messagebox

from database import fetch_all, fetch_one, execute_query


class ManageCategories:

    def __init__(self, parent):

        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Manage Categories")
        self.window.state("zoomed")
        self.window.configure(bg="#F4F6F8")

        self.edit_id = None

        self.create_ui()
        self.load_categories()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =========================================================
    # MAIN UI
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
            text="Manage Categories",
            font=("Arial", 24, "bold"),
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
        # MAIN CONTAINER
        # =====================================================

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
        # STATISTICS
        # =====================================================

        stats = tk.Frame(
            main,
            bg="#F4F6F8"
        )
        stats.pack(
            fill="x",
            pady=(0, 25)
        )

        # Total Categories

        self.total_card = self.create_stat_card(
            stats,
            "Total Categories",
            "0"
        )

        self.total_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )

        # Categories With Food

        self.food_card = self.create_stat_card(
            stats,
            "Categories With Food",
            "0"
        )

        self.food_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(12, 0)
        )

        # =====================================================
        # CONTENT
        # =====================================================

        content = tk.Frame(
            main,
            bg="white"
        )
        content.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # LEFT SIDE - ADD CATEGORY
        # =====================================================

        left = tk.Frame(
            content,
            bg="white",
            width=350
        )

        left.pack(
            side="left",
            fill="y",
            padx=30,
            pady=30
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="Add Category",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            pady=(0, 30)
        )

        tk.Label(
            left,
            text="Category Name",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        self.category_entry = tk.Entry(
            left,
            font=("Arial", 13),
            relief="solid",
            bd=1
        )

        self.category_entry.pack(
            fill="x",
            ipady=9
        )

        # Add / Update button

        self.save_button = tk.Button(
            left,
            text="Add Category",
            font=("Arial", 12, "bold"),
            bg="#8B0000",
            fg="white",
            activebackground="#660000",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.add_category
        )

        self.save_button.pack(
            fill="x",
            pady=(25, 10),
            ipady=10
        )

        # Clear

        tk.Button(
            left,
            text="Clear",
            font=("Arial", 12, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#333333",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_form
        ).pack(
            fill="x",
            ipady=10
        )

        # =====================================================
        # RIGHT SIDE
        # =====================================================

        right = tk.Frame(
            content,
            bg="white"
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 30),
            pady=30
        )

        # =====================================================
        # SEARCH
        # =====================================================

        search_frame = tk.Frame(
            right,
            bg="white",
            height=55
        )

        search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        search_frame.pack_propagate(False)

        tk.Label(
            search_frame,
            text="Search",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        ).pack(
            side="left",
            padx=(0, 15)
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_categories
        )

        tk.Button(
            search_frame,
            text="Refresh",
            font=("Arial", 11, "bold"),
            bg="#333333",
            fg="white",
            activebackground="#222222",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.load_categories
        ).pack(
            side="left",
            padx=(15, 0),
            ipadx=15,
            ipady=7
        )

        # =====================================================
        # TABLE
        # =====================================================

        table = tk.Frame(
            right,
            bg="white"
        )

        table.pack(
            fill="both",
            expand=True
        )

        # ---------------- TABLE HEADER ----------------

        self.table_header = tk.Frame(
            table,
            bg="#333333",
            height=50
        )

        self.table_header.pack(
            fill="x"
        )

        self.table_header.pack_propagate(False)

        self.create_header(
            self.table_header,
            "ID",
            0.10
        )

        self.create_header(
            self.table_header,
            "Category Name",
            0.38
        )

        self.create_header(
            self.table_header,
            "Food Items",
            0.20
        )

        self.create_header(
            self.table_header,
            "Action",
            0.32
        )

        # ---------------- TABLE BODY ----------------

        body = tk.Frame(
            table,
            bg="white"
        )

        body.pack(
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            body,
            bg="white",
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            body,
            orient="vertical",
            command=self.canvas.yview
        )

        self.rows_frame = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.rows_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.rows_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas
        )

        # Mouse wheel only for this window

        self.window.bind(
            "<MouseWheel>",
            self.mouse_scroll
        )

        self.window.bind(
            "<Button-4>",
            self.mouse_scroll
        )

        self.window.bind(
            "<Button-5>",
            self.mouse_scroll
        )

        self.category_entry.focus_set()

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            bg="white",
            height=105
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 12),
            bg="white",
            fg="#666666"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 2)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 27, "bold"),
            bg="white",
            fg="#8B0000"
        )

        value_label.pack(
            anchor="w",
            padx=25
        )

        card.value_label = value_label

        return card

    # =========================================================
    # TABLE HEADER
    # =========================================================

    def create_header(
        self,
        parent,
        text,
        weight
    ):

        label = tk.Label(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg="#333333",
            fg="white",
            anchor="w"
        )

        label.place(
            relx=sum([]),
            rely=0,
            relwidth=weight,
            relheight=1
        )

        # Position is calculated separately
        existing = getattr(
            parent,
            "_header_position",
            0
        )

        label.place_configure(
            relx=existing
        )

        parent._header_position = existing + weight

    # =========================================================
    # TABLE RESIZE
    # =========================================================

    def resize_canvas(self, event):

        try:

            self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )

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
    # LOAD DATA
    # =========================================================

    def load_categories(self):

        try:

            query = """
                SELECT
                    c.id,
                    c.category_name,
                    COUNT(f.id) AS food_count
                FROM categories c
                LEFT JOIN foods f
                    ON c.id = f.category_id
                GROUP BY
                    c.id,
                    c.category_name
                ORDER BY c.id DESC
            """

            categories = fetch_all(query)

            self.display_categories(categories)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load categories.\n\n{e}",
                parent=self.window
            )

    # =========================================================
    # DISPLAY
    # =========================================================

    def display_categories(
        self,
        categories
    ):

        for widget in self.rows_frame.winfo_children():
            widget.destroy()

        # ---------------- EMPTY ----------------

        if not categories:

            tk.Label(
                self.rows_frame,
                text="No categories found.",
                font=("Arial", 14),
                bg="white",
                fg="#777777"
            ).pack(
                pady=40
            )

        # ---------------- ROWS ----------------

        for index, category in enumerate(categories):

            bg = (
                "#FFFFFF"
                if index % 2 == 0
                else "#F7F7F7"
            )

            row = tk.Frame(
                self.rows_frame,
                bg=bg,
                height=60
            )

            row.pack(
                fill="x"
            )

            row.pack_propagate(False)

            # ID

            tk.Label(
                row,
                text=str(category["id"]),
                font=("Arial", 11),
                bg=bg,
                fg="#333333",
                anchor="w"
            ).place(
                relx=0,
                rely=0,
                relwidth=0.10,
                relheight=1
            )

            # Category

            tk.Label(
                row,
                text=category["category_name"],
                font=("Arial", 11, "bold"),
                bg=bg,
                fg="#222222",
                anchor="w"
            ).place(
                relx=0.10,
                rely=0,
                relwidth=0.38,
                relheight=1
            )

            # Food Count

            tk.Label(
                row,
                text=str(category["food_count"]),
                font=("Arial", 11),
                bg=bg,
                fg="#555555",
                anchor="w"
            ).place(
                relx=0.48,
                rely=0,
                relwidth=0.20,
                relheight=1
            )

            # Actions

            action = tk.Frame(
                row,
                bg=bg
            )

            action.place(
                relx=0.68,
                rely=0,
                relwidth=0.32,
                relheight=1
            )

            tk.Button(
                action,
                text="Edit",
                font=("Arial", 10, "bold"),
                bg="#333333",
                fg="white",
                activebackground="#222222",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=lambda c=category:
                self.edit_category(c)
            ).pack(
                side="left",
                padx=(5, 5),
                pady=12,
                ipadx=12
            )

            tk.Button(
                action,
                text="Delete",
                font=("Arial", 10, "bold"),
                bg="#8B0000",
                fg="white",
                activebackground="#660000",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=lambda c=category:
                self.delete_category(c)
            ).pack(
                side="left",
                padx=5,
                pady=12,
                ipadx=8
            )

        # Statistics

        total = len(categories)

        with_food = sum(
            1
            for category in categories
            if category["food_count"] > 0
        )

        self.total_card.value_label.config(
            text=str(total)
        )

        self.food_card.value_label.config(
            text=str(with_food)
        )

        self.update_scroll_region()

    # =========================================================
    # ADD
    # =========================================================

    def add_category(self):

        name = self.category_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Required",
                "Please enter category name.",
                parent=self.window
            )

            self.category_entry.focus_set()

            return

        try:

            existing = fetch_one(
                """
                SELECT id
                FROM categories
                WHERE LOWER(category_name)
                      = LOWER(%s)
                """,
                (name,)
            )

            if existing:

                messagebox.showwarning(
                    "Duplicate",
                    "This category already exists.",
                    parent=self.window
                )

                return

            execute_query(
                """
                INSERT INTO categories
                (category_name)
                VALUES (%s)
                """,
                (name,)
            )

            messagebox.showinfo(
                "Success",
                "Category added successfully.",
                parent=self.window
            )

            self.clear_form()
            self.load_categories()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.window
            )

    # =========================================================
    # EDIT
    # =========================================================

    def edit_category(
        self,
        category
    ):

        self.edit_id = category["id"]

        self.category_entry.delete(
            0,
            tk.END
        )

        self.category_entry.insert(
            0,
            category["category_name"]
        )

        self.save_button.config(
            text="Update Category",
            command=self.update_category
        )

        self.category_entry.focus_set()

    # =========================================================
    # UPDATE
    # =========================================================

    def update_category(self):

        if self.edit_id is None:
            return

        name = self.category_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Required",
                "Please enter category name.",
                parent=self.window
            )

            return

        try:

            existing = fetch_one(
                """
                SELECT id
                FROM categories
                WHERE LOWER(category_name)
                      = LOWER(%s)
                AND id != %s
                """,
                (
                    name,
                    self.edit_id
                )
            )

            if existing:

                messagebox.showwarning(
                    "Duplicate",
                    "Another category with this name already exists.",
                    parent=self.window
                )

                return

            execute_query(
                """
                UPDATE categories
                SET category_name = %s
                WHERE id = %s
                """,
                (
                    name,
                    self.edit_id
                )
            )

            messagebox.showinfo(
                "Success",
                "Category updated successfully.",
                parent=self.window
            )

            self.clear_form()
            self.load_categories()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.window
            )

    # =========================================================
    # DELETE
    # =========================================================

    def delete_category(
        self,
        category
    ):

        category_id = category["id"]
        category_name = category["category_name"]
        food_count = category["food_count"]

        if food_count > 0:

            messagebox.showwarning(
                "Cannot Delete",
                f"'{category_name}' has "
                f"{food_count} food item(s) assigned.\n\n"
                "Remove those food items first.",
                parent=self.window
            )

            return

        confirm = messagebox.askyesno(
            "Delete Category",
            f"Are you sure you want to delete\n"
            f"'{category_name}'?",
            parent=self.window
        )

        if not confirm:
            return

        try:

            execute_query(
                """
                DELETE FROM categories
                WHERE id = %s
                """,
                (category_id,)
            )

            messagebox.showinfo(
                "Deleted",
                "Category deleted successfully.",
                parent=self.window
            )

            self.load_categories()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.window
            )

    # =========================================================
    # SEARCH
    # =========================================================

    def search_categories(
        self,
        event=None
    ):

        search = self.search_entry.get().strip()

        if not search:

            self.load_categories()

            return

        try:

            query = """
                SELECT
                    c.id,
                    c.category_name,
                    COUNT(f.id) AS food_count
                FROM categories c
                LEFT JOIN foods f
                    ON c.id = f.category_id
                WHERE c.category_name LIKE %s
                GROUP BY
                    c.id,
                    c.category_name
                ORDER BY c.id DESC
            """

            categories = fetch_all(
                query,
                (f"%{search}%",)
            )

            self.display_categories(categories)

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                str(e),
                parent=self.window
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self):

        self.edit_id = None

        self.category_entry.delete(
            0,
            tk.END
        )

        self.save_button.config(
            text="Add Category",
            command=self.add_category
        )

        self.category_entry.focus_set()

    # =========================================================
    # MOUSE / TOUCHPAD SCROLL
    # =========================================================

    def mouse_scroll(
        self,
        event
    ):

        try:

            if not self.canvas.winfo_exists():
                return

            if event.num == 4:

                self.canvas.yview_scroll(
                    -1,
                    "units"
                )

            elif event.num == 5:

                self.canvas.yview_scroll(
                    1,
                    "units"
                )

            elif event.delta > 0:

                self.canvas.yview_scroll(
                    -1,
                    "units"
                )

            elif event.delta < 0:

                self.canvas.yview_scroll(
                    1,
                    "units"
                )

        except tk.TclError:

            pass

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


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    ManageCategories(root)

    root.mainloop()
