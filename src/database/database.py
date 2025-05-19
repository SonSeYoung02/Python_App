import mysql.connector          # MySQL 데이터베이스에 연결하기 위한 라이브러리
import os                       # 파일 경로 처리 및 현재 파일 위치 탐색에 사용
from dotenv import load_dotenv  #.env 파일에 저장된 환경변수 불러오기(sql 비밀번호)
from pathlib import Path

class Database:
    """MySQL 연결 및 초기화 관리 클래스"""
    def __init__(self):
        self._load_env()
        self._connect_db()
        self._initialize_db()
    
    def _load_env(self):
        """환경변수(.env)에서 DB 접속 정보 로드"""
        load_dotenv() # 환경변수 불러오기
        try:
            self.host = os.environ["DB_HOST"]
            self.user = os.environ["DB_USER"]
            self.password = os.environ["DB_PASSWORD"]
            self.database = os.environ["DB_NAME"]
            self.port = int(os.environ["DB_PORT"])
        except KeyError as e:
            raise RuntimeError(f"[❌오류] .env 설정 누락: {e}")

    def _connect_db(self):
        """MySQL 데이터베이스 연결"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as e:
            raise RuntimeError(f"[❌오류] DB 연결 실패: {e}")

    def _initialize_db(self):
        """init.sql을 실행하여 DB 초기 테이블 생성"""
        self._first_init_sql()

    def _first_init_sql(self,filepath=None):
        """init.sql 파일을 읽어 SQL 실행"""
        if filepath is None: # 내부에서 항상 절대경로로 처리리
            base_dir = Path(__file__).resolve().parent.parent.parent
            filepath = base_dir/"db"/"init.sql"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                sql = f.read()
                for statement in sql.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        try:
                            self.cursor.execute(stmt)
                        except mysql.connector.Error as e:
                            print(f"[❌오류] SQL실행오류: {e}")
                self.conn.commit()
        except FileExistsError:
            print(f"[❌오류] init.sql 파일을 찾을 수 없습니다: {filepath}")

    