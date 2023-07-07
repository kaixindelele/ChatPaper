import os
import re
import shutil

def replace_title(save_to_path, title):
    # Define input and output file names
    input_file_name = os.path.join(save_to_path, "template.tex")
    output_file_name = os.path.join(save_to_path , "main.tex")

    # Open the input file and read its content
    with open(input_file_name, 'r') as infile:
        content = infile.read()
    content = content.replace(r"\title{TITLE} ", f"\\title{{{title}}} ")

    # Open the output file and write the modified content
    with open(output_file_name, 'w') as outfile:
        outfile.write(content)


# return all string in \cite{...} \citet{...} or \citep{...}.

# check if citations are in bibtex.

# replace citations

# sometimes the output may include thebibliography and bibitem . remove all of it.

# return all .png and replace it using placeholder.

def find_tex_files(directory_path):
    tex_files = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".tex"):
            tex_files.append(filename)

    return tex_files

def find_figure_names(tex_file_path):
    # Regular expression pattern to find \includegraphics commands
    pattern = r'\\includegraphics.*?{(.*?)}'
    with open(tex_file_path, 'r') as file:
        content = file.read()
    # Find all matches in the file content
    matches = re.findall(pattern, content)
    # Matches will be a list of figure names
    return matches

def create_copies(output_dir):
    tex_files = find_tex_files(output_dir)
    for tex_file in tex_files:
        path =  os.path.join(output_dir, tex_file)
        all_figs = find_figure_names(path)
        for fig in all_figs:
            original_fig = os.path.join(output_dir, "fig.png")
            target_fig = os.path.join(output_dir, fig)
            shutil.copy2(original_fig, target_fig)


# todo: post-processing the generated algorithm for correct compile.



if __name__ == "__main__":
    pass



