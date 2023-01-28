import { TestCase } from './helpers/TestCase.js';
import { reverse } from "wasm-reverse";
import { Capsule } from './helpers/Capsule.js';
// @ts-ignore
import pkg from 'ember-reverse';
const { reverse: ember_reverse } = pkg;

new TestCase<string>({
	iterations: 10_000,
})
	.add({
		name: 'Wasm',
		getInstance: (hex_input) => new Capsule<string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.split('').reverse().join('');
		},
		tests: {
			reverse: (item) => {
                item.set(reverse(item.get()))
            }
		}
	}).add({
		name: 'ember_reverse',
		getInstance: (hex_input) => new Capsule<string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.split('').reverse().join('');
		},
		tests: {
			reverse: (item) => {
				item.set(ember_reverse(item.get()))
            }
		}
	}).add({
		name: 'Javascript',
		getInstance: (hex_input) => new Capsule<string>().set(hex_input),
		validate: (value, input) => {
			return value.get() === input.split('').reverse().join('');
		},
		tests: {
			reverse: (item, value) => {
                let v = "";
                for(let i = value.length - 1; i > -1; i--) {
                  v += value[i];
                }
                return item.set(v);
            }
		}
	}).report(
		'test'.repeat(500)
	)
