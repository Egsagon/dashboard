// run.js -- Handles socket communications with the backend

// Setup cell positions
// Note: We use indexes to link cells and modules to avoid duplicates errors
const cells = document.querySelectorAll('[class*=cell]')
for (let i = 0; i < config.boards[board].modules.length; i++) {
    const cell = cells[i]
    const module = config.boards[board].modules[i]
    let [_, sx, sy, px, py] = /(\d+)x(\d+),(\d+)\+(\d+)/g.exec(module.geometry)

    cell.style.gridColumn = `${px} / span ${sx}`
    cell.style.gridRow = `${py} / span ${sy}`
    cell.style.aspectRatio = `${sx} / ${sy}`
}

// Handle server poll receptions
socket.on('poll', data => {
    loader.style.display = 'none'
    for (const [id, result] of Object.entries(data))
        polls[id].callback(...result)
})

// Handle disconnections
socket.on('disconnect', () => loader.style.display = 'flex')

// Handle connections
const loader = document.querySelector('#loader')
socket.on('connect', () => {
    socket.emit('start', polls)
})

// Ping server to stay alive
setInterval(() => socket.emit('ping', response => {
    // Reload the page if connection was lost
    if (response !== 'ok') location.reload()
}), 30 * 1000)

// EOF