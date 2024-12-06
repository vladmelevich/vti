
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