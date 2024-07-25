from textnode import *
from htmlnode import *
from split_delimiter import *
from markdown_blocks import *
from markdown_to_html import *
from move_dir import *
import re


def main():
    source_path_dir = "/home/bilsby/Workspace/Projects/public/static"
    destination_path_dir = "/home/bilsby/Workspace/Projects/public/public"
    move_dir_contents(source_path_dir, destination_path_dir)

    markdown_dir_path = "/home/bilsby/Workspace/Projects/public/content"
    template_path = "/home/bilsby/Workspace/Projects/public/template.html"
    destination_path = "/home/bilsby/Workspace/Projects/public/public"

    generate_pages_recursive(markdown_dir_path, template_path, destination_path)


def generate_pages_recursive(markdown_dir_path, template_path, destination_path):
    if markdown_dir_path.startswith("/home/bilsby/Workspace/Projects") == False:
        return
    if destination_path.startswith("/home/bilsby/Workspace/Projects") == False:
        return
    
    if os.path.exists(destination_path) == False:
        os.mkdir(destination_path)
        print(f"Creating directory '{destination_path}'")
    
    if os.path.exists(markdown_dir_path):
        contents_list = os.listdir(markdown_dir_path)
        print(f"Searching for markdown files in {markdown_dir_path}")
        print(f"Contents: {contents_list}")
        for file in contents_list:
            file_path = os.path.join(markdown_dir_path, file)
            if os.path.isfile(file_path) and file_path.endswith(".md"):
                markdown_file_name = file_path.split("/")[-1]
                print(f"Markdown file found: {markdown_file_name}. Converting...")
                markdown_file = open(file_path, "r")
                markdown = markdown_file.read()
                nodes = markdown_to_html_node(markdown)
                contents = nodes.to_html()
                title = extract_title(markdown)

                shutil.copy(template_path, destination_path)
                template_file_name = template_path.split("/")[-1]
                new_template_path = os.path.join(destination_path, template_file_name)
                template_file = open(new_template_path, "r")
                template_contents = template_file.read()
                template_file.close()

                updated_contents = template_contents.replace("{{ Title }}", title)
                final_contents = updated_contents.replace("{{ Content }}", contents)
                template_file_write = open(new_template_path, "w")
                template_file_write.write(final_contents)
                rename =  os.path.join(destination_path, "index.html")
                os.rename(new_template_path, rename)

                template_file.close()
                markdown_file.close()

        for directory in contents_list:
            directory_path = os.path.join(markdown_dir_path, directory)
            if os.path.isdir(directory_path):
                new_markdown_dir_path = os.path.join(markdown_dir_path, directory)
                new_destination_path = os.path.join(destination_path, directory)
                generate_pages_recursive(new_markdown_dir_path, template_path, new_destination_path)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        for i in range(0, 5):
            heading_count = block[0:6].count("#")
            clean_block = block[heading_count + 1::]
            if heading_count == 1:
                return clean_block
            else:
                raise Exception("Invalid markdown - No title found")

main()
