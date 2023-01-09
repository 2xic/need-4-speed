import {TestCase} from './helpers/TestCase.js';
import {Input} from './helpers/Input.js';
import crypto from 'crypto';
import sha256 from 'sha256-wasm';

new TestCase<bigint>(
	
)
.add({
		name: 'Buffer - Bitwise',
		getInstance: (hex_input) => Buffer.alloc(64),
		validate: (buf, input) => {
			/*
			console.log(buf);
			process.exit(0);
			*/
			return buf.readBigInt64LE() == input;
		},
		tests: {
			load: (item, input) => {
				let copy = input + 0n;
				let index = 0;
				while(copy > 0) {
					item[index++] = Number(copy & 0xFFn);
					copy >>= 8n;
				}
				return copy;
			}
		}
})
.add({
		name: 'Buffer - toString',
		getInstance: (hex_input) => Buffer.alloc(64),
		validate: (buf, input) => {
			return buf.readBigInt64LE() == input;
		},
		tests: {
			load: (item, input) => {
				// <Buffer 2c 01 00 00 00 00 00 00 00 00>
				let hexString = input.toString(16);//.split('').reverse().join('');
				hexString = hexString.padStart((hexString.length)%2 + hexString.length, '0')
				hexString = (hexString.match(/.{1,2}/g)?.map((item, index) => {
					return item.split('').reverse().join('');
				}).join('') ||'').split('').reverse().join('');

				Buffer.from(hexString, 'hex').copy(item, 0);
			}
		}
})
.add({
		name: 'Uint8Array - bitwise',
		getInstance: (hex_input) => new Uint8Array(64),
		validate: (buf, input) => {
			return Buffer.from(buf).readBigInt64LE() == input;
		},
		tests: {
			load: (item, input) => {
				let copy = input + 0n;
				let index = 0;
				while(copy > 0) {
					item[index++] = Number(copy & 0xFFn);
					copy >>= 8n;
				}
				return copy;
			}
		}
})
.add({
		name: 'Buffer writeBigInt64BE',
		getInstance: (hex_input) => Buffer.alloc(64),
		validate: (buf, input) => {
		//	console.log(buf);
			return Buffer.from(buf).readBigInt64LE() == input;
		},
		tests: {
			load: (item, input) => {
				item.writeBigInt64LE(input);
			}
		}
})
.add({
		name: 'Dataview',
		getInstance: (hex_input) =>  new ArrayBuffer(64),
		validate: (buf, input) => {
			return Buffer.from(buf).readBigInt64LE() == input;
		},
		tests: {
			load: (item, input) => {
				new DataView(item).setBigInt64(0, input, true);
			}
		}
})
.report(
	[300n, 1024n, 512n, 256n, 10n, 20n, 100n, 50n],
	{
		sorted: true
	}
)
