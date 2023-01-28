import { TestCase } from './helpers/TestCase.js';
import { Capsule } from './helpers/Capsule.js';

new TestCase<number>({
	iterations: 100_000,
})
	.add({
		name: 'toString',
		getInstance: (hex_input) => new Capsule<number | string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.toString();
		},
		tests: {
			reverse: (item) => {
                item.set(item.get().toString())
            }
		}
	}).add({
		name: 'implicit casting',
		getInstance: (hex_input) => new Capsule<number | string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.toString();
		},
		tests: {
			reverse: (item) => {
                item.set('' + item.get())
            }
		}
	}).add({
		name: 'template string',
		getInstance: (hex_input) => new Capsule<number | string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.toString();
		},
		tests: {
			reverse: (item) => {
                item.set(`${item.get()}`)
            }
		}
	}).add({
		name: 'arr join',
		getInstance: (hex_input) => new Capsule<number | string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.toString();
		},
		tests: {
			reverse: (item) => {
                item.set([item.get()].join(''))
            }
		}
	}).report(
		[
            10000,
            Math.pow(2, 256),
            Math.pow(2, 128),
            Math.pow(2, 64),
            Math.pow(2, 32),
            0xdeafbeef,
            Number('1'.repeat(100))
        ],
        {
            sorted: true
        }
	)
