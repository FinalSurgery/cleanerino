#!/usr/bin/python3

import os

home_path = "C:/Users/alexd/" # user's home path, the script assume that your Download folder is in this path,
destination_path = "C:/Users/alexd/Documents" # in my case this path is the same but you can put a different path if you want the folders and files to end up somewhere else.
affected_folder = ["Downloads/", "Pictures/", "Music/", "Documents/", "Videos/"] # the folder you want to sort through.
 # combined output that defines the folder that will be sorted through.

# below are key value pairs, the extensions of the files you want to move are the values, 
# the directory you want it to end up in is a combination of "home_path" variable and the key
formats = {
    "/Pictures/" : ("jpeg", "jpg", "png", "gif", "bmp"),
    "/Documents/" : ("pdf", "doc", "docx", "html", "log", "swf", "txt", "odt"),
    "/Archive/" : ("rar", "zip", "7z", "tar"),
    "/Application/" : ("exe", "msi"),
    "/delete/" : ("torrent", "dll", "save", "iso", "yaml", "py", "cfg")
}

# parses filenames to narrow down the results to an extension.
def find_extension(file):
    split_elements = file.split(".") 
    last_element = len(split_elements)
    return split_elements[last_element-1]

# figures out the new directory of the file where it will be moved.
def establish_location(ext):
    new_directory = [k for k, v in formats.items() if ext in v].pop() # look through dict and find the key matching the value of the extension
    return f"{destination_path}{new_directory}"

# standard method for cleaning up strings.
def cleaner(path):
    brain_path = [f"{home_path}{path}"]
    special_characters = "[]\'\""
    check_path = str(brain_path[0])
    return check_path

# the primary logic of the script, it will establish if it needs to delete a file or not and move it to it's new location.
def sort_file_logic(old,new,delete):
    if "delete" in delete:
        try:
            os.remove(f"{old}")
        except OSError as e:
            print(e)
    else:
        os.replace(src=old,dst=new)

# main logic in charge of parsing outputs, error handling and looping the application 
def main():
    for folders in affected_folder:
        path = cleaner(folders)
        directory_list = os.listdir(path)
        for file in directory_list:
            folder = os.path.isdir(file)
            if folder == False:
                ext = find_extension(file)
                try:
                    old_location = f"{path}{file}"
                    new_location = f"{establish_location(ext)}{file}"
                    try:
                        sort_file_logic(old=old_location,new=new_location,delete=establish_location(ext))
                    except FileNotFoundError: # if you want to add a new directory and new extensions in the dict above this will create the directory and recursivly run the function to continue the output
                        if "delete" not in establish_location(ext):
                            os.mkdir(establish_location(ext))                
                            main()
                except IndexError as e:
                    print(f"indexerror: {e}")
                except PermissionError as b:
                    print(f"perission error: {b}")
                
                    
            

if __name__=="__main__":
    main()