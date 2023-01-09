
export class Input {
	constructor(private n: number) {}


	public random() {
		const results = new Array(this.n).map(() => {
			const chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
			return chars[Math.round(Math.random() * (chars.length - 1))];

		})

		return results.join('');
	}

	public hex() {
		const results = new Array(this.n).map(() => {
			return Math.floor(Math.random() * 16).toString(16);
		});

		return results.join('');
	}
}
