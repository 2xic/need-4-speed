

export class Capsule<T> {
	private value: T | undefined;

	public set(value:T) {
		this.value = value;
		return this;
	}

	public get() {
		if (!this.value) {
			throw new Error('Value not set');
		}
		return this.value;
	}

	/*
	public toString() {
		return this.value.toString();
	}
	*/
}

