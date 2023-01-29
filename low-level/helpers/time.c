#include <time.h> 
#include <stdlib.h>
#include <stdio.h>

#define BILLION  1000000000L

long now() {
    struct timespec start;

    if( clock_gettime( CLOCK_REALTIME, &start) == -1 ) {
      printf( "clock gettime" );
      exit( EXIT_FAILURE );
    }

    return start.tv_sec * BILLION + start.tv_nsec;
}
