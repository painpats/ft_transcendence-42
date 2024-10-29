let playerScore = 0;
let opponentScore = 0;
const canvas = document.getElementById("pongIaCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 800;
canvas.height = 500;

const paddleWidth = 10, paddleHeight = 100;
const player = {  x: canvas.width - paddleWidth - 10, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, dy: 0, speed: 5};
const opponent = { x: 10, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, dy: 0};

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(event) {
    if (event.key === "ArrowUp") {
        player.dy = -1 * player.speed;
    } else if (event.key === "ArrowDown") {
        player.dy = player.speed;
    }
}

function keyUpHandler(event) {
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
		player.dy = 0;
    }
}

const ball = { x: canvas.width / 2, y: canvas.height / 2, radius: 17, dx: 6, dy: 0, Vmax: 16 };

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
	ctx.fillText(playerScore, canvas.width / 4, 50);
	ctx.fillText("/5", (canvas.width / 4) + 20, 50);
	ctx.fillText(opponentScore, (canvas.width / 4) * 3, 50);
	ctx.fillText("/5", ((canvas.width / 4 ) * 3) + 20, 50);
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
		if (ball.dy > canvas.height - (ball.y + ball.radius)) {
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

    if (ball.x - ball.radius < 22) {
		if (opponent.y < ball.y && opponent.y + opponent.height > ball.y && ball.dx < 0)
		{
			if (ball.dx < -ball.Vmax)
			{
				ball.dx = 2 * (ball.Vmax / 3);
				ball.dy = 3 * ((ball.y - (opponent.y + opponent.height / 2)) / (opponent.height / 2));
			}
			else
			{
				ball.dx *= -1;
				if (ball.dx < ball.Vmax)
					ball.dx += 1;
				ball.dy = 5 * ((ball.y - (opponent.y + opponent.height / 2)) / (opponent.height / 2));
			}
		}
		if (ball.x - ball.radius / 2 < 0)
		{
			opponentScore++;
			resetBall(-1);
		}

		if (opponent.y >= ball.y && opponent.y < ball.y + ball.radius && ball.x < canvas.width - 10)
			bottomOpponentDoubleTap();
		if (opponent.y + opponent.height <= ball.y && opponent.y + opponent.height > ball.y - ball.radius && ball.x < canvas.width - 10)
			topOpponentDoubleTap();
	}

    if (ball.x + ball.radius > canvas.width - 22) {
		if (player.y < ball.y && player.y + player.height > ball.y && ball.dx > 0)
		{
			if (ball.dx > ball.Vmax)
			{
				ball.dx = -2 * (ball.Vmax / 3);
				ball.dy = 3 * ((ball.y - (player.y + player.height / 2)) / (player.height / 2));
			}
			else
			{
				if (ball.dx < ball.Vmax)
					ball.dx += 1;
				ball.dx *= -1;
				ball.dy = 5 * ((ball.y - (player.y + player.height / 2)) / (player.height / 2));
			}
		}
		if (ball.x + ball.radius / 2 > canvas.width)
		{
			playerScore++;
			resetBall(1);
		}

		if (player.y >= ball.y && player.y < ball.y + ball.radius && ball.x < canvas.width - 10)
			bottomPlayerDoubleTap();
		if (player.y + player.height <= ball.y && player.y + player.height > ball.y - ball.radius && ball.x < canvas.width - 10)
			topPlayerDoubleTap();
    }

	if (ball.dx == 0 && ball.x == canvas.width / 2)
	{
		ball.dx = 6;
		ball.dy = 0;
	}

    ball.x += ball.dx;
    ball.y += ball.dy;

}

function resetBall(n) {
	ball.x = canvas.width / 2;
	ball.y = canvas.height / 2;
	ball.dy = 0;
	ball.dx = 6 * n;
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
let guessBall = { x: 0, y: canvas.height / 2, dx: 0, dy: 0 };
let lastAICheckTime = 0, dirTap = 0;

function AIProg(deltaTime) {
    if (lastAICheckTime > 1000) {
        lastAICheckTime = 0;

        if (ball.dx < 0) {
            guessBall.x = ball.x;
            guessBall.y = ball.y;
            guessBall.dx = ball.dx;
            guessBall.dy = ball.dy;

            while (guessBall.x - ball.radius > 22) {
                if (guessBall.y + ball.radius > canvas.height || guessBall.y - ball.radius < 0)
                    guessBall.dy *= -1;

                guessBall.x += guessBall.dx;
                guessBall.y += guessBall.dy;
            }

        }
		else if (ball.dx > 0) {
			guessBall.y = canvas.height / 2; }
		else if (ball.dx == 0) {
			guessBall.y = 4 * (canvas.height / 5);
		}
		else
			guessBall.y = 0;
    	}

    if (guessBall.y - ball.radius > opponent.y + 100) {
        opponent.dy = 5; 
    } else if (guessBall.y < opponent.y ) {
        opponent.dy = -5;
    } else {
        opponent.dy = 0; 
    }
	

    lastAICheckTime += deltaTime; 
}

function endGame() {
    document.getElementById('playerScore').value = opponentScore; 
    document.getElementById('opponentScore').value = playerScore; 
    document.getElementById('opponentAlias').value = "Flipperbot";
    document.getElementById('game-form').submit();
}

let gameOver = false;
let lastFrameTime = 0;

function gameLoop(currentTime) {
    let deltaTime = currentTime - lastFrameTime;
    lastFrameTime = currentTime;
	if (!gameOver) { 
		if (opponentScore >= 5 || playerScore >= 5) {
			gameOver = true;
			setTimeout(endGame, 1000);
            return;
        }

    	update();
    	draw();
    	AIProg(deltaTime);
    	requestAnimationFrame(gameLoop);
	}
}

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
	if (playerScore < 5 && opponentScore < 5) {
    	const canvasRect = canvas.getBoundingClientRect();
    	const offsetY = 10; 

    	p_buttonUp.style.top = (canvasRect.bottom + offsetY) + 'px';
    	p_buttonUp.style.left = (canvasRect.right - p_buttonUp.offsetWidth - p_buttonDown.offsetWidth - 5) + 'px'; 

    	p_buttonDown.style.top = (canvasRect.bottom + offsetY) + 'px';
    	p_buttonDown.style.left = (canvasRect.right - p_buttonDown.offsetWidth) + 'px';
	}
}

buttonsPositon();


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

document.body.appendChild(p_buttonDown);
document.body.appendChild(p_buttonUp);


gameLoop(0);
