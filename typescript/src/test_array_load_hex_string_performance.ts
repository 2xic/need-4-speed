import { TestCase } from './helpers/TestCase.js';
import { Input } from './helpers/Input.js';


new TestCase<string>().add({
	name: 'Buffer from hex',
	getInstance: (hex_input) => Buffer.alloc(hex_input.length / 2),
	validate: (buf, input) => {
		return buf.toString('hex') == input;
	},
	tests: {
		load: (buf, item) => {
			Buffer.from(item, 'hex').copy(buf);
		},
		slice: (buf) => buf.slice(Math.floor(buf.length / 2))
	}
}).add({
	name: 'Uint8Array from hex',
	getInstance: (hex_input) => new Uint8Array(hex_input.length / 2),
	validate: (buf, input) => Buffer.from(buf).toString('hex') == input,
	tests: {
		load: (buf, item) => {
			item.match(/.{1,2}/g)?.map((item, index) => {
				buf[index] = parseInt(item, 16);
			})
		},
		slice: (buf) => buf.slice(Math.floor(buf.length / 2))
	}
}).report(new Input(100).hex())
