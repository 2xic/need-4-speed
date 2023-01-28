const Module = require('./out/swap.cjs');

class ExportClass {
    constructor() {}

    async init() {
        await new Promise((resolve) => {
            Module['onRuntimeInitialized'] = function () {
                resolve();
            }
        })
    }

    reverse(string) {
        var string_in_ptr = Module.allocateUTF8(string);
        var ppcStr = Module._malloc(4);
        Module._queryString(ppcStr, string_in_ptr);
        var pcStr = Module.getValue(ppcStr, "i32");
        var jsStr = Module.UTF8ToString(pcStr);
        Module._free(ppcStr);
        Module._free(string_in_ptr);
        return jsStr;
    }
}

const x = new ExportClass();

module.exports = {
    reverse: ((str) => x.reverse(str))
};
