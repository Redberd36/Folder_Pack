import shutil, pickle, os, os.path, time# Other Python modules
from sys import exit
from time import sleep
from os import path
from tkinter import * # Windows GUI
from tkinter import filedialog # Windows GUI

txt = [""] # Global variables for directories
dir1 = ""
dir2 = ""
Name = ""
Name2 = ""
act = "normal"
pmenu = ""
rev1 = ""
rev2 = ""
check = 0
count = 0
schange = False

######################################################################

win = Tk() # Quick label tkinter API
ico = PhotoImage(file="Folder_Packaging_Logo.png")
win.iconphoto(False, ico)# Set program Icon image
win.title("Folder_Pack") # Title of program window
win.geometry("241x340+470+120")
win.resizable(width=False, height=False)
win.bind('<Escape>', lambda e: win.destroy()) # Escape key exits window
#win.withdraw() <- Exit window

v = StringVar() # Error warning text
warn = Label(win, textvariable=v)
warn.grid(row=13, column=0)
v.set("")
    
def save():
    global v,saving,revert,check,schange # Grab global variables
    if check >= 2:
        print("SAVE WORKS", schange, check)
        if schange == True:
            p = os.getcwd()
            fp = os.chdir(p)
            files = os.listdir(fp)
            for P in files:
                if P == "Move_Pref.txt":
                    print(P + " has been deleted")
                    os.remove("Move_Pref.txt")
                    
        pickle.dump(txt, open("Move_Pref.txt", "wb")) # Save variable(s)
        path = os.getcwd()
        fpath = os.chdir(path)
        file = os.listdir(fpath)
        for p in file:
            if p == "Move_Pref.txt": # *Move_Pref.txt file exists condition*
                print(p)
                os.system('attrib +h Move_Pref.txt') # Hidden file attribute
                
        # Disable save button
        saving.grid_remove()
        saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black")
        saving.grid(row=12, column=0)
        saving.configure(state=DISABLED, background="#BA9FAA")
        # Enable revert button
        revert.configure(state=ACTIVE, background="#BA9FAA")
        revert = Button(win, text="Revert defaults",pady=0, padx=2, bg="#BA9FAA", fg="black", command=popmenu)
        revert.grid(row=13, column=0)

### TIMED MESSAGES CODE ###
    #path = os.getcwd()
    #fpath = os.chdir(path)
    #file = os.listdir(fpath)
    #for p in file:
        #if p == "Move_Pref.txt": # *Move_Prefs.txt file exists condition*
            #print(p + " Does exist!" + txt[0])
            #saving.configure(state=DISABLED)
            #v.set("Previous save data exists")
            #win.after(1500, clear) # Timer delay for text disappearing
            #return
#def clear():
    #global saving
    #saving.configure(state=ACTIVE, background="#BA9FAA")
    #saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black", command=save)
    #saving.grid(row=10, column=0)
    #v.set("") # Reset the timed text error
    #return

        
##Reset_Prefs function##
def reset():
    global rev1,rev2,check,move,revert
    path = os.getcwd()
    fpath = os.chdir(path)
    file = os.listdir(fpath)
    
    for p in file:
        if p == "Move_Pref.txt":
            print(p + " has been deleted")
            os.remove("Move_Pref.txt")
            check = 0
            checks() # Disable move button
            revert.grid_remove()
            revert = Button(win, text="Revert defaults",pady=0, padx=2, bg="#BA9FAA", fg="black", command=popmenu)
            revert.grid(row=13, column=0)
            revert.configure(state=DISABLED)
            rev1.grid_remove()
            rev2.grid_remove()
            txt[0] = ""
            txt[1] = ""
            return
def popmenu():
    global revert,pmenu
    revert.configure(state=DISABLED)
    
    stop = Toplevel(win) # Generate new tkinter window
    pmenu = stop # Save variable for X-iting screen
    stop.geometry("200x100+490+200")
    stop.resizable(width=False, height=False)
    stop.title("Caution...")
    icon = PhotoImage(file="Folder_Packaging_Logo.png")
    stop.iconphoto(False, icon)# Set program Icon image
    msg = Label(stop, padx=7.5, text="Do you want to erase preferences?")
    msg.grid(row=0, column=0)
    stop.focus_set() # Focus on new window
    stop.protocol("WM_DELETE_WINDOW", exitpop) # X exits window
    stop.bind('<Escape>', lambda e: exitpop()) # Escape key exits window
    
    yes = Button(stop, text="Yes",padx=13, bg="#BA9F9B", command=lambda:[reset(), stop.destroy()])
    yes.place(x=36,y=42)
    no = Button(stop, text="No",padx=13, bg="#BA9F9B", command=lambda:[exitpop(), stop.destroy()])
    no.place(x=111,y=42)
   
    spcc = Label(stop, text="")
    spcc.grid(row=1, column=0)
    return
def exitpop():
    global revert,pmenu
    pmenu.destroy()
    revert.configure(state=ACTIVE)
    revert = Button(win, text="Revert defaults",pady=0, padx=2, bg="#BA9FAA", fg="black", command=popmenu)
    revert.grid(row=13, column=0)
    return

### Command Function list ###    
def move_items():
    global ent,count
    dr1 = str(txt[0])
    dr2 = str(txt[1])
    items = os.listdir(dr1)
    #print(dr1, dr2)
    
    exten = [list(x) for x in ent.get().split(' ')]
    exten = list(filter(None, exten)) # Remove any empty spaces within word list
    #print(num, "Final word:", ''.join(exten[count]))
    
    #count -> int for counting up to final word num
    delay = 0
    num = len(exten) # final amount of words in nested list strings

    if len(exten) == 0:
        print("STRING IS EMPTY")
        return
    elif len(exten) >= 1:
        for f in items:
            if count != num:
                if f.lower().endswith(''.join(exten[count])):
                    print(f, count)
                    shutil.move(dr1+"/"+f, dr2)
            else:
                return       
        if count != num:
            while delay < 3:
                delay+=1
                if delay >= 3:
                    count+=1
                    move_items()
                    break;
        else:
            return

def pack_models():
    dr1 = str(txt[0])
    amount = 0
    texcount = 0
    zipnum = 0
    pack = 0
    zipname = False
    compare = ""
    final = ""
    zipath = [""] # Keep track of newly made folder directories for .zip 
    ddfiles = [""]
    texfiles = [""]
    ext = [".obj",".fbx",".3ds",".dae",".x3d",".blend"
           ".gltf",".glb",".pmx",".stl", ".mtl",".alembic"]
    tex = [".psd",".psb",".tif",".exr",".bmp",".gif",
           ".jpg",".png",".tga",".dds",".dxt",".pvr", ".bpp"
           ".tpl",".vtf",".s3tc",".3dc",".mtd",".pdd",".webp"]
    objfile = os.listdir(dr1)
    print(dr1)

    # Find 3D mesh files in input folder
    for mesh in objfile:
        if mesh.lower().endswith(tuple(ext)):
            ddfiles.append(str(mesh).split(' '))
            ddfiles = list(filter(None, ddfiles))
    print(len(ddfiles), ddfiles)

    # Go through each 3D mesh file -> create/name folder -> move into named folder
    for folder in objfile:
        # Pack created 3D mesh folder into zip file
        if pack < len(zipath) and amount >= len(ddfiles):
            shutil.make_archive(''.join(zipath[pack]), 'zip', dr1+'/'+''.join(zipath[pack]))
            shutil.move(os.getcwd()+'/'+''.join(zipath[pack]+'.zip'), dr1) # Move from texture file.py folder path to 3D mesh folders
            print("PYTHON SCRIPT LOCATION", os.getcwd())
            print("MADE ZIP FILE", ''.join(zipath[pack]))
            pack+=1
                
        if ''.join(ddfiles[0]) != "" and amount < len(ddfiles) and ''.join(ddfiles[amount]) in folder:
            print("Times repeated:",amount)
            obj=folder.split('.')
            obj.pop(1)
            final = ''.join(obj)
            print("Folder name:",final)
            
            # Check if folder is already made
            if path.exists(os.path.join(dr1+'/'+final)) == True:
                print("ALREADY EXISTS", "COMPATED TO:", final)
                # If other mesh files are named like folder -> Add to folder
                if compare == final:
                    print("Comparasion:",folder)
                    shutil.move(dr1+'/'+folder, newpath)
                    amount+=1
                    
            elif path.exists(os.path.join(dr1+'/'+final)) == False:
                # Save final 3D mesh folder name for comparasion
                compare=final
                # Make new folder path from mesh file
                newpath = os.path.join(dr1+'/'+final)
                os.mkdir(newpath)
                print(newpath,',',folder, zipname)
                shutil.move(dr1+'/'+folder, newpath)

                if zipname == True:
                    if str(zipath[zipnum]) != final: # Folder name =/= saved name
                        zipname = False
                        zipnum+=1
                if zipname == False: # Grab strings for .zip function
                    zipath.append(final)
                    zipath = list(filter(None, zipath))
                    print("ZIP FILE LIST", zipath)
                    zipname = True
                
                # Find all associated texture files to folder
                for textures in objfile:
                    if textures.endswith(tuple(tex)) or textures.lower().endswith(tuple(tex)) or textures.upper().endswith(tuple(tex)):
                        texfiles.append(str(textures).split(' '))
                        texfiles = list(filter(None, texfiles))
                print(len(texfiles), texfiles)
                
                # move all associated texture files to mesh folder
                for movetext in objfile:
                    if texcount < len(texfiles):
                        if ''.join(texfiles[texcount]) in movetext:
                            text=movetext.split('_')
                            text = ''.join(text[0])
                            print(text)
                        
                            if text == compare:
                                shutil.move(dr1+'/'+movetext, newpath)
                            texcount+=1
                amount+=1
        
    

#############################
        
def checks():
    global check,move,saving,revert,schange
    print("checks:", check)
    if check >= 2 and path.exists("Move_Pref.txt") == False:
        # Input/Ouput =/= save file
        schange = True # Deleting previous save file on
        # Enabled save button
        saving.grid_remove()
        saving.configure(state=ACTIVE, background="#BA9FAA")
        saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black", command=save)
        saving.grid(row=12, column=0)
        # Enabled move button
        move.grid_remove()
        move.configure(state=ACTIVE, background="#BF7777")
        move = Button(win, text="Move Files", pady=0, padx=2, bg="#BF7777", fg="black", command=move_items)
        move.grid(row=9, column=0, ipady=3)
        
    elif check >= 2 and path.exists("Move_Pref.txt") == True:
        # Input/Ouput + save file
        # Disable save button
        saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black", command=save)
        saving.grid(row=12, column=0)
        saving.configure(state=DISABLED, background="#BA9FAA")
        # Emable move button
        move = Button(win, text="Move Files", pady=0, padx=2, bg="#BF7777", fg="black", command=move_items)
        move.grid(row=9, column=0, ipady=3)
        revert = Button(win, text="Revert defaults",pady=0, padx=2, bg="#BA9FAA", fg="black", command=popmenu)
        revert.grid(row=13, column=0)
        
    if check < 2:
        # No selection for Input/Ouput
        # Disable save button
        saving.grid_remove()
        saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black")
        saving.grid(row=12, column=0)
        saving.configure(state=DISABLED, background="#BA9FAA")
        # Disable move button
        move.grid_remove()
        move = Button(win, text="Move Files", pady=0, padx=2, bg="#BF7777", fg="black")
        move.grid(row=9, column=0, ipady=3)
        move.configure(state=DISABLED, background="#BF7777")

def dirmatch():
    global dir1,dir2,move,saving,revert,schange
    print("NEW_NAME--->",dir1)
    if dir1 != Name or dir2 != Name2:
        print("Saved String:", Name)
        # Enabled save button
        schange = True # Deleting previous save file on
        #saving.grid_remove()
        saving.configure(state=ACTIVE, background="#BA9FAA")
        saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black", command=save)
        saving.grid(row=12, column=0)
        revert.grid_remove()
        revert = Button(win, text="Revert defaults",pady=0, padx=2, bg="#BA9FAA", fg="black")
        revert.grid(row=13, column=0)
        revert.configure(state=DISABLED, background="#BA9FAA")
    else:
        checks()
        return

        
#################################################################

print("Does the prefs file exist?:",path.exists("Move_Pref.txt")) # Loading safe prefs
if path.exists("Move_Pref.txt") == True:
    txt = pickle.load(open("Move_Pref.txt", "rb")) # Save variable(s)  
    dir1 = txt[0]
    dir2 = txt[1]

    Name = dir1 #Grab original string
    Name2 = dir2
    schange = True
    
    check = 2
    checks()

    if len(txt[0]) > 33:
        number1 = 0
        totally1 = ""
        lin1 = "..."
        for let in txt[0]:
            totally1 += let
            number1 += 1
            if number1 == 33:
                break
        #print("First ", number1, totally1)
    elif len(txt[0]) <= 33:
         totally1 = dir1 # Original directory length
         lin1 = ""
         
    if len(txt[1]) > 33:
        number2 = 0
        totally2 = ""
        lin2 = "..."
        for let in txt[1]:
            totally2 += let
            number2 += 1
            if number2 == 33:
                break
        #print("Second", number2, totally2)
    elif len(txt[1]) <= 33:
         totally2 = dir2 # Original directory length
         lin2 = ""
        
    print(dir1, ":", dir2)
    rev1=stat1 = Label(win, text=totally1 + lin1, fg="gray") #Converting letters into string
    stat1.grid(row=3, column=0)
    rev2=stat2 = Label(win, text=totally2 + lin2, fg="gray")
    stat2.grid(row=6, column=0)
elif path.exists("Move_Pref.txt") == False:
    schange = False # Deleting previous save file off
    saving = Button(win, text="Save as default", pady=0, padx=2, bg="#BA9FAA", fg="black")
    saving.grid(row=12, column=0)
    saving.configure(state=DISABLED, background="#BA9FAA")
    
    move = Button(win, text="Move Files", pady=0, padx=2, bg="#BF7777", fg="black")
    move.grid(row=9, column=0, ipady=3)
    move.configure(state=DISABLED, background="#BF7777")
    
    revert = Button(win, text="Revert defaults",pady=0, padx=2, bg="#BA9FAA", fg="black")
    revert.grid(row=13, column=0)
    revert.configure(state=DISABLED, background="#BA9FAA")
    

if txt[0] == "":
    rev1=stat1 = Label(win, fg="gray")
    stat1.grid(row=3, column=0)
    rev2=stat2 = Label(win, fg="gray")
    stat2.grid(row=6, column=0)
    
    rev1.grid_remove()
    rev2.grid_remove()



def input_dir():
    global check,rev1,dir1 # Grab global variable
    file_path = filedialog.askdirectory() # Get directory menu
    #file_path = filedialog.askopenfilename
    #(title="Select directory", filetypes=[("png files", "*.png")])
    dir1 = file_path
    if path.exists("Move_Pref.txt") == False:
        Name = dir1
    
    if dir1 != "":
        txt.remove(txt[0])
        txt.insert(0, str(dir1))
        if len(txt[0]) > 33: # Shorten directory names
            nums = 0
            totals = ""
            lines = "..."
            for let in txt[0]:
                totals += let
                nums += 1
                if nums == 33:
                    break
        elif len(txt[0]) <= 33:
            totals = dir1 # Original directory length
            lines = ""
            rev1.grid_remove()
            
        rev1=stat1 = Label(win, text=totals + lines, fg="gray")
        rev1.grid(row=3, column=0)
        check += 1
        dir1 = txt[0]
        
        if check > 2:
            dirmatch()
        elif check <= 2:
            checks() # Check count for move button off/on
        print("Input:", dir1)
        
def output_dir():
    global check,rev2,dir2 # Grab global variable
    file_path = filedialog.askdirectory()
    dir2 = file_path
    if path.exists("Move_Pref.txt") == False:
        Name2 = dir2

    if dir2 != "":
        if len(txt) != 1:
            txt.remove(txt[1])
        txt.insert(1, str(dir2))
        if len(txt[1]) > 33: # Shorten directory names
            num = 0
            total = ""
            line = "..."
            for let in txt[1]:
                total += let
                num += 1
                if num == 33:
                    break
        elif len(txt[1]) <= 33 :
            total = dir2 # Original directory length
            line = ""
            rev2.grid_remove()
            
        rev2=stat2 = Label(win, text=total + line, fg="gray")
        rev2.grid(row=6, column=0)
        check += 1
        dir2 = txt[1]

        if check > 2:
            dirmatch()
        elif check <= 2:
            checks() # Check count for move button off/on
        print("Output:", dir2)
    else:
        check -= 1
        return


############################################################

line1 = Label(win, text="Select input file directory.")
line1.grid(row=0, column=0)

inp = Button(win, text="Change input Directory",padx=30, bg="#E3C2BC", command=input_dir)
inp.grid(row=1, column=0, pady=2)

# Status 1 line

line2 = Label(win, text="Select output file directory.")
line2.grid(row=4, column=0)

out = Button(win, text="Change output Directory",padx=26, bg="#BA9F9B", command=output_dir)
out.grid(row=5, column=0, pady=2)
#out.pack() # Pack the text on screen

# Status 2 line 6

spc1 = Label(win, text="")
spc1.grid(row=7, column=0)

ent = Entry(win, width=25) # <--- Writing stuff
ent.insert(0, "")
ent.grid(row=8, column=0)

# Move button stack 9

fold = Button(win, text="Create Texture Folders",padx=26, bg="#BA9F8A", command=pack_models)
fold.grid(row=10, column=0)

spc2 = Label(win, text="                                                                              ")
spc2.grid(row=11, column=0)

# Saving button stack 12

# Revert button stack 13

spc3 = Label(win, text="                                                                              ")
spc3.grid(row=14, column=0)

spc4 = Label(win, text="                                                                              ")
spc4.grid(row=15, column=0)


win.mainloop() # Running the window program


