# Load all necessary modules.
import tkinter as tk
import tk_helpers as tk_h
import turtle as tl
import pandas as pd
from random import choice
from time import sleep

# Handy global constants.
APP_TITLE = "Learn World Countries"
ROOT_WINDOW = "1280x720"  # reduce window to 720p after minimising
# https://commons.wikimedia.org/wiki/File:BlankMap-World-large.png
WORLD_COUNTRIES_BLANK_IMG = "./assets/BlankMap-World-large.gif"
#WORLD_COUNTRIES_NAMED_IMG = "./assets/NamedMap-World-large.gif"
WORLD_COUNTRIES_WIDTH = 4096
WORLD_COUNTRIES_HEIGHT = 2048
# https://www.clipartmax.com/middle/m2i8d3H7N4N4N4K9_pin-2-google-maps-pin-png
PIN_ICON = "./assets/map-pin-icon.gif"  # file exported to .gif
PIN_STARTING_POSITION = (-180.0,-120.0)
PIN_VERTICAL_SHIFT = 15  # so it points sharply onto the given country
FONT = "Arial"
FONT_SIZE = 20
MARKER_FONT = (FONT, FONT_SIZE, "normal")
GOOD_MARKER_FONT = (FONT, FONT_SIZE, "italic")
WRONG_MARKER_FONT = (FONT, FONT_SIZE, "bold")


class ControlsBar(tk.Frame):
    """Control buttons sub-frame."""

    def __init__(self, master, countries_map):
        super().__init__()

        self.master = master
        self.countries_map = countries_map

        # Quiz start button.
        self.start_bttn = tk.Button(
            master=self,
            text="Start",
            command=self.start_quiz
        )
        self.start_bttn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.gen_markers_bttn = tk.Button(
            master=self,
            text="Generate markers",
            command=self.master.countries_map.generate_markers
        )
        self.gen_markers_bttn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Toggle fullscreen mode button.
        self.fscreen_bttn = tk.Button(
            master=self,
            text="Fullscreen",
            command=lambda: tk_h.toggle_fscreen(master=root)
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # View application info button.
        self.about_bttn = tk.Button(
            master=self,
            text="About",
            #command=
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Exit app button.
        self.quit_bttn = tk.Button(
            master=self,
            text="Quit",
            command=root.destroy
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # User entry prompt.
        self.answer_sv = tk.StringVar()
        self.answer_entry = tk.Entry(
            master=self,
            textvariable=self.answer_sv,
            bd=3
        )
        self.answer_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        # Bind ENTER key w/ answer_entry.
        root.bind("<Return>", (lambda event: self.get_user_input()))

        # Entry confirmation button.
        self.answer_bttn = tk.Button(
            master=self,
            text="Answer",
            command=self.get_user_input
        )
        self.answer_bttn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.block_input()

    def start_quiz(self):
        self.master.countries_map.hide_markers()

        self.master.t_pin.showturtle()

        self.countries_map.indicate_on_map(
            country=self.master.data_handler.next_country,
            pin=self.master.t_pin
        )

        self.enable_input()

        self.start_bttn.config(state="disabled")

    def get_user_input(self):
        input_sv = self.answer_entry.get().title()
        self.clear_entry_field()

        country = self.master.data_handler.next_country
        self.master.data_handler.validate_answer(
            user_answer=input_sv,
            correct_answer=country
        )

        self.master.data_handler.fetch_next_country()
        country = self.master.data_handler.next_country
        self.master.countries_map.indicate_on_map(
            country=country,
            pin=self.master.t_pin
        )

    def clear_entry_field(self):
        self.answer_entry.delete(0, tk.END)

    def block_input(self):
        self.answer_entry.config(state="disabled")
        self.answer_bttn.config(state="disabled")

    def enable_input(self):
        self.answer_entry.config(state="normal")
        self.answer_bttn.config(state="normal")
        self.answer_entry.focus_set()


class StatusBar(tk.Frame):
    """Information and score sub-frame."""

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.known = tk.IntVar().get()
        self.all = len(self.master.data_handler.all_countries)

        self.status_lbl_txt = f"{self.known} / {self.all}"
        self.status_lbl = tk.Label(master=self, text=self.status_lbl_txt)
        self.status_lbl.pack(side=tk.RIGHT)

    def inc_known(self):
        self.known += 1

    def update_status(self):
        new_value = f"{self.known} / {self.all}"
        self.status_lbl.config(text=new_value)


class ScrolledCanvas(tl.ScrolledCanvas):
    """Handy scrolled background container."""

    def __init__(self, master):
        super().__init__(master)


class ScreenMap(tl.TurtleScreen):
    """Background graphics and turtle aggregator."""

    MARKERS = {
        "normal": 1,
        "small": 0.5,
        "tiny": 0.3
    }

    def __init__(self, master, canvas):
        super().__init__(canvas)

        self.master = master
        self.t_world_countries = None
        self.edu_markers = []

        # Determine screen dimensions.
        self.screensize(WORLD_COUNTRIES_WIDTH, WORLD_COUNTRIES_HEIGHT)

        self.addshape(WORLD_COUNTRIES_BLANK_IMG)  # load blank world map image
#        self.addshape(WORLD_COUNTRIES_NAMED_IMG)  # load named world map image
        self.addshape(PIN_ICON)  # load pin image

        self.set_up_blank()

        # Fetch and display mouce click coordinates.
        self.onclick(tk_h.get_tl_mouse_click_coords)

#    def set_up_named(self):
#        self.t_world_countries = tl.RawTurtle(
#            self,
#            shape=WORLD_COUNTRIES_NAMED_IMG
#        )

    def set_up_blank(self):
        self.t_world_countries = tl.RawTurtle(
            self,
            shape=WORLD_COUNTRIES_BLANK_IMG
        )

    def indicate_on_map(self, country, pin):
        country_data = self.master.data_handler.fetch_country_data(
            country=self.master.data_handler.next_country,
            data_frame=self.master.data_handler.coords_data
        )
        coords = self.master.data_handler.fetch_country_coords(data=country_data)
        self.master.t_pin.set_pin(position=coords, shift=PIN_VERTICAL_SHIFT)

    def generate_markers(self):
        self.master.controls_bar.gen_markers_bttn.config(state="disabled")
        self.master.controls_bar.start_bttn.config(state="disabled")
        all_countries = self.master.data_handler.all_countries
        for country in all_countries:
            new_marker_data = self.master.data_handler.fetch_country_data(
                country=country,
                data_frame=self.master.data_handler.coords_data
            )
            new_marker_name = country
            new_marker_position = self.master.data_handler.fetch_country_coords(
                data=new_marker_data
            )
            new_marker_marker = self.master.data_handler.fetch_country_marker(
                data=new_marker_data
            )
            new_marker = MarkCountry(
                master=self,
                name=new_marker_name,
                marker=new_marker_marker
            )
            new_marker.set_pin(position=new_marker_position, shift=0)
            new_marker.showturtle()
            self.edu_markers.append(new_marker)
        self.master.controls_bar.start_bttn.config(state="normal")

    def hide_markers(self):
        for marker in self.edu_markers:
            marker.hideturtle()


class TurtlePin(tl.RawTurtle):
    """Moving turtle country indicator."""

    def __init__(self, master):
        super().__init__(master)

        # Turtle pin setup.
        self.hideturtle()
        self.shape(PIN_ICON)
        self.speed("fastest")
        self.penup()
        self.set_pin(position=PIN_STARTING_POSITION, shift=PIN_VERTICAL_SHIFT)
        self.speed("slowest")

    def set_pin(self, position, shift):
        xcoor = position[0]
        ycoor = position[1] + shift
        self.goto(xcoor, ycoor)


class MarkGood(TurtlePin):
    """Known country marker."""

    def __init__(self, master, name, marker):
        super().__init__(master)

        self.master = master
        self.name = name
        self.marker = marker

        # Good answer marker setup.
        self.hideturtle()
        self.shape("circle")
        self.color("green")
        self.turtlesize(marker)
        self.speed("fastest")
        self.onclick(
            fun=self.display_name,
            btn=1
        )

    def display_name(self, x, y):
        self.turtlesize(0.1)
        self.write(self.name, font=GOOD_MARKER_FONT)
        self.master.master.after(5000, self.display_animation)

    def display_animation(self):
        self.clear()
        self.turtlesize(self.marker)


class MarkWrong(MarkGood):
    """Unknown country marker."""

    def __init__(self, master, name, marker):
        super().__init__(master, name, marker)

        # Wrong answer marker setup.
        self.color("red")


class MarkCountry(MarkGood):
    """Neutral country marker."""

    def __init__(self, master, name, marker):
        super().__init__(master, name, marker)

        # Neutral marker color.
        self.color("midnight blue")


class DataHandler(object):
    """This component is responsible for juggling app data."""

    # Countries coords data file.
    COORDS_DATA_FILE = "./assets/world_countries_coords.csv"

    def __init__(self, master):
        self.master = master

        self.coords_data = pd.read_csv(DataHandler.COORDS_DATA_FILE)
        self.all_countries = self.coords_data.country.to_list()
        self.next_country = self.draw_country(countries=self.all_countries)

    # Randomly pick next country to learn.
    def draw_country(self, countries):
        drawn_country = choice(countries)
        return drawn_country

    def fetch_country_data(self, country, data_frame):
        country_data = data_frame[data_frame.country == country]
        return country_data

    def fetch_country_coords(self, data):
        country_xcoor = data.xcoor
        country_ycoor = data.ycoor
        country_coords = (float(country_xcoor), float(country_ycoor))
        return country_coords

    def fetch_country_marker(self, data):
        country_marker = data.marker.to_string(index=False)
        country_marker_size = self.master.countries_map.MARKERS[country_marker]
        return country_marker_size

    # Check if the user knows correct country name.
    def validate_answer(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            print(True)
            new_good_data = self.fetch_country_data(
                country=self.next_country,
                data_frame=self.coords_data
            )
            new_good_name = self.next_country
            new_good_position = self.fetch_country_coords(data=new_good_data)
            new_good_marker = self.fetch_country_marker(data=new_good_data)
            new_good_marker = MarkGood(
                master=self.master.countries_map,
                name=new_good_name,
                marker=new_good_marker
            )
            new_good_marker.set_pin(position=new_good_position, shift=0)
            new_good_marker.showturtle()
            self.master.status_bar.inc_known()
            self.master.status_bar.update_status()
        else:
            print(False)
            new_wrong_data = self.fetch_country_data(
                country=self.next_country,
                data_frame=self.coords_data
            )
            new_wrong_name = self.next_country
            new_wrong_position = self.fetch_country_coords(data=new_wrong_data)
            new_wrong_marker = self.fetch_country_marker(data=new_wrong_data)
            new_wrong_marker = MarkWrong(
                master=self.master.countries_map,
                name=new_wrong_name,
                marker=new_wrong_marker
            )
            new_wrong_marker.set_pin(position=new_wrong_position, shift=0)
            new_wrong_marker.showturtle()

    def fetch_next_country(self):
        try:
            self.all_countries.remove(self.next_country)
            self.next_country = self.draw_country(countries=self.all_countries)
        except IndexError:
            self.master.controls_bar.block_input()
            self.master.t_pin.hideturtle()


class MainApplication(tk.Frame):
    """Application core structure."""

    def __init__(self, master):
        super().__init__()

        self.data_handler = DataHandler(master=self)

        # Construct GUI components.
        self.canvas = ScrolledCanvas(master=self)
        self.countries_map = ScreenMap(master=self, canvas=self.canvas)
        self.controls_bar = ControlsBar(
            master=self,
            countries_map=self.countries_map
        )
        self.status_bar = StatusBar(master=self)

        # Place GUI components onto main frame.
        self.controls_bar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

#        self.countries_map.generate_markers()

        self.t_pin = TurtlePin(master=self.countries_map)


if __name__ == "__main__":
    # Tkinter root application instance.
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(ROOT_WINDOW)
#    root.attributes("-fullscreen", True)
    MainApplication(master=root).pack(side=tk.TOP, expand=True, fill=tk.BOTH)
    root.mainloop()
