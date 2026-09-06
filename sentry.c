#include <unistd.h>
#include <stdlib.h>

int main() {
	daemon(0,0);

	while(1) {
		// check if src folder has been updated. run sort_music.py if it has
		system("/home/user/Programming/sort_music/0.3/bin/sort_music.py");
		sleep(5);
	}
	return 0;
}
