emcc swap.c -o out/swap.cjs -s\
"EXTRA_EXPORTED_RUNTIME_METHODS=['UTF8ToString', 'allocateUTF8', 'getValue']" \
-s "EXPORTED_FUNCTIONS=['_malloc', '_free']"
