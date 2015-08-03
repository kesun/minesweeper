$(document).ready(function(){
    this.oncontextmenu = function() {
        return false;
    }
    if($('.cellgg').length > 0){
        declareLoser();
    }else if($('.cellUnknown').length == 0){
        declareWinner();
    }
});

function new_game(){
    ajax_request(0, 0, "restart");
    $('.cell').empty();
    $('#gg').hide();
}

function open_cell(attrs){
    var x = attrs.getAttribute("cell_x");
    var y = attrs.getAttribute("cell_y");
    var event = "leftClick";

    ajax_request(x, y, event);
}

function flag_cell(attrs){
    var x = attrs.getAttribute("cell_x");
    var y = attrs.getAttribute("cell_y");
    var event = "rightClick";

    ajax_request(x, y, event);
}

function ajax_request(x, y, event){
    var JSONObj = {'x': x, 'y': y, 'event': event};
    // console.log(JSON.stringify(JSONObj));
    $.ajax({
        contentType: 'application/json; charset=utf-8',
        type: 'POST',
        url: '/playgrid.json',
        data: JSON.stringify(JSONObj),
    }).done(function(data){
        //console.log("ajax_request done", data);
        updateGame(data);
    });
}

function updateGame(data){
    var state = parseInt(data.state);
    updateGrid(data.field);
    console.log('state', state);
    switch(state){
        case -1:
            declareLoser();
            break;
        case 1:
            declareWinner();
            break;
    }
}

function updateGrid(field){
    //console.log('updateGrid');
    var $cells = $('.cell');
    for(var i = 0; i < field.length; i++){
        curRow = field[i];
        for(var j = 0; j < curRow.length; j++){
            var ind = curRow.length * i + j;
            var $cell = $($cells[ind]);
            var curObj = curRow[j];
            if(curObj.isRevealed){
                // console.log(curObj.mineCount);
                if(curObj.isMine){
                    $cell.removeClass().addClass('cell verticalCenter cellgg');
                }else{
                    if(curObj.mineCount == 0){
                        $cell.removeClass().addClass('cell verticalCenter cellRevealed');
                    }else{
                        $cell.removeClass().addClass('cell verticalCenter cellMineNumber').text(curObj.mineCount);
                    }
                }
            }else{
                if(curObj.isFlagged){
                    $cell.removeClass().addClass('cell verticalCenter cellFlagged');
                }else{
                    $cell.removeClass().addClass('cell verticalCenter cellUnknown');
                }
            }
        }
    }
}

function declareWinner(){
    stopGame("YAY!");
    console.log("YOU WIN!");
}

function declareLoser(){
    stopGame("Lol you noob.");
    console.log("You stepped on a mine, gg.");
}

function stopGame(message){
    $('#gg').show().height($('#field').height()).text(message);
}