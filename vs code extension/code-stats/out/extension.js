"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
var vscode = require("vscode");
var startTime = Date.now();
function activate(context) {
    console.log('Extension gestartet');
    startTime = Date.now();
    var statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 999);
    statusBarItem.command = 'codingTimer.showTime';
    statusBarItem.tooltip = 'Vergangene Zeit';
    statusBarItem.text = formatTime();
    statusBarItem.show();
    setInterval(function () {
        statusBarItem.text = formatTime();
    }, 1000);
    function formatTime() {
        var vergangeneZeit = (Date.now() - startTime) / 1000;
        var text = "Du programmierst seit: ";
        if (vergangeneZeit > 3600) {
            text += Math.floor(vergangeneZeit / 3600).toString() + " h  ";
            vergangeneZeit -= 3600 * Math.floor(vergangeneZeit / 3600);
        }
        if (vergangeneZeit > 60) {
            text += Math.floor(vergangeneZeit / 60).toString() + " m  ";
            vergangeneZeit -= 60 * Math.floor(vergangeneZeit / 60);
        }
        if (vergangeneZeit < 60) {
            text += Math.floor(vergangeneZeit).toString() + " s";
        }
        return text;
    }
    var showTimeCommand = vscode.commands.registerCommand('codingTimer.showTime', function () {
        vscode.window.showInformationMessage(formatTime());
    });
    context.subscriptions.push(statusBarItem, showTimeCommand);
}
function deactivate() { }
