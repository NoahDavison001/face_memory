import os
import sys
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import ttk


def main():
    # create tkinter window
    window = Tk()
    window.title("Facial memory trainer")
    window.geometry("1000x800")
    window.resizable(width=True, height=True)
    answer_var = StringVar()
    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window, sys))

    # create frame widget
    if not window.winfo_exists():
        return
    mainframe = ttk.Frame(window, padding = "3 4 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # get the image paths
    images = load_images()

    # create variables
    state = {
        "index": 0, 
        "images": images,
        "seen": [],
        "image_label": None,
        "feedback_label": None
    }

    # show first image
    state["image_label"] = show_image(images[0], mainframe, window)

    # create ui layout
    ttk.Label(mainframe, text="Have you seen this face before?").grid(column=2, row=2, sticky=(W, N))
    ttk.Button(mainframe, text="yes", command=lambda: handle_response("y", state, mainframe, window)).grid(column=1, row=3, sticky=(N, E))
    ttk.Button(mainframe, text="no", command=lambda: handle_response("n", state, mainframe, window)).grid(column=2, row=3)
    ttk.Button(mainframe, text="Exit", command=window.destroy).grid(column=3, row=3, sticky=(N, W))
    # ttk.Button(mainframe, text="next", command=lambda: show_next_image).grid(column=2, row=5, sticky=(N))

    # wait for button inputs
    window.mainloop()







def handle_response(response, state, mainframe, window):
    # current iamge path
    image_path = state["images"][state["index"]]

    # check answer
    correct = check_seen(image_path, state["seen"])
    if not correct:
        log_seen(image_path, state["seen"])
    
    # clear previous feedback
    if state["feedback_label"]:
        state["feedback_label"].destroy()

    # create new feedback label
    feedback = give_feedback(correct, response, mainframe)
    state["feedback_label"] = feedback

    # show next image
    state["index"] += 1
    if state["index"] < len(state["images"]):
        # remove old image
        if state["image_label"]:
            state["image_label"].destroy()
        new_label = show_image(state["images"][state["index"]], mainframe, window)
        state["image_label"] = new_label
    else:
        # done
        end = ttk.Label(mainframe, text="no more images", font=("none 14 bold"))
        end.grid(column=2, row=5)





def on_close(window, sys):
    window.destroy()
    sys.exit()



        

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





def show_image(image, mainframe, window):
    # format image variables
    image1 = PIL.Image.open(image)

    # dynamically resize window
    window.update_idletasks()
    max_width = int(window.winfo_width() * 0.8)
    max_height = int(window.winfo_height() * 0.6)

    image1.thumbnail((max_width, max_height), PIL.Image.Resampling.LANCZOS)
    photo = PIL.ImageTk.PhotoImage(image1)

    # create image label
    current_image = ttk.Label(mainframe, image=photo)
    current_image.image = photo
    current_image.grid(column=3, row=1, sticky=(N, S, W, E))

    return current_image





def check_seen(image, seen):
    return image in seen





def log_seen(image, seen):
    seen.append(image)
    return





def give_feedback(correct, answer, mainframe):
    if correct and answer == "y":
        feedback = ttk.Label(mainframe, text="Correct!", font=("none 12 bold"))
    
    elif not correct and answer == "n":
        feedback = ttk.Label(mainframe, text="Correct!", font=("none 12 bold"))
        
    else:
        feedback = ttk.Label(mainframe, text="Incorrect.", font=("none 12 bold"))
    
    feedback.grid(column=2, row=4)
    return feedback





if __name__ == "__main__":
    main()




    



