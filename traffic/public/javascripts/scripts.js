function CreateRequest()
{
    var Request = false;

    if (window.XMLHttpRequest)
    {
        //Gecko-совместимые браузеры, Safari, Konqueror
        Request = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        //Internet explorer
        try
        {
            Request = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (CatchException)
        {
            Request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }

    if (!Request)
    {
        alert("Невозможно создать XMLHttpRequest");
    }

    return Request;
}


/*
Функция посылки запроса к файлу на сервере
r_method  - тип запроса: GET или POST
r_path    - путь к файлу
r_args    - аргументы вида a=1&b=2&c=3...
user_handler - функция-обработчик ответа от сервера
*/
function SendRequest(r_method, r_path, r_args, user_handler)
{
    //Создаём запрос
    var Request = CreateRequest();

    //Проверяем существование запроса еще раз
    if (!Request)
    {
        return;
    }

    //Назначаем пользовательский обработчик
    Request.onreadystatechange = function()
    {
        //Если обмен данными завершен
        if (Request.readyState == 4)
        {
            //Передаем управление обработчику пользователя
            user_handler(Request);
        }
    }

    //Проверяем, если требуется сделать GET-запрос
    if (r_method.toLowerCase() == "get" && r_args.length > 0)
        r_path += "?" + r_args;

    //Инициализируем соединение
    Request.open(r_method, r_path, true);

    if (r_method.toLowerCase() == "post")
    {
        //Если это POST-запрос

        //Устанавливаем заголовок
        Request.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=utf-8");
        //Посылаем запрос
        Request.send(r_args);
    }
    else
    {
        //Если это GET-запрос

        //Посылаем нуль-запрос
        Request.send(null);
    }
}

function go(){
    //Создаем функцию обработчик
    var Handler = function(Request)
    {
        alert(Request.responseText);
    }
    let args = "{\n    \"start_street\": \"Торжковская улица\",\n    \"start_number\": \"15\",\n    \"end_street\": \"Кантемировская улица\",\n    \"end_number\": \"25\"\n}";
    //Отправляем запрос
    SendRequest("POST", "http://localhost:5000/api/map",args,Handler);
}
