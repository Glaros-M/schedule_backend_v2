import datetime
from flask import Flask, make_response
from flask import request
import logging
# wsgi server
from waitress import serve
import os

import view_generator
from log_handlers import DBHandler
import download_data
from upload_data import upload_file, save_file
from view_generator import get_table_by_group_name, get_table_by_teacher_name
from config import LOG_LVL, PORT, VERSION, SYSTEM_TYPE

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

if not os.path.exists('logs'):
    os.mkdir('logs')
if not os.path.exists('files'):
    os.mkdir('files')

logger = logging.getLogger("INFO")
logger.setLevel(LOG_LVL)

info_file_handler = logging.FileHandler(f"logs/info {datetime.date.today()}.log", mode='a')
info_console_handler = logging.StreamHandler()
info_formatter = logging.Formatter(f"%(levelname)s %(asctime)s %(module)s > %(message)s ")
info_file_handler.setFormatter(info_formatter)
info_console_handler.setFormatter(info_formatter)
logger.addHandler(info_file_handler)
logger.addHandler(info_console_handler)
db_handler = DBHandler(level=logging.INFO)
logger.addHandler(db_handler)


@app.route("/")
def hello_world():
    logger.info(f"get /")
    resp = make_response("hello world")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.get("/status")
def get_status() -> dict:
    logger.info(f"get status")
    out = {"status": "ok"}
    return out


@app.get("/groups")
def get_all_groups() -> dict:
    logger.info(f"get groups")
    grops_list = download_data.get_groups_list()
    out = {"groups": grops_list}
    return out


@app.get("/schedule")
def get_schedule_by_group_name() -> str:  # Возвращается шаблон
    group_name = request.args.get('group_name')
    logger.info(f"get schedule for |{group_name}| ")
    if not group_name or group_name == "" or group_name == " ":
        out = "<h2>Пожалуйста, введите корректный номер группы или выберите из списка!</h2>"
        return out
    out = get_table_by_group_name(group_name=group_name)
    return out


@app.get("/teachers")
def get_all_teachers() -> dict:
    logger.info(f"get teachers")
    teachers_list = download_data.get_teachers_list()
    out = {"teachers": teachers_list}
    return out


@app.get("/teacher")
def get_teacher_schedule() -> str:  # Возвращает шаблон
    teacher = request.args.get('teacher_name')
    logger.info(f"get teacher's schedule for |{teacher}| ")
    if not teacher or teacher == "" or teacher == " ":
        out = "<h2>Пожалуйста, введите корректно Фамилию и инициалы преподавателя или выберите из списка!</h2>"
        return out
    out = get_table_by_teacher_name(teacher=teacher)
    return out


@app.get("/upload_form")
def get_upload_form() -> str:
    return view_generator.get_upload_form()


@app.post("/upload_form")
def post_upload_form() -> str:
    entry_point = request.form.get('entry_point')
    file = request.files["file"]
    file_path = save_file(file)
    status = None
    description = None
    if file_path:
        try:
            description = upload_file(path=file_path, entry_point=entry_point)
            status = "Расписание успешно загружено!"
        except Exception as e:
            logger.error(e)
            return view_generator.get_upload_form(
                status="РАСПИСАНИЕ НЕ ЗАГРУЖЕНО!",
                description=f"Проверьте загружаемый файл или обратитесь в отдел КИС<br/>Ошибка:<br/>{e}")

    return view_generator.get_upload_form(status=status,
                                          description=description,
                                          entry_point=entry_point,
                                          file_name=file.filename)


@app.after_request
def add_headers(response):
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    print(
        f"""
                               ⠤               ⠤                            
                              ▐▀▄▄            ▄▀▌                           
                              ▌  ▀▄   ▄▄▄   ▄▀  ▌                           
                             ▐▌    ▀▀▀   ▀▀▀    ▐▌                          
                             ▐▌                 ▐▌                          
                             ▐▌                 ▐▌                          
                              █                 ▐                           
                          ▄▄▄▄▀█▀▀▀          ▄▄▄█▄▄▄▄                       
                        ▄▀   ▄▄▀█▀           ▀▀█▄▄  ▀▀▀                     
                           ▄▀  ▄▄█▀         ▀█▀▄  ▀▀▄                       
                         ▀▀  ▄▀   ▀▀▀▄▄▄▄▄▄▀▀   ▀▄   ▀                      
                            ▀  ▄▄▀▀▀▄     ▄▀▀▀▄▄  ▀▄                        
                              ▄▀     █▄  █      █                           
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█       █▀▀█       █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                              ▀▄▄▀▄▄▀▄▀  ▀▄▄▀▄▄▀▄▀                          
 ███████  ██████    █████   ██   ██               ██  ███    ████    █████  
  ██  ██   ██  ██  ██   ██  ███ ███               ██  ██      ██    ██   ██ 
  ██       ██  ██  ██   ██  ███████               ██ ██       ██    ████    
  █████    █████   ██   ██  ██ █ ██               █████       ██     █████  
  ██       ██ ██   ██   ██  ██   ██               ██ ███      ██        ███ 
  ██       ██  ██  ██   ██  ██   ██               ██  ██      ██    ██   ██ 
 ████     ████ ██   █████   ██   ██               ██  ███    ████    █████  
                                                               
                              Schedule_backend v {VERSION}
                                    {SYSTEM_TYPE}
                              
        """
    )

    logger.info(f"RUNING  on http://localhost:{PORT}")
    # app.run(host="localhost", port=5003, debug=False)
    # logger.info("test")
    serve(app, host='0.0.0.0', port=PORT, _quiet=True)
