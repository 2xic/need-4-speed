import { TestCase } from './helpers/TestCase.js';
import { Capsule } from './helpers/Capsule.js';
import moment from 'moment-timezone';

import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';
import timezone from 'dayjs/plugin/timezone.js';
// @ts-ignore
import pkg from 'date-fns-tz';
import { DateTime } from 'luxon';
const { formatInTimeZone } = pkg;

// @ts-ignore
import spacetime from 'spacetime';

dayjs.extend(utc)
dayjs.extend(timezone)

const locale = 'en-US';
const timeZone = 'Europe/Oslo';

const INPUT_DATE = new Date().toISOString();
const EXPECTED_DATE = new Date().toLocaleString(locale, { timeZone })


new TestCase<string>({
	iterations: 10_000,
})
	.add({
		name: 'Date.toLocaleString',
		getInstance: (input) => new Capsule().set(INPUT_DATE),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				item.set(new Date(INPUT_DATE).toLocaleString(locale, { timeZone }))
			}
		}
	})
	.add({
		name: 'Moment tz',
		getInstance: (input) => new Capsule<string>().set(input),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				let converted = moment(
					item.get()
				).tz(timeZone)

				return item.set(converted.format('M/D/YYYY, h:mm:ss A'))
			}
		}
	})
	.add({
		name: 'Dayjs tz',
		getInstance: (input) => new Capsule<string>().set(input),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				const converted = dayjs(item.get())
					.tz(timeZone)
				return item.set(converted.format('M/D/YYYY, h:mm:ss A'))
			}
		}
	})

	.add({
		name: 'Intl.DateTimeFormat',
		getInstance: (input) => new Capsule<string>().set(input),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				return item.set(new Intl.DateTimeFormat('en-US', {
					timeZone,
					year: 'numeric', month: 'numeric', day: 'numeric',
					hour: 'numeric', minute: 'numeric', second: 'numeric',
					hour12: true,
				}).format(new Date(item.get())))
			}
		}
	})

	.add({
		name: 'date-fns-tz',
		getInstance: (input) => new Capsule<string>().set(input),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				return item.set(formatInTimeZone(
					(item.get()),
					timeZone,
					'M/d/yyyy, h:mm:ss a'
				))
			}
		}
	})

	.add({
		name: 'Luxon',
		getInstance: (input) => new Capsule<string>().set(input),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				return item.set(
					DateTime.fromISO(item.get()).setZone(timeZone).toFormat(
						'M/d/yyyy, h:mm:ss a'
					)
				)
			}
		}
	})


	.add({
		name: 'spacetime',
		getInstance: (input) => new Capsule<string>().set(input),
		validate: (buf) => {
			return buf.get() === EXPECTED_DATE;
		},
		tests: {
			execution: (item) => {
				return item.set(
					spacetime(item.get()).goto(timeZone).unixFmt(
						'M/d/yyyy, h:mm:ss a'
					)
				)
			}
		}
	})
	/*
	.add({
		name: 'Temporal',
		https://github.com/tc39/proposal-temporal
		// Not out yet.,
	})
	*/
	.report(
		INPUT_DATE,
		{sorted: true}
	)
