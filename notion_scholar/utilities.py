class NotionScholarError(Exception):
    """A base class for notion-scholar exceptions."""


def append_string_to_file(string: str, file_path: str):
    with open(file_path, 'a') as f:
        f.write('\n')
        f.write(string)


def merge_files(input_path: str, output_file: str) -> None:
    with open(input_path, 'br') as f:
        content = f.read()

    with open(output_file, 'ba') as f:
        f.write(b'\n')
        f.write(content)


def clean_file(file_path: str) -> None:
    with open(file_path, 'w'):
        pass
