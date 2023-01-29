#include "../helpers/time.c"
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

/*
    Is malloc always used as syscall ? 
    Seems like it.

    Expected brk / sbrk
*/
int* allocate_segment(int bytes){
    int *memory = (int*)malloc(bytes * sizeof(int));
    
    memory[0] = 1;  
    for(int i = 1; i < bytes; i++) {
        memory[i] = memory[i - 1] + 1;
    }

    return memory;
}


int main() {
    long start = now();

    int mb = 1000000;
    int gb = 1000 * mb;

    int* small_segment = allocate_segment(32);
    free(small_segment);

    int* medium_segment = allocate_segment(gb / 4);
    free(medium_segment);

    int* big_segment = allocate_segment(gb);
    free(big_segment);

    long end = now(); 
    long delta = end - start;

    printf("Time : %li ns\n", delta);
    printf("Time : %li sec\n", delta / BILLION);
}
