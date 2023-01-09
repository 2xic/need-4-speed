import { TestCase } from './helpers/TestCase.js';
import crypto from 'crypto';
import sha256 from 'sha256-wasm';
import { buffer } from 'stream/consumers';
import bswap from "bswap";

const testscases: Array<[string, bigint]> = [
    [
        '00000000000000000000000000bb00bb',
        248569428022375151095381198408414920704n
    ],
        ['cc00cc00000000000000000000000000', 13369548n],
    ['aaaaaaaaaaaaaaaa', 12297829382473034410n],
    ['aaaaaaaaaaaaaaaa', 12297829382473034410n],
    [
        'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        249540402408688206539808045449963355067n
    ],
    [
        'cccccccccccccccccccccccccccccccc',
        272225893536750770770699685945414569164n
    ],

];


export function reverse(input: string) {
    let output = '';
    for (let i = input.length - 1; i >= 0; i--) {
        output += input[i];
    }
    return output;
}



const testCase = new TestCase<bigint>()

for (const [expected_hex, input] of testscases) {

    const validate = (buf: Buffer) => {
        return buf.toString('hex').includes(expected_hex);
    }

    testCase.
        add({
            name: 'toString write',
            getInstance: (hex_input) => Buffer.alloc(64),
            validate: (buf, input) => {
                return validate(Buffer.from(buf));
            },
            tests: {
                load: (item, input) => {
                    item.write(reverse(input.toString(16)), 'hex');
                }
            }
        })
        .add({
            name: 'Uint8Array - bitwise',
            getInstance: (hex_input) => new Array(64),
            validate: (buf, input) => validate(Buffer.from(buf)),
            tests: {
                load: (item, input) => {
                    
                    const a = BigInt(input);
                    const b = (2n**256n - 1n);
                    const flipped = (a ^ b) + BigInt(1);
                    console.log(input.toString(16));
                    console.log(flipped.toString(16));                    
                }
            }
        })
        /*
        .add({
            name: 'Uint8Array - bitwise',
            getInstance: (hex_input) => new ArrayBuffer(64),
            validate: (buf, input) => {
                console.log(Buffer.from(buf).toString('hex'));
                console.log(reverse(input.toString(16)));
                console.log((
                    ((input & 0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAn) >> BigInt(1)) |
                    ((input & 0x55555555555555555555555555555555n) << BigInt(1))
                ).toString(16))
                console.log((
                    ((input & 0x0Fn) << 4n | (input & 0xF0n) >> 4n)
                ).toString(16))

                var right = (input & 0b00001111n);

                // Step 3
                var right= (right<<4n);

                // Step 2
                var left = (input & 0b11110000n);
                // Step 4
                var left = (left>>4n);

                // Step 5
                console.log ((right | left).toString(16));

                return validate(Buffer.from(buf))

            },
            tests: {
                load: (item, input) => {
                    // Combine even and odd bits
                    for (let i = 0; i < 8; i++){
                        new DataView(item).setBigInt64(i * 8, input >> BigInt(i), true)
                    }

                    console.log(bswap(input))
                }
            }
        })
        */
       ;


    testCase.execute(
        [input]
    )
}

testCase.report([])

