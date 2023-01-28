import { Config, ConfigOptions } from "./Config.js";

export class Benchmark {
	public config: Config;

	constructor(
		options?: Partial<ConfigOptions>
	) {
		this.config = new Config({
			iterations: 10_000,
			...options,
		});
	}


	public benchmark<T, I>({
		name,
		input,
		tests,
		getInstance,
		validate,
	}: {
		name: string;
		input: I,
		tests: Record<string, (object: T, item: I) => void>,
		validate: (object: T, input: I) => boolean
		getInstance: (input: I) => T,
	}) {

		const results: Record<string, number> = {};

		for (let i = 0; i < this.config.iterations; i++) {
			const instance = getInstance(input);

			for (const [name, execute] of Object.entries(tests)) {
				const current = results[name] || 0;
				results[name] = current + this.time(() => execute(instance, input))
			}

			if (!validate(instance, input)){
				throw new Error(`${name} -> Expected successful validation ${input} ${instance}`);
			}
		}

		return results;
	}

	private time(callback: () => void) {
		const start = performance.now();

		callback();

		return performance.now() - start;
	}
}
