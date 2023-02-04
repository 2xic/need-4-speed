#include "../helpers/time.c"
#include <stdlib.h>
#include <unistd.h>

/*
    Time used ~25 sec sec 
    sizeof(int) is 4 bytes, so we write ~ 4gb
*/
int main() {
    long start = now();

    int mb = 1000000;
    int gb = 1000 * mb;
    FILE *fptr = fopen(".dummy","w");
    int value = 42;
    for(int i = 1; i < gb; i++) {
        // fwrite will also seek
        fwrite(&value, sizeof(int), 1, fptr); 
    }

    fclose(fptr);

    long end = now(); 
    long delta = end - start;

    printf("Time : %li ns\n", delta);
    printf("Time : %li sec\n", delta / BILLION);
}
