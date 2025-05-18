import os
import sys
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import ttk
from random import randint

# global variable for size of database
db_size = 9



def main():
    # create tkinter window
    window = Tk()
    window.title("Facial memory trainer")
    window.geometry("450x400")
    window.resizable(width=True, height=True)
    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window, sys))
    window.configure(bg='lightblue')

    # create frame widget
    if not window.winfo_exists():
        return
    mainframe = Frame(window, bg='lightblue')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10)

    # columns share width, image gets more space in rows
    for i in range(3):
        mainframe.columnconfigure(i, weight=1)
    mainframe.rowconfigure(0, weight=3)
    mainframe.rowconfigure(1, weight=1)
    mainframe.rowconfigure(2, weight=1)

    # get the image paths
    images = load_images()

    # randomize starting photo
    random_index = randint(0, db_size)

    # create image container and label
    image_container = Frame(mainframe, width=400, height=300, bg='lightblue')
    image_container.grid(column=2, row=1, sticky=(N, S, E, W))
    image_container.grid_propagate(False)
    photo = PIL.ImageTk.PhotoImage(PIL.Image.open(images[random_index]))
    image_label = ttk.Label(mainframe, image=photo)
    image_label.image = photo
    image_label.grid(column=2, row=1, sticky=(N))

    # create variables
    state = {
        "index": random_index, 
        "images": images,
        "seen": [],
        "image_label": image_label,
        "feedback_label": None,
        "image_container": image_container,
        "recent_images": [random_index]
    }
    
    # create ui layout
    ttk.Label(mainframe, text="Have you seen this face before?").grid(column=2, row=2, sticky=(N))
    ttk.Button(mainframe, text="yes", command=lambda: handle_response("y", state, mainframe, window, image_container)).grid(column=2, row=3, sticky=(W))
    ttk.Button(mainframe, text="no", command=lambda: handle_response("n", state, mainframe, window, image_container)).grid(column=2, row=3)
    ttk.Button(mainframe, text="Exit", command=window.destroy).grid(column=2, row=3, sticky=(E))
    
    # bind to resize
    resize_after_id = None
    old_width, old_height = window.winfo_width, window.winfo_height
    def on_resize(event):
        new_width = event.width
        new_height = event.height
        nonlocal resize_after_id, old_width, old_height
        if new_width != old_width or new_height != old_height:
            if resize_after_id is not None:
                window.after_cancel(resize_after_id)
            resize_after_id = window.after(200, lambda: update_image(state, window))
            old_width, old_height = new_width, new_height
    window.bind("<Configure>", on_resize)

    # wait for button inputs
    window.mainloop()







def handle_response(response, state, mainframe, window, image_container):
    # current iamge path
    image_path = state["images"][state["index"]]

    # check answer
    correct = check_seen(image_path, state["seen"])
    if not correct:
        log_seen(image_path, state["seen"])

    # create new feedback label
    feedback = give_feedback(correct, response, mainframe, window, image_container)
    state["feedback_label"] = feedback

    # show feedback for 1 second then move onto next image
    window.after(1000, lambda: show_next(state, mainframe, window, image_container))

def show_next(state, mainframe, window, image_container):
    # reset colours
    window.configure(bg='lightblue')
    mainframe.configure(bg='lightblue')
    image_container.configure(bg='lightblue')

    if state["feedback_label"]:
        state["feedback_label"].destroy()

    # show next (different) image
    state["index"] = new_random_number(state)
    show_image(state, state["images"][state["index"]], window)






def new_random_number(state):
    # generate new unique image index
    new_number = state["index"]

    while new_number in state["recent_images"]:
        new_number = randint(0, db_size)

    # add chosen index to list and remove old one
    state["recent_images"].append(new_number)
    if len(state["recent_images"]) == 4:
        state["recent_images"].pop(0)
    
    return new_number





def on_close(window, sys):
    window.destroy()
    sys.exit()





def update_image(state, window):
    show_image(state, state["images"][state["index"]], window)
    return



        

def load_images():
    # get list of file names in faces/
    short_images = os.listdir("faces/")
    images = []
    
    # prepend "faces/" to each one
    for image in short_images:
        # check if it is valid
        if not image.endswith(".jpg"):
            continue
        else:
            images.append(os.path.join("faces", image))

    return images





def show_image(state, image, window):
    # format image variables
    image1 = PIL.Image.open(image)

    # dynamically resize window
    window.update_idletasks()
    max_width = int(window.winfo_width() * 0.8)
    max_height = int(window.winfo_height() * 0.6)

    # resize container
    if max_width == 1 or max_height == 1:
        max_width, max_height = 400, 300

    image1.thumbnail((max_width, max_height), PIL.Image.Resampling.LANCZOS)
    photo = PIL.ImageTk.PhotoImage(image1)

    # create image label
    current_image = state["image_label"]
    current_image.configure(image=photo)
    current_image.image = photo

    return current_image





def check_seen(image, seen):
    return image in seen





def log_seen(image, seen):
    seen.append(image)
    return





def give_feedback(correct, answer, mainframe, window, image_container):
    if correct and answer == "y":
        feedback = ttk.Label(mainframe, text="Correct!", font=("none 12 bold"))
        window.configure(bg='green')
        mainframe.configure(bg='green')
        image_container.configure(bg='green')
    
    elif not correct and answer == "n":
        feedback = ttk.Label(mainframe, text="Correct!", font=("none 12 bold"))
        window.configure(bg='green')
        mainframe.configure(bg='green')
        image_container.configure(bg='green')
    else:
        feedback = ttk.Label(mainframe, text="Incorrect.", font=("none 12 bold"))
        window.configure(bg='red')
        mainframe.configure(bg='red')
        image_container.configure(bg='red')
    feedback.grid(column=2, row=4)
    return feedback





if __name__ == "__main__":
    main()




    



