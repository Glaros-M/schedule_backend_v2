``` 
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
                                                               
                              Schedule_backend v 1.04
```


Точки подключения при запуске: 
* http://localhost:9000/ - проверка соединения и allow_origin
* http://localhost:9000/groups - json groups = list[group_name]
* http://localhost:9000/schedule?group_name=ИС1-221-ОТ - таблица с конкретной группой
* http://localhost:9000/teachers - json teachers = list[teacher_name]
* [http://localhost:9000/teacher?teacher_name=Артемов А.Ю.](http://localhost:9000/teacher?teacher_name=%D0%90%D1%80%D1%82%D0%B5%D0%BC%D0%BE%D0%B2%20%D0%90.%D0%AE.)-  - таблица с конкретной группой
* http://localhost:9000/upload_form - форма загрузки данных

Продуктивная версия работает по адресам: 
* https://vgltuapi.ru/groups - json groups = list[group_name]
* https://vgltuapi.ru/schedule?group_name=БД2-192-ЗБ - таблица с конкретной группой
* https://vgltuapi.ru/teachers - json teachers = list[teacher_name]
* [https://vgltuapi.ru/teacher?teacher_name=Артемов А.Ю.](https://vgltuapi.ru/teacher?teacher_name=%D0%90%D1%80%D1%82%D0%B5%D0%BC%D0%BE%D0%B2%20%D0%90.%D0%AE.)- таблица с конкретной группой

Так же расположена по адресу: https://vgltu.ru/obuchayushchimsya/raspisanie-zanyatij
