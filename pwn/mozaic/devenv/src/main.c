
#include "./include/utils.h"

extern char banner[];

void printHelp()
{
    printline(
        "Commands implemented are:\n"
        "default: -- read from stdin and echo on stdout\n"
        "\tuntill quit command is issued\n"
        "h: -- print this message\n"
        "q: -- quit\n"
        "more commands coming soon!"
    );
}

void parseCommand(char* command, unsigned int* exitFlag)
{
    switch(*command){
    case 'h':
        printHelp();
        break;
    case 'q':
        *exitFlag = 1;
        break;
    default:
        printline(command);
        break;
    }
}

void loop()
{
    unsigned int exitFlag = 0;
    char buffer[64] = {0};

    while(1){
        write(1, "$> ", 3);
        readline(buffer);
        parseCommand(buffer, &exitFlag);
        if(exitFlag == 1)
            break;
    }
}

void printBanner()
{
    printline(banner);
}

void _start()
{
    printBanner();
    printHelp();
    loop();

    exit(0);
}