
let hideNotification;

function showNotification(resultObject) {
    if (hideNotification) {
        clearTimeout(hideNotification);
    }
    let div = document.getElementById('notification_div');
    div.style.display = 'block';
    div.style.background = resultObject.success ? "green" : "red";
    div.innerText = resultObject.message;
    hideNotification = setTimeout(() => {
        div.style.display = 'none';
    }, 5000);
}
