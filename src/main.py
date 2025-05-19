from src.utils.note_ui import NoteUI
from src.utils import NoteManager
from src.database import Database
from src.repository import NoteRepository

def main():
    database = Database()
    note_repository = NoteRepository(database)
    note_manager = NoteManager(note_repository)
    note_ui = NoteUI(note_manager)
    note_ui.ui()

if __name__ == "__main__":
    main()