import random
import re

suffix_set = {
    "",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "X",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
}
roman_plus_number_regex = "M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$|\d$"


def combine_files(filename1, filename2):
    outfile_name = "data/combined_albums.txt"
    outfile = open(outfile_name, "w")
    for line in open(filename1, "r").readlines():
        outfile.write(line)

    for line in open(filename2, "r").readlines():
        outfile.write(line)

    remove_dup_names(outfile_name)
    scramble_txt(outfile_name)


def remove_dup_names(filename):
    lines = None
    with open(filename, "r") as infile:
        lines = set(infile.readlines())
    with open(filename, "w") as outfile:
        for line in lines:
            outfile.write(line)


def generate_numbered_names(filename):
    prog = re.compile(roman_plus_number_regex)
    outfile_name = filename.split(".")[0] + "_generated.txt"
    with open(outfile_name, "w") as outfile:
        with open(filename, "r") as infile:
            for line in infile:
                sub = prog.sub("", line).strip()
                gen_names = _generate_permutation(sub)
                for name in gen_names:
                    outfile.write(name + "\n")


def _generate_permutation(string):
    return [string + " " + suffix for suffix in random.sample(suffix_set, 3)]


def scramble_txt(filename):
    content = None
    with open(filename) as f:
        content = f.readlines()
    random.shuffle(content)
    with open(filename, "w") as f:
        for line in content:
            f.write(line)
