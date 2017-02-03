var reverser = function (s) {
    let i = s.length - 1;
    let out = '';
    for (i; i > -1; i -= 1) {
        out += s.charAt(i);
    }
    return out;
};

console.log(reverser('racecar'));