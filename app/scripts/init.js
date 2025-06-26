// init.js -- Initialization setup

const socket = io()
const polls = {}

// Poll hook
const poll = (command, callback) => {
    polls[Object.keys(polls).length] = {'command': command, 'callback': callback}
}

// Command hook
const exec = (command, callback) => socket.emit('exec', command, callback)

// Apply grid width
const width = config.boards[board]?.width || config.width
document.body.style.gridTemplateColumns = `repeat(${width}, 1fr)`

// EOF