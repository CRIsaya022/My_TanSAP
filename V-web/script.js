document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('heartCanvas');
    var ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var hearts = [];
    var heartImage = new Image();
    heartImage.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z' fill='%23ff4466'/%3E%3C/svg%3E";
    
    var showText = false; 
    var animationStarted = false;

    function addHeart() {
        var scale = Math.random() * 0.5 + 0.5; // Scale heart size
        hearts.push({
            x: Math.random() * canvas.width,
            y: canvas.height + 30,
            speed: Math.random() * 2 + 1,
            scale: scale,
            width: 44 * scale,
            height: 44 * scale
        });
    }

    function drawHearts() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (var i = 0; i < hearts.length; i++) {
            var heart = hearts[i];
            ctx.drawImage(heartImage, heart.x, heart.y, heart.width, heart.height);
            heart.y -= heart.speed;

            if (heart.y < -30) {
                hearts.splice(i, 1);
                i--;
            }
        }

        if (showText) {
            drawText();
        }
    }

    function drawText() {
        ctx.font = '48px serif';
        ctx.fillStyle = 'pink';
        ctx.textAlign = 'center';
        ctx.fillText('Will you be my Valentine, Aileen?', canvas.width / 2, canvas.height / 2);
    }

    function loop() {
        if (animationStarted) {
            addHeart();
        }
    }

    function startDrawing() {
        drawHearts();
        requestAnimationFrame(startDrawing);
    }

    function playAudio() {
    var audio = document.querySelector('audio');
    audio.play();

    
    animationStarted = true;
    startDrawing(); // Initialize the drawing loop
    setInterval(loop, 300); 

    //Timeout to show the text after 10 seconds
    setTimeout(function() {
        showText = true;
    }, 10000);

    // Hide the play button
    document.getElementById('playAudioButton').style.display = 'none';
}


    // Expose playAudio to global scope if needed
    window.playAudio = playAudio;
});
