# template for "Stopwatch: The Game"

# define global variables
import simplegui
counter = int(0)
x = 0
y = 0
timer_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    if t > 5999:
        return "Woah there!"
    else:
        A = t / 600
        B = ((t // 10 ) % 60) // 10
        C = ((t // 10 ) % 60) % 10
        D = t % 10
        return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer_running
    timer.start()
    timer_running = True
    
def stop():
    global x, y, timer_running
    if timer_running == True:
        y += 1
        if (counter % 10) == 0:
            x += 1
        timer_running = False
    else:
        timer_running == False
    timer.stop()
    
def reset():
    global counter, x, y
    counter = 0
    x = 0
    y = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter), [150, 212], 24, "White")
    canvas.draw_text(str(x) + "/" + str(y), [320, 50], 24, "White")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 400,400)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()


# Please remember to review the grading rubric