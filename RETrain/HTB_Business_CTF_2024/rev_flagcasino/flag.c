#include <stdio.h>
#include <stdlib.h>
int check(int cipher){
    
    unsigned int seed;   
    for (seed = 0; seed <= 0xFF; seed++) {
        srand(seed);
        if(rand()==cipher){
        printf("%c",seed) ;
        }
        }
    }

int main() {
    int i;
    int cp[] = {0x244B28BE,0x0AF77805,0x110DFC17,0x7AFC3A1,0x6AFEC533,0x4ED659A2,0x33C5D4B0,0x286582B8,0x43383720 ,0x55A14FC,0x19195F9F,0x43383720,0x63149380,0x615AB299,0x6AFEC533,0x6C6FCFB8,0x43383720,0x0F3DA237,0x6AFEC533,0x615AB299,0x286582B8,0x55A14FC,0x3AE44994,0x6D7DFE9,0x4ED659A2,0x0CCD4ACD,0x57D8ED64,0x615AB299,0x22E9BC2A}; 
    for(i = 0;i<29;i++){
        check(cp[i]);
    }  
}
