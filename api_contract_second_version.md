API Contract

```text
Request (Регистрация здания)
    URI: /register_building
    HTTP Verb: POST
    Body example: 
    {
        "type": "organization"
        "name": "OO-1",
        "password": "1234567",
        "coord_x": 12.3,
        "coord_y": 5.4
    }
    Body example: 
    {
        "type": "storage"
        "name": "MHO-1",
        "password": "1234567",
        "coord_x": 12.3,
        "coord_y": 5.4,
        "max_bio": 100.4,
        "max_glass": 30.2,
        "max_plastic": 0
    }
Response:
HTTP Status:
    201 Created
    400 Bad Request 
```

```text
Request (Выполнить вход)
    URI: /login
    HTTP Verb: POST
    Body example:
    {
        "name": "OO-1",
        "password": "1234567"
    }
Response:
HTTP Status:
    200 OK - Вход выполнен
    400 Bad Request - Неверное имя или пароль
```

```text
Request (Получить свою организацию, если выполнен вход в качестве организации)
    URI: /organization
    HTTP Verb: GET
    
Response:
HTTP Status:
    200 OK 
    Body example:
    {
        "id": 1,
        "name": "OO-1",
        "coord_x": 12.3,
        "coord_y": 5.4,
        "cur_bio": 0,
        "cur_glass": 0,
        "cur_plastic": 0
    }

    404 Not Found
```

```text
Request (Получить хранилище, если вход выполнен в качестве хранилища)
    URI: /storage
    HTTP Verb: GET
    
Response:
HTTP Status:
    200 OK 
    Body example:
    {
        "id": 1,
        "name": "MHO-1",
        "coord_x": 12.3,
        "coord_y": 5.4
        "max_bio": 100.4,
        "max_glass": 30.2,
        "max_plastic": 0
        "cur_bio": 0,
        "cur_glass": 0,
        "cur_plastic": 0
    }

    404 Not Found
```

```text
Request (Получить все хранилища, расстояния до них и свободное место,
если выполнен вход в качестве организации)
    URI: /storage/all
    HTTP Verb: GET
Response:
HTTP Status:
    200 OK 
    Body example: {
        1: { 
            "name": "MHO-1",
            "free_space": {"bio": 88.0, "glass": 30.2, "plastic": 0},
            "distance": 13.5
            }
        ...
    }

    404 Not Found
```

```text
Request (Получить хранилище по имени, расстояние и свободное место,
если выполнен вход в качестве организации)
    URI: /storage/{name}
    HTTP Verb: GET
Response:
HTTP Status:
    200 OK 
    Body example: {
        "name": "MHO-1",
            "free_space": {"bio": 88.0, "glass": 30.2, "plastic": 0},
            "distance": 13.5
    }

    404 Not Found
```

```text
Request Организация генерирует отходы, 
если выполнен вход в качестве организации
    URI: /generate
    HTTP Verb: POST
    Body example: {
        "type": "bio",
        "amount": 12.4
    }
Response:
HTTP Status:
    200 OK
    404 Not Found
    400 Bad Request
```

```text
Request Организация отправляет отходы в Хранилище (выбор хранилища
 происходит автоматически, если не указать количество - оправить все, 
что есть)
    URI: /send_automatically
    HTTP Verb: POST
    Body example: {
        "type": "bio",
        "amount": 12.4
    }
    Body example: {
        "type": "bio"
    } 
Response:
HTTP Status:
    200 OK Отходы были направлены в Хранилище, возвращаются хранилища и
количество отходов, которое они смогли принять
    Body example: {
        "MHO-1": 12.4
    }
    404 Not Found (Organisation or storage not found)
    400 Bad Request 
```

```text
Request Организация cгенерировать и сразу отправить, 
если выполнен вход в качестве организации
    URI: /generate_and_send
    HTTP Verb: POST
    Body example: {
        "type": "bio",
        "amount": 12.4
    }
Response:
HTTP Status:
    200 OK Отходы были направлены в Хранилище, возвращаются хранилища и
количество отходов, которое они смогли принять
    Body example: {
        "MHO-1": 12.4
    }
    404 Not Found
    400 Bad Request
```

```text
Request Ближайшее свободное хранилище
    URI: /closest_storage
    HTTP Verb: GET
Response:
HTTP Status:
    200 OK Ближайшее свободное хранилище и размер свободного места в нем
    Body example: {
        "name": "MHO-1",
        "free_space": {"bio": 88.0, "glass": 30.2, "plastic": 0}
    }

    404 Not Found
```

```text
Request 
    URI:
    HTTP Verb: 
    Body example: {
        
    }
Response:
HTTP Status:
    200 OK
```
