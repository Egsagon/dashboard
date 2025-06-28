// init.js -- Initialization setup

const get_cookie = name => {
    // so:questions/10730362

    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const lock = (name, callback) => {
    // Ensures only one callback for each name is executed
    // Callbacks are executed *after* full HTML initialization
    // This is useful for duplicated modules

    locks[name] = callback
}

const qlock = (query, callback) => {
    // Same as lock(), but callback is called for each duplicate node

    locks[query] = () => document.querySelectorAll(query).forEach(callback)
}

const socket = io({auth: {token: get_cookie('token')}})
const polls = {}
const locks = {}

// Poll hook
const poll = (command, callback) => {
    polls[Object.keys(polls).length] = {'command': command, 'callback': callback}
}

// Command hook
const exec = (command, callback) => socket.emit('exec', command, callback)

// Apply grid width
const width = config.boards[board]?.width || config.width
document.body.style.gridTemplateColumns = `repeat(${width}, 1fr)`

// Apply CSS configuration
for (const [key, value] of Object.entries(config.css)) {
    document.documentElement.style. setProperty('--' + key, value)
}

// EOF