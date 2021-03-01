function update_score()
{
    document.getElementById('score_display').innerHTML = score.toString();
}

document.body.onload = function()
{
    update_score();
};

document.body.onclick = function(e)
{
    if(!e.isTrusted || e.type != "click")
        return;

    let r = new XMLHttpRequest();
    r.open("POST", "/send", false);
    r.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    r.send(JSON.stringify({'x': e.x, 'y': e.y,
        'winx': window.innerWidth, 'winy': window.innerHeight}));

    let parsed_response = JSON.parse(r.response);
    if('next_url' in parsed_response)
    {
        document.location.href = parsed_response['next_url'];
    }
    else if(parsed_response['bingo'])
    {
        ++score;
        update_score();
    }
};
