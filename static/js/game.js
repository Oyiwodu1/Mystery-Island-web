// GET HTML ELEMENTS

const startButton = document.getElementById("startButton");
const menuButton = document.getElementById("menuButton");
const navigation = document.querySelector("nav");


// MOBILE NAVIGATION

menuButton.addEventListener("click", function () {
    navigation.classList.toggle("active");
});


// BEGIN ADVENTURE BUTTON

startButton.addEventListener("click", function () {
    window.location.href = "/game";
});