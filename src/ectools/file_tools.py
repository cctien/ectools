def keep_first_n_lines(file_path: str, n: int):
    with open(file_path, "r") as file:
        lines = file.readlines()
    kept_lines = lines[:n]
    with open(file_path, "w") as file:
        file.writelines(kept_lines)
