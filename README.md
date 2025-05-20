Facial Memory Trainer for desktop

When run, presents user with a series of (AI generated) images of human faces, and asks the user to state whether they have seen the face before or not.
  If the user is correct about whether that specific face has been shown this session, the UI flashes green.
  If the user is incorrect, it flashes red. The program then continues to the next face. 
  It is recommended to restart the session after having seen all the images in the current database. 

'Seen' counter shows the user how far through the database they are in a given session.
'Accuracy' counter shows the user their current percentage of correct answers in a given session.

Global variables at the top of the code allow the user to alter the rate at which new faces are added to the active image pool, depending on how many answers they have given.
  Can also change the starting active pool size (default 10), although it is reccomended to keep it low.
  There is currently 3 custom breakpoints for changing the progression rate, set at 25, 50 and 75, although these should be altered to fit the user.
  More testing is also needed to find the optimum rates to maintain a good balance of new and repeated faces in the active pool.

Current database includes 96 images, although includes a script (get_images.py) which adds more to the library (from https://ThisPersonDoesNotExist.com).
  
Future updates could include:
  Tailoring introduction rate to the user's accuracy score, introducing more faces if the user is doing well and less if they are struggling.
  Ability to remove 'Mastered' faces from active pool if the user gets them correct too many times.
  


