import os
import sys
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import ttk
from random import randint, shuffle

# global variable for size of database and learning speed
db_size = 96
start_number = 10
repeated_image_buffer = 3

# tweakable learning / spaced repetition rate (speed of adding new faces to active pool)
boundary_1 = 25
boundary_1_rate = 4
boundary_2 = 50
boundary_2_rate = 3
boundary_3 = 75
boundary_3_rate = 2



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
    shuffle(images)

    # randomize starting photo
    random_index = randint(0, start_number - 1)

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
        "images": images[:start_number],
        "seen": [],
        "image_label": image_label,
        "feedback_label": None,
        "seen_counter_label": None,
        "prompt_label": None,
        "end_label": None,
        "score_label": None,
        "image_container": image_container,
        "recent_images": [random_index], 
        "all_images": images,
        "next_image_index": start_number + 1,
        "response_count": 0,
        "correct": 0,
    }
    
    # create ui layout
    state["prompt_label"] = Label(mainframe, text="Have you seen this face before?", bg='lightblue')
    state["prompt_label"].grid(column=2, row=2, sticky=(N))
    ttk.Button(mainframe, text="yes", command=lambda: handle_response("y", state, mainframe, window, image_container)).grid(column=2, row=3, sticky=(W))
    ttk.Button(mainframe, text="no", command=lambda: handle_response("n", state, mainframe, window, image_container)).grid(column=2, row=3)
    ttk.Button(mainframe, text="Exit", command=window.destroy).grid(column=2, row=3, sticky=(E))
    state["seen_counter_label"] = Label(mainframe, text=f"Seen: 0/{len(state["all_images"])}", bg='lightblue')
    state["seen_counter_label"].grid(column=2, row=4, sticky=(E))
    state["score_label"] = Label(mainframe, text="Accuracy: 100%", bg='lightblue')
    state["score_label"].grid(column=2, row=4, sticky=(W))

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
    # count the response
    state["response_count"] += 1

    # add images to active pool, depending on set rate in different bands
    if len(state["images"]) < boundary_1 and (state["response_count"] % boundary_1_rate == 0):
        state["images"] = state["all_images"][:state["next_image_index"]]
    elif len(state["images"]) < boundary_2 and (state["response_count"] % boundary_2_rate == 0):
        state["images"] = state["all_images"][:state["next_image_index"]]
    elif len(state["images"]) < boundary_3 and (state["response_count"] % boundary_3_rate == 0):
        state["images"] = state["all_images"][:state["next_image_index"]]
    elif len(state["images"]) < len(state["all_images"]):
        state["images"] = state["all_images"][:state["next_image_index"]]
    else:
        state["end_label"] = Label(mainframe, text="All images have been seen.", bg='lightblue')
        state["end_label"].grid(column=2, row=5, font=("none 12"), sticky=(N))
    if state["next_image_index"] < len(state["all_images"]) - 1:
        state["next_image_index"] += 1
        

    # current image path
    image_path = state["images"][state["index"]]

    # check answer
    correct = check_seen(image_path, state["seen"])
    if not correct:
        log_seen(image_path, state["seen"])
        # update seen counter
        state["seen_counter_label"].configure(text=f"Seen: {len(state["seen"])}/{len(state["all_images"])}")

    # create new feedback label
    feedback = give_feedback(correct, response, mainframe, window, image_container, state)
    state["feedback_label"] = feedback

    # update percentage label
    state["score_label"].configure(text=f"Accuracy: {((state["correct"] / state["response_count"]) * 100):.1f}%")

    # show feedback for 1 second then move onto next image
    window.after(1000, lambda: show_next(state, mainframe, window, image_container))

def show_next(state, mainframe, window, image_container):
    # reset colours
    window.configure(bg='lightblue')
    mainframe.configure(bg='lightblue')
    image_container.configure(bg='lightblue')
    if state.get("end_label") is not None:
        state["end_label"].configure(bg='lightblue')
    state["prompt_label"].configure(bg='lightblue')
    state["seen_counter_label"].configure(bg='lightblue')
    state["score_label"].configure(bg='lightblue')

    if state["feedback_label"]:
        state["feedback_label"].destroy()

    # show next (different) image
    state["index"] = new_random_number(state)
    show_image(state, state["images"][state["index"]], window)






def new_random_number(state):
    # generate new unique image index
    new_number = state["index"]

    while new_number in state["recent_images"]:
        new_number = randint(0, len(state["images"]) - 1)

    # add chosen index to list and remove old one
    state["recent_images"].append(new_number)
    while len(state["recent_images"]) > repeated_image_buffer:
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





def give_feedback(correct, answer, mainframe, window, image_container, state):
    if correct and answer == "y":
        feedback = Label(mainframe, text="Correct!", font=("none 12 bold"), bg='green')
        # update correct counter
        state["correct"] += 1
        # sort colours
        window.configure(bg='green')
        mainframe.configure(bg='green')
        image_container.configure(bg='green')
        if state.get("end_label") is not None:
            state["end_label"].configure(bg='green')
        state["prompt_label"].configure(bg='green')
        state["seen_counter_label"].configure(bg='green')
        state["score_label"].configure(bg='green')
    
    elif not correct and answer == "n":
        feedback = Label(mainframe, text="Correct!", font=("none 12 bold"), bg='green')
        # update correct counter
        state["correct"] += 1
        # sort colours
        window.configure(bg='green')
        mainframe.configure(bg='green')
        image_container.configure(bg='green')
        if state.get("end_label") is not None:
            state["end_label"].configure(bg='green')
        state["prompt_label"].configure(bg='green')
        state["seen_counter_label"].configure(bg='green')
        state["score_label"].configure(bg='green')
    else:
        feedback = Label(mainframe, text="Incorrect.", font=("none 12 bold"), bg='red')
        # sort colours
        window.configure(bg='red')
        mainframe.configure(bg='red')
        image_container.configure(bg='red')
        if state.get("end_label") is not None:
            state["end_label"].configure(bg='red')
        state["prompt_label"].configure(bg='red')
        state["seen_counter_label"].configure(bg='red')
        state["score_label"].configure(bg='red')
    feedback.grid(column=2, row=4)
    return feedback





if __name__ == "__main__":
    main()




    



