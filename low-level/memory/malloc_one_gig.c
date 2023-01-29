#include "../helpers/time.c"
#include <stdlib.h>
#include <unistd.h>

/*
    Time used 5 - 8 sec 
    sizeof(int) is 4 bytes, so we allocate 4gb
*/
int main() {
    long start = now();

    int mb = 1000000;
    int gb = 1000 * mb;
    int *memory = (int*)malloc(gb * sizeof(int));
    
    memory[0] = 1;  
    for(int i = 1; i < gb; i++) {
        memory[i] = memory[i - 1] + 1;
    }

    long end = now(); 
    long delta = end - start;

    printf("Time : %li ns\n", delta);
    printf("Time : %li sec\n", delta / BILLION);

    free(memory);
}
