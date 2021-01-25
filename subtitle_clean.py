import re, os
import concurrent.futures

# Loading -> cleaning -> saving cleaned versions
new_file_dir = r"C:\Users\Tijs\Documents\Universiteit Tijs\First Year MSc\TxMM\project_data\CleanedSubtitles"
subtitle_re = re.compile(
    "(\d+\n[\d\:\,\W]+\n)|(\[[\w*\d*\s*]*[^\[]+[\w*\d*\s*]*\])|(<i>)|(<\/i>)|(\(([A-Z]\s*\W*l*[a-z]*)*\))|(\{\d*\})|(<[\w*\d*\s*]*[^<]+[\w*\d*\s*]*>)|(\[[\w*\d*\s*]*[^\[]+[\w*\d*\s*]*\])")


def clean(paths_names):
    ### srt_nontext = re.compile("(\d+\n[\d\:\,\W]+\n)|(\[[\w*\d*\s*]*[^\[]+[\w*\d*\s*]*\])|(<i>)|(<\/i>)|(\(([A-Z]\s*\W*l*[a-z]*)*\))") 
    # Regex above is for '.srt' files - matches specific non-text lines (subtitle timing info etc.) and info for the 
    # hearing impaired (which is not needed). Test/demo: https://regex101.com/r/HzgKov/7
    #### sub_nontext = re.compile("\{\d*\}")
    # Regex above is for '.sub' files - matches specific non-text elements. Test/demo: https://regex101.com/r/0wV1Q1/1
    #### smi_nontext = re.compile("(<[\w*\d*\s*]*[^<]+[\w*\d*\s*]*>)")
    # Regex above is for '.smi' files - matches specific non-text elements (subtitle timing info etc.). 
    # Test/demo: https://regex101.com/r/5YJfHy/1
    #### txt_nontext = re.compile("(\[[\w*\d*\s*]*[^\[]+[\w*\d*\s*]*\])")
    # Regex above is for '.txt' files - matches specific non-text elements (subtitle timing info etc.). 
    # Test/demo: https://regex101.com/r/J6P0dE/1
    # Also, for .txt subtitle files, we can simply remove the first 12 lines, thereby removing useless metadata (and actually
    # prevent this metadata from contaminating the actual data)

    file_path = paths_names[0]
    file_name = paths_names[1]
    title = file_name
    with open(file_path, encoding='utf-8', errors='ignore') as file_text:
        subtitle_text = file_text.read()

    subtitle_text_cleaned = subtitle_re.sub(' ', subtitle_text) # Replacing stuff with whitespaces instead of just 
    # deleting, because otherwise some words might be incorrectly contracted.

    if file_name.endswith(".srt"):
        title = title.replace(".srt", "")
        new_file_name = title + ".txt"

    elif file_name.endswith(".sub"):
        title = title.replace(".sub", "")
        new_file_name = title + ".txt"
        subtitle_text_cleaned = subtitle_text_cleaned.replace('|', ' ')  # Replacing the barriers '|' that occur in .sub
        # files with whitespaces instead of just deleting, because again otherwise some words might be incorrectly contracted.

    elif file_name.endswith(".smi"):
        title = title.replace(".smi", "")
        new_file_name = title + ".txt"

    elif file_name.endswith(".txt"):
        title = title.replace(".txt", "")
        new_file_name = title + ".txt"

    new_file_path = os.path.join(new_file_dir, new_file_name)
    with open(new_file_path, mode='w', encoding='utf-8') as cleaned_file:
        cleaned_file.write(subtitle_text_cleaned)


def run(paths_names):
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        executor.map(clean, paths_names)


def main():
    scandir_imp = os.scandir(r"C:\Users\Tijs\Documents\Universiteit Tijs\First Year MSc\TxMM\project_data\Subtitles")
    file_paths = []
    file_names = []
    for file in scandir_imp:
        file_paths.append(file.path)
        file_names.append(file.name)
    scandir_non_imp = os.scandir(r"C:\Users\Tijs\Documents\Universiteit Tijs\First Year MSc\TxMM\project_data\NonImpairedSubtitles")
    for file in scandir_non_imp:
        file_paths.append(file.path)
        file_names.append(file.name)

    paths_names = zip(file_paths, file_names)
    
    run(paths_names)


if __name__ == "__main__":
    main()
