/* Daniel Porteous
   696965
   25/10/14
 */
 
/* be able to print tree, print a list oh who is 
   gifting who, also output to a file */
   
/* Changed to a linked structure */

/*********************************************************/
/* Hash includes */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

/*********************************************************/
/* Hash defines */
#define MAXNAME  20
#define MAXLINE  80
#define MAXFAM   20

#define ADULT    100
#define CHILD    101

#define FILENAME "data.txt"

/*********************************************************/
/* Defining necessary structures */
typedef struct person_s person_t;

struct person_s {
    char *fname;
    char *lname;
    char *lastyear;
    int gifted;
    int status;
};


/*********************************************************/
/* Function prototypes */
int      read_line(char *line, int maxlen);
person_t populate_struct(char *line);
void     print_array(person_t A[], int n);

/*********************************************************/

int
main(int argc, char *argv[]) {
    char indiv_line[MAXLINE+1];
    int num_adults = 0, num_children = 0;
    
    person_t temp;
    person_t adults[MAXFAM];
    person_t children[MAXFAM];
    
    /* Opening the data file */
    if (freopen(FILENAME, "r", stdin)==NULL) {
	    printf("Unable to open \"%s\"\n", FILENAME);
		exit(EXIT_FAILURE);
	}
	printf("File %s opened.\n", FILENAME);
	
    while(read_line(indiv_line, MAXLINE)) {
        /* Ignore comments and empty lines */
        if(indiv_line[0] != '#' && indiv_line[0]) {
            temp = populate_struct(indiv_line);
            if(temp.status == ADULT){
                adults[num_adults++] = temp;
            } else {
                children[num_children++] = temp;
            }
        }
    }
    printf("Generated array\n");
    
    
    
    print_array(children, num_children);
    print_array(adults, num_adults);
    return 0;
}

/*********************************************************/
/* read a line of input into the array passed as argument
 * returns false if there is no input available
 * all whitespace characters are removed
 */
int
read_line(char *line, int maxlen) {
	int i=0, c;
	/* get a whole input line, retain non-blanks only */
	
	while (((c=getchar())!=EOF) && (c!='\n')) {
		if (i<maxlen && !isspace(c)) {
			line[i++] = c;
		}
	}
	line[i] = '\0';
	return ((i>0) || (c!=EOF));
}

/*********************************************************/

/* root retains the original head.
   next is used to track down the tree.
   temp holds the new node.
 */


/* Getting all the data from the line */

person_t
populate_struct(char *line) {
    int i = 0, j = 0;
    person_t output;
    
    /* Mallocing space for and writing to first name */
    output.fname = malloc(sizeof(char)*MAXNAME+1);
    assert(output.fname);
    while(line[i] != ','){
        output.fname[j++] = line[i++];
    }
    output.fname[j] = '\0';
    i++;
    j = 0;
    
    /* Again, but for last name */
    output.lname = malloc(sizeof(char)*MAXNAME+1);
    assert(output.lname);
    while(line[i] != ','){
        output.lname[j++] = line[i++];
    }
    output.lname[j] = '\0';
    i++;
    j = 0;
    
    /* Getting the adult/child status */
    if(line[i] == 'A'){
        output.status = ADULT;
    } else if (line[i] == 'C'){
        output.status = CHILD;
    } else {
        printf("The entry %s %s has an invalid status\n",
               output.fname, output.lname);
        printf("It must be must be A or C, fix your data.\n");
        exit(EXIT_FAILURE);
    }
    
    return output;
}

void
print_array(person_t A[], int n){
    int i;
    for(i=0; i<n; i++){
        printf("%s, ", A[i].fname);
    }
    printf("\n");
}