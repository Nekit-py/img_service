# Веб-апи сервис для сохранения изображений и тегов к ним.
### Возможности сервиса:
- Получение списка изображений и их тегов;
-  Фильтрация изображений по тегам;
-  Скачивание/просмотр изображений;
	>Для хранения информации используется реляционная СУБД PostgreSQL.

### Загрузка файлов
Загрузка файлов осуществляется с помощью функции **upload_images**, которая принимает на вход имя тега подгружаемых файлов и сами файлы.
```python
@app.post("/uploadimg/")
async def upload_image(img_tag: str, files: List[UploadFile]=File(...)):
	...
```
### Пример:
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/uploadimg/?img_tag=cats' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@kitty_1.jpg;type=image/jpeg' \
  -F 'files=@kitty_2.jpg;type=image/jpeg'
```
### Получение списка изображений

Функция **show_img_list** возвращает из базы список всех изображений и их тэгов. На вход принимает список изображений в виде строк. По умолчанию функция возвращает список всех изображений.
```python
@app.get("/imglist/")
async def show_img_list(images: Optional[List[str]] = Query(None)):
	...
```
### Пример:
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/imglist/?images=kitty_1.jpg&images=dog_2.jpg' \
  -H 'accept: application/json'
```

### Фильтрация по тегам
Функция **filter_by_tag** на вход принимает список тегов в виде строк.  Возвращает список всех изображений по заданному тегу.
```python
@app.get("/tagfilter/")
async def show_img_by_tags(tags: Optional[List[str]] = Query(None)):
	...
```
### Пример:
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/tagfilter/?tags=cats' \
  -H 'accept: application/json'
```
### Просмотр   изображения
Функция **show_img** позволяет осуществить просмотр изображения. На вход принимает имя файла в виде строки, который необходимо просмотреть.
```python
@app.get("/downloadimage/")
def show_img(img_name: str):
	...
```
### Пример:
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/showimg/?img_name=dog_2.jpg' \
  -H 'accept: application/json'
```
### Скачивание   изображения
Функция **download_file** позволяет осуществить скачивание изображения. На вход принимает имя файла в виде строки, который необходимо скачать.
```python
@app.get("/downloadimage/")
def download_file(img_name: str):
	...
```
### Пример:
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/downloadimage/?img_name=kitty_1.jpg' \
  -H 'accept: application/json'
```
