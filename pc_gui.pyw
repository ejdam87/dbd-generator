import tkinter as tk
import tkinter.font as tk_font
import dbd
import image_handler as imh
from typing import List

KILLER_LIST_PATH = "killers\\killers.txt"
SURVIVOR_LIST_PATH = "survivors\\survivors.txt"
KILLER_PERKS_PATH = "killer_perks\\killer_perks.txt"
SURVIVOR_PERKS_PATH = "survivor_perks\\survivor_perks.txt"

KILLER_LIST_IMAGES = "killers"
KILLER_PERKS_IMAGES = "killer_perks"
SURVIVOR_LIST_IMAGES = "survivors"
SURVIVOR_PERKS_IMAGES = "survivor_perks"

ICON_PATH = "icon.ico"

BACKGROUND_COLOR = "#000000"
FOREGROUND_COLOR = "#FFFFFF"
ACTIVE_BG_COLOR = "#545753"
ACTIVE_FG_COLOR = "#00FF00"

IM_WIDTH = 80
IM_HEIGHT = 80

FONT = ("Helvetica", 12)

class Window:

    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.geometry("800x450")
        self.root.title("DBD character / build generator")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.iconbitmap(ICON_PATH)

        im = imh.load_image("question_mark.png")
        self.question_mark_image = imh.get_tk_image(imh.resize_image((IM_WIDTH, IM_HEIGHT), im))
        
        columns = 4
        rows = 9

        self.kperk_pool = dbd.load_data(KILLER_PERKS_PATH)
        self.sperk_pool = dbd.load_data(SURVIVOR_PERKS_PATH)
        self.killer_pool = dbd.load_data(KILLER_LIST_PATH)
        self.survivor_pool = dbd.load_data(SURVIVOR_LIST_PATH)

        self.killer_images = dict(zip(self.killer_pool, imh.get_images(KILLER_LIST_IMAGES, self.killer_pool)))
        self.killer_perks_images = dict(zip(self.kperk_pool, imh.get_images(KILLER_PERKS_IMAGES, self.kperk_pool)))
        self.survivor_images = dict(zip(self.survivor_pool, imh.get_images(SURVIVOR_LIST_IMAGES, self.survivor_pool)))
        self.survivor_perks_images = dict(zip(self.sperk_pool, imh.get_images(SURVIVOR_PERKS_IMAGES, self.sperk_pool)))

        self.character_picked = tk.StringVar()
        self.character_type = tk.StringVar()
        self.perks = [tk.StringVar() for _ in range(4)]

        # --- Widgets creation

        self.heading = tk.Label(self.root,
                                text="Dead by Daylight generator",
                                bg=BACKGROUND_COLOR,
                                fg=FOREGROUND_COLOR,
                                font=FONT)

        self.killer_type = tk.Radiobutton(self.root,
                                          text="killer",
                                          variable=self.character_type,
                                          value="killer",
                                          indicator=0,
                                          bg=BACKGROUND_COLOR,
                                          fg=FOREGROUND_COLOR,
                                          selectcolor=ACTIVE_BG_COLOR,
                                          font=FONT)

        self.survivor_type = tk.Radiobutton(self.root,
                                            text="survivor",
                                            variable=self.character_type,
                                            value="survivor",
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
                                            command=lambda : self.configure_pool("perk"),
                                            bg=BACKGROUND_COLOR,
                                            fg=FOREGROUND_COLOR,
                                            font=FONT)

        self.character_config_button = tk.Button(self.root,
                                                 text="Configure character pool",
                                                 command=lambda : self.configure_pool("character"),
                                                 bg=BACKGROUND_COLOR,
                                                 fg=FOREGROUND_COLOR,
                                                 font=FONT)

        self.restore_pools_button = tk.Button(self.root,
                                              text="Restore pools",
                                              command=self.restore_pools,
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

        self.character_image_label = tk.Label(self.root, image=self.question_mark_image, bg=BACKGROUND_COLOR)

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
                                             image=self.question_mark_image,
                                             bg=BACKGROUND_COLOR)

                                    for i in range(4)

                                 ]

        # ---

        # --- Widget placement
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

        self.perk_config_button.grid(row=8, column=3, pady=10)
        self.character_config_button.grid(row=8, column=2, pady=10)
        self.restore_pools_button.grid(row=8, column=1, pady=10)
        self.info_button.grid(row=8, column=0, pady=10)
        # ---

    def show_character(self) -> None:

        if self.character_type.get() == "killer":

            killer = dbd.get_character(self.killer_pool)
            self.character_picked.set(killer)
            self.character_image_label["image"] = self.killer_images[killer]
            
        elif self.character_type.get() == "survivor":

            survivor = dbd.get_character(self.survivor_pool)
            self.character_picked.set(survivor)
            self.character_image_label["image"] = self.survivor_images[survivor]

    def show_build(self) -> None:

        build = []

        if self.character_type.get() == "killer":
            build = dbd.get_build(self.kperk_pool)

        elif self.character_type.get() == "survivor":
            build = dbd.get_build(self.sperk_pool)

        if build != []:

            for i, perk in enumerate(self.perks):

                perk.set(build[i])

                if self.character_type.get() == "killer":
                    self.perk_image_labels[i]["image"] = self.killer_perks_images[build[i]]
                else:
                    self.perk_image_labels[i]["image"] = self.survivor_perks_images[build[i]]


    def configure_pool(self, _type: str) -> None:
        
        config_window = tk.Toplevel(self.root, bg=BACKGROUND_COLOR)
        config_window.title("Configure perk pool")
        config_window.iconbitmap(ICON_PATH)

        config_frame = tk.Frame(config_window)
        config_canvas = tk.Canvas(config_frame)
        config_scrollbar = tk.Scrollbar(config_frame, orient="vertical", command=config_canvas.yview)

        config_window.grid_columnconfigure(0, weight=1)
        config_window.grid_columnconfigure(1, weight=1)
        config_window.grid_rowconfigure(0, weight=1)
        config_window.grid_rowconfigure(1, weight=1)
        config_window.grid_rowconfigure(2, weight=1)

        config_frame.grid_columnconfigure(0, weight=1)
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_rowconfigure(0, weight=1)

        pool_widgets = []
        control_variables = []

        item_frame = tk.Frame(config_frame)
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
                                  command=lambda: self._save_pool(pool_widgets),
                                  bg=BACKGROUND_COLOR,
                                  fg=FOREGROUND_COLOR,
                                  font=FONT)


        self._load_pool(item_frame, _type, pool_widgets, control_variables)

        config_canvas.create_window(0, 0, window=item_frame)
        item_frame.update_idletasks()

        config_canvas.configure(scrollregion=config_canvas.bbox('all'), 
                                yscrollcommand=config_scrollbar.set)
        
        # --- Grid onto toplevel
        config_frame.grid(row=0, column=0, sticky="NS", rowspan=3)
        check_button.grid(row=0, column=1)
        uncheck_button.grid(row=1, column=1)
        save_button.grid(row=2, column=1)
        # ---

        # --- Grid onto config_frame
        config_canvas.grid(row=0, column=0, sticky="NEWS")
        config_scrollbar.grid(row=0, column=1, sticky="NES")
        # ---

    def _load_pool(self,
                   window: tk.Frame,
                   _type: str,
                   widget_list: List[tk.Checkbutton],
                   control_list: List[tk.IntVar]) -> None:

        if _type == "perk":

            if self.character_type.get() == "survivor":

                control_list = [tk.IntVar() for _ in range(len(self.sperk_pool))]
                self._create_config_widgets(window,
                                            self.sperk_pool,
                                            widget_list,
                                            control_list,
                                            self.survivor_perks_images)


            elif self.character_type.get() == "killer":

                control_list = [tk.IntVar() for _ in range(len(self.kperk_pool))]
                self._create_config_widgets(window,
                                            self.kperk_pool,
                                            widget_list,
                                            control_list,
                                            self.killer_perks_images)

        elif _type == "character":

            if self.character_type.get() == "survivor":

                control_list = [tk.IntVar() for _ in range(len(self.survivor_pool))]
                self._create_config_widgets(window,
                                            self.survivor_pool,
                                            widget_list,
                                            control_list,
                                            self.survivor_images)

            elif self.character_type.get() == "killer":

                control_list = [tk.IntVar() for _ in range(len(self.killer_pool))]
                self._create_config_widgets(window,
                                            self.killer_pool,
                                            widget_list,
                                            control_list,
                                            self.killer_images)

    def restore_pools(self) -> None:
        
        restore_window = tk.Toplevel(self.root,
                                     bg=BACKGROUND_COLOR)

        restore_window.iconbitmap(ICON_PATH)

        restore_window.title("Restore pools")

        tk.Label(restore_window, text="Which pool would you like to reset?",
                 width=50,
                 bg=BACKGROUND_COLOR,
                 fg=FOREGROUND_COLOR).pack(pady=5)

        tk.Button(restore_window,
                  text="Killer pool",
                  command=self._restore_killer,
                  bg=BACKGROUND_COLOR,
                  fg=FOREGROUND_COLOR).pack(pady=5)

        tk.Button(restore_window,
                  text="Survivor pool",
                  command=self._restore_survivor,
                  bg=BACKGROUND_COLOR,
                  fg=FOREGROUND_COLOR).pack(pady=5)

        tk.Button(restore_window,
                  text="Killer perk pool",
                  command=self._restore_kperks,
                  bg=BACKGROUND_COLOR,
                  fg=FOREGROUND_COLOR).pack(pady=5)

        tk.Button(restore_window,
                  text="Survivor perk pool",
                  command=self._restore_sperks,
                  bg=BACKGROUND_COLOR,
                  fg=FOREGROUND_COLOR).pack(pady=5)


    def _save_pool(self,
                   pool: List[str],
                   checkbuttons: List[tk.Checkbutton],
                   control_variables: List[tk.IntVar],
                   _type: str) -> None:
        
        pass

    def _check_all(self, checkbuttons: List[tk.Checkbutton]) -> None:
        
        for check in checkbuttons:
            check.select()

    def _uncheck_all(self, checkbuttons: List[tk.Checkbutton]) -> None:

        for check in checkbuttons:
            check.deselect()

    def _restore_killer(self) -> None:

        self.killer_pool = dbd.load_data(KILLER_LIST_PATH)

    def _restore_survivor(self) -> None:

        self.survivor_pool = dbd.load_data(SURVIVOR_LIST_PATH)

    def _restore_kperks(self) -> None:

        self.kperk_pool = dbd.load_data(KILLER_PERKS_PATH)

    def _restore_sperks(self) -> None:

        self.sperk_pool = dbd.load_data(SURVIVOR_PERKS_PATH)

    def _create_config_widgets(self,
                        window: tk.Frame,
                        pool: List[str],
                        widget_list: List[tk.Checkbutton],
                        control_list: List[tk.IntVar],
                        image_list: List["ImageTk.PhotoImage"]):

        for i, item in enumerate(pool):

            window.grid_rowconfigure(i, weight=1)
            button = tk.Checkbutton(window, text=item, variable=control_list[i])
            button.grid(row=i, column=0, sticky="NEWS")
            tk.Label(window, image=image_list[item]).grid(row=i, column=1)

            widget_list.append(button)

    def show_info(self) -> None:

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
