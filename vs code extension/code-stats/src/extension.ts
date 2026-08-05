import * as vscode from 'vscode';

let startTime = Date.now();


export function activate(context: vscode.ExtensionContext) {
    console.log('Extension gestartet');

    startTime = Date.now();

    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        999
    
    );
    statusBarItem.command = 'codingTimer.showTime';
    statusBarItem.tooltip = 'Vergangene Zeit';
    statusBarItem.text = formatTime();
    statusBarItem.show();

    setInterval(() => {


        statusBarItem.text = formatTime();        
    }, 1000);

    function formatTime() {

        let vergangeneZeit = (Date.now() - startTime) / 1000;

                let text = "Du programmierst seit: ";

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
    const showTimeCommand = vscode.commands.registerCommand(
        'codingTimer.showTime', 
        () => {
            vscode.window.showInformationMessage(
                formatTime()
            );
        }
    );
     
    context.subscriptions.push(
        statusBarItem,
        showTimeCommand
    );
}

export function deactivate() {}