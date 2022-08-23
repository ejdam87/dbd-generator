import tkinter as tk
import tkinter.font as tk_font
import dbd
from char_types import CharacterTypes, ItemTypes
import image_handler as imh
from typing import List, Tuple


# --- Paths to data-files
KILLER_LIST_PATH = "killers\\killers.txt"
SURVIVOR_LIST_PATH = "survivors\\survivors.txt"
KILLER_PERKS_PATH = "killer_perks\\killer_perks.txt"
SURVIVOR_PERKS_PATH = "survivor_perks\\survivor_perks.txt"
# ---

# --- Paths to folders with images
KILLER_LIST_IMAGES = "killers"
KILLER_PERKS_IMAGES = "killer_perks"
SURVIVOR_LIST_IMAGES = "survivors"
SURVIVOR_PERKS_IMAGES = "survivor_perks"
# ---

ICON_PATH = "icon.ico"

# --- Colors
BACKGROUND_COLOR = "#000000"
FOREGROUND_COLOR = "#FFFFFF"
ACTIVE_BG_COLOR = "#545753"
ACTIVE_FG_COLOR = "#00FF00"
# ---

# --- Image sizes
PERK_IM_WIDTH = 80
PERK_IM_HEIGHT = 80

CHAR_IM_WIDTH = 150
CHAR_IM_HEIGHT = 150
# ---

FONT = ("Helvetica", 12)
HEADING = ("Helvetica", 18)

# --- Size of the window at startup
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
# ---

class Window:

    def __init__(self) -> None:

        # --- Configuration of main window
        self.root = tk.Tk()
        self.root.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
        self.root.title("DBD character / build generator")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.iconbitmap(ICON_PATH)
        # ---

        # --- Loading assets
        im = imh.load_image("question_mark.png")
        self.small_qm_image = imh.get_tk_image(
                                               imh.resize_image((PERK_IM_WIDTH, PERK_IM_HEIGHT),
                                               im)
                                              )

        self.big_qm_image = imh.get_tk_image(
                                             imh.resize_image((CHAR_IM_WIDTH, CHAR_IM_HEIGHT),
                                             im)
                                            )

        self.kperk_pool = dbd.load_data(KILLER_PERKS_PATH)
        self.sperk_pool = dbd.load_data(SURVIVOR_PERKS_PATH)
        self.killer_pool = dbd.load_data(KILLER_LIST_PATH)
        self.survivor_pool = dbd.load_data(SURVIVOR_LIST_PATH)

        self.base_kperk_pool = self.kperk_pool[:]
        self.base_sperk_pool = self.sperk_pool[:]
        self.base_killer_pool = self.killer_pool[:]
        self.base_survivor_pool = self.survivor_pool[:]

        self.killer_images = dict(
                                  zip(
                                      self.killer_pool,
                                      imh.get_images(
                                                     KILLER_LIST_IMAGES,
                                                     self.killer_pool,
                                                     (CHAR_IM_WIDTH, CHAR_IM_HEIGHT)
                                                    )
                                     )
                                 )

        self.killer_perks_images = dict(
                                        zip(
                                            self.kperk_pool,
                                            imh.get_images(
                                                           KILLER_PERKS_IMAGES,
                                                           self.kperk_pool,
                                                           (PERK_IM_WIDTH, PERK_IM_HEIGHT)
                                                          )
                                           )
                                       )

        self.survivor_images = dict(
                                    zip(
                                        self.survivor_pool,
                                        imh.get_images(
                                                       SURVIVOR_LIST_IMAGES,
                                                       self.survivor_pool,
                                                       (CHAR_IM_WIDTH, CHAR_IM_HEIGHT)
                                                      )
                                       )
                                   )

        self.survivor_perks_images = dict(
                                          zip(
                                              self.sperk_pool,
                                              imh.get_images(
                                                             SURVIVOR_PERKS_IMAGES,
                                                             self.sperk_pool,
                                                             (PERK_IM_WIDTH, PERK_IM_HEIGHT)
                                                            )
                                             )
                                         )
        # ---

        # --- Global stringVars
        self.character_picked = tk.StringVar()  # Picked character name
        self.character_type = tk.IntVar()    # Killer / Survivor
        self.perks = [tk.StringVar() for _ in range(4)] # Picked perks

        # --- Widgets creation
        self.heading = tk.Label(self.root,
                                text="Dead by Daylight generator",
                                bg=BACKGROUND_COLOR,
                                fg=FOREGROUND_COLOR,
                                font=HEADING)

        self.killer_type = tk.Radiobutton(self.root,
                                          text="killer",
                                          variable=self.character_type,
                                          value=CharacterTypes.KILLER.value,
                                          indicator=0,
                                          bg=BACKGROUND_COLOR,
                                          fg=FOREGROUND_COLOR,
                                          selectcolor=ACTIVE_BG_COLOR,
                                          font=FONT)

        self.survivor_type = tk.Radiobutton(self.root,
                                            text="survivor",
                                            variable=self.character_type,
                                            value=CharacterTypes.SURVIVOR.value,
                                            indicator=0,
                                            bg=BACKGROUND_COLOR,
                                            fg=FOREGROUND_COLOR,
                                            selectcolor=ACTIVE_BG_COLOR,
                                            font=FONT)

        self.character_button = tk.Button(self.root,
                                          text="Generate character",
                                          command=self.show_character,
                                          bg=BACKGROUND_COLOR,
                                          fg=FOREGROUND_COLOR,
                                          font=FONT)

        self.build_button = tk.Button(self.root,
                                      text="Generate build",
                                      command=self.show_build,
                                      bg=BACKGROUND_COLOR,
                                      fg=FOREGROUND_COLOR,
                                      font=FONT)

        self.perk_config_button = tk.Button(self.root,
                                            text="Configure perk pool",
                                            command=lambda : self.configure_pool(ItemTypes.PERK.value),
                                            bg=BACKGROUND_COLOR,
                                            fg=FOREGROUND_COLOR,
                                            font=FONT)

        self.character_config_button = tk.Button(self.root,
                                                 text="Configure character pool",
                                                 command=lambda : self.configure_pool(ItemTypes.CHARACTER.value),
                                                 bg=BACKGROUND_COLOR,
                                                 fg=FOREGROUND_COLOR,
                                                 font=FONT)

        self.info_button = tk.Button(self.root,
                                     text="info",
                                     command=self.show_info,
                                     bg=BACKGROUND_COLOR,
                                     fg=FOREGROUND_COLOR,
                                     font=FONT)

        self.character_label = tk.Label(self.root,
                                        textvariable=self.character_picked,
                                        bg=BACKGROUND_COLOR,
                                        fg=FOREGROUND_COLOR,
                                        font=FONT)

        self.character_image_label = tk.Label(self.root, image=self.big_qm_image, bg=BACKGROUND_COLOR)

        self.perk_labels = [

                        tk.Label(self.root,
                                 textvariable=self.perks[i],
                                 bg=BACKGROUND_COLOR,
                                 fg=FOREGROUND_COLOR,
                                 font=FONT)

                        for i in range(4)

                           ]

        self.perk_image_labels = [
                                    tk.Label(self.root, 
                                             image=self.small_qm_image,
                                             bg=BACKGROUND_COLOR)

                                    for i in range(4)

                                 ]

        # ---

        # --- Widget placement
        columns = 4
        rows = 9

        for i in range(columns):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            self.root.grid_rowconfigure(i, weight=1)

        self.heading.grid(row=0, column=0, columnspan=4, pady=10)
        self.killer_type.grid(row=1, column=0, pady=10)
        self.survivor_type.grid(row=1, column=3, pady=10)
        self.character_button.grid(row=2, column=0, columnspan=4, pady=10)
        self.build_button.grid(row=3, column=0, columnspan=4, pady=10)
        self.character_image_label.grid(row=4, column=0, columnspan=4, pady=10)
        self.character_label.grid(row=5, column=0, columnspan=4, pady=10)

        for i, im_label in enumerate(self.perk_image_labels):
            im_label.grid(row=6, column=i)
        for i, label in enumerate(self.perk_labels):
            label.grid(row=7, column=i)

        self.perk_config_button.grid(row=8, column=2, pady=10, columnspan=2)
        self.character_config_button.grid(row=8, column=1, pady=10)
        self.info_button.grid(row=8, column=0, pady=10)
        # ---

    def show_character(self) -> None:
        """
        Method to show selected character
        """

        if self.character_type.get() == CharacterTypes.KILLER:

            killer = dbd.get_character(self.killer_pool)
            self.character_picked.set(killer)
            self.character_image_label["image"] = self.killer_images[killer]
            
        elif self.character_type.get() == CharacterTypes.SURVIVOR:

            survivor = dbd.get_character(self.survivor_pool)
            self.character_picked.set(survivor)
            self.character_image_label["image"] = self.survivor_images[survivor]

    def show_build(self) -> None:
        """
        Method to show selected perks
        """

        build = []

        if self.character_type.get() == CharacterTypes.KILLER:
            build = dbd.get_build(self.kperk_pool)

        elif self.character_type.get() == CharacterTypes.SURVIVOR:
            build = dbd.get_build(self.sperk_pool)

        if build != []:

            for i, perk in enumerate(self.perks):

                perk.set(build[i])

                if self.character_type.get() == CharacterTypes.KILLER:
                    self.perk_image_labels[i]["image"] = self.killer_perks_images[build[i]]
                else:
                    self.perk_image_labels[i]["image"] = self.survivor_perks_images[build[i]]


    def configure_pool(self, _type: str) -> None:
        """
        Method to handle all the pool configuration
        """

        config_window = tk.Toplevel(self.root, bg=BACKGROUND_COLOR)
        config_window.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
        config_window.title("Configure perk pool")
        config_window.iconbitmap(ICON_PATH)

        config_frame = tk.Frame(config_window,
                                bg=BACKGROUND_COLOR,
                                bd=0)

        config_canvas = tk.Canvas(config_frame,
                                  bg=BACKGROUND_COLOR,
                                  borderwidth=0,
                                  highlightthickness=0)

        config_scrollbar = tk.Scrollbar(config_frame,
                                        orient="vertical",
                                        command=config_canvas.yview)

        config_window.grid_columnconfigure(0, weight=1)
        config_window.grid_columnconfigure(1, weight=1)
        config_window.grid_rowconfigure(0, weight=1)
        config_window.grid_rowconfigure(1, weight=1)
        config_window.grid_rowconfigure(2, weight=1)

        config_frame.grid_columnconfigure(0, weight=1)
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_rowconfigure(0, weight=1)

        image_pool, item_pool, base_pool = self._get_pools(_type)
        pool_widgets = []
        control_variables = [tk.IntVar() for _ in range(len(base_pool))]

        item_frame = tk.Frame(config_frame,
                              bg=BACKGROUND_COLOR)

        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=1)

        check_button = tk.Button(config_window,
                                  text="Check all",
                                  command=lambda: self._check_all(pool_widgets),
                                  bg=BACKGROUND_COLOR,
                                  fg=FOREGROUND_COLOR,
                                  font=FONT)

        uncheck_button = tk.Button(config_window,
                                  text="Un-check all",
                                  command=lambda: self._uncheck_all(pool_widgets),
                                  bg=BACKGROUND_COLOR,
                                  fg=FOREGROUND_COLOR,
                                  font=FONT)

        save_button = tk.Button(config_window,
                                  text="Save pool",
                                  command=lambda: self._save_pool(pool_widgets, control_variables, _type),
                                  bg=BACKGROUND_COLOR,
                                  fg=FOREGROUND_COLOR,
                                  font=FONT)

        self._create_config_widgets(item_frame,
                                    base_pool,
                                    item_pool,
                                    pool_widgets,
                                    control_variables,
                                    image_pool)

        config_canvas.create_window(0, 0, window=item_frame)
        item_frame.update_idletasks()

        config_canvas.configure(scrollregion=config_canvas.bbox('all'), 
                                yscrollcommand=config_scrollbar.set)
        
        # --- Grid onto toplevel
        config_frame.grid(row=0, column=1, sticky="NES", rowspan=3, pady=10)
        check_button.grid(row=0, column=0)
        uncheck_button.grid(row=1, column=0)
        save_button.grid(row=2, column=0)
        # ---

        # --- Grid onto config_frame
        config_canvas.grid(row=0, column=0, sticky="NS")
        config_scrollbar.grid(row=0, column=1, sticky="NS")
        # ---

        config_canvas.bind_all("<MouseWheel>", lambda e: self._wheel_scroll(config_canvas, e))

    def _create_config_widgets(self,
                        window: tk.Frame,
                        base_pool: List[str],
                        pool: List[str],
                        widget_list: List[tk.Checkbutton],
                        control_list: List[tk.IntVar],
                        image_list: List["ImageTk.PhotoImage"]):
        """
        Method to list item checkboxes with images
        """

        for i, item in enumerate(base_pool):

            window.grid_rowconfigure(i, weight=1)
            button = tk.Checkbutton(window,
                                    text=item,
                                    variable=control_list[i],
                                    bg=BACKGROUND_COLOR,
                                    fg=FOREGROUND_COLOR,
                                    activebackground=BACKGROUND_COLOR,
                                    activeforeground=FOREGROUND_COLOR,
                                    highlightcolor=BACKGROUND_COLOR,
                                    selectcolor=BACKGROUND_COLOR)

            if item in pool:
                button.select()

            button.grid(row=i, column=0, sticky="NEWS")

            tk.Label(window,
                     image=image_list[item],
                     bg=BACKGROUND_COLOR).grid(row=i, column=1)

            widget_list.append(button)

    def _save_pool(self,
                   checkbuttons: List[tk.Checkbutton],
                   control_variables: List[tk.IntVar],
                   _type: int) -> None:
        """
        Method to save checkbutton values to pool
        """

        item_pool = self._get_pools(_type)[1]

        for i, check in enumerate(checkbuttons):

            if control_variables[i].get() == 0 and check.cget("text") in item_pool:
                item_pool.remove(check.cget("text"))
            elif control_variables[i].get() == 1 and check.cget("text") not in item_pool:
                item_pool.append(check.cget("text"))


    def _get_pools(self, _type: int) -> Tuple[List[tk.PhotoImage], List[str], List[str]]:
        """
        Method to get image pool, current selected pool and base pool based on type of item
        """

        if _type == ItemTypes.PERK.value:
            if self.character_type.get() == CharacterTypes.SURVIVOR:
                return self.survivor_perks_images, self.sperk_pool, self.base_sperk_pool

            if self.character_type.get() == CharacterTypes.KILLER:
                return self.killer_perks_images, self.kperk_pool, self.base_kperk_pool

        if _type == ItemTypes.CHARACTER.value:
            if self.character_type.get() == CharacterTypes.SURVIVOR:
                return self.survivor_images, self.survivor_pool, self.base_survivor_pool

            if self.character_type.get()== CharacterTypes.KILLER:
                return self.killer_images, self.killer_pool, self.base_killer_pool

    def _check_all(self, checkbuttons: List[tk.Checkbutton]) -> None:
        
        for check in checkbuttons:
            check.select()

    def _uncheck_all(self, checkbuttons: List[tk.Checkbutton]) -> None:

        for check in checkbuttons:
            check.deselect()

    def _wheel_scroll(self, canvas: tk.Canvas, event: tk.Event) -> None:
        """
        Method for mousewheel scroll
        """

        canvas.yview_scroll( int( -1 * (event.delta / 120) ), "units")

    def show_info(self) -> None:
        """
        Method to show author information
        """

        info_window = tk.Toplevel(self.root,
                                     bg=BACKGROUND_COLOR)

        info_window.iconbitmap(ICON_PATH)

        info_window.title("Info")

        tk.Label(info_window,
                 text="This is a build / character generator for Dead by Daylight (DBD)",
                 bg=BACKGROUND_COLOR,
                 fg=FOREGROUND_COLOR).pack(pady=10)

        tk.Label(info_window,
                 text="Creator: Adam Dzadon",
                 bg=BACKGROUND_COLOR,
                 fg=FOREGROUND_COLOR).pack()

        tk.Label(info_window,
                 text="contact: adam.dzadon@gmail.com",
                 bg=BACKGROUND_COLOR,
                 fg=FOREGROUND_COLOR).pack()

        tk.Label(info_window,
                 text="github: https://github.com/ejdam87",
                 bg=BACKGROUND_COLOR,
                 fg=FOREGROUND_COLOR).pack(pady=10)


window = Window()
window.root.mainloop()
