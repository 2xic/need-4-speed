import { Capsule } from './helpers/Capsule.js';
import { TestCase } from './helpers/TestCase.js';
import { reverse_bigint } from "wasm-reverse";

export function reverse(input: string) {
    let output = '';
    for (let i = input.length - 1; i >= 0; i--) {
        output += input[i];
    }
    return output;
}

const validate = (buf: Buffer, expected_hex: string) => {
    if (!buf.toString('hex').includes(expected_hex)){
        console.log([buf.toString('hex'), expected_hex]);
        return false;
    }
    return true;
}

const LUT = new Array(256);
for (let i = 0; i < 256; i++) {
    LUT[i] = BigInt((i & 0xF) << 4) | BigInt((i & 0xF0) >> 4);
}
const mapper: Record<string, number> = {};
[...new Array(256)].map((_, index) => mapper[index.toString()] = index)

let reversex = (a:string[]) =>[...a].map(a.pop, a)

new TestCase<[string, bigint, bigint]>({
    iterations: 10_000,
}).
    add({
        name: 'toString write safe',
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
    .
    add({
        name: 'toString write unsafe',
        getInstance: () => Buffer.allocUnsafe(64),
        validate: (buf, [expected_hex, _]) => {
            return validate(Buffer.from(buf), expected_hex);
        },
        tests: {
            load: (item, [_, input]) => {
                const left = item.write(reverse(input.toString(16)), 'hex');
                item.fill(0, left);
            }
        }
    })
    .add({
        name: 'Uint8Array - bitwise',
        getInstance: ([_, __, size]) => new Capsule<Buffer>().set(Buffer.alloc(Number(size)/ 8)),
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
                const results = Buffer.from(byteSwap(input, n).toString(16), 'hex')
                results.copy(buf.get(), buf.get().length - results.length)
            }
        }
    })
    .add({
        name: 'Array - bitwise faster (for)',
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
        name: 'Array - bitwise faster (no function - no saftey check)',
        getInstance: ([_, __, size]) => new Capsule<Array<number>>().set(new Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                const buffer = buf.get();
                for (let i = 0; i < n && input; i += 8) {
                    buffer[(i / 8)] = Number(input & 0xffn);
                    input >>= 8n;
                }
        }
        }
    })
    .add({
        name: 'Uint8Array - bitwise faster (for)',
        getInstance: ([_, __, size]) => new Capsule<Uint8Array>().set(new Uint8Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                function byteSwap(num: bigint, n: bigint, buffer: Uint8Array) {
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
        name: 'Uint8Array - bitwise faster (no function - no saftey check)',
        getInstance: ([_, __, size]) => new Capsule<Uint8Array>().set(new Uint8Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                const buffer = buf.get();
                for (let i = 0; i < n && input; i += 8) {
                    buffer[(i / 8)] = Number(input & 0xffn);
                    input >>= 8n;
                }
        }
        }
    })
    .add({
        name: 'Array - mapper',
        getInstance: ([_, __, size]) => new Capsule<Array<number>>().set(new Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                const buffer = buf.get();
                const qq = Number(n) / 8;
                for (let v = 0; v < qq; v += 1) {
//                    console.log([(input & 0xffn).toString(), mapper])
                    buffer[v] = mapper[(input & 0xffn).toString()];
                    input >>= 8n;
                }
        }
        }
    })
    .add({
        name: 'Uint8Array generator',
        getInstance: ([_, __, size]) => new Capsule<Uint8Array>().set(new Uint8Array(Number(size) / 8)),
        validate: (buf, [expected_hex, _]) => validate(Buffer.from(buf.get()), expected_hex),
        tests: {
            load: (buf, [_x, input, n]) => {
                function* x() {
                    const buffer = buf.get();
                    for (let i = 0; i < n && input; i += 8) {
                        yield Number(input & 0xffn);
                        input >>= 8n;
                    }
                }
                const xy = new Uint8Array(x())
                buf.get().set(xy);
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
        ],
        {
            sorted: true,
        }
    );
