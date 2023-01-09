import {markdownTable} from 'markdown-table';
import {benchmark} from './benchmark.js';

export class TestCase<I> {
	private testCases: TestCaseDescription<any, I>[] = [];

	constructor() {}

	private results: Record<string, Record<string, number>> = {};
		
	public add<V>(testCase: TestCaseDescription<V, I>) {
		this.testCases.push(testCase);
		return this;
	}

	public execute(inputs: I[]) {
		this.testCases.map((item) => {
			inputs.forEach((input) => {
				const benchmarkResults = benchmark({
					name: item.name,
					input,
					getInstance: item.getInstance,
					tests: item.tests,
					validate: item.validate,
				});
				
				this.results[item.name] = this.results[item.name] || ({} as Record<string, number>);

				for(const [key, value] of Object.entries(benchmarkResults)) {
					const prev = this.results[item.name][key] || 0;
					this.results[item.name][key] = prev + value;
				}
			})
		});

		this.testCases = this.testCases.slice(this.testCases.length)

		return this.results;
	}

	public report(input: I | I[], options?: {
		sorted: boolean
	}) {
		const inputs = Array.isArray(input) ? input: [input];
		const testCases = this.execute(inputs);

		const columns: string[] = []
		let rows: string[][] =  [];

		if (!columns.includes('name')) {
			columns.push('name');
		}

		Object.entries(testCases).map(([name, results]) => {
			for (const [column, value] of Object.entries(results)) {
				if (!columns.includes(column)) {
					columns.push(column);
				}
			}

			rows.push([...columns.map((item) => {
				if (item === 'name'){
					return name;
				}
				return results[item].toString()
			})]);
		})

		if (!columns.includes('total')) {
			columns.push('total');
		}

		rows = rows.map((item) => {
			const sum_row = item.slice(1).reduce((a,b) => a + b);

			return [...item, sum_row];
		})

		if (options?.sorted) {
			rows = rows.sort((row_a, row_b) => {
				return (parseInt(row_a[row_a.length - 1]) - parseInt(row_b[row_b.length - 1]))
			})
		}

		rows = rows.map((item) => {
			return item.map((item, index) => {
				if (index === 0) {
					return item;
				} else {
					const [first, second] = item.toString().split(".");
					//console.log(item.toString().split("."))
					return first + "." + second.padEnd(22, "0");
				}
			})
		})

		const results = markdownTable([
    	[...columns],
    	...rows,
	  ], {align: ['l', 'c', 'r']})
		
		console.log(results);
		console.log('')
	}
}

interface TestCaseDescription<V, I> {
	name: string;
	getInstance: (input: I) => V,
	tests: Record<string, (object: V, item: I) => void>
	validate: (object: V, input: I) => boolean
}
