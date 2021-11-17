from pathlib import Path


project_path = Path(__file__).parent.parent
data_directory_path = project_path.joinpath('data')
input_path = data_directory_path.joinpath('input.bib')
bibliography_path = data_directory_path.joinpath('bibliography.bib')

database_url = ""
token = ""
