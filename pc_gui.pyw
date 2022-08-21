import tkinter as tk
import tkinter.font as tk_font
import dbd
import image_handler as imh

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
                                            command=self.configure_perk_pool,
                                            bg=BACKGROUND_COLOR,
                                            fg=FOREGROUND_COLOR,
                                            font=FONT)

        self.character_config_button = tk.Button(self.root,
                                                 text="Configure character pool",
                                                 command=self.configure_character_pool,
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


    def configure_perk_pool(self) -> None:
        
        config_window = tk.Toplevel(self.root, bg=BACKGROUND_COLOR)
        config_window.title("Configure perk pool")
        config_window.iconbitmap(ICON_PATH)

        optionbox = tk.Listbox(config_window,
                               bg=BACKGROUND_COLOR,
                               fg=FOREGROUND_COLOR,
                               width=40,
                               height=20,
                               selectbackground=ACTIVE_BG_COLOR,
                               font=FONT)

        delete_button = tk.Button(config_window,
                                  text="Delete selected",
                                  command=lambda: self._delete_perk_from_pool(optionbox),
                                  bg=BACKGROUND_COLOR,
                                  fg=FOREGROUND_COLOR,
                                  font=FONT)

        optionbox.pack()
        delete_button.pack(padx=10, pady=20)

        self._show_pool(optionbox, "perk")

    def configure_character_pool(self) -> None:
        
        config_window = tk.Toplevel(self.root, bg=BACKGROUND_COLOR)
        config_window.title("Configure character pool")
        config_window.iconbitmap(ICON_PATH)

        optionbox = tk.Listbox(config_window,
                               bg=BACKGROUND_COLOR,
                               fg=FOREGROUND_COLOR,
                               width=40,
                               height=20,
                               selectbackground=ACTIVE_BG_COLOR,
                               font=FONT)

        delete_button = tk.Button(config_window,
                                  text="Delete selected",
                                  command=lambda: self._delete_character_from_pool(optionbox),
                                  bg=BACKGROUND_COLOR,
                                  fg=FOREGROUND_COLOR,
                                  font=FONT)

        optionbox.pack()
        delete_button.pack(padx=10, pady=20)

        self._show_pool(optionbox, "character")

    def _show_pool(self, optionbox: tk.Listbox, _type: str) -> None:

        if _type == "perk":

            if self.character_type.get() == "survivor":

                for perk in self.sperk_pool:
                    optionbox.insert(tk.END, perk)

            elif self.character_type.get() == "killer":

                for perk in self.kperk_pool:
                    optionbox.insert(tk.END, perk)

        elif _type == "character":

            if self.character_type.get() == "survivor":

                for char in self.survivor_pool:
                    optionbox.insert(tk.END, char)

            elif self.character_type.get() == "killer":

                for char in self.killer_pool:
                    optionbox.insert(tk.END, char)

    def _delete_perk_from_pool(self, optionbox: tk.Listbox) -> None:
        
        selected = optionbox.curselection()
        optionbox.delete(selected[0])

        if self.character_type.get() == "survivor":
            self.sperk_pool.pop(selected[0])
        elif self.character_type.get() == "killer":
            self.kperk_pool.pop(selected[0])

    def _delete_character_from_pool(self, optionbox: tk.Listbox) -> None:

        selected = optionbox.curselection()
        optionbox.delete(selected[0])

        if self.character_type.get() == "survivor":
            self.survivor_pool.pop(selected[0])
        elif self.character_type.get() == "killer":
            self.killer_pool.pop(selected[0])

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


    def _restore_killer(self) -> None:

        self.killer_pool = dbd.load_data(KILLER_LIST_PATH)

    def _restore_survivor(self) -> None:

        self.survivor_pool = dbd.load_data(SURVIVOR_LIST_PATH)

    def _restore_kperks(self) -> None:

        self.kperk_pool = dbd.load_data(KILLER_PERKS_PATH)

    def _restore_sperks(self) -> None:

        self.sperk_pool = dbd.load_data(SURVIVOR_PERKS_PATH)

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
