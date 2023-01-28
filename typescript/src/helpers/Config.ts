
export class Config {
    constructor(
        private options: ConfigOptions
    ) {}

    public get iterations() {
        return this.options.iterations;
    }

    public get raw() {
        return this.options;
    }
}

export interface ConfigOptions {
    iterations: number;
}
