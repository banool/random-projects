/* Daniel Porteous
   696965
   25/10/14
 */
 
/* be able to print tree, print a list oh who is 
   gifting who, also output to a file */

/*********************************************************/
/* Hash includes */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

/*********************************************************/
/* Hash defines */
#define MAXNAME 20
#define MAXLINE 80

#define ADULT 100
#define CHILD 101

#define FILENAME "data.txt"

/*********************************************************/
/* Defining necessary structures */
typedef struct person_s person_t;

struct person_s {
    char *fname;
    char *lname;
    char *lastyear;
    int status;
    int gifted;
};

typedef struct node_s node_t;

struct node_s {
    person_t data;
    node_t *left, *rght;
};

/*********************************************************/
/* Function prototypes */
node_t *createNode(char *line, node_t *root);
int     read_line(char *line, int maxlen);
node_t *process_line(char *line, node_t *root);
void    do_print_p(node_t *root);
void    printp_recursion(node_t *root, int *count);

/*********************************************************/

int
main(int argc, char *argv[]) {
    char indiv_line[MAXLINE+1];
    
    node_t *root=NULL;
    
    /* Opening the data file */
    if (freopen(FILENAME, "r", stdin)==NULL) {
	    printf("Unable to open \"%s\"\n", FILENAME);
		exit(EXIT_FAILURE);
	}
	printf("File %s opened.\n", FILENAME);
	
    while(read_line(indiv_line, MAXLINE)) {
        /* Ignore comments */
        if(indiv_line[0] != '#' && indiv_line[0]) {
            root = process_line(indiv_line, root);
        }
    }
    do_print_p(root);
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

node_t
*process_line(char *line, node_t *root) {
    node_t *next, *temp;
    
    if(!root){
        root = createNode(line, root);
    }
    
    next = root;
    temp = createNode(line, root);
    while(next) {
        /*printf("\nnext: %s\n temp: %s\n", next->data.fname, temp->data.fname); */
        /* Alphabetically less */
        if(strcmp(next->data.fname, temp->data.fname) > 0) {
            if(next->left) {
                /*printf("going left\n"); */
                next = next->left;
            } else {
                /*printf("making at left"); */
                next->left = temp;
            }
        }
        /* Alphabetically more */
        else if(strcmp(next->data.fname, temp->data.fname) < 0) {
            if(next->rght) {
                /*printf("going right\n"); */
                next = next->rght;
            } else {
                /*printf("making at right\n"); */
                next->rght = temp;
            }
        }
        /* Same. Thus the string already exists in the tree */
        else {
            return root;
        }
    }
    return root;

}

/* Getting all the data from the line */

node_t
*createNode(char *line, node_t *root) {
    int i = 0, j = 0;
    
    /* Iniitially mallocing the node */
    node_t *p = malloc(sizeof(node_t));
    assert(p);
    
    /* Mallocing space for and writing to first name */
    p->data.fname = malloc(sizeof(char)*MAXNAME+1);
    assert(p->data.fname);
    while(line[i] != ','){
        p->data.fname[j++] = line[i++];
    }
    p->data.fname[j] = '\0';
    i++;
    j = 0;
    
    /* Again, but for last name */
    p->data.lname = malloc(sizeof(char)*MAXNAME+1);
    assert(p->data.lname);
    while(line[i] != ','){
        p->data.lname[j++] = line[i++];
    }
    p->data.lname[j] = '\0';
    i++;
    j = 0;
    
    /* Getting the adult/child status */
    if(line[i] == 'A'){
        p->data.status = ADULT;
    } else if (line[i] == 'C'){
        p->data.status = CHILD;
    } else {
        printf("The entry %s %s has an invalid status\n",
               p->data.fname, p->data.lname);
        printf("It must be must be A or C, fix your data.\n");
        exit(EXIT_FAILURE);
    }
    
    /* Setting the left and right pointers to NULL */
    p->left = NULL;
    p->rght = NULL;
    return p;
}


/* print out a tree, simple formatting
 */

void
do_print_p(node_t *root) {
    int count = 0;
    printf("\n");
    if(root){
        printp_recursion(root, &count);
    }
    printf("\n");
}

/* By recursing down the right branch when possible, then
   the left branch, it prints the tree in alphabetical order.
   The count variable tracks recursion depth so that the
   correct whitespace can be printed.
 */

void
printp_recursion(node_t *root, int *count){
    int i;
    
    if(root->rght){
        *count += 1;
        printp_recursion(root->rght, count);
        *count -= 1;
    }
    
    for(i=0; i < (*count); i++){
        printf("      ");
    }
    printf("%s %c\n", root->data.fname, root->data.lname[0]);
    
    if(root->left){
        *count += 1;
        printp_recursion(root->left, count);
        *count -= 1;
    }
}