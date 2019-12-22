# Homework 1

## Hubo the Artist (1-1)
Feeling exhausted after work every day, Hubo decided to learn painting for fun and fulfill after-work life.
But before learning to paint, Hubo wants to see some good paintings first.
Help Hubo appreciate some paintings drawn with beepers on the world.

Your job is to convert given world files to image files in the png format.

### A Special cs1robots Library
In this homework assignment, you are given a special cs1robots library that allows you to draw a grayscale image with your Robot and Beepers.

Using this special cs1robots library, you can change the color of the beepers by dropping multiple of them on the same position. This is how you change the color of the beepers:

* When you drop a single beeper, it’s shown in a very light gray color.  
* The color of the beeper gets darker as you drop more beepers on the same position.  
* The darkness of the beeper’s color increases linearly as you add more beepers on the same position.  
* When there are 16 beepers or more on the same position, the beeper is shown black.  

### Task
Given a world with beepers, convert the beepers on the world to an image file in the png format.

Write a code that creates a robot on the given world and scan all positions in the world. Then, create a new image and color each pixel based on the number of beepers in the corresponding position of the given robot world.

### Assumptions
1. The world size is 16 x 16.

### Rules
1. You can write your code between the line `# --- Your code starts from here ---` and the line `# --- Your code ends here ---`.  
   If you edit any other part of the given skeleton code, the grader script may not function properly.

2. Your program must not raise any errors or exceptions while running.

3. If there are n beepers in a position, the brightness of the corresponding pixel must be b = 255 - max(n \* 16 - 1, 0) if n is less than or equal to 16. Therefore the pixel must be colored with color in a form of a tuple (b, b, b) with the brightness b.

### Scoring criteria
The given world file is successfully converted to an image file in png format. (5 points per test case, 5 test cases, 25 points total)


## Hubo the Artist II (1-2)
Hubo thinks that it’s time to start a hands-on practice for painting.
Before painting its own masterpiece, Hubo decided to copy one or two famous paintings on the canvas (or the world, in fact).
Help Hubo draw a world that resembles existing pictures with beepers.

Your job is to convert a given png formatted image file to a robot world.

### Task
Given an image file, convert the image to a robot world with beepers.

Write a code that loads a given image file, creates a world and a robot, and draw the loaded image on the world using beepers.

### Assumptions
1. The size of the given image file is 16 x 16.

### Rules
1. You can write your code between the line `# --- Your code starts from here ---` and the line `# --- Your code ends here ---`.  
   If you edit any other part of the given skeleton code, the grader script may not function properly.

2. Your program must not raise any errors or exceptions when executed.

3. Create a world size of 16 x 16. You must draw the given image on a 16 x 16 world.

4. To calculate the number of beepers required to be dropped on a position of the world:
  * Let the brightness of a pixel (r + g + b) / 3, where r, g, and b indicate the brightness of the red, blue, and green light required to show the color of the pixel, respectively.  
  * Let t be the brightness of a pixel on an image to the corresponding world position.  
  * The required number of beepers is the largest integer that is less than or equal to (256 - t) / 16.  

### Scoring criteria
Given image file is successfully converted to a drawing on a robot world with beepers. (5 points per test case, 5 test cases, 25 points total)