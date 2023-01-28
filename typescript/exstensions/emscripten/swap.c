#include <emscripten.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>


void EMSCRIPTEN_KEEPALIVE queryString(char** ppStr, char*v_str) {
   int size = strlen(v_str);
   char *g_str = ((char*)malloc(size));
   for (int i = 0; i < size; i++) {
      g_str[size - i - 1] = (v_str)[i];
   }
   *ppStr = g_str;
}
