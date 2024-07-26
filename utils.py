import os, shutil, base64, re

def is_base64_image(data):
    base64_pattern = re.compile(r'^data:image/(png|jpeg|jpg);base64,([A-Za-z0-9+/=]+)$')
    return base64_pattern.match(data)


def makedir(dir_path):
    try:
        os.makedirs(dir_path)
    except FileExistsError:
        pass

def emptydir(dir,delete_dirs=False):
    # loop through all the files and subdirectories in the directory
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path):
                # remove the file
                print(f"{file_path} deleted")
                os.remove(file_path)
            elif delete_dirs and os.path.isdir(file_path):
                # remove the subdirectory and its contents
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

