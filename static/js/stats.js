document.getElementById("open-add").addEventListener("click", function() {
    document.getElementById("add-modal-block").classList.add("open")
})


document.getElementById("close-add").addEventListener("click", function() {
    document.getElementById("add-modal-block").classList.remove("open")
})


document.getElementById("commit-add").addEventListener("click", function() {
    document.getElementById("add-modal-block").classList.remove("open")
})


window.addEventListener('keydown', (e) => {
    if(e.key === "Escape") {
        document.getElementById("add-modal-block").classList.remove("open")
    }
})


const buttons = document.querySelectorAll('.date_data');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Убираем активный класс у всех кнопок
        buttons.forEach(btn => btn.classList.remove('active'));

        // Добавляем активный класс только к нажатой кнопке
        button.classList.add('active');
    });
});



//6
document.getElementById("open-add-paying").addEventListener("click", function() {
    document.getElementById("add-modal-block-paying").classList.add("open")
})

//5


document.getElementById("close-add-paying").addEventListener("click", function() {
    document.getElementById("add-modal-block-paying").classList.remove("open")
})

//4

document.getElementById("commit-add-paying").addEventListener("click", function() {
    document.getElementById("add-modal-block-paying").classList.remove("open")
})

//3

window.addEventListener('keydown', (e) => {
    if(e.key === "Escape") {
        document.getElementById("add-modal-block-paying").classList.remove("open")
    }
})