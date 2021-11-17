def merge_files(input_path: str, bibliography_path: str) -> None:
    with open(input_path, 'br') as f:
        content = f.read()

    with open(bibliography_path, 'ba') as f:
        f.write(b'\n')
        f.write(content)

    with open(input_path, 'w'):
        pass
