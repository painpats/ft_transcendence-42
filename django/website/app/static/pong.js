let playerScore = 0;
let opponentScore = 0;
const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 800;
canvas.height = canvas.width * 0.625;

const paddleWidth = canvas.width * 0.0125, paddleHeight = canvas.width * 0.125;
const player = {  x: canvas.width - paddleWidth - canvas.width * 0.0125, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, dy: 0, speed: canvas.width / 160};
const opponent = { x: canvas.width * 0.0125, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, dy: 0, speed: canvas.width / 160};

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(event) {
    if (event.key === "ArrowUp") {
        player.dy = -1 * player.speed;
    } else if (event.key === "ArrowDown") {
        player.dy = player.speed;
    }
	else if (event.key === "w" || event.key === "W") {
        opponent.dy = -1 * opponent.speed;
    }
	else if (event.key === "s" || event.key === "S") {
        opponent.dy = opponent.speed;
	}
}

function keyUpHandler(event) {
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
		player.dy = 0;
 	} else if (event.key === "w" || event.key === "W" || event.key === "s" || event.key === "S") {
        opponent.dy = 0;
    }
}

const ball = { x: canvas.width / 2, y: canvas.height / 2, radius: 0.02125 * canvas.width, dx: 0.0075 * canvas.width, dy: 0, Vmax: 0.02125 * canvas.width };

function drawRect(x, y, w, h) {
    ctx.fillStyle = "#fff";
    ctx.fillRect(x, y, w, h);
}

function drawBall(x, y, r) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = "#fff";
    ctx.fill();
    ctx.closePath();
}

function putScores() {
	ctx.font = "30px Arial";
	ctx.fillStyle = "#fff";
	ctx.fillText(playerScore, canvas.width / 4, 22);
	ctx.fillText("/5", (canvas.width / 4) + 20, 22);
	ctx.fillText(opponentScore, (canvas.width / 4) * 3, 22);
	ctx.fillText("/5", ((canvas.width / 4 ) * 3) + 20, 22);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawRect(player.x, player.y, player.width, player.height);

    drawRect(opponent.x, opponent.y, opponent.width, opponent.height);

    drawBall(ball.x, ball.y, ball.radius);

    putScores();
}

function update() {
	buttonsPositon();
    player.y += player.dy;
    opponent.y += opponent.dy;

    player.y = Math.max(Math.min(player.y, canvas.height - paddleHeight), 0);
    opponent.y = Math.max(Math.min(opponent.y, canvas.height - paddleHeight), 0);

    
	
    if (ball.y + ball.radius > canvas.height) {
        ball.dy *= -1;
		if (ball.dy >= canvas.height - (ball.y + ball.radius)) {
			
			if (ball.dx > 0) {
				ball.dx = 22;
				ball.dy = -10;
				ball.y = canvas.height - ball.radius - 2;
			}
			else {
				ball.dx = -22;
				ball.dy = -10;
				ball.y = canvas.height - ball.radius - 2;
			}
		}
	}
	
	if (ball.y - ball.radius < 0) {
        ball.dy *= -1;
		if (-ball.dy > ball.y - ball.radius) {
			if (ball.dx > 0) {
				ball.dx = 22;
				ball.dy = 10;
				ball.y = ball.radius + 2;
			}
			else {
				ball.dx = -22;
				ball.dy = 10;
				ball.y = ball.radius + 2;
			}
		}
	}

	
    if (ball.x - ball.radius < 2 * opponent.width + 1) {
		if (opponent.y < ball.y && opponent.y + opponent.height > ball.y && ball.dx < 0)
		{
			if (ball.dx < -ball.Vmax)
			{
				ball.dx = (ball.Vmax / 2);
				ball.dy = 3 * ((ball.y - (opponent.y + opponent.height / 2)) / (opponent.height / 2));
			}
			else
			{
				ball.dx *= -1;
				if (ball.dx < ball.Vmax)
					ball.dx += opponent.width / 10;
				ball.dy = 5 * ((ball.y - (opponent.y + opponent.height / 2)) / (opponent.height / 2));
			}
		}
		if (ball.x - ball.radius / 2 < 0)
		{
			resetBall(-1);
			opponentScore++;
		}

		
		if (opponent.y >= ball.y && opponent.y < ball.y + ball.radius && ball.x < canvas.width - 10)
			bottomOpponentDoubleTap();
		if (opponent.y + opponent.height <= ball.y && opponent.y + opponent.height > ball.y - ball.radius && ball.x < canvas.width - 10)
			topOpponentDoubleTap();
	}

	
    if (ball.x + ball.radius > canvas.width - (2 * opponent.width + 1)) {
		if (player.y < ball.y && player.y + player.height > ball.y && ball.dx > 0)
		{
			
			if (ball.dx > ball.Vmax)
			{
				ball.dx = -(ball.Vmax / 2);
				ball.dy = 3 * ((ball.y - (player.y + player.height / 2)) / (player.height / 2));
			}
			else
			{
				if (ball.dx < ball.Vmax)
					ball.dx += player.width / 10;
				ball.dx *= -1;
				ball.dy = 5 * ((ball.y - (player.y + player.height / 2)) / (player.height / 2));
			}
		}
		if (ball.x + ball.radius / 2 > canvas.width)
		{
			resetBall(1);
			playerScore++;
		}

		
		if (player.y >= ball.y && player.y < ball.y + ball.radius && ball.x < canvas.width - 10)
			bottomPlayerDoubleTap();
		if (player.y + player.height <= ball.y && player.y + player.height > ball.y - ball.radius && ball.x < canvas.width - 10)
			topPlayerDoubleTap();
    }

	
	if (ball.dx == 0 && ball.x == canvas.width / 2)
	{
		ball.dx = 4;
		ball.dy = 0;
	}

    ball.x += ball.dx;
    ball.y += ball.dy;

}

function resetBall(n) {
	ball.x = canvas.width / 2;
	ball.y = canvas.height / 2;
	ball.dy = 0;
	ball.dx = (0.0075 * canvas.width) * n;
}

function bottomOpponentDoubleTap() {
	if (ball.dx == 0 && ball.dy > 0)
	{
		ball.x += 15;
		ball.dx = ball.dy + 3;
		ball.dy = opponent.dy;
	}
	else if (ball.dx != 0)
	{
		ball.dy = ball.dx;
		ball.dx = 0;
	}
}

function topOpponentDoubleTap() {
	if (ball.dx == 0 && ball.dy < 0)
	{
		ball.x += 15;
		ball.dx = -ball.dy + 3;
		ball.dy = opponent.dy;
	}
	else if (ball.dx != 0)
	{
		ball.dy = -ball.dx;
		ball.dx = 0;
	}
}


function bottomPlayerDoubleTap() {
	if (ball.dx == 0 && ball.dy > 0)
	{
		ball.x -= 15;
		ball.dx = -ball.dy - 3;
		ball.dy = player.dy;
	}
	else if (ball.dx != 0)
	{
		ball.dy = -ball.dx;
		ball.dx = 0;
	}
}

function topPlayerDoubleTap() {
	if (ball.dx == 0 && ball.dy < 0)
	{
		ball.x -= 15;
		ball.dx = ball.dy - 3;
		ball.dy = player.dy;
	}
	else if (ball.dx != 0)
	{
		ball.dy = ball.dx;
		ball.dx = 0;
	}
}

function endGame() {
    document.getElementById('playerScore').value = playerScore;
    document.getElementById('opponentScore').value = opponentScore;
    document.getElementById('opponentAlias').value = "Flipper";
    document.getElementById('game-form').submit();
}

let gameOver = false;

function gameLoop() {
	if (!gameOver) { 
		if (opponentScore >= 5 || playerScore >= 5) {
			gameOver = true;
			
			setTimeout(endGame, 1000);
            return;
        }

        update();
        draw();
        requestAnimationFrame(gameLoop);
    }
}


const o_buttonDown = document.createElement('button');
o_buttonDown.innerText = 'DOWN';
o_buttonDown.className = 'btn btn-warning'; 
o_buttonDown.style.position = 'fixed';
o_buttonDown.style.zIndex = '9999'; 

const o_buttonUp = document.createElement('button');
o_buttonUp.innerText = 'UP';
o_buttonUp.className = 'btn btn-warning'; 
o_buttonUp.style.position = 'fixed';
o_buttonUp.style.zIndex = '9999'; 

const p_buttonDown = document.createElement('button');
p_buttonDown.innerText = 'DOWN';
p_buttonDown.className = 'btn btn-warning'; 
p_buttonDown.style.position = 'fixed';
p_buttonDown.style.zIndex = '9999'; 

const p_buttonUp = document.createElement('button');
p_buttonUp.innerText = 'UP';
p_buttonUp.className = 'btn btn-warning'; 
p_buttonUp.style.position = 'fixed';
p_buttonUp.style.zIndex = '9999'; 

function buttonsPositon() {
    const canvasRect = canvas.getBoundingClientRect();
    const offsetY = 10; 

    o_buttonUp.style.top = (canvasRect.bottom + offsetY) + 'px';
    o_buttonUp.style.left = (canvasRect.left) + 'px';

    o_buttonDown.style.top = (canvasRect.bottom + offsetY) + 'px';
    o_buttonDown.style.left = (canvasRect.left + o_buttonUp.offsetWidth + 5) + 'px'; 

    p_buttonUp.style.top = (canvasRect.bottom + offsetY) + 'px';
    p_buttonUp.style.left = (canvasRect.right - p_buttonUp.offsetWidth - p_buttonDown.offsetWidth - 5) + 'px'; 

    p_buttonDown.style.top = (canvasRect.bottom + offsetY) + 'px';
    p_buttonDown.style.left = (canvasRect.right - p_buttonDown.offsetWidth) + 'px';
}

buttonsPositon();

o_buttonDown.addEventListener('mousedown', function() {
    opponent.dy = opponent.speed;
});

o_buttonDown.addEventListener('mouseup', function() {
    opponent.dy = 0;
});


o_buttonUp.addEventListener('mousedown', function() {
    opponent.dy = -1 * opponent.speed;
});

o_buttonUp.addEventListener('mouseup', function() {
    opponent.dy = 0;
});


p_buttonDown.addEventListener('mousedown', function() {
    player.dy = player.speed;
});

p_buttonDown.addEventListener('mouseup', function() {
    player.dy = 0;
});


p_buttonUp.addEventListener('mousedown', function() {
    player.dy = -1 * player.speed;
});

p_buttonUp.addEventListener('mouseup', function() {
    player.dy = 0;
});

document.body.appendChild(o_buttonDown);
document.body.appendChild(o_buttonUp);
document.body.appendChild(p_buttonDown);
document.body.appendChild(p_buttonUp);


gameLoop();
