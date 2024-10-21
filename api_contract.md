## API Contract

```
Request (Создать организацию)
    URI: /create_org
    HTTP Verb: POST
    Body example:
    {
        "name": "OO-1",
        "coord_x": 12.3,
        "coord_y": 5.4
    }
Response:
HTTP Status:
    201 Created - Организация создана
    400 Bad Request - Организация не создана
```

```
Request (Создать хранилище)
    URI: /create_storage
    HTTP Verb: POST
    Body example:
    {
        "name": "MHO-1",
        "coord_x": 12.3,
        "coord_y": 5.4
        "max_bio": 100.4,
        "max_glass": 30.2,
        "max_plastic": 0
    }
Response:
HTTP Status:
    201 Created - Хранилище создано
    400 Bad Request - Хранилище не создано
```

```
Request (Получить организацию по имени)
    URI: /organization?name={s}
    HTTP Verb: GET
    Body example: {
        "name": "OO-1"
    }
Response:
HTTP Status:
    200 OK Если организация существует
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

```
Request (Получить хранилище по имени)
    URI: /storage?name={s}
    HTTP Verb: GET
    Body example: {
        "name": "MHO-1"
    }
Response:
HTTP Status:
    200 OK Если хранилище с таким именем существует
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

```
Request Организация генерирует отходы
    URI: /generate
    HTTP Verb: POST
    Body example: {
        "name": "OO-1",
        "type": "bio",
        "amount": 12.4
    }
Response:
HTTP Status:
    200 OK
    404 Not Found
```

```
Request Организация отправляет отходы в Хранилище (выбор хранилища
 происходит автоматически)
    URI: /send_automatically
    HTTP Verb: POST
    Body example: {
        "name": "OO-1",
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
```

```
Request Ближайшее свободное хранилище
    URI: /closest_storage
    HTTP Verb: GET
    Body example: {
        "name": "OO-1"
    }
Response:
HTTP Status:
    200 OK Ближайшее свободное хранилище и размер свободного места в нем
    Body example: {
        "name": "MHO-1",
        "free_space": {"bio": 88.0, "glass": 30.2, "plastic": 0}
    }

    404 Not Found
```

```
Request 
    URI:
    HTTP Verb: 
    Body example: {
        
    }
Response:
HTTP Status:
    200 OK
```
