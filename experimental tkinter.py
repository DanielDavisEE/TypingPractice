import tkinter as tk

def flash_set(colour, item):
    item.cget('background') = bg_colour
    bg_colour = [int(background_colour[1:3], 16),
                 int(background_colour[3:5], 16),
                 int(background_colour[5:7], 16)]
    rgb = [int(colour[1:3], 16),
           int(colour[3:5], 16),
           int(colour[5:7], 16)]
    flash(rgb, bg_colour)
    

def flash(rgb, bg_colour):

    for i in range(len(rgb)):
        num = rgb[i]
        diff = num - bg_colour[i]
        if num != bg_colour:
            rgb[i] =  int(format(num - diff // 10, 'x'), 16)
    colour = '#' + \
        '{:0>2}'.format(format(rgb[0], 'x')) + \
        '{:0>2}'.format(format(rgb[1], 'x')) + \
        '{:0>2}'.format(format(rgb[2], 'x'))
    print(colour)
    square.configure(bg=colour)
    square.update_idletasks()
    loop = False
    for i in range(len(rgb)):
        if rgb[i] != bg_colour[i]:
            loop = True
            break
    if loop:
        root.after(15, lambda: flash(rgb, bg_colour))
        
    
root = tk.Tk()
root.geometry('900x400')
background_colour = '#f0f0f0'
root.tk_setPalette(background=background_colour)
square = tk.Frame(root)
square.pack(fill=tk.BOTH, expand=1)
quit_button = tk.Button(square, text='hi', command=lambda: flash_set('#dd0000'))#'#00bb00'
quit_button.grid(padx=20, pady=20, ipadx=20, ipady=20)


root.mainloop()

