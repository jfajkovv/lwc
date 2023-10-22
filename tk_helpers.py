def get_screen_size():
    """Returns active screen resolution."""
    import tkinter as tk
    root = tk.Tk()
    root.update_idletasks()
    root.attributes("-fullscreen", True)
    root.state("iconic")
    screen_geometry = root.winfo_geometry()
#    screen_geometry = screen_geometry.split('+', 1)[0].split('x')
    screen_geometry = screen_geometry.split('+', 1)[0]
    root.destroy()
    return screen_geometry


def get_tl_mouse_click_coords(x, y):
    """View mouse click coordinates from turtle's screen."""
    coords = f"{x},{y}\n"
    print(coords)


def toggle_fscreen(master):
    """Switch between fullscreen and windowed modes."""
    if master.attributes("-fullscreen"):
        master.attributes("-fullscreen", False)
    else:
        master.attributes("-fullscreen", True)
