import os
from PIL import Image



def main():

    # get the image paths
    images = load_images()
    seen = []

    # until we run out of images
    for image in images:
        show_image(image)

        answer = get_user_response()
        # allow the user to quit out
        if answer == "x":
            break
        
        # check if the user is correct
        correct = check_seen(image, seen)
        if correct == False:
            log_seen(image, seen)
        
        # tell the user if they are right
        give_feedback(correct, answer)

        print(image)


        

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



def show_image(image):
    im = Image.open(image)
    im.show()
    return



def get_user_response():
    answer = input("Have you seen this face before? (y, n, x)")
    return answer



def check_seen(image, seen):
    return image in seen



def log_seen(image, seen):
    seen.append(image)
    return



def give_feedback(correct, answer):
    if correct and answer == "y":
        print("correct")
    elif not correct and answer == "n":
        print("correct")
    else:
        print("incorrect")
    return 
        


if __name__ == "__main__":
    main()




    



