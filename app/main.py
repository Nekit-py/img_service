from typing import List, Optional
from db_manager import DBManager
from fastapi import (
        FastAPI, UploadFile,
        File, Form, Query,
        HTTPException,
        )
from fastapi.responses import (
        HTMLResponse, FileResponse,
        Response, StreamingResponse,
        )


dbm = DBManager()
app = FastAPI(debug=True)

@app.post("/uploadimg/")
async def upload_image(img_tag: str="other", files: List[UploadFile]=File(...)):
    """
    Uploading files
    :param img_tag: str: image tag
    :param files: List[UploadFile]: list of uploaded files
    :return dict where key is image tags and value is list of file names
    """
    if not files:
        raise HTTPException(status_code=404, detail="List of upload files is empty")
    for img in files:
        img_data = img.file.read()
        dbm.append_row(img_tag, img.filename, img_data)
    return {img_tag: [img.filename for file in files]}

@app.get("/showimg/")
async def show_img(img_name: str):
    """
    Shows an image by the specified name
    :param img_name: str: the name of the file to show
    """
    if not img_name:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(content=dbm.get_image(img_name), media_type="image/jpg")

@app.get("/downloadimage/")
def download_file(img_name: str):
    """
    Downloads an image by the specified name
    :params img_name: str: the name of the file to download
    """
    if not img_name:
        raise HTTPException(status_code=404, detail="Item not found")
    def iter_image():
        yield from dbm.get_image(img_name, True)
    return StreamingResponse(iter_image(), media_type="application/octet-stream")

@app.get("/imglist/")
async def show_img_list(images: Optional[List[str]]=Query(None)):
    """
    A list of files and their tags stored in the database
    :param images: Optional[List[str]: image name list
    :return returns a list of dicts where the key is the tag name and the value is the file name
    """
    return dbm.show_img_list(images)

@app.get("/tagfilter/")
async def show_img_by_tags(tags: Optional[List[str]]=Query(None)):
    """
    Filters the image by tags
    :param images: Optional[List[str]: tas list
    :return images filtered by tags
    """
    return dbm.filter_by_tag(tags)

@app.get("/")
async def main():
    """
    Index page
    """
    return "Welcome to the image service."
