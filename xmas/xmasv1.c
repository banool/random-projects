/* Daniel Porteous 696965*/
/* Date: 22/10/14 */

#include <stdio.h> /* Standard I/O */
#include <stdlib.h> /* Standard Library */
#include <string.h>
#include <strings.h>

#define MAXNAME 60
#define MAXPEEPS 50
#define LINELEN 100
#define FILEINP 1
#define NOINP 0

/* For status */
#define     ADULT       100
#define     CHILD       101

/* For gifter_found */
#define     FOUND       110
#define     NOTFOUND    111

typedef struct person person_t;

struct person {
    int status;
    int gifter_found;
    char *name;
    char *prev_gifter;
};

/* Prototypes */

int open_file(int argc, char *argv[]);
int read_line(int fileinput, char *line, int maxlen)

/******************************************************************************/

int
main(int argc, char **argv){
    char line[LINELEN+1];
    
    person_t people[MAXPEEPS];
    
    while(read_line((open_file(argc, argv) != FILEINP), line, LINELEN)){}
    return 0;
}

int
open_file(int argc, char *argv[]){
	if(argc > 1 && ((strcmp(argv[1], "-help")) == 0 || 
	          (strcmp(argv[1], "--help")) == 0 || 
	          (strcmp(argv[1], "-h") == 0))){
	    printf("How to use:\n");
	    
	    exit(EXIT_FAILURE);
	} else if(freopen("data.txt", "r", stdin)==NULL){
        printf("Unable to open \"%s\"\n", "data.txt");
		exit(EXIT_FAILURE);
	    return NOINP;
	} else {
	    return FILEINP;
	}
}

int
read_line(int fileinput, char *line, int maxlen) {
	int i=0, c;
	/* get a whole input line, retain non-blanks only */
	
	while (((c=getchar())!=EOF) && (c!='\n')) {
		if (i<maxlen && !isspace(c)) {
			line[i++] = c;
		}
	}
	line[i] = '\0';
	if (fileinput) {
		/* print out the input command */
		if (line[0]) {
			printf("%c", line[0]);
		}
		if (i>1) {
			/* and the argument */
			printf(" %s", line+1);
		}
		printf("\n");
	}
	return ((i>0) || (c!=EOF));
}