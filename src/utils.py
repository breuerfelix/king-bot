def log(message: str):
    print(message)


def check_for_lines(path: str, current_lines: list) -> dict:
    lines_to_add: list = []
    lines_to_remove: list = []

    with open(path, "r") as file:
        lines = file.read().splitlines()

    for line in lines:
        if line not in current_lines:
            log("new line: " + str(line))
            lines_to_add.append(line)

    for job in current_lines:
        if job not in lines:
            log("removed / changed line: " + str(line))
            lines_to_remove.append(job)

    return {'add': lines_to_add, 'remove': lines_to_remove}
