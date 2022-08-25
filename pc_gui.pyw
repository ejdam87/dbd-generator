import tkinter as tk
import tkinter.font as tk_font
import dbd
from char_types import CharacterTypes, ItemTypes
import image_handler as imh
from typing import List, Tuple, Optional


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
IM_WIDTH = 80
IM_HEIGHT = 80

BIG_IM_WIDTH = 150
BIG_IM_HEIGHT = 150

BIG_SIZE = (BIG_IM_WIDTH, BIG_IM_HEIGHT)
SMALL_SIZE = (IM_WIDTH, IM_HEIGHT)
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
        self.qm_im = imh.load_image("question_mark.png")
        self.big_qm = imh.get_tk_image(imh.resize_image(BIG_SIZE, self.qm_im))
        self.small_qm = imh.get_tk_image(imh.resize_image(SMALL_SIZE, self.qm_im))

        self.kperk_pool = dbd.load_data(KILLER_PERKS_PATH)
        self.sperk_pool = dbd.load_data(SURVIVOR_PERKS_PATH)
        self.killer_pool = dbd.load_data(KILLER_LIST_PATH)
        self.survivor_pool = dbd.load_data(SURVIVOR_LIST_PATH)

        self.base_kperk_pool = self.kperk_pool[:]
        self.base_sperk_pool = self.sperk_pool[:]
        self.base_killer_pool = self.killer_pool[:]
        self.base_survivor_pool = self.survivor_pool[:]

        self.big_ims = {}
        self.small_ims = {}

        zip_pool = []
        for item_pool, path in [(self.sperk_pool, SURVIVOR_PERKS_IMAGES),
                     (self.survivor_pool, SURVIVOR_LIST_IMAGES),
                     (self.killer_pool, KILLER_LIST_IMAGES),
                     (self.kperk_pool, KILLER_PERKS_IMAGES)]:

            zip_pool += list(zip(item_pool, imh.get_images(path, item_pool)))


        self.images = dict(zip_pool)
        # ---

        # --- Global stringVars
        self.status = tk.StringVar()
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

        self.character_image_label = tk.Label(self.root,
                                              image=self.big_qm,
                                              bg=BACKGROUND_COLOR)

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
                                             image=self.small_qm,
                                             bg=BACKGROUND_COLOR)

                                    for i in range(4)

                                 ]

        self.status_bar = tk.Label(self.root,
                                   textvariable=self.status,
                                   bg=BACKGROUND_COLOR,
                                   fg=FOREGROUND_COLOR,
                                   font=FONT)
        # ---

        # --- Widget placement
        columns = 4
        rows = 10

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
            label.grid(row=7, column=i, pady=10)

        self.perk_config_button.grid(row=8, column=2, pady=10, columnspan=2)
        self.character_config_button.grid(row=8, column=1, pady=10)
        self.info_button.grid(row=8, column=0, pady=10)
        self.status_bar.grid(row=9, column=0, pady=10, columnspan=4)
        # ---

    def show_character(self) -> None:
        """
        Method to show selected character
        """

        if not self._check_picked():
            return

        if self.character_type.get() == CharacterTypes.KILLER:

            killer = dbd.get_character(self.killer_pool)
            self.character_picked.set(killer)

            if killer not in self.big_ims:
                self.big_ims[killer] = imh.get_tk_image(imh.resize_image(BIG_SIZE, self.images[killer]))

            self.character_image_label["image"] = self.big_ims[killer]
            
        elif self.character_type.get() == CharacterTypes.SURVIVOR:

            survivor = dbd.get_character(self.survivor_pool)

            if survivor not in self.big_ims:
                self.big_ims[survivor] = imh.get_tk_image(imh.resize_image(BIG_SIZE, self.images[survivor]))

            self.character_picked.set(survivor)
            self.character_image_label["image"] = self.big_ims[survivor]

    def show_build(self) -> None:
        """
        Method to show selected perks
        """

        if not self._check_picked():
            return

        build = []

        if self.character_type.get() == CharacterTypes.KILLER:
            build = dbd.get_build(self.kperk_pool)

        elif self.character_type.get() == CharacterTypes.SURVIVOR:
            build = dbd.get_build(self.sperk_pool)


        for i, perk in enumerate(self.perks):

            if i >= len(build):
                self.perk_image_labels[i]["image"] = self.small_qm
                perk.set("")
                continue

            perk.set(build[i])

            if build[i] not in self.small_ims:

                if self.character_type.get() == CharacterTypes.KILLER:
                    self.small_ims[build[i]] = imh.get_tk_image(imh.resize_image(SMALL_SIZE, self.images[build[i]]))
                else:
                    self.small_ims[build[i]] = imh.get_tk_image(imh.resize_image(SMALL_SIZE, self.images[build[i]]))

            self.perk_image_labels[i]["image"] = self.small_ims[build[i]]


    def configure_pool(self, _type: str) -> None:
        """
        Method to handle all the pool configuration
        """

        if not self._check_picked():
            return

        pools = self._get_pools(_type)
        item_pool, base_pool = pools
        pool_widgets = []
        control_variables = [tk.IntVar() for _ in range(len(base_pool))]


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
                                    control_variables)

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
                        control_list: List[tk.IntVar]):
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

            if item not in self.small_ims:
                self.small_ims[item] = imh.get_tk_image(imh.resize_image(SMALL_SIZE, self.images[item]))

            tk.Label(window,
                     image=self.small_ims[item],
                     bg=BACKGROUND_COLOR).grid(row=i, column=1)

            widget_list.append(button)

    def _save_pool(self,
                   checkbuttons: List[tk.Checkbutton],
                   control_variables: List[tk.IntVar],
                   _type: int) -> None:
        """
        Method to save checkbutton values to pool
        """

        item_pool = self._get_pools(_type)[0]

        for i, check in enumerate(checkbuttons):

            if control_variables[i].get() == 0 and check.cget("text") in item_pool:
                item_pool.remove(check.cget("text"))
            elif control_variables[i].get() == 1 and check.cget("text") not in item_pool:
                item_pool.append(check.cget("text"))


    def _get_pools(self, _type: int) -> Optional[ Tuple[ List[str], List[str] ] ]:
        """
        Method to get image pool, current selected pool and base pool based on type of item
        """

        if _type == ItemTypes.PERK.value:
            if self.character_type.get() == CharacterTypes.SURVIVOR:
                return self.sperk_pool, self.base_sperk_pool

            if self.character_type.get() == CharacterTypes.KILLER:
                return self.kperk_pool, self.base_kperk_pool

        if _type == ItemTypes.CHARACTER.value:
            if self.character_type.get() == CharacterTypes.SURVIVOR:
                return self.survivor_pool, self.base_survivor_pool

            if self.character_type.get()== CharacterTypes.KILLER:
                return self.killer_pool, self.base_killer_pool

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

    def _check_picked(self) -> bool:

        if self.character_type.get() == 0:
            self.status.set("You have to pick character (e.g. killer / survivor)")
            return False

        self.status.set("")
        return True

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
