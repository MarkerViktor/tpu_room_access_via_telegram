# Room Access BOT #

Общая информация проекта расположена в файле [«Общая информация.pdf»](https://github.com/MarkerViktor/tpu_room_access_via_telegram/blob/master/Общая%20информация.pdf)

### Команды бота: ###

##### Пользователи #####
Основная сущность системы контроля доступа. Именно к ней привязана модель лица, 
распозноваемая на входе в аудиторию
- **Список всех пользователей**   
    `/users_list`  
    Отвечает сообщением со списком всех пользователей с их ID.
    Если не указать имя группы, то будет выведен список всех пользователей.

- **Создать пользователя**  
    `/new_user {фамилия} {имя}`  
    Отвечает сообщением с идентификатором нового пользователя и ссылкой на добавлние конфигурации лица.
    Имя группы -- опциональный аргумент. Если указать, пользователь будет сразу добавлен в указанную группу.

- **Удалить пользователя**  
    `/delete_user  {ID пользователя}`  
    Отвечает сообщением со всеми данными пользователя и прикрепленным файл конфигурации его лица.
    
- **Настроить или обновить модель лица пользователя**  
    `/setup_user_model {ID пользователя}` + прикрепить файл конфигурации  
    Отвечает сообщением со всеми данными пользователя и прикрепленным новый файл конфигурации его лица 
    или 10 валидных фотографий.

##### Аудитории и доступ к ним #####
Сущности помещений, к которым осуществляется доступ, администрируемые назначенными админами.
- **Список аудиторий с указанием их местоположения**  
    `/rooms_list`  
    Отвечает сообщением со списком всех аудиторий и их местоположением.
- **Список пользователей, имеющих доступ к аудиории**  
    `/allowed_users_list {ID аудитории}`  
    Отвечает сообщением с названием аудитории и списком пользователей, которые имеют доступ к ней.

- **Дать пользователям доступ в аудиторию**  
    `/alow_access {ID аудитории} {ID пользователя 1} {ID пользователя 2}`    
    Отвечает сообщением с названием аудитории и списком пользователей, у которых имеется личный доступ.

- **Запретить пользователям доступ в аудиторию**  
    `/deny_access {ID аудитории} {ID пользователя 1} {ID пользователя 2}`  
    Отвечает сообщением с названием аудитории и списком пользователей,
    которым только что запретили доступ.
    
- **Список администраторов аудитории**  
    `/room_admins_list {ID аудитории}`  
    Отвечает сообщением с названием аудитории и списком администраторов с их никами в телеграм.

- **Дать администратору возможность администрировать аудиторию**  
    `/add_room_admin {ID аудитории} {ID администратора}`  
    Отаечает сообщением с навзанием аудитории и списком администраторов с их никами в телеграмм.
    Может выполнять только администратор указанной аудитории.

- **Запретить администратору администрировать аудиторию**  
    `/delete_room_admin {ID аудитории} {ID администратора}`   
    Отаечает сообщением с названием аудитории и списком только что удаленных администраторов 
    с их никами в телеграмм. Может выполнять только администратор указанной аудитории.

##### Администраторы #####
- **Список всех администраторов (доступен всем)**  
    `/admins_list`  
    Отвечает сообщением со списком всех администраторов с их никами в телеграмм.

- **Добавить нового администратора**  
    `/new_admin @{ник администратора}`  
    Отвечает сообщением с указанием, что администратор должен хоть раз написать боту,
    чтобы разрешить личные сообщения

- **Удалить администратора**  
    `/delete_admin @{ник администратора}`  
    Отвечает сообщением с ником удаленного администратора.

##### Посещения #####
- **Список посещений аудитории за определенный день**  
    `/room_visits_list {ID аудитории} {дата}`  
    Отвечает сообщением со списком всех посещений в хронологическом порядке с указаением времени посещения.

- **Список посещений пользователя за определенный день**  
    `/user_visits_list {ID пользователя} {дата}`  
    Отвечает сообщением со списком всех посещений в хронологическом порядке с указаением времени посещения.
_______________________________
##### Группы (в будущем) #####
Пользователи, состоящие в группе, имеют доступ к разрешенным для группы аудиториям. 
При проверке сначала проверяется наличие личного доступа, затем доступа у групп, в которых состоит пользователь.
- **Список всех групп**  
    `/groups_list`  
    Отвечает сообщением со списком всех групп

- **Создать новую группу (и добавить в нее пользователей)**  
    `/group_new {названиегруппы} {ID пользователя 1} {ID пользователя 2} ...`   
    Отвечает сообщением с названием новой группы и списком ее пользователей с их ID. 
    Добавлять пользователей необязательно

- **Удалить группу**  
    `/group_delete {название группы}`  
    Отвечает сообщением с названием удаленной группы и списком ее пользователей с их ID. 

- **Список всех пользоватлей группы**  
    `/group_users_list {группа}`  
    Отвечает сообщением с названием группы и списком ее пользователей с их ID. 

- **Добавить пользователей в группу**  
    `/group_users_add {навзание группы} {ID пользователя 1} {ID пользователя 2} ...`  
    Отвечает сообщением с названием новой группы и списком ее новых пользователей с их ID. 

- **Исключить пользователей из группы**  
    `/group_users_delete {название группы} {ID пользователя 1} {ID пользователя 2} ...`  
    Отвечает сообщением с названием новой группы и списком ее новых пользователей с их ID.
    
