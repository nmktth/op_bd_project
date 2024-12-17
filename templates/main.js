document.getElementById('add_product_form').addEventListener('submit', function(event) {
    event.preventDefault(); // Не даем форме отправиться по умолчанию

    let ozonLink = document.getElementById('ozon').value; // Получаем ссылку товара из формы

    // Отправляем POST-запрос на сервер
    fetch('/add-product/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `ozon=${ozonLink}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.price) {
            // Если цена найдена, отображаем её в section
            document.querySelector('.products').innerHTML = `Цена: ${data.price} ₽`;
        } else {
            document.querySelector('.products').innerHTML = `Ошибка: ${data.error}`;
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});
