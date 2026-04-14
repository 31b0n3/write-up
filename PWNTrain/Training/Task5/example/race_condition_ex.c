#include <pthread.h>

#include <stdio.h>



int counter;

void *IncreaseCounter(void *args) {

  counter += 1;

  sleep(0.1);

  printf("Thread %d has counter value %d\n", (unsigned int)pthread_self(),

         counter);

}



int main() {

  pthread_t p[10];

  for (int i = 0; i < 10; ++i) {

    pthread_create(&p[i], NULL, IncreaseCounter, NULL);

  }

  for (int i = 0; i < 10; ++i) {

    pthread_join(p[i], NULL);

  }

  return 0;

}

