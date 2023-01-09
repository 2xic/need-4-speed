const EPOCHS = 1_000;


function time(callback: () => void) {
	const start = performance.now();
	
	callback();

	return performance.now() - start;
}

export function benchmark<T, I>({
	name,
	input,
	getInstance,
	tests,
	validate,
}: {
	name: string;
	input: I,
	tests: Record<string, (object: T, item: I) => void>,
	validate: (object: T, input: I) => boolean
	getInstance: (input: I) => T,
}) {

	const results: Record<string, number> = {};

	for (let i = 0; i < EPOCHS; i++) {
		const instance = getInstance(input);

		for (const [name, execute] of Object.entries(tests)) {
			const current = results[name] || 0;
			results[name] = current + time(() => execute(instance, input))
		}
		
		if (!validate(instance, input)){
			throw new Error(`${name} -> Expected successful validation ${input} ${instance}`);
		}
	}

	return results;
}
