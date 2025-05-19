import mysql.connector          # MySQL 데이터베이스에 연결하기 위한 라이브러리
from src.database import Database 

class NoteRepository:
    def __init__(self, database: Database):
        self.conn = database.conn
        self.cursor = database.cursor
        
    """기록 불러오기"""
    def fetch_note(self):
        self.cursor.execute("SELECT * FROM notes")
        results = self.cursor.fetchall()
        return {note['id']: note for note in results}
    
    """새 메모 추가 후 저장"""
    def save_note(self, title, schedule_date, content, image_path):
        try:
            sql = "INSERT INTO notes (title, schedule_date, content, image_path) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql,(title, schedule_date, content, image_path))
            self.conn.commit()
            return self.connector.lastrowid
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"[❌오류] 저장오류: {e}")
        return None
    
    """기록 업데이트"""
    def update_note(self, note_id, title=None, schedule_date=None, content=None, image_path = None):
        try:    
            if title is not None:
                self.cursor.execute("UPDATE notes SET title = %s WHERE id = %s", (title, note_id))
            if schedule_date is not None:
                self.cursor.execute("UPDATE notes SET schedule_date = %s WHERE id = %s", (schedule_date, note_id))
            if content is not None:
                self.cursor.execute("UPDATE notes SET content = %s WHERE id = %s", (content,note_id))
            if image_path is not None:
                self.cursor.execute("UPDATE notes SET image_path = %s WHERE id = %s", (image_path,note_id))
            self.conn.commit() # DB에 올리기
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"[❌오류] 수정오류: {e}")
    """기록 삭제"""
    def delete_note(self, note_id):
        try:
            self.cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,)) #SQL DB에 삭제하는 명령어
            self.conn.commit() # DB에 올리기
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"[❌오류] 삭제오류: {e}")

    """기록 찾기"""
    def note_exists(self, note_id):
        self.cursor.execute("SELECT 1 FROM notes WHERE id = %s", (note_id,)) # DB에서 SQL명령어로로 id 존재하는지 찾기
        result = self.cursor.fetchone()  
        return result is not None
    
    """명령어 닫기"""
    def __del__(self):
        self.cursor.close() # cusor 닫기
        self.conn.close()   # conn 닫기기