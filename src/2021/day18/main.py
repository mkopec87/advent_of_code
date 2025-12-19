INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"


class Node:
    def __init__(self, left=None, right=None, value=None, parent=None):
        self.left = left
        self.right = right
        self.value = value
        self.leaf = value is not None
        self.parent = parent

    def depth(self):
        d = 0
        p = self.parent
        while p:
            p = p.parent
            d += 1
        return d

    def magnitude(self):
        if self.leaf:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, other):
        added = Node(left=self, right=other)
        self.parent = added
        other.parent = added
        while added.reduce():
            pass
        return added

    def reduce(self):
        leaves = self.leaves()

        exploding_pair = next(
            (node.parent for node in leaves if node.depth() == 5), None
        )
        if exploding_pair:
            print(f"Exploding pair: {exploding_pair}")

            left_neighbour_index = leaves.index(exploding_pair.left) - 1
            if left_neighbour_index >= 0:
                leaves[left_neighbour_index].value += exploding_pair.left.value

            right_neighbour_index = leaves.index(exploding_pair.right) + 1
            if right_neighbour_index < len(leaves):
                leaves[right_neighbour_index].value += exploding_pair.right.value

            parent = exploding_pair.parent
            new_node = Node(value=0, parent=parent)
            if parent.left == exploding_pair:
                parent.left = new_node
            else:
                parent.right = new_node
            return True

        splitting_node = next((node for node in leaves if node.value > 9), None)
        if splitting_node:
            left_val = int(splitting_node.value / 2)
            right_val = splitting_node.value - left_val
            print(f"Splitting node: {splitting_node} into {left_val}, {right_val}")
            parent = splitting_node.parent
            new_node = Node(parent=parent)
            new_left = Node(value=left_val, parent=new_node)
            new_right = Node(value=right_val, parent=new_node)
            new_node.left = new_left
            new_node.right = new_right
            if parent.left == splitting_node:
                parent.left = new_node
            else:
                parent.right = new_node
            return True

        return False

    def leaves(self) -> list["Node"]:
        if self.leaf:
            return [self]
        else:
            r = []
            r.extend(self.left.leaves())
            r.extend(self.right.leaves())
            return r

    def __str__(self):
        if self.leaf:
            return str(self.value)
        return f"[{self.left},{self.right}]"


def parse(line, parent=None) -> Node:
    def find_comma_index(line):
        opened = 0
        for i, ch in enumerate(line):
            if ch == "[":
                opened += 1
            elif ch == "]":
                opened -= 1
            elif ch == "," and opened == 0:
                return i

    if line[0] == "[":
        line = line[1:-1]  # drop brackets

        # find splitting comma
        comma_index = find_comma_index(line)
        part1 = line[:comma_index]
        part2 = line[comma_index + 1 :]

        node = Node(parent=parent)
        node.left = parse(part1, parent=node)
        node.right = parse(part2, parent=node)
        return node

    else:
        return Node(value=int(line[0]), parent=parent)


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    max_mag = -1
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue
            first = parse(lines[i])
            second = parse(lines[j])
            first += second
            max_mag = max(max_mag, first.magnitude())

    total = parse(lines[0])
    for line in lines[1:]:
        number = parse(line)
        total += number

    result_part1 = total.magnitude()
    result_part2 = max_mag

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
