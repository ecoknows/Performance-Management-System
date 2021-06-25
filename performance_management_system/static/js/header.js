let menu_container = $('#menu-container')
let menu_button = $('#menu-btn')

menu_button.click(()=>{
    menu_button.toggleClass('open')
    menu_container.toggleClass('hidden')
})