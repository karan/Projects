var canvas = document.createElement('canvas');

var start = Date.now();
var fiveSeconds = function () {
    if ((Date.now() - start) % 500 >= 0 && (Date.now() - start) % 500 <= 16) {
        console.log(Date.now() - start);
    }
    window.requestAnimationFrame(fiveSeconds);
};

fiveSeconds();