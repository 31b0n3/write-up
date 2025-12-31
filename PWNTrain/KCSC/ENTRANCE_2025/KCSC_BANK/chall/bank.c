#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#define MAX_LEN 0x10
struct GlobalState {
    char username[MAX_LEN];
    char password[MAX_LEN];
    char description[MAX_LEN];
    unsigned long long balance;
} state;

#define username state.username
#define password state.password
#define description state.description

void (*funcViewBalance)(void) = NULL;

void viewBalance(void);

void timeout(int sig) {
    if (sig == SIGALRM) {
        printf("\nTimeout!\n");
        exit(0);
    }
}

void init()
{
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    setbuf(stdin, NULL);
    signal(SIGALRM, timeout);
    alarm(60);
    funcViewBalance = &viewBalance;
}

void menu()
{
    printf("=====================\n");
    printf("===== KCSC BANK =====\n");
    printf("=====================\n");
    printf("1. Register\n");
    printf("2. Login\n");
    printf("3. Exit\n");
}

void registerUser()
{
    printf("Username: ");
    fgets(username, MAX_LEN, stdin);
    printf("Password: ");
    fgets(password, MAX_LEN, stdin);
    printf("Description: ");
    fgets(description, MAX_LEN, stdin);
    printf("Registration successful!\n");
}

bool login()
{
    char user[MAX_LEN] = {0};
    char pass[MAX_LEN] = {0};
    if (username[0] == 0 || password[0] == 0)
    {
        printf("No registered user. Please register first.\n");
        return false;
    }
    printf("Username: ");
    fgets(user, MAX_LEN, stdin);
    printf("Password: ");
    fgets(pass, MAX_LEN, stdin);
    if (strcmp(user, username) != 0 || strcmp(pass, password) != 0)
    {
        printf("Login failed!\n");
        return false;
    }
    printf("Login successful!\n");
    return true;
}

void menu2()
{
    printf("=====================\n");
    printf("===== KCSC BANK =====\n");
    printf("=====================\n");
    printf("1. View Balance\n");
    printf("2. View Description\n");
    printf("3. Change Description\n");
    printf("4. Feedback\n");
    printf("5. Exit\n");
}
void viewDescription()
{
    printf("Description: %s\n", description);
}
void viewBalance()
{
    printf("Balance: %lld\n", state.balance);
}
void changeDescription()
{
    printf("New Description: ");
    int size = read(0, description, MAX_LEN + 0x10);
    description[size] = '\x00';
    printf("Description updated!\n");
}
void feedback()
{
    char feedback[256];
    printf("Your Feedback: ");
    fgets(feedback, sizeof(feedback), stdin);
    state.balance += 1;
    printf("Thank you for your feedback!\n");
}
void win()
{
    char flag[512];
    FILE *f = fopen("/flag.txt", "r");
    if (f == NULL)
    {
        printf("Flag file not found!\n");
        return;
    }
    fgets(flag, sizeof(flag), f);
    printf("Congratulations! Here is your flag: %s\n", flag);
    fclose(f);
}
void main()
{
    int choice;
    bool checkLogin = false;
    init();
    while (true)
    {
        menu();
        printf("Choice: ");
        scanf("%d", &choice);
        getchar(); // consume newline
        switch (choice)
        {
            case 1:
                registerUser();
                break;
            case 2:
                checkLogin = login();
                break;
            case 3:
                printf("Exiting...\n");
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }

        if(checkLogin)
            break;
    }

    while (true)
    {
        menu2();
        printf("Choice: ");
        scanf("%d", &choice);
        getchar(); // consume newline
        switch (choice)
        {
            case 1:
                funcViewBalance();
                break;
            case 2:
                viewDescription();
                break;
            case 3:
                changeDescription();
                break;
            case 4:
                feedback();
                break;
            case 5:
                printf("Exiting...\n");
                return;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}