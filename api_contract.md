## API Contract

```text
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

```text
Request (Создать хранилище, в этом запросе также проверяется таблица Queue, 
если хранилище может что-либо принять, оно принимает)
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

```text
Request (Получить организацию по имени)
    URI: /organization/{name}
    HTTP Verb: GET
    
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

```text
Request (Получить хранилище по имени)
    URI: /storage/{name}
    HTTP Verb: GET
    
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

```text
Request (Получить все хранилища, расстояния до них и свободное место)
    URI: /storage/all
    HTTP Verb: GET
    Body example:
    {
        "name": "OO-1"
     }
Response:
HTTP Status:
    200 OK 
    Body example:
    Body example: {
        1: { 
            "name": "MHO-1",
            "free_space": {"bio": 88.0, "glass": 30.2, "plastic": 0},
            "distance": 13.5
            }
    }

    404 Not Found
```

```text
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
    400 Bad Request
```

```text
Request Организация отправляет отходы в Хранилище (выбор хранилища
 происходит автоматически, если не указать количество - оправить все, 
что есть,
Если организация не была найдена, то запрос откладывается в таблицу
Queue до появления нового хранилище)
    URI: /send_automatically
    HTTP Verb: POST
    Body example: {
        "name": "OO-1",
        "type": "bio",
        "amount": 12.4
    }
    Body example: {
        "name": "OO-1",
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

```textile
Request Организация генерирует и сразу отправляет отходы
(комбинирование двух предудущих запросов)
    URI: /generate_and_send
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
    404 Not Found (Organisation or storage not found)
    400 Bad Request 
```

```text
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

```text
Request Получить текущую очередь
    URI: /get_queue
    HTTP Verb: GET
Response:
HTTP Status:
    200 OK
    Body example: {"1":{
                    "organization_name": "OO-1",
                    "waste_type": "bio",
                    "waste_amount": 12.3,
                    "when_added": "12.09.2024"
                    }
                    ...
                   }
```
