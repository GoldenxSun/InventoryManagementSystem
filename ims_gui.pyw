"""
Inventory Management System
Author: GoldenxSun

This script creates a graphical user interface (GUI) for an Inventory Management System using Tkinter.
The application allows users to manage products, including adding, editing, deleting, and searching for products.
Additionally, it supports processing incoming and outgoing goods and generating QR codes for products.

Main Features:
- List products in a table with search functionality.
- Add, edit, and delete products.
- Process incoming and outgoing goods.
- Generate QR codes for products.

Dependencies:
- Tkinter (for GUI)
- InventoryManagement (custom module for database operations)

Constants:
- BUTTON_COLOR: Color for buttons in the application.
- BACKGROUND_COLOR: Background color for the main application window and frames.
- TABULAR_COLOR_1: Color for even rows in the product list.
- TABULAR_COLOR_2: Color for odd rows in the product list.
- TEXT_COLOR: Color for text in the application.
- HIGHLIGHT_COLOR: Color for highlighted elements in the application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry, Button
from inventory_db import InventoryManagement

BUTTON_COLOR = "#7e5ab6"
BACKGROUND_COLOR = "#f3f1f9"
TABULAR_COLOR_1 = "#7e5ab6"
TABULAR_COLOR_2 = "#d196b1"
TEXT_COLOR = "#0e0a16"
HIGHLIGHT_COLOR = "#c27478" 

class Application(tk.Tk):
    def __init__(self):
        """
        Initializes the Application class, setting up the main window and 
        inventory management system.
        """
        super().__init__()
        self.inventory_management = InventoryManagement()
        self.title("Inventory Management System")
        self.center_window(800, 582)
        self.configure(bg=BACKGROUND_COLOR)

        self.create_widgets()
        self.list_products()

    def center_window(self, width, height):
        """
        Centers the application window on the screen.

        Parameters:
            width (int): The width of the window.
            height (int): The height of the window.

        Returns:
            None
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """
        Creates and arranges the main widgets in the application window,
        including buttons and the product list tree view.

        Returns:
            None
        """
        self.frame_buttons = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.frame_buttons.pack(pady=20, side=tk.TOP)

        self.button_refresh = tk.Button(self.frame_buttons, text="Refresh", width=15, command=self.list_products, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_refresh.grid(row=0, column=0, padx=5)

        self.button_add = tk.Button(self.frame_buttons, text="Add Product", width=15, command=self.open_add_product_window, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_add.grid(row=0, column=1, padx=5)

        self.button_edit = tk.Button(self.frame_buttons, text="Edit Product", width=15, command=self.open_edit_product_window, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_edit.grid(row=0, column=2, padx=5)

        self.button_delete = tk.Button(self.frame_buttons, text="Delete Product", width=15, command=self.delete_product, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_delete.grid(row=0, column=3, padx=5)

        self.button_incoming = tk.Button(self.frame_buttons, text="Incoming Goods", width=15, command=self.process_incoming_goods, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_incoming.grid(row=0, column=4, padx=30)

        self.button_outgoing = tk.Button(self.frame_buttons, text="Outgoing Goods", width=15, command=self.process_outgoing_goods, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_outgoing.grid(row=1, column=4, padx=30)

        self.label_search = tk.Label(self.frame_buttons, text="Search by Product Name or ID:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_search.grid(row=1, column=0, padx=5, pady=10, sticky=tk.E)

        self.entry_search = tk.Entry(self.frame_buttons, width=40)
        self.entry_search.grid(row=1, column=1, columnspan=2, padx=5, pady=10)
        self.entry_search.bind('<Return>', self.search_product)

        self.button_search = tk.Button(self.frame_buttons, text="Search", width=15, command=self.search_product, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_search.grid(row=1, column=3, padx=5, pady=10)

        self.frame_tree = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.frame_tree.pack(pady=10, side=tk.BOTTOM)

        self.tree = ttk.Treeview(self.frame_tree, columns=('ID', 'Name', 'Quantity', 'Price', 'Description'), show='headings', height=20)
        self.tree.heading('ID', text='ID')
        self.tree.column('ID', width=80)
        self.tree.heading('Name', text='Name')
        self.tree.column('Name', width=230)
        self.tree.heading('Quantity', text='Quantity')
        self.tree.column('Quantity', width=80)
        self.tree.heading('Price', text='Price')
        self.tree.column('Price', width=80)
        self.tree.heading('Description', text='Description')
        self.tree.column('Description', width=230)
        self.tree.pack(pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.heading('ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('Name', text='Product Name', anchor=tk.CENTER)
        self.tree.heading('Quantity', text='Quantity', anchor=tk.CENTER)
        self.tree.heading('Price', text='Price', anchor=tk.CENTER)
        self.tree.heading('Description', text='Description', anchor=tk.CENTER)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('Treeview', background=BACKGROUND_COLOR, foreground=TEXT_COLOR, rowheight=25, font=('Helvetica', 10))
        self.style.configure('Treeview.Heading', background=BUTTON_COLOR, foreground=TEXT_COLOR, font=('Helvetica', 10, 'bold'))

        self.scrollbar = tk.Scrollbar(self.frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=11)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.bind('<Double-Button-1>', self.on_double_click)

    def list_products(self):
        """
        Lists all products in the tree view by retrieving them 
        from the inventory management system.

        Returns:
            None
        """
        self.tree.delete(*self.tree.get_children())
        products = self.inventory_management.list_products()

        self.tree.tag_configure('evenrow', background=TABULAR_COLOR_1, foreground=TEXT_COLOR, font=('Helvetica', 10))
        self.tree.tag_configure('oddrow', background=TABULAR_COLOR_2, foreground=TEXT_COLOR, font=('Helvetica', 10))
        
        for idx, (id, name, quantity, price, description) in enumerate(products):
            values = (id, name, quantity, price, description)
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=values, tags=(tag,))

    def open_add_product_window(self):
        """
        Opens a new window to add a product to the inventory.

        Returns:
            None
        """
        self.add_product_window = Toplevel(self, bg=BACKGROUND_COLOR)
        self.add_product_window.title("Add Product")
        width = 300
        height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.add_product_window.geometry(f'{width}x{height}+{x}+{y}')

        self.label_id = Label(self.add_product_window, text="ID:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_id.pack(pady=10)

        self.entry_id = Entry(self.add_product_window, width=30)
        self.entry_id.pack()

        self.label_name = Label(self.add_product_window, text="Product Name:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_name.pack(pady=10)

        self.entry_name = Entry(self.add_product_window, width=30)
        self.entry_name.pack()

        self.label_quantity = Label(self.add_product_window, text="Quantity:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_quantity.pack(pady=10)

        self.entry_quantity = Entry(self.add_product_window, width=30)
        self.entry_quantity.pack()

        self.label_price = Label(self.add_product_window, text="Price (€):", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_price.pack(pady=10)

        self.entry_price = Entry(self.add_product_window, width=30)
        self.entry_price.pack()

        self.label_description = Label(self.add_product_window, text="Description:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_description.pack(pady=10)

        self.entry_description = Entry(self.add_product_window, width=30)
        self.entry_description.pack()

        self.button_add_product = Button(self.add_product_window, text="Add Product", command=self.add_product, bg=BUTTON_COLOR, fg=TEXT_COLOR)
        self.button_add_product.pack(pady=20)
        self.entry_description.bind('<Return>', self.add_product)

    def add_product(self, event=None):
        """
        Adds a new product to the inventory based on user input
        in the add product window.

        Parameters:
            event (optional): The event that triggered the function call, defaults to None.

        Returns:
            None

        Raises:
            ValueError: If the input data is invalid.
        """
        product_id = self.entry_id.get()
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        description = self.entry_description.get()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            quantity = int(quantity) if quantity else 0
            price = float(price.replace(',', '.')) if price else 0.0
            product_id = int(product_id) if product_id else 0

            self.inventory_management.add_product(name, quantity, price, description, product_id)
            self.add_product_window.destroy()
            self.list_products()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity and price.")


    def open_edit_product_window(self):
        """
        Opens a new window to edit an existing product in the inventory.

        Returns:
            None
        """
        try:
            selected_product_index = self.tree.selection()[0]
            selected_product = self.tree.item(selected_product_index, 'values')
            product_id = int(selected_product[0])

            product_details = self.inventory_management.get_product(product_id)

            if product_details:
                self.edit_window = Toplevel(self, bg=BACKGROUND_COLOR)
                self.edit_window.title("Edit Product")

                Label(self.edit_window, text="Name:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10)
                self.entry_name = Entry(self.edit_window, width=30)
                self.entry_name.grid(row=0, column=1, padx=10, pady=10)
                self.entry_name.insert(0, product_details[1])

                Label(self.edit_window, text="Quantity:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10)
                self.entry_quantity = Entry(self.edit_window, width=30)
                self.entry_quantity.grid(row=1, column=1, padx=10, pady=10)
                self.entry_quantity.insert(0, product_details[2])

                Label(self.edit_window, text="Price:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=10)
                self.entry_price = Entry(self.edit_window, width=30)
                self.entry_price.grid(row=2, column=1, padx=10, pady=10)
                self.entry_price.insert(0, product_details[3])

                Label(self.edit_window, text="Description:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=3, column=0, padx=10, pady=10)
                self.entry_description = Entry(self.edit_window, width=30)
                self.entry_description.grid(row=3, column=1, padx=10, pady=10)
                self.entry_description.insert(0, product_details[4])

                Button(self.edit_window, text="Save Changes", width=15, command=lambda: self.save_product_changes(product_id), bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=4, columnspan=2, pady=10)

            else:
                messagebox.showerror("Error", "Product not found.")
        except IndexError:
            messagebox.showerror("Error", "Please select a product to edit.")

    def save_product_changes(self, product_id):
        """
        Saves the changes made to a product's details.

        Parameters:
            product_id (int): The ID of the product being updated.

        Returns:
            None
        """
        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()
        description = self.entry_description.get().strip()

        if name and quantity and price and description:
            try:
                quantity = int(quantity)
                price = float(price)
                
                self.inventory_management.update_product(product_id, name, quantity, price, description)
                
                self.edit_window.destroy()
                self.list_products()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for quantity and price.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")


    def delete_product(self):
        """
        Deletes the selected product from the inventory.

        Returns:
            None
        """
        try:
            selected_product_index = self.tree.selection()[0]
            selected_product = self.tree.item(selected_product_index, 'values')
            product_id = int(selected_product[0])

            confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete this product?")
            if confirmation:
                self.inventory_management.delete_product(product_id)
                self.list_products()

        except IndexError:
            messagebox.showerror("Error", "Please select a product.")

    def search_product(self, event=None):
        """
        Searches for a product by ID or name based on user input.

        Parameters:
            event (optional): The event that triggered the function call, defaults to None.

        Returns:
            None
        """
        search_term = self.entry_search.get().strip()
        if not search_term:
            self.list_products()
            return

        try:
            product_id = int(search_term)
            product = self.inventory_management.get_product(product_id)
            if product:
                self.tree.delete(*self.tree.get_children())
                self.tree.insert('', tk.END, values=product)
            else:
                messagebox.showinfo("Information", f"No product found with ID '{product_id}'.")
        except ValueError:
            products = self.inventory_management.list_products()
            matching_products = [p for p in products if search_term.lower() in p[1].lower()]

            if matching_products:
                self.tree.delete(*self.tree.get_children())
                for idx, product in enumerate(matching_products):
                    values = product
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    self.tree.insert('', 'end', values=values, tags=(tag,))
            else:
                messagebox.showinfo("Information", f"No product found with the name '{search_term}'.")

    def process_incoming_goods(self):
        """
        Opens a window for processing incoming goods for a selected product.

        Returns:
            None
        """
        self.incoming_window = Toplevel(self, bg=BACKGROUND_COLOR)
        self.incoming_window.title("Process Incoming Goods")
        Label(self.incoming_window, text="Product ID:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10)
        self.entry_product_id_incoming = Entry(self.incoming_window, width=30)
        self.entry_product_id_incoming.grid(row=0, column=1, padx=10, pady=10)

        Label(self.incoming_window, text="Quantity to Add:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10)
        self.entry_quantity_incoming = Entry(self.incoming_window, width=30)
        self.entry_quantity_incoming.grid(row=1, column=1, padx=10, pady=10)

        Button(self.incoming_window, text="Add", width=15, command=self.add_incoming_goods, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=2, columnspan=2, pady=10)

    def add_incoming_goods(self):
        """
        Adds incoming goods to the inventory for the specified product.

        Returns:
            None
        """
        product_id = self.entry_product_id_incoming.get().strip()
        quantity = self.entry_quantity_incoming.get().strip()

        if product_id and quantity:
            try:
                product_id = int(product_id)
                quantity = int(quantity)
                self.inventory_management.add_stock(product_id, quantity)
                self.incoming_window.destroy()
                self.list_products()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    def process_outgoing_goods(self):
        """
        Opens a window for processing outgoing goods for a selected product.

        Returns:
            None
        """
        self.outgoing_window = Toplevel(self, bg=BACKGROUND_COLOR)
        self.outgoing_window.title("Process Outgoing Goods")
        Label(self.outgoing_window, text="Product ID:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10)
        self.entry_product_id_outgoing = Entry(self.outgoing_window, width=30)
        self.entry_product_id_outgoing.grid(row=0, column=1, padx=10, pady=10)

        Label(self.outgoing_window, text="Quantity to Remove:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10)
        self.entry_quantity_outgoing = Entry(self.outgoing_window, width=30)
        self.entry_quantity_outgoing.grid(row=1, column=1, padx=10, pady=10)

        Button(self.outgoing_window, text="Remove", width=15, command=self.remove_outgoing_goods, bg=BUTTON_COLOR, fg=TEXT_COLOR).grid(row=2, columnspan=2, pady=10)

    def remove_outgoing_goods(self):
        """
        Removes outgoing goods from the inventory for the specified product.

        Returns:
            None
        """
        product_id = self.entry_product_id_outgoing.get().strip()
        quantity = self.entry_quantity_outgoing.get().strip()

        if product_id and quantity:
            try:
                product_id = int(product_id)
                quantity = int(quantity)
                self.inventory_management.remove_stock(product_id, quantity)
                self.outgoing_window.destroy()
                self.list_products()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    def on_double_click(self, event):
        """
        Handles the double-click event on a product in the tree view.
        Prompts the user to create a QR code for the selected product.

        Parameters:
            event: The event that triggered the function call.

        Returns:
            None
        """
        try:
            item = self.tree.selection()[0]
            product = self.tree.item(item, 'values')

            answer = messagebox.askyesno("QR-Code erstellen", f"Möchten Sie einen QR-Code für {product[1]} erstellen?")
            if not answer:
                return

            self.qr_window = Toplevel(self, bg=BACKGROUND_COLOR)
            self.qr_window.title(f"QR-Code: {product[1]}")
            width = 500
            height = 550
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            self.qr_window.geometry(f'{width}x{height}+{x}+{y}')

            product_data = f"{product[0]}, {product[1]}, {product[3]}, {product[4]}"
            self.inventory_management.generate_qr_code(product_data, product[0])

            self.qr_label = Label(self.qr_window, text=f"QR-Code für {product[0]}, {product[1]}, {product[4]} wurde erstellt.", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
            self.qr_label.pack(pady=20)

            self.qr_image = tk.PhotoImage(file=f".\\QRCodes\\qr_code_{product[0]}.png")
            self.qr_image_label = Label(self.qr_window, image=self.qr_image, bg=BACKGROUND_COLOR)
            self.qr_image_label.pack(pady=10)

        except IndexError:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Produkt aus.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
