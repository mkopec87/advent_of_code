def load_data(debug: bool) -> str:
    if debug:
        with open("sample_input.txt") as f:
            d = f.read()
    else:
        from aocd import data

        d = data
    print(f"{len(d.splitlines())} lines read [debug={debug}]")
    return d
