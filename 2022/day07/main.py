import re


class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.files = {}

    def get_child(self, name):
        if name not in self.children:
            self.children[name] = Folder(name, self)
        return self.children[name]

    def add_file(self, name, size):
        self.files[name] = size

    def size(self):
        local_size = sum(self.files.values())
        for child in self.children.values():
            local_size += child.size()
        return local_size

    def __str__(self):
        s = ""
        f = self
        while f is not None:
            s = f.name + "/" + s
            f = f.parent
        return s


def rec_find_sizes(folder, result):
    folder_str = str(folder)
    if folder_str not in result:
        result[folder_str] = folder.size()
    for ch in folder.children.values():
        rec_find_sizes(ch, result)


def main():
    with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    print(f"{len(lines)} lines read")

    root = Folder("/")
    current_folder = root
    for line in lines:
        if line.startswith("dir"):
            continue
        elif line.startswith("$ cd"):
            target = re.match(r"\$ cd (.*)", line).group(1)
            if target == "..":
                current_folder = current_folder.parent
            elif target == "/":
                current_folder = root
            else:
                child_folder = current_folder.get_child(target)
                current_folder = child_folder
        elif m := re.match(r"(\d+) (.*)", line):
            file_size = int(m.group(1))
            file_name = m.group(2)
            current_folder.add_file(file_name, file_size)

    folder_to_size = {}
    rec_find_sizes(root, folder_to_size)

    result_part1 = sum(filter(lambda s: s < 100_000, folder_to_size.values()))
    print(f"Result part 1: {result_part1}")

    min_folder_size = 30000000 - (70000000 - folder_to_size["//"])
    result_part2 = min(filter(lambda c: c >= min_folder_size, folder_to_size.values()))
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
