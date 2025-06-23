// init.js -- Initialization setup

const socket = io()
const polls = {}

const poll = (command, callback) => {
    // Poll hooker
    // Defined here so all modules can access it at runtime

    polls[Object.keys(polls).length] = {'command': command, 'callback': callback}
}

// Apply grid width
const width = config.boards[board]?.width || config.width
document.body.style.gridTemplateColumns = `repeat(${width}, 1fr)`

// EOF