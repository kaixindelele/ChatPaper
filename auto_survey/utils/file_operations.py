import hashlib
import os, shutil
import datetime
from utils.tex_processing import replace_title
import re

def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)
    return s

def hash_name(input_dict):
    '''
    input_dict= {"title": title, "description": description}

    For same input_dict, it should return the same value.
    '''
    name = str(input_dict)
    name = name.lower()
    md5 = hashlib.md5()
    md5.update(name.encode('utf-8'))
    hashed_string = md5.hexdigest()
    return hashed_string



def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format), source+'/'+destination)
    return destination

def copy_templates(template, title):
    # Create a copy in the outputs folder.
    #   1. create a folder "outputs_%Y%m%d_%H%M%S" (destination_folder)
    #   2. copy all contents in "latex_templates/{template}" to that folder
    #   3. return (bibtex_path, destination_folder)
    now = datetime.datetime.now()
    target_name = now.strftime("outputs_%Y%m%d_%H%M%S")
    source_folder = f"utils/latex_templates/{template}"
    destination_folder = f"outputs/{target_name}"
    shutil.copytree(source_folder, destination_folder)
    bibtex_path = os.path.join(destination_folder, "ref.bib")
    # bibtex_path = destination_folder + "/ref.bib"
    replace_title(destination_folder, title)
    return bibtex_path, destination_folder

def list_folders(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]



