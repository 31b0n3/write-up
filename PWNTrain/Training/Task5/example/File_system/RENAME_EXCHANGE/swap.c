#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/fs.h>
#include <errno.h> // Added this to read system errors

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <file1> <file2>\n", argv[0]);
        return 1;
    }

    while (1) {
        // We capture the result of the syscall into an integer variable
        int result = syscall(SYS_renameat2, AT_FDCWD, argv[1], AT_FDCWD, argv[2], RENAME_EXCHANGE);
        
        // Check if the result is -1 (which means an error occurred)
        if (result == -1) {
            perror("The swap failed because"); // Prints the exact error message
            return 1; // Kill the program so it doesn't spam your terminal forever
        } else {
            printf("DONE\n");
        }
    }

    return 0;
}