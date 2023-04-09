let sidebar_empty = document.getElementById('sidebar-empty')
let sidebar = document.getElementById('sidebar')
let menu_button = document.getElementById('menu-button')

// Появление бокового меню
menu_button.onclick = function() {
    sidebar.style.display = 'flex'
}

// Скрытие бокового меню
sidebar_empty.onclick = function() {
    sidebar.style.display = 'none'
}