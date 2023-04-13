# This script will use tkinter to create a GUI featuring a combobox, button and image
# Displays artwork of the pokemon selected from the combobox
# Button will set the currently displayed image as Windows desktop background

import tkinter as tk
import tkinter.ttk as ttk
import os
import poke_api #import our already created poke_api.py module

# create window and set title
window = tk.Tk()
window.title("Change Desktop Background")
 
# set icon and grab screen size
# adjust window size and position
icon_image = "icon.png"
window.wm_iconphoto(True, tk.PhotoImage(file=icon_image))

# set window size
screen_width = window.winfo_screen width()
screen_height = window.winfo_screen height()
x_position = (screen_width//2)-(600//2)
y_position = (screen_height//2)-(500//2)
window.geometry("600x500+{}+{}".format(x_position, y_position))

# attach combobox to window
pokemon_list = poke_api.get_pokemon_list() #retrieve list of pokemon from poke_api
pokemon_select = ttk.Combobox(window, values=pokemon_list, state='readonly', justify='center')
pokemon_select.grid(row=0, column=0, sticky="nsew")
pokemon_select.set("Select Pokemon")

# attach and disable button to window
desktop_btn = ttk.Button(window, text="Set as Desktop Image", state='disable', command=None)
desktop_btn.grid(row=1, column=0)

# attach image frame to window
image_frame = tk.Frame(window, bd=3, relief="sunken")
image_frame.grid (row=0, column=1, rowspan=2, sticky="nsew")

# create image label
image_label = ttk.Label(image_frame)
image_label.pack()

# create default image and display in label
default_image = tk.PhotoImage(file= 'default_image.png')
image_label.configure(image=default_image)
image_label.image = default_image

# define callback for when pokemon is changed in combobox
# when pokemon name is chosen, download image from pokeapi,
# display image in image frame, 
# and enable button
def selectImage():
    name_selected = pokemon_select.get()
    if name_selected != 'Select Pokemon':
        desktop_btn.configure(state='enable')
        image_file_path = poke_api.download_image(name_selected)
        image_selected = tk.PhotoImage(file=image_file_path)
        image_label.configure(image=image_selected)
        image_label.image = image_selected

# set combobox command
pokemon_select.bind("<<ComboboxSelected>>", selectImage)

# define function when set as desktop image button is clicked
# sets current image as windows desktop background
def setDesktopImage():
    # code to get image file path and set image as desktop background
    os.system("reg add 'HKCU\\Control Panel\\Desktop' /v Wallpaper /t REG_SZ /d " + image_file_path + " /f")

# set button command
desktop_btn.config(command=setDesktopImage)

# start main loop
window.mainloop()