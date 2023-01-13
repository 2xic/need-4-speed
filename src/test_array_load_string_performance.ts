import { TestCase } from './helpers/TestCase.js';
import { Input } from './helpers/Input.js';

new TestCase<string>().add({
	name: 'Buffer',
	getInstance: (input) => Buffer.alloc(input.length),
	validate: (buf, input) => {
		return buf.toString('ascii') == input;
	},
	tests: {
		alloc: () => Buffer.alloc(1024).map((item) => 0),
		load: (buf, item) => {
			for (let i = 0; i < item.length; i++) {
				buf.write(item[i].toString(), i, 'ascii')
			}
		},
		concat: (buf) => Buffer.concat([buf, buf]),
		read: (buf) => [...buf],
	}
}).add({
	name: 'Array',
	getInstance: () => new Array(0),
	validate: (buf, input) => {
		return buf.join('') == input;
	},
	tests: {
		alloc: () => new Array(1024).map((item) => 0),
		load: (buf, item) => {
			for (const i of item) {
				buf.push(i)
			}
		},
		concat: (x, y) => [...x, ...y],
		read: (buf) => [...buf],
	},
}).report(new Input(100).random())
