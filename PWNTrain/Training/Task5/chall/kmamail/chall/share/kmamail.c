#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

char *user;

void backdoor() {
    system("/bin/sh");
}

void init() { // crate dir "data"
    struct stat st;

    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    if (stat("data", &st) != 0 || !S_ISDIR(st.st_mode)) {
        mkdir("data", 0755);
    }
    chdir("data"); //enter dir "data"
}

void reg_acc() {
    struct stat st;
    FILE *f;
    char username[256], password[256];

    printf("Username: ");
    scanf("%255[a-zA-Z0-9]", username);
    printf("Password: ");
    scanf("%255s", password);

    if (stat(username, &st) == 0 && S_ISDIR(st.st_mode)) {
        puts("[-] Account existed!");
        return;
    }
    if (mkdir(username, 0755)!=0) {
        printf("[-] Failed to create user '%s'\n", username);
        return;
    }

    chdir(username);
    f = fopen("passwd", "w");
    if (f==NULL) {
        puts("[-] Failed to open passwd!");
        return;
    }
    fprintf(f, "%s", password);
    fclose(f);
    chdir("..");

    puts("[+] Account created!");
}

bool log_acc() {
    struct stat st;
    FILE *f;
    char username[256], password[256], tmp_password[256];

    printf("Username: ");
    scanf("%255[a-zA-Z0-9]", username);
    printf("Password: ");
    scanf("%255s", tmp_password);

    if (stat(username, &st) != 0 || !S_ISDIR(st.st_mode)) {
        puts("[-] Username or password is incorrect!");
        return false;
    }

    chdir(username);
    f = fopen("passwd", "r");
    if (f==NULL) {
        puts("Failed to open passwd!");
        return false;
    }
    fscanf(f, "%s", password);
    fclose(f);
    chdir("..");

    if (strcmp(password, tmp_password)) {
        puts("[-] Username or password is incorrect!");
        return false;
    }
    user = strdup(username);
    puts("[*] Logged in!");
    return true;
}

void send_mail() {
    struct stat st;
    FILE *f;
    char receiver[256], title[256], content[1024];
    char count = 0;
    int i = 0;

    puts("--- RECEIVER --------------------");
    scanf("%255[a-zA-Z0-9]", receiver);
    getchar();
    puts("--- TITLE -----------------------");
    fgets(title, 256, stdin);
    if (title[strlen(title)-1]=='\n')
        title[strlen(title)-1] = '\0';
    puts("--- CONTENT ---------------------");
    for (i=0; i<1021 && count!=3; i++) {
        content[i] = getchar();
        if (content[i]=='\n') {
            content[i++] = '\\';
            content[i] = 'n';
            count++;
        } else {
            count = 0;
        }
    }

    if (stat(receiver, &st) != 0 || !S_ISDIR(st.st_mode)) {//TOCTOU
        puts("[-] Receiver does not exist!");
        return;
    }

    puts("[*] Sending your email...");
    usleep(1000000);// 

    chdir(receiver);    //Enter to receiver to create file
    f = fopen("mail", "w");
    fprintf(f, "%s\n", user);
    fprintf(f, "%s\n", title);
    fprintf(f, "%s\n", content);
    chdir("..");
    fclose(f);
    puts("[*] Mail sent!");
}

void read_mail() {
    struct stat *st = malloc(sizeof(struct stat));
    FILE *f;
    char *buf;

    chdir(user);
    if (stat("mail", st) != 0) {  
        puts("[-] No mail received!");
        return;
    }
    buf = alloca(st->st_size);

    puts("[*] Opening mail...");
    usleep(1000000);

    puts("[*] Reading mail...");
    f = fopen("mail", "r");
    puts("--- SENDER --------------------");
    fgets(buf, 256, f);
    printf("%s", buf);
    puts("--- TITLE -----------------------");
    fgets(buf, 256, f);
    printf("%s", buf);
    puts("--- CONTENT ---------------------");
    for (int i=0; i<1024; i++) {
        buf[i] = fgetc(f);
        if (buf[i]=='n' && buf[i-1]=='\\') {
            buf[--i] = '\n';
        } else if (buf[i]=='\n') { 
            buf[i] = '\0';
            break;
        }
    }
    printf("%s", buf);

    chdir("..");
}

int main(int argc, char const *argv[])
{
    bool is_done = false, is_login = false;
    int option;

    init();
    while (!is_done) {
        if (is_login) {
            puts("---- MENU ----");
            puts("1. Send mail");
            puts("2. Read mail");
            puts("0. Exit");
            printf("> ");
            scanf("%d", &option);
            getchar();

            switch (option) {
            case 0:
                puts("[*] Logged out!");
                is_login = false;
                break;
            case 1:
                send_mail();
                break;
            case 2:
                read_mail();
                break;
            default:
                puts("[-] Invalid choice!");
            }
        } else {
            puts("---- MENU ----");
            puts("1. Register");
            puts("2. Login");
            puts("0. Exit");
            printf("> ");
            scanf("%d", &option);
            getchar();

            switch (option) {
            case 0:
                puts("[*] See you later!");
                is_done = true;
                break;
            case 1:
                reg_acc();
                break;
            case 2:
                is_login = log_acc();
                break;
            default:
                puts("[-] Invalid choice!");
            }
        }
    }

    return 0;
}