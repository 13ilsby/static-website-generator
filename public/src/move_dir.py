import shutil
import os

def move_dir_contents(source_path, destination_path):
    if source_path.startswith("/home/bilsby/Workspace/Projects") == False:
        return
    if destination_path.startswith("/home/bilsby/Workspace/Projects") == False:
        return
    
    destination_dir_name = destination_path.split("/")[-1]
    destination_parent = destination_path.split("/")[-2]

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path, destination_dir_name)
        print(f"Deleting {destination_dir_name} and its contents from {destination_path}")
    
    os.mkdir(destination_path)
    print(f"Creating directory '{destination_dir_name}' in {destination_parent}")
    
    if os.path.exists(destination_path):
        contents_list = os.listdir(source_path)
        print(f"Accessing {source_path}")
        print(f"Contents: {contents_list}")
        for file in contents_list:
            file_path = os.path.join(source_path, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination_path)
                print(f"Copying file '{file}' from {file_path} to {destination_path}")
    
        for directory in contents_list:
            directory_path = os.path.join(source_path, directory)
            if os.path.isdir(directory_path):
                dst_directory_path = os.path.join(destination_path, directory)
                move_dir_contents(directory_path, dst_directory_path)
