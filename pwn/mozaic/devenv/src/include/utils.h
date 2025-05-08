#pragma once

extern int write(int fd, void* buff, unsigned int bufflen);
extern int read(int fd, void* buff, unsigned int bufflen);

void printline(char* buffer);
void readline(char* buff);
int stringlen(char* string);
void exit(int exitCode);