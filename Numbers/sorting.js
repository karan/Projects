var bubbleSort = function (arr) {
    'use strict';
    let a = arr.slice();
    let i = 0;
    let sorted = false;
    while (!sorted) {
        sorted = true;
        for (i = 0; i < a.length - 1; i += 1) {
            if (a[i] > a[i + 1]) {
                let temp = a[i + 1];
                a[i + 1] = a[i];
                a[i] = temp;
                sorted = false;
            }
        }
    }
    return a;
};

var mergeSort = function (a) {
    'use strict';
    let n = a.length;

    if (n === 1) {
        return a;
    }

    let a1 = mergeSort(a.slice(0, n / 2));
    let a2 = mergeSort(a.slice(n / 2, n));

    return merge(a1, a2);
};

var merge = function (a, b) {
    let out = [];
    while (a.length > 0 && b.length > 0) {
        if (a[0] > b[0]) {
            out.push(b[0]);
            b.splice(0, 1);
        } else {
            out.push(a[0]);
            a.splice(0, 1);
        }
    }
    while (a.length > 0) {
        out.push(a[0]);
        a.splice(0, 1);
    }
    while (b.length > 0) {
        out.push(b[0]);
        b.splice(0, 1);
    }
    return out;
}

var testArray = [2, 5, 1, 9, 4, 3, 8, 6, 7, 0];
console.log(testArray);
console.log(mergeSort(testArray));
console.log(testArray);