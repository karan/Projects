var checkIfPrime = function (n) {
    'use strict';
    var i = 2;
    if (n === 1) {
        return false;
    }
    for (i = 2; i <= Math.sqrt(n); i += 1) {
        if (n % i === 0) {
            return false;
        }
    }
    return true;
};

//console.log(checkIfPrime(input));

var primeFactors = function (n) {
    'use strict';
    let factors = [];
    let i = 1;
    for (i; i < Math.floor(n / 2); i += 1) {
        if (n % i === 0 && checkIfPrime(i)) {
            factors.push(i);
        }
    }
    if (checkIfPrime(n)) {
        factors.push(n);
    }
    return factors;
};

var stuff = [];
var primeFactorize = function (n) {
    'use strict';
    /*
    1. find all prime factors
    2. divide by a factor, add that factor to list
    3. repeat for the quotient
    4. stop when no more prime factors
    */
    let allFactors = primeFactors(n);
    if (allFactors.length !== 0) {
        stuff.push(allFactors[0]);
        primeFactorize(n / allFactors [0]);
    }
};

primeFactorize(600);
console.log(stuff);