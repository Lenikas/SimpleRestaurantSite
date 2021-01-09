function validateForm() {
    if (isEmpty(document.getElementById('name').value.trim())) {
        alert('Введите ваше имя!');
        return false;
    }
    if (isEmpty(document.getElementById('mail').value.trim()))
        {
        alert('Введите вашу почту для уведомления о брони!');
        return false;
    }
    if (isEmpty(document.getElementById('date').value.trim())) {
        alert('Выберете дату бронирования!');
        return false;
    }
    return true;
}

function isEmpty(str) {
    return (str.length === 0 || !str.trim());
}
