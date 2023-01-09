import {TestCase} from './helpers/TestCase.js';
import {Input} from './helpers/Input.js';
import {Capsule} from './helpers/Capsule.js';
import crypto from 'crypto';
import sha256 from 'sha256-wasm';
// @ts-ignore
import tz from 'timezone';
import moment from 'moment-timezone';
import dayjs from 'dayjs';
var utc = require('dayjs/plugin/utc')
dayjs.extend(utc)
/*
const date = new Date();
console.log(date.toLocaleString('en-GB', { timeZone: 'Europe/Oslo' }))
console.log(date.toLocaleString('en-GB', { timeZone: 'UTC' }))
process.exit(0);
const time = moment('09/01/2023, 16:34:34');
console.log(
	time.toDate().toLocaleString('en-GB', { timeZone: 'UTC' })
);

process.exit(0)
*/

new TestCase<Date>()
.add({
		name: 'Date.toLocaleString',
		getInstance: (input) => new Date(input.toISOString()),
		validate: (buf, input) => {
			return buf.toLocaleString('en-GB', { timeZone: 'UTC' }) === input.toLocaleString('en-GB', { timeZone: 'UTC' });
		},
		tests: {
			execution: (item) => item.toLocaleString('en-GB', { timeZone: 'UTC' })
		}
})
.add({
		name: 'Date.timezone',
		getInstance: (input) => new Capsule<string>().set(input.toISOString()),
		validate: (buf, input) => {
			return buf.get().toString() === input.toLocaleString('en-GB', { timeZone: 'UTC' });
		},
		tests: {
			execution: (item) => {
				const utc = tz(item.get());
				const converted = moment(new Date(tz(utc,'%c','en-GB','UTC')))
				  .tz('UTC')
				return item.set(converted.format('DD/MM/YYYY, HH:mm:ss'))
			}
		}
})
.add({
		name: 'Moment',
		getInstance: (input) => new Capsule<moment.Moment>().set(moment(input)),
		validate: (buf, input) => {
			return false;
//			return dayjs(buf.get().toDate()) === dayjs(input.toLocaleString('en-GB', { timeZone: 'UTC' })).utc();
		},
		tests: {
			execution: (item) => {
				dayjs(item.get().toDate()).toISOString()
				item.set(item.get().tz('UTC'))
			}
		}
})
.report(
	new Date()
)
