// Same logic as sieve.c 
let LENGTH = 170000;
const flags = new Array(8192 + 1);
let count = 0;

while(LENGTH--){
    count = 0;

    for (let i = 2; i <= 8192; i++) {
        flags[i] = 1;
    }
    for (let i = 2; i <= 8192; i++) {
        if (flags[i]) {
            for(let k = i + i; k <= 8192; k+= i) {
                flags[k] = 0;
            }
            count++;
        }
    }
}
console.log(`Count : ${count}`);
