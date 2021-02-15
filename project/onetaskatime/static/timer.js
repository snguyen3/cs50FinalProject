// timer adapted from source: https://www.w3schools.com/howto/howto_js_countdown.asp
// timer adapted from source two: https://stackoverflow.com/questions/13328919/timer-for-only-30-mins
// start, pause, and get_timer functions self-coded

//starts running timer when page loads
window.onload = run_timer();
var overTime = 0;
var running = true;
var x;
var y;
var paused = false;

// Update the count down every 1 second
function run_timer() {

    x = setInterval(function() {

        // Get today's date and time
        // var now = new Date().getTime();
        countDown -= 1000;
        // Find the distance between now and the count down date
        // var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var minutes = Math.floor(countDown / (1000 * 60));
        var seconds = Math.floor((countDown % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
        document.getElementById("demo").innerHTML = "<h3>" + minutes + "m " + seconds + "s </h3>";

        // If the count down is finished, write some text
        if (countDown == 0 || countDown < 0) {
            running = false;
            clearInterval(x);
            countup_timer();
        }
    }, 1000);
}

// Starts counting up in a different time interval once time planned hits 0 to see how much overtime the user is taking
function countup_timer() {
    y = setInterval(function() {
        overTime += 1000;
        var over_min = Math.floor(overTime / (1000 * 60));
        var over_sec = Math.floor((overTime % (1000 * 60)) / 1000);
        document.getElementById("demo").innerHTML = "<h3>Over Time: " + over_min + "m " + over_sec + "s </h3>";
        document.getElementById("demo").style.color = "red";
    }, 1000);
}

// Pauses the timer
function pause() {
    var pause_min;
    var pause_sec;

    // if the interval running is the countdown timer, it clears the interval and displays the time it was paused at
    if (running) {
        clearInterval(x);
        pause_min = Math.floor(countDown / (1000 * 60));
        pause_sec = Math.floor((countDown % (1000 * 60)) / 1000);
        document.getElementById("demo").innerHTML = "<h3>Paused at: " + pause_min + "m " + pause_sec + "s </h3>";
        paused = true;
    }
    // if the interval running is the overtime timer, it clears the interval and displays the time it was paused at
    else if (!running) {
        clearInterval(y);
        pause_min = Math.floor(overTime / (1000 * 60));
        pause_sec = Math.floor((overTime % (1000 * 60)) / 1000);
        document.getElementById("demo").innerHTML = "<h3>Paused at: " + pause_min + "m " + pause_sec + "s </h3>";
        paused = true;
    }
}

// If timer is paused, starts the timer
function start() {
    // Runs timer if timer is paused
    if (paused) {
        // If timer is counting down, starts the right interval
        if (running) {
            run_timer();
            paused = false;
        }
        // If timer is counting up, starts the right interval
        else if (!running) {
            countup_timer();
            paused = false;
        }
    }
}

// Gets the time spent to finish the task
function get_time() {
    var timeSpent;
    if (running) {
        clearInterval(x);
        // gets time spent when task is completed before the time planned has passed
        timeSpent = timePlanned - countDown;
    } else if (!running) {
        clearInterval(y);
        // gets time spent when task is completed after the time planned has passed
        timeSpent = timePlanned + overTime;
    }
    min_spent = Math.round(timeSpent / (1000 * 60));
    document.getElementById("total_time").value = min_spent;
}

