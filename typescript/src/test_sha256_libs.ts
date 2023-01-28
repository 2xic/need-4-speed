import { TestCase } from './helpers/TestCase.js';
import { Input } from './helpers/Input.js';
import crypto from 'crypto';
import sha256 from 'sha256-wasm';

new TestCase<Buffer>()
	.add({
		name: 'Crypto',
		getInstance: (hex_input) => Buffer.alloc(hex_input.length / 2),
		validate: (buf, input) => {
			return true;
		},
		tests: {
			hash: (item) => crypto.createHash('sha256').update(item).digest()
		}
	}).add({
		name: 'sha256-wasm',
		getInstance: (hex_input) => Buffer.alloc(hex_input.length / 2),
		validate: (buf, input) => {
			return true;
		},
		tests: {
			hash: (item) => sha256().update(item).digest()
		}
	}).report(
		Buffer.from(new Input(256).hex(), 'hex')
	)
