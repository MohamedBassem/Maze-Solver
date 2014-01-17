import Tkinter
from PIL import Image, ImageTk
from sys import argv
from Queue import Queue

if( len(argv) < 2 ):
    print "You shoud provid the image as a command line argument"
    exit(0)

frame = Tkinter.Tk(className="Maze Solver")
maze = Image.open(argv[1]).convert("RGB")
image_pixels = maze.load()
canvas = Tkinter.Canvas(frame, width=maze.size[0], height=maze.size[1])
canvas.pack()
image_label = ImageTk.PhotoImage(maze)
item = canvas.create_image(maze.size[0]//2, maze.size[1]//2, image=image_label)

start_point = (-1,-1)
end_point = (-1,-1)
path_color = (255,0,0)
ground_color = (255,255,255)

points_so_far = 0
def callback(event):
    global points_so_far,start_point,end_point,ground_color
    if event.x > maze.size[0] or event.y > maze.size[1]:
        print "Invalid Coordinates , choose again."
        return
    elif points_so_far == 0:
        print "Start Point : " , (event.x,event.y)
        start_point = (event.x,event.y)
        print "Please choose the ending point."
    elif points_so_far == 1:
        print "End Point : " , (event.x,event.y)
        end_point = (event.x , event.y)
        print "Please choose the ground color."
    elif points_so_far == 2:
        print "Ground Color : " , image_pixels[event.x,event.y]
        print "Please wait while computing the path ..."
        ground_color = image_pixels[event.x,event.y]
        canvas.unbind("<Button-1>")
        solve_maze()
    points_so_far += 1
    
direction = [ (0,1) , (1,0) , (-1,0) , (0,-1) ]

def bfs(start_i,start_j):
    Q = Queue()
    vis = {}
    parent = {}
    Q.put( (start_i,start_j) )
    parent[(start_i,start_j)] = (-1,-1)
    vis[(start_i,start_j)] = 1
    end = (-1,-1)
    while not Q.empty():
        curr = Q.get()
        i = curr[0]
        j = curr[1]
        if (i,j) == end_point :
            end = (i,j)
            break
        if image_pixels[i,j] != ground_color :
            continue
        
        for d in direction:
            if i+d[0] >= maze.size[0] or i+d[0] < 0 or j+d[1] >= maze.size[1] or j+d[1] < 0 or (i+d[0],j+d[1]) in vis:
                continue
            else:
                vis[(i+d[0],j+d[1])] = 1
                parent[(i+d[0] , j+d[1])] = (i,j)
                Q.put( (i+d[0] , j+d[1]) )
    if end == (-1,-1):
        return False
    else:
        while end != (-1,-1):
            image_pixels[end[0],end[1]] = path_color
            end = parent[end]
        return True

def solve_maze():
    global canvas,item,image_label
    found = bfs(start_point[0], start_point[1])
    if not found :
        print "No Path Found"
    else:
        canvas.delete("all")
        image_label = ImageTk.PhotoImage(maze)
        item = canvas.create_image(maze.size[0]//2, maze.size[1]//2, image=image_label)
        print "SOLVED !"


canvas.bind("<Button-1>", callback)
print "Please Choose the starting point."
Tkinter.mainloop()