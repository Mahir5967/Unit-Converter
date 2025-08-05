import tkinter as tk
from tkinter import ttk, messagebox

# Global variables
from_unit_var = None
to_unit_var = None
result_label = None
input_entry = None
current_converter_type = "Length"
converter_title_label = None
from_dropdown = None
to_dropdown = None

def create_main_window():
    root = tk.Tk()
    root.title("Unit Converter")
    root.geometry("460x480")
    root.minsize(447, 465)
    root.resizable(True, True)
    return root

def show_about():
    messagebox.showinfo("About", "→ Unit Converter v1.0\n→ Built with Python Tkinter\n→ Converts various measurements")

def switch_converter(converter_type):
    global current_converter_type, from_unit_var, to_unit_var, from_dropdown, to_dropdown, input_entry, result_label
    
    current_converter_type = converter_type
    converter_title_label.configure(text=f"{converter_type} Unit Converter")
    
    # Reset input and result
    if input_entry:
        input_entry.delete(0, tk.END)
    if result_label:
        result_label.config(text="Result: ")
    
    # Update unit dropdowns based on converter type
    units = get_units(converter_type)
    from_dropdown['values'] = units
    to_dropdown['values'] = units
    
    # Set default units for each converter type
    if converter_type == "Length":
        from_unit_var.set("Meters")
        to_unit_var.set("Millimeters")
    elif converter_type == "Temperature":
        from_unit_var.set("Celsius")
        to_unit_var.set("Fahrenheit")
    elif converter_type == "Weight":
        from_unit_var.set("Kilograms")
        to_unit_var.set("Grams")

def new_converter():
    global input_entry, result_label
    if input_entry:
        input_entry.delete(0, tk.END)
    if result_label:
        result_label.config(text="Result: ")

def exit_app(root):
    if messagebox.askokcancel("Exit", "Your Unit Converter is being closed"):
        root.quit()

def create_menu_bar(root):
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_converter)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: exit_app(root))

    # Converter Menu
    converter_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Converter", menu=converter_menu)
    converter_menu.add_command(label="Length Converter", command=lambda: switch_converter("Length"))
    converter_menu.add_command(label="Temperature Converter", command=lambda: switch_converter("Temperature"))
    converter_menu.add_command(label="Weight Converter", command=lambda: switch_converter("Weight"))

    # Help Menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)

def convert_length(value, from_unit, to_unit):
    to_meters = {
        "Millimeters": 0.001,
        "Centimeters": 0.01,
        "Meters": 1.0,
        "Kilometers": 1000.0,
        "Inches": 0.0254,
        "Feet": 0.3048,
        "Yards": 0.9144,
        "Miles": 1609.34
    }
    meters = value * to_meters[from_unit]
    result = meters / to_meters[to_unit]
    return result

def convert_temperature(value, from_unit, to_unit):
    # Convert to Celsius first
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    
    # Convert from Celsius to target unit
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15

def convert_weight(value, from_unit, to_unit):
    to_grams = {
        "Milligrams": 0.001,
        "Grams": 1.0,
        "Kilograms": 1000.0,
        "Metric Tons": 1000000.0,
        "Ounces": 28.3495,
        "Pounds": 453.592
    }
    grams = value * to_grams[from_unit]
    result = grams / to_grams[to_unit]
    return result

def get_units(converter_type):
    if converter_type == "Length":
        return ["Millimeters", "Centimeters", "Meters", "Kilometers", "Inches", "Feet", "Yards", "Miles"]
    elif converter_type == "Temperature":
        return ["Celsius", "Fahrenheit", "Kelvin"]
    elif converter_type == "Weight":
        return ["Milligrams", "Grams", "Kilograms", "Metric Tons", "Ounces", "Pounds"]

def perform_conversion():
    global current_converter_type
    try:
        value_text = input_entry.get().strip()
        if not value_text:
            messagebox.showerror("Error", "Please enter a value to convert!")
            return
        value = float(value_text)
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()
        
        # Select conversion function based on current converter type
        if current_converter_type == "Length":
            result = convert_length(value, from_unit, to_unit)
        elif current_converter_type == "Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        elif current_converter_type == "Weight":
            result = convert_weight(value, from_unit, to_unit)
        else:
            messagebox.showerror("Error", "Invalid converter type")
            return

        # Format result based on magnitude
        if abs(result) < 0.0001:
            result_text = f"{result:.4e}" 
        elif abs(result) < 1:
            result_text = f"{result:.6f}".rstrip('0').rstrip('.')
        else:
            result_text = f"{result:.4f}".rstrip('0').rstrip('.')
            
        result_label.config(text=f"Result: {result_text} {to_unit}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {str(e)}")

def create_gui():
    global from_unit_var, to_unit_var, result_label, input_entry, converter_title_label, from_dropdown, to_dropdown

    root = create_main_window()
    create_menu_bar(root)

    # Theme Styling
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#f4f6fa')
    style.configure('TLabel', background='#f4f6fa', font=('Segoe UI', 11))
    style.configure('TButton', font=('Segoe UI', 10, 'bold'), foreground='white', background='#2e86de')
    style.map('TButton', background=[('active', '#1b4f72')])
    style.configure('TCombobox', font=('Segoe UI', 10))

    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky="nsew")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    converter_title_label = ttk.Label(main_frame, text="Length Unit Converter", font=("Segoe UI", 16, "bold"), foreground="#2e4053")
    converter_title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

    input_frame = ttk.LabelFrame(main_frame, text="Enter Value", padding="10")
    input_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))
    input_frame.columnconfigure(1, weight=1)

    ttk.Label(input_frame, text="Value:", background="#dddddd").grid(row=0, column=0, padx=(0, 10), sticky="w")
    input_entry = ttk.Entry(input_frame, width=20, font=("Segoe UI", 11))
    input_entry.grid(row=0, column=1, sticky="ew")
    input_entry.bind('<Return>', lambda event: perform_conversion())

    unit_frame = ttk.LabelFrame(main_frame, text="Select Units", padding="10")
    unit_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 15))

    from_unit_var = tk.StringVar()
    to_unit_var = tk.StringVar()

    ttk.Label(unit_frame, text="From:", background="#dddddd").grid(row=0, column=0, padx=(0, 10), sticky="w")
    from_dropdown = ttk.Combobox(unit_frame, textvariable=from_unit_var, state="readonly", width=15)
    from_dropdown.grid(row=0, column=1, padx=(0, 20))

    ttk.Label(unit_frame, text="To:", background="#dddddd").grid(row=0, column=2, padx=(0, 10), sticky="w")
    to_dropdown = ttk.Combobox(unit_frame, textvariable=to_unit_var, state="readonly", width=15)
    to_dropdown.grid(row=0, column=3)

    convert_button = ttk.Button(main_frame, text="🔄 Convert", command=perform_conversion)
    convert_button.grid(row=3, column=0, columnspan=3, pady=20)

    result_frame = ttk.LabelFrame(main_frame, text="Conversion Result", padding="10")
    result_frame.grid(row=4, column=0, columnspan=3, sticky="ew")
    result_label = ttk.Label(result_frame, text="Result: Enter a value and click Convert", font=("Segoe UI", 11, "bold"), foreground="#2e86de", background="#dddddd")
    result_label.grid(row=0, column=0, sticky="w")

    instructions = ttk.Label(main_frame, text="💡 Tip: Press Enter after typing a value to convert quickly",
                            font=("Segoe UI", 9), foreground="#616a6b")
    instructions.grid(row=5, column=0, columnspan=3, pady=(10, 0))

    # Initialize converter with default settings
    switch_converter("Length")
    input_entry.focus()
    return root

# Main program
if __name__ == "__main__":
    print("Starting Unit Converter...")
    root = create_gui()
    root.mainloop()
    print("Unit Converter closed.")