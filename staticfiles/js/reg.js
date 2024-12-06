document.getElementById("reg_but").addEventListener("click", function() {
    document.getElementById("how_are_you").classList.add("open")
})


//4

document.getElementById("no_more").addEventListener("click", function() {
    document.getElementById("how_are_you").classList.remove("open")
})

function more_more_and_more() {
    document.getElementById("how_are_you").classList.remove("open")
    document.getElementById("who_is_he").classList.add("open")
}

document.getElementById("no_more2").addEventListener("click", function() {
    document.getElementById("who_is_he").classList.remove("open")
})