import { TestCase } from './helpers/TestCase.js';
import { Capsule } from './helpers/Capsule.js';
// @ts-ignore
import tz from 'timezone';
import moment from 'moment-timezone';

import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';
import timezone from 'dayjs/plugin/timezone.js';
import weekday from 'dayjs/plugin/weekday.js';
import minMax from 'dayjs/plugin/minMax.js';

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(weekday);
dayjs.extend(minMax);

const locale = 'en-US';
const timeZone = 'Europe/Oslo';

const INPUT_DATE = new Date().toISOString();
const EXPECTED_DATE = new Date().toLocaleString(locale, { timeZone })


new TestCase<string>({
    iterations: 10_000,
})
    .add({
        name: 'dayjs example line (dayjs)',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                dayjs().startOf('month').add(1, 'day').set('year', 2018).format('YYYY-MM-DD HH:mm:ss');
            }
        }
    })
    .add({
        name: 'dayjs example line (moment)',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                moment().startOf('month').add(1, 'day').set('year', 2018).format('YYYY-MM-DD HH:mm:ss');
            }
        }
    })
    .add({
        name: 'dayjs.utc()',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                dayjs().utc()
            }
        }
    })
    .add({
        name: 'moment.utc()',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                moment().utc()
            }
        }
    })
    .add({
        name: 'dayjs -> oslo -> utc',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                dayjs().tz('Europe/Oslo').utc().toISOString()
            }
        }
    })
    .add({
        name: 'moment -> oslo -> utc',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                item.set(moment().tz('Europe/Oslo').utc().toISOString())
            }
        }
    })
    .add({
        name: 'dayjs(precomputed) -> oslo -> utc',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                dayjs().tz('Europe/Oslo').utc().toISOString()
            }
        }
    })
    .add({
        name: 'moment(precomputed) -> oslo -> utc',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return buf.get() == dayjs('2022-01-01').tz('Europe/Oslo').utc().startOf('day').toISOString();

        },
        tests: {
            execution: (item) => {
                item.set(moment('2022-01-01').tz('Europe/Oslo').utc().startOf('day').toISOString())
            }
        }
    })
    .add({
        name: 'dayjs(precomputed).weekday()',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                dayjs().weekday().toString()
            }
        }
    })
    .add({
        name: 'moment(precomputed).weekday()',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return buf.get() == dayjs('2022-01-01').weekday().toString();
        },
        tests: {
            execution: (item) => {
                item.set(moment('2022-01-01').weekday().toString())
            }
        }
    })







    .add({
        name: 'dayjs.min',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                item.set(dayjs.min([
                    dayjs('2022-01-01'),
                    dayjs('2022-01-02')
                ]).toString())
            }
        }
    })
    .add({
        name: 'moment.min',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                item.set(moment.min([
                    moment('2022-01-02'),
                    moment('2022-01-01')
                ]).toString())
            }
        }
    })


    .add({
        name: 'dayjs.max',
        getInstance: (input) => new Capsule().set(INPUT_DATE),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                item.set(dayjs.max([
                    dayjs('2022-01-01'),
                    dayjs('2022-01-02')
                ]).toString())
            }
        }
    })
    .add({
        name: 'moment.max',
        getInstance: (input) => new Capsule<string>().set(input),
        validate: (buf) => {
            return true;
        },
        tests: {
            execution: (item) => {
                item.set(moment.max([
                    moment('2022-01-02'),
                    moment('2022-01-01')
                ]).toString())
            }
        }
    })
    .report(
        INPUT_DATE
    )
