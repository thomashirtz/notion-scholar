from pathlib import Path
from notion_scholar.bibtex import get_bib_database_from_file
from urllib.parse import quote


def check_missing_and_extra_pdfs(bibtex_path, folder_path):
    """
    Checks for missing and extra PDF files in a folder compared to a BibTeX file.

    This function reads a BibTeX file, retrieves all its entries (with their titles),
    and compares the BibTeX keys (IDs) with the list of PDF files in a specified folder.
    The PDFs should follow the naming convention '<bibtex_key>.pdf'. The function identifies:

    1. Missing PDFs: BibTeX entries that do not have a corresponding PDF file in the folder.
    2. Extra PDFs: PDF files in the folder that do not correspond to any BibTeX entries.

    For each missing PDF, the function prints the BibTeX key, title, and provides a Google Scholar
    search link for the missing entry, based on the title.

    Args:
        bibtex_path (str or Path): The file path to the BibTeX (.bib) file.
        folder_path (str or Path): The folder path where the corresponding PDF files are located.

    Example:
        >>> bibtex_path = Path(r"/resources\sample.bib")
        >>> folder_path = Path(r"/resources")
        >>> check_missing_and_extra_pdfs(bibtex_path, folder_path)

    Output:
        The function prints:
        - Missing PDFs with BibTeX key, title, and a Google Scholar search link.
        - Extra PDFs in the folder that are not present in the BibTeX file.
    """

    # Step 1: Get the BibTeX database from the .bib file
    bib_database = get_bib_database_from_file(bibtex_path)

    # Extract a dictionary of {ID: title} from the BibTeX database
    bib_entries = {entry['ID']: entry.get('title', 'No title available') for entry in bib_database.entries}

    # Step 2: Get the list of PDF files in the folder
    folder = Path(folder_path)
    pdf_files = [file.stem for file in folder.glob("*.pdf")]  # Use stem to get filename without extension

    # Step 3: Find missing PDFs (keys in BibTeX but no PDF in the folder)
    missing_pdfs = {key: bib_entries[key] for key in bib_entries if key not in pdf_files}

    # Step 4: Find extra PDFs (PDFs in the folder that are not in the BibTeX file)
    extra_pdfs = [pdf for pdf in pdf_files if pdf not in bib_entries]

    # Step 5: Print the results
    if missing_pdfs:
        print("Missing PDFs (these entries are in the .bib file but no corresponding PDF is found):")
        for key, title in missing_pdfs.items():
            # Encode the title for URL
            encoded_title = quote(title)
            google_scholar_link = f"https://scholar.google.com/scholar?q={encoded_title}"
            print(f"- {key}.pdf : {title}")
            print(f"  {google_scholar_link}")
    else:
        print("All BibTeX entries have corresponding PDFs.")

    if extra_pdfs:
        print("\nExtra PDFs (these PDFs are in the folder but not in the .bib file):")
        for pdf in extra_pdfs:
            print(f"- {pdf}.pdf")
    else:
        print("No extra PDFs in the folder.")


if __name__ == '__main__':
    bibtex_path = Path(r"/resources\sample.bib")
    folder_path = Path(r"/resources")
    check_missing_and_extra_pdfs(bibtex_path, folder_path)
