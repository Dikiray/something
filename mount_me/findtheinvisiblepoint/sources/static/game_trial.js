// The following function was copied from https://stackoverflow.com/a/1527832/11248508
function getRandomInt(lower, upper)
{
    //to create an even sample distribution
    //return Math.floor(lower + (Math.random() * (upper - lower + 1)));

    //to produce an uneven sample distribution
    //return Math.round(lower + (Math.random() * (upper - lower)));

    //to exclude the max value from the possible values
    return Math.floor(lower + (Math.random() * (upper - lower)));
}


var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');


// The following code was copied from https://stackoverflow.com/a/4038655/11248508
window.onload = window.onresize = function() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}


// actual x, actual y
var ax = 0, ay = 0;
var square_side_half = 50;
var pixel_side_half = 3;

canvas.onclick = function(e)
{
    if(!e.isTrusted || e.type != "click")
        return;

    if(Math.abs(e.x - ax) <= pixel_side_half && Math.abs(e.y - ay) <= pixel_side_half)
    {
        alert('Bingo!');
        ax = getRandomInt(0, canvas.width);
        ay = getRandomInt(0, canvas.height);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
};

canvas.oncontextmenu = function(e)
{
    if(!e.isTrusted || e.type != "contextmenu")
        return true;

    let is_good_click = Math.abs(e.x - ax) <= square_side_half && Math.abs(e.y - ay) <= square_side_half;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if(is_good_click)
    {
        ctx.fillStyle = 'green';
    }
    else
    {
        ctx.fillStyle = 'red';
    }
    ctx.fillRect(e.x - square_side_half, e.y - square_side_half, 2 * square_side_half + 1, 2 * square_side_half + 1);

    if(is_good_click)
    {
        ctx.fillStyle = 'pink';
        ctx.fillRect(ax - pixel_side_half, ay - pixel_side_half, 2 * pixel_side_half, 2 * pixel_side_half);
    }

    return false;
};
