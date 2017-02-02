var factorialLoop = function (n) {
    'use strict';
    let i = 1;
    let p = n;
    for (i = 1; i < n; i += 1) {
        p *= i;
    }
    return p;
};

console.log(factorialLoop(4));

var factorialRecur = function (n) {
	'use strict';
	if (n === 1) {
		return n;
	} else {
		return n * factorialRecur (n - 1);
	}
};

console.log(factorialRecur(4));