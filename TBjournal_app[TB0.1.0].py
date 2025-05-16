import ttkbootstrap as tb
import time
from PIL import Image, ImageTk

class JournalApp(tb.Window):
    def __init__(self):
        super().__init__(themename="morph")
        self.title("Journal App")
        self.geometry("900x700")
        self.fullscreen = False
        
        # Create container for all pages
        self.container = tb.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialise pages
        self.pages = {}
        for Page in (MainMenuPage, WritePage, ReadPage, StatsPage, SettingsPage):
            page_name = Page.__name__
            self.pages[page_name] = Page(parent=self.container, controller=self)
            self.pages[page_name].grid(row=0, column=0, sticky="nsew")

        self.show_page("MainMenuPage")
        self.bind("<Escape>", lambda e: self.toggle_fullscreen(False))

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
        if hasattr(page, "on_page_enter"):
            page.on_page_enter()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def toggle_theme(self):
        current = self.style.theme.name
        new_theme = "morph" if current == "darkly" else "darkly"
        self.style.theme_use(new_theme)

class MainMenuPage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Simplified layout to avoid grid issues
        main_frame = tb.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Logo and Title
        header = tb.Frame(main_frame)
        header.pack(pady=40)
        
        image = Image.open("images/smilecat.jpg").resize((100, 100))
        self.logo = ImageTk.PhotoImage(image)
        tb.Label(header, image=self.logo).pack(side='left', padx=20)
        
        title_frame = tb.Frame(header)
        title_frame.pack(side='left')
        tb.Label(title_frame, text="Journal App", 
                font=('Helvetica', 24, 'bold')).pack(anchor='w')
        tb.Label(title_frame, text="A Time Machine for Your Mind.", 
                font=('Helvetica', 14), bootstyle='secondary').pack(anchor='w')
        tb.Separator(title_frame, orient='horizontal', bootstyle='secondary').pack(fill='x', pady=3)

        # Navigation Buttons
        nav_buttons = [
            ('📝 New Entry', 'WritePage'),
            ('📖 Read Entries', 'ReadPage'),
            ('📊 Analytics', 'StatsPage'),
            ('⚙️ Settings', 'SettingsPage')
        ]

        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        for text, page in nav_buttons:
            tb.Button(
                btn_frame,
                text=text,
                command=lambda p=page: self.controller.show_page(p),
                width=30,
                padding=10,
                bootstyle='outline'
            ).pack(pady=10, fill='x')

        # Footer Controls
        footer = tb.Frame(main_frame)
        footer.pack(side='bottom', pady=20)
        
        tb.Button(footer, 
                 text="🌓 Toggle Theme", 
                 command=self.controller.toggle_theme,
                 bootstyle='outline',
                 padding=5).pack(side='left', padx=10)
        
        tb.Button(footer, 
                 text="🖥️ Toggle Fullscreen", 
                 command=self.controller.toggle_fullscreen,
                 bootstyle='outline',
                 padding=5).pack(side='left', padx=10)

class WritePage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tb.Label(self, text="Write Page - Coming Soon!", 
                font=('Helvetica', 16)).pack(pady=50, expand=True)
        tb.Button(self, text="← Main Menu", command=lambda: self.controller.show_page("MainMenuPage")).pack(side="bottom", pady=15)



class ReadPage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tb.Label(self, text="Read Page - Coming Soon!", 
                font=('Helvetica', 16)).pack(pady=50, expand=True)
        tb.Button(self, text="← Main Menu", command=lambda: self.controller.show_page("MainMenuPage")).pack(side="bottom", pady=15)


class StatsPage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tb.Label(self, text="Learn Page", font=('Helvetica', 16)).pack(pady=10)

        # Create a Notebook to hold both the Glossary and Acronyms
        notebook = tb.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Tab 1: Glossary
        glossary_frame = tb.Frame(notebook)
        notebook.add(glossary_frame, text="Glossary")

        glossary_columns = ("Term", "Explanation")
        glossary_tree = tb.Treeview(glossary_frame, columns=glossary_columns, show="headings", height=8)
        glossary_tree.heading("Term", text="Term")
        glossary_tree.heading("Explanation", text="Explanation")
        glossary_tree.column("Term", width=150, anchor="center")
        glossary_tree.column("Explanation", width=350, anchor="w")

        # Glossary data
        glossary_data = [
            ("Fake", "This is fake made up data."),
            ("Bandwidth", "The maximum rate of data transfer."),
            ("Latency", "The delay before a transfer of data begins."),
            ("Throughput", "The amount of material or items passing through a system.")
        ]

        for term, explanation in glossary_data:
            glossary_tree.insert("", tb.END, values=(term, explanation))

        glossary_scrollbar = tb.Scrollbar(glossary_frame, orient="vertical", command=glossary_tree.yview)
        glossary_tree.configure(yscroll=glossary_scrollbar.set)
        glossary_scrollbar.pack(side="right", fill="y")
        glossary_tree.pack(side="left", fill="both", expand=True)

        # Tab 2: Acronyms
        acronyms_frame = tb.Frame(notebook)
        notebook.add(acronyms_frame, text="Acronyms")

        acronym_columns = ("Acronym", "Definition")
        acronym_tree = tb.Treeview(acronyms_frame, columns=acronym_columns, show="headings", height=8)
        acronym_tree.heading("Acronym", text="Acronym")
        acronym_tree.heading("Definition", text="Definition")
        acronym_tree.column("Acronym", width=150, anchor="center")
        acronym_tree.column("Definition", width=350, anchor="w")

        acronym_data = [
            ("FLAP", "Friendly Llamas Always Party"),
            ("ZING", "Zebra Investigating Noodle Growth"),
            ("BLOB", "Big Lumpy Orange Blob"),
            ("WOMB", "Waffles On Mars Brigade"),
            ("GIGGLE", "Giant Iguanas Giggling Gleefully Loudly Everywhere"),
            ("SNORT", "Silly Narwhals Ordering Raspberry Tarts"),
            ("PLANK", "Penguins Learning Ancient Ninja Karate"),
            ("QUACK", "Quantum Unicorns And Cat Kangaroos"),
            ("FIZZ", "Frogs In Zany Zigzags"),
            ("TWIG", "Tigers Wearing Interesting Glasses"),
            ("BOOP", "Bouncing Octopuses On Pogo-sticks"),
            ("ZAP", "Zany Astronauts Partying"),
            ("NIFTY", "Ninjas Inventing Flying Toy Yaks"),
            ("WOBBLE", "Wombats Observing Bouncing Blue Elephants"),
            ("SPORK", "Spoons Playing Organ Recitals Kindly"),
            ("JOLT", "Jellyfish Operating Light Telephones"),
            ("DINKY", "Ducks In Neon Knit Yarmulkes"),
            ("PLOP", "Platypuses Loving Outstanding Pancakes"),
            ("KABOOM", "Kangaroos And Baboons Operating On Mars")
        ]

        for acronym, definition in acronym_data:
            acronym_tree.insert("", tb.END, values=(acronym, definition))

        acronym_scrollbar = tb.Scrollbar(acronyms_frame, orient="vertical", command=acronym_tree.yview)
        acronym_tree.configure(yscroll=acronym_scrollbar.set)
        acronym_scrollbar.pack(side="right", fill="y")
        acronym_tree.pack(side="left", fill="both", expand=True)

        tb.Button(self, text="← Main Menu", command=lambda: self.controller.show_page("MainMenuPage")).pack(side="bottom", pady=15)

class SettingsPage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        
    def create_widgets(self):
        tb.Label(self, text="Application Settings", font=('Helvetica', 16)).pack(pady=20)
        theme_frame = tb.Frame(self)
        theme_frame.pack(pady=10)
        light_label = tb.Label(theme_frame, text="Light", font=('Helvetica', 12))
        light_label.pack(side="left", padx=(0, 10))
        
        # Current theme status
        current_theme = self.controller.style.theme.name
        self.is_dark_mode = tb.BooleanVar(value=(current_theme == "darkly"))
        
        # Theme toggle switch (dark/light)
        switch = tb.Checkbutton(
            theme_frame,
            bootstyle="round-toggle",
            variable=self.is_dark_mode,
            command=self.toggle_theme
        )
        switch.pack(side="left")
        
        # Add icon/label for dark mode
        dark_label = tb.Label(theme_frame, text="Dark", font=('Helvetica', 12))
        dark_label.pack(side="left", padx=(10, 0))
        
        tb.Button(self, text="← Main Menu", command=lambda: self.controller.show_page("MainMenuPage")).pack(side="bottom", pady=15)

    def toggle_theme(self):
        self.controller.toggle_theme()

if __name__ == "__main__":
    app = JournalApp()
    app.mainloop()