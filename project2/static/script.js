document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect('http://' + document.domain + ':' + location.port);

    let channel;

    joinChannel('last_channel')

    socket.on('message', (data) => {
        const p = document.createElement('p');
        if (data.username) {
            p.innerHTML = `[` + data.username + `, ` + data.time_stamp + `]` + ` : ` + data.msg;
            document.querySelector('#chat-box').append(p);
            document.querySelector('#message').value = '';
        } else {
            printSysMsg(data.msg)
        }
    });

    document.querySelector('#send').onclick = () => {
        socket.send({
            'msg': document.querySelector('#message').value,
            'username': username,
            'channel': channel
        });
    };

    document.querySelectorAll('.select-channel').forEach(li => {
        li.onclick = () => {
            let newChannel = li.innerHTML;
            changeHeader(newChannel);
            if (newChannel == channel) {
                msg = `You are already in ${newChannel} channel.`;
                printSysMsg(msg);
            } else {
                leaveChannel(channel);
                joinChannel(newChannel);
                channel = newChannel;
            }
        }
    });

    function leaveChannel(channel) {
        socket.emit('leave', {
            'username': username,
            'channel': channel
        })
        localStorage.removeItem('last_channel');
    }

    function joinChannel(channel) {
        socket.emit('join', {
            'username': username,
            'channel': channel
        })
        localStorage.setItem('last_channel', channel);
        document.querySelector('#chat-box').innerHTML = '';
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#chat-box').append(p);

    }

    function changeHeader(newChannel) {
        document.querySelector('#channeName').innerHTML = newChannel;
    }

});
