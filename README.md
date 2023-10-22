# About
Learn World Countries (LWC) is an interactive geographical quiz. Use it and learn countries names from all over the world!

![app-markers-screenshot](/assets/app_markers_ss.png?raw=true "App has interactive markers")

# Gameplay
After launching the program you'll see the world map which you can navigate using horizontal and vertical scrollbars. A couple of other options are available from the top panel:

You may *Generate markers* (it takes a while) in order to populate the map with dots. All kinds of markers are interactive; after clicking one you'll get the opportunity to familiarise yourself with particular country name.

*Start* initialises the gameplay and removes all markers from the map (if they were formed earlier) -- you don't want to cheat, don't you?
Then simply follow the pin and try to input the name of the country in question. You don't have to use the *Answer* button after filling an entry field, just hit **Enter** to pass your answer. If you don't know what state it's about, just input anything to move on to the next country. Good answers are marked via green dots. Wrong ones: in red. Both are clickable so you shall learn in case of getting a bad guess.

![app-gameplay-screenshot](/assets/app_gameplay_ss.png?raw=true "The gameplay is simple")

*Fullscreen*, *About* (to-be-made) and *Quit* are self-explanatory.

There's also a count information in right-bottom corner -- how many countries out of total 195 are you able to name?

# Mechanics
The core of the application is a **.csv** file filled with data. This file is opened with pandas and parsed via internal code.
Every country is paired with particular x and y coordinate responsible for map location. Each state has also a predefined marker size.
Due to the small scope of the architecture rest of the technical intricacies are simply documented in the code.

# Dependencies
The project was built upon `tkinter`, `turtle` and `pandas` modules, so you will need these.
