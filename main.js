'use strict';

const {app, BrowserWindow} = require('electron')
const {ipcMain} = require('electron') //to communicate from main process

var window = null

function createWindow () {
    window = new BrowserWindow({width: 1000, height: 1000, minHeight: 600, minWidth: 600})
    window.loadFile('index.html')
}

ipcMain.on('login', function () {
  window.loadFile('followBackList.html')
});

app.on('ready', createWindow)

app.on('window-all-closed', () => {
   app.quit()
 })
