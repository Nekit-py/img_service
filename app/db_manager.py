import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import Optional, List


load_dotenv(".env")

USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DATA_BASE = os.environ.get("DATA_BASE")

class DBManager:
    """
    The class is responsible for working with the PostgreSQL database
    """

    def __init__(self):
        self.con = psycopg2.connect(user=USER,
                                password=PASSWORD,
                                host=HOST,
                                port=PORT,
                                )

        self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.con.cursor()
        self.cur.execute("SELECT datname FROM pg_database;")
        list_database = self.cur.fetchall()

        if not (DATA_BASE,) in list_database:
            self.cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DATA_BASE))
                )
        self.cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'IMAGES_DATA_TABLE');")
        if self.cur.fetchone()[0]:
            create_table_query = """
                CREATE TABLE IMAGES_DATA_TABLE (
                    id serial primary key,
                    img_tag text not null,
                    file_name text not null,
                    file_data bytea not null
                )
            """
            self.cur.execute(create_table_query)
            self.con.commit()

    def append_row(self, img_tag: str, file_name: str, file_data: bytes):
        """
        Adds image data to the database
        :param: img_tag: str: image tag name
        :param: file_name: str: uploaded file name
        :param: file_data: bytes: uploaded file in byte representation
        """
        self.cur.execute(f"INSERT INTO IMAGES_DATA_TABLE (id, img_tag, file_name, file_data) VALUES (DEFAULT, %s, %s, %s)",
                (img_tag, file_name, file_data))
        self.con.commit()

    def show_img_list(self, images: Optional[List[str]]) -> list[tuple[str]]:
        """
        A list of files and their tags stored in the database
        :param images: Optional[List[str]: image name list
        :return returns a list of dicts where the key is the tag name and the value is the file name
        """
        if images:
            self.cur.execute("SELECT img_tag, file_name from IMAGES_DATA_TABLE WHERE file_name IN %s", (tuple(images), ))
        else:
            self.cur.execute("SELECT img_tag, file_name from IMAGES_DATA_TABLE")
        cols = ("img_tag", "file_name")
        img_list = [dict(zip(cols, row)) for row in self.cur.fetchall()]
        return img_list

    def filter_by_tag(self, tags: list[str]) -> list[tuple[str]]:
        """
        Filters the image by tags
        :param images: Optional[List[str]: tas list
        :return images filtered by tags
        """
        self.cur.execute("SELECT img_tag, file_name from IMAGES_DATA_TABLE WHERE img_tag IN %s", (tuple(tags), ))
        cols = ("img_tag", "file_name")
        filtered_by_tag_img_list = [dict(zip(cols, row)) for row in self.cur.fetchall()]
        return filtered_by_tag_img_list

    def get_image(self, file_name: str, download: bool = False) -> bytes:
        """
        Displays the required image for viewing, or downloads it
        :param: file_name: str: name of the image to view/download
        :param: download: bool: in order to download an image, you need to set download=True
        """
        self.cur.execute("SELECT file_name, file_data from IMAGES_DATA_TABLE WHERE file_name = %s", (file_name, ))
        name, file_bytes = self.cur.fetchone()
        return file_bytes if download else bytes(file_bytes)

    def _trancate_table(self, table_name: str) -> None:
        """
        Clearing the table
        """
        self.cur.execute(f"Truncate {table_name};")
