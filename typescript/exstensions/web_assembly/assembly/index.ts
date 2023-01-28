import { BigInt } from "as-bigint/assembly/BigInt"
import { i256Safe } from "as-bignum/assembly";

export function reverse(value: string): string {
  let v = new StaticArray<string>(value.length + 1);
  for(let i = value.length - 1; i > -1; i--) {
    unchecked(v[value.length - i] = unchecked(value[i]));
  }
  return v.join('');
//  return value.split('').reverse().join('');
}


/**
 * Number was 2 big for wasm
 * Does not currently work
 * i256 requiered.
 *
 */
export function reverse_bigint(value: i256Safe, n:usize): i64 {
    if (n % 8 !== 0) {
        throw new Error('n must be divisible by 8');
    }
    const aaaa: BigInt = BigInt.fromString(value);
    let reversed: BigInt = BigInt.from(0);
    console.log(n.toString());
    console.log(value.toString());
    for (let i: usize = 0; i < n; i += 8) {
        reversed = (reversed.leftShift(8)).bitwiseOr((aaaa.bitwiseAnd(0xff)));
        aaaa.rightShift(8);
//        value >>= 8;
    }
    return reversed.toInt64();
}
