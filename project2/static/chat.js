document.addEventListener('DOMContentLoaded', () => {

    let msg = document.querySelector('#message');
    msg.addEventListener('keyup', event => {
        if (event.keyCode === 13) {
            document.querySelector('#send').click()
        }
    })

})
