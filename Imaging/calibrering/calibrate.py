from PIL import Image, ImageEnhance
from regressions import linear_regress

def search_high(img, x, y, up=False):
    # find higher value up or down return better value or false
    found = False
    startval = img.getpixel((x,y))
    myval = startval
    while True:
        oldy = y
        if up:
            y = y-1
        else:
            y = y+1
        if (y==0 or y>img.height) and not found:
            return False
        newval = img.getpixel((x,y))
        if newval >= myval:
            found = True
            myval=newval
        else:
            if found:
                return(x,oldy)
            else:
                return False

def search_low(img, x, y, up=False):
    # find lowest value up or down return better value or false
    found = False
    startval = img.getpixel((x,y))
    myval = startval
    while True:
        oldy = y
        if up:
            y = y-1
        else:
            y = y+1
        if (y==0 or y>img.height) and not found:
            return False
        newval = img.getpixel((x,y))
        if newval <= myval:
            found = True
            myval=newval
        else:
            if found:
                return(x,oldy)
            else:
                return False

def find_next_high(img, x, y):
    # find the nearest heigh pixel in same x column
    new1 = search_high(img, x,y)
    new2 = search_high(img, x,y,True)
    #print("new1", new1)
    #print('new2', new2)
    if not new1:
        if not new2:
            return ((x,y))
        return new2
    if not new2:
        return new1
    if img.getpixel(new1) > img.getpixel(new2):
        return new1
    return new2

def get_img_slope(filename):
    img = Image.open(filename)
    procent = 0.2
    width = img.width
    height = img.height
    crop_field = (0+width*procent,0+height*procent, width-width*procent, height-height*procent)
    img2 = img.crop(crop_field)
    grey = img2.convert('L')
    width = img2.width
    height = img2.height
    # find first y value
    y = height / 2
    y=51
    arr =[]
    for i in range (0,width):
        point = find_next_high(grey,i,y)
        arr.append(point)
    degree = linear_regress(arr)
    #print("slope", degree, "degree")
    return -degree

def get_img_freq(filename):
    img = Image.open(filename)
    grey = img.convert('L')
    x=50
    y=50
    #print ("start", x,y )
    start = find_next_high(grey,x,y)
    #print ("nystart", start)
    x=start[0]
    y=start[1]
    up = search_low(grey, x,y)
    #print("up",up)
    down = search_low(grey, x,y, up=True)
    #print("down", down)
    diff = up[1]-down[1]
    #print ("diff", diff)
    #print ( diff/100.0)
    return diff/100.0

if __name__ == "__main__":
    filename = "Imaging/calibrering/testdata/align/image0.jpg"
    deg = get_img_slope(filename)
    print("degree: ", deg)

    # img = Image.open(filename)
    # img.rotate(-deg).show()

    freq = get_img_freq(filename)
    print("freq",freq)
