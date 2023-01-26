// global
var app = SpreadsheetApp.getUi();
var ss = SpreadsheetApp.getActiveSpreadsheet();

// create menu entry in spreadsheet upon opening
function onOpen() {
  app.createMenu('Move Sheet')
    .addItem('Move Active Sheet to End', 'moveactiveSheet')
    .addItem('Move Sheet', 'movespecificSheet')
    .addToUi();  
}

// move active sheet to position zero
function moveactiveSheet() {
  var sheets = ss.getSheets();
  ss.moveActiveSheet(sheets.length);  
}

// select sheet number (correct for zero-based array) and move to front
function movespecificSheet() {
  //var int = app.prompt('Select Sheet', 'Use int. only', app.ButtonSet.OK_CANCEL)
  //  .getResponseText();
  var sheets = ss.getSheets();
  ss.setActiveSheet(sheets[0]);
  //ss.moveActiveSheet(0);  
}
