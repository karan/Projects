var isPrime = function (n) {
    'use strict';
    let i = 2;
    if (n < 2) {
        return false;
    }
    for (i; i <= Math.sqrt(n); i += 1) {
        if (n % i === 0) {
            return false;
        }
    }
    return true;
};

var primeFactors = function (n) {
    let factors = [];
    if (isPrime(n)) {
        factors.push(n);
    } else {
        let i = 0;
        for (i; i <= Math.sqrt(n); i += 1) {
            if (n % i === 0 && isPrime(i)) {
                factors.push(i);
            }
        }
    }
    return factors;
};

var primeFactorize = function (n) {
    let factors = [];
    let findFactors = function (n) {
        let allFactors = primeFactors (n);
        if (allFactors.length !== 0) {
            factors.push(allFactors[0]);
            findFactors(n / allFactors[0]);
        }
    };
    findFactors (n);
    return factors;
};

console.log(primeFactorize(107));