import { Capsule } from './helpers/Capsule.js';
import { TestCase } from './helpers/TestCase.js';


export function reverse(input: string) {
    let output = '';
    for (let i = input.length - 1; i >= 0; i--) {
        output += input[i];
    }
    return output;
}

const validate = (buf: Buffer, expected_hex: string) => {
    return buf.toString('hex').includes(expected_hex) || expected_hex.includes(buf.toString('hex'));
}

const LUT = new Array(256);
for (let i = 0; i < 256; i++) {
    LUT[i] = BigInt((i & 0xF) << 4) | BigInt((i & 0xF0) >> 4);
}

new TestCase<[string, bigint, bigint]>({
    iterations: 10_000,
}).
    add({
        name: 'toString write',
        getInstance: () => Buffer.alloc(64),
        validate: (buf, [expected_hex, _]) => {
            return validate(Buffer.from(buf), expected_hex);
        },
        tests: {
            load: (item, [_, input]) => {
                item.write(reverse(input.toString(16)), 'hex');
            }
        }
    })
    .add({
        name: 'Uint8Array - bitwise',
        getInstance: ([_, __, size]) => new Capsule<Buffer>(),
        validate: (buf, [expected_hex, _]) => validate(buf.get(), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                function byteSwap(num: bigint, n: bigint) {
                    if (n % 8n !== 0n) {
                        throw new Error('n must be divisible by 8');
                    }
                    let reversed = 0n;
                    for (let i = 0; i < n; i += 8) {
                        reversed = (reversed << 8n) | (num & 0xffn);
                        num >>= 8n;
                    }
                    return reversed;
                }
                buf.set(Buffer.from(byteSwap(input, n).toString(16), 'hex'))
            }
        }
    })
    .add({
        name: 'Uint8Array - bitwise faster (for)',
        getInstance: ([_, __, size]) => new Capsule<Array<number>>().set(new Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                function byteSwap(num: bigint, n: bigint, buffer: Array<number>) {
                    if (n % 8n !== 0n) {
                        throw new Error('n must be divisible by 8');
                    }
                    for (let i = 0; i < n && num; i += 8) {
                        buffer[(i / 8)] = Number(num & 0xffn);
                        num >>= 8n;
                    }
                }
                byteSwap(input, n, buf.get());
            }
        }
    })
    .add({
        name: 'Uint8Array - bitwise faster (while)',
        getInstance: ([_, __, size]) => new Capsule<Array<number>>().set(new Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                function byteSwap(num: bigint, n: bigint, buffer: Array<number>) {
                    if (n % 8n !== 0n) {
                        throw new Error('n must be divisible by 8');
                    }
                    let i = 0;
                    while (i < n) {
                        buffer[(i / 8)] = Number((num) & 0xffn);
                        num >>= 8n;
                        i += 8;
                    }
                }
                byteSwap(input, n, buf.get());
            }
        }
    })
    /*
    .add({
        name: 'Uint8Array - bitwise faster (while -> auto compute)',
        getInstance: ([_, __, size]) => new Capsule<Array<number>>().set(new Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                function byteSwap(num: bigint, n: bigint, buffer: Array<number>) {
                    if (n % 8n !== 0n) {
                        throw new Error('n must be divisible by 8');
                    }
                    let i = 0;
                    buffer[(0 / 8)] = Number((num >> BigInt(0)) & 0xffn);
                    buffer[(8 / 8)] = Number((num >> BigInt(8)) & 0xffn);
                    buffer[(16 / 8)] = Number((num >> BigInt(16)) & 0xffn);
                    buffer[(24 / 8)] = Number((num >> BigInt(24)) & 0xffn);
                    buffer[(32 / 8)] = Number((num >> BigInt(32)) & 0xffn);
                    buffer[(40 / 8)] = Number((num >> BigInt(40)) & 0xffn);
                    buffer[(36 / 8)] = Number((num >> BigInt(36)) & 0xffn);
                }
                console.log(n);
                console.log(Buffer.from(buf.get()).toString('hex'))
                byteSwap(input, n, buf.get());
            }
        }
    })
    */
    .report(
        [
            [
                '00000000000000000000000000bb00bb',
                248569428022375151095381198408414920704n,
                128n
            ],
            [
                'cc00cc00000000000000000000000000',
                13369548n,
                128n
            ],
            [
                'aaaaaaaaaaaaaaaa',
                12297829382473034410n,
                64n
            ],
            [
                'aaaaaaaaaaaaaaaa',
                12297829382473034410n,
                64n
            ],
            [
                'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
                249540402408688206539808045449963355067n,
                128n
            ],
            [
                'cccccccccccccccccccccccccccccccc',
                272225893536750770770699685945414569164n,
                128n
            ],
        ]
    );

