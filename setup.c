#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#endif

#define SOURCE_DIR "exe"
#define TARGET_DIR "C:\\Program Files\\MyApp"  // Windows path
#define TARGET_ENV_VAR "MYAPP_HOME"

void install_windows() {
    printf("Installing on Windows...\n");
    
    // Create target directory
    if (CreateDirectory(TEXT(TARGET_DIR), NULL) || GetLastError() == ERROR_ALREADY_EXISTS) {
        printf("Target directory created or already exists.\n");
    } else {
        printf("Error creating target directory: %d\n", GetLastError());
        return;
    }
    
    // Copy files from source directory to target directory
    WIN32_FIND_DATA findFileData;
    HANDLE hFind = FindFirstFile(TEXT(SOURCE_DIR "\\*"), &findFileData);
    if (hFind == INVALID_HANDLE_VALUE) {
        printf("Error finding files: %d\n", GetLastError());
        return;
    }
    
    do {
        if (!(findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            char sourcePath[MAX_PATH];
            char targetPath[MAX_PATH];
            snprintf(sourcePath, MAX_PATH, "%s\\%s", SOURCE_DIR, findFileData.cFileName);
            snprintf(targetPath, MAX_PATH, "%s\\%s", TARGET_DIR, findFileData.cFileName);
            
            if (CopyFile(sourcePath, targetPath, FALSE)) {
                printf("Copied %s to %s\n", sourcePath, targetPath);
            } else {
                printf("Error copying file %s: %d\n", sourcePath, GetLastError());
            }
        }
    } while (FindNextFile(hFind, &findFileData) != 0);
    
    FindClose(hFind);
    
    // Set environment variable
    if (SetEnvironmentVariable(TEXT(TARGET_ENV_VAR), TEXT(TARGET_DIR))) {
        printf("Environment variable %s set to %s\n", TARGET_ENV_VAR, TARGET_DIR);
    } else {
        printf("Error setting environment variable: %d\n", GetLastError());
    }
}

void install_linux() {
    printf("Installing on Linux...\n");
    
    // Execute the setup script
    int ret = system("./setup.sh");
    if (ret == 0) {
        printf("Setup script executed successfully.\n");
    } else {
        perror("Error executing setup script");
    }
}

int main() {
#ifdef _WIN32
    install_windows();
#else
    install_linux();
#endif

    printf("Installation complete!\n");
    return 0;
}
