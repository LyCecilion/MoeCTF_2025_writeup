#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srandom(time(0));
    printf("%d\n", random() % 114514);
    return 0;
}