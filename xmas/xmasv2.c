/* Daniel Porteous 696965*/
/* Date: 22/10/14 */

#include <stdio.h> /* Standard I/O */
#include <stdlib.h> /* Standard Library */
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <assert.h>

#define LINELEN	80	/* maximum length of any input line */

#define INSERT	'i'	/* command to add a string */
#define PRINT1	'p'	/* command to do plain print */
#define PRINT2	's'	/* command to do snazzy print */
#define ROTATE	'r'	/* command to do a tree edge rotation */
#define TABULA	't'	/* command to tabulate statistics */
#define FREEIT	'f'	/* command to free all space */
#define ALLOPS  "irpstf"
			/* list of all valid operators */

#define FILINP	1	/* indicates input coming from a file */
#define PROMPT	"> "
#define FILENAME "data.txt"
#define COMMENT "#"

/* For status */
#define     ADULT       100
#define     CHILD       101

/* For gifter_found */
#define     FOUND       110
#define     NOTFOUND    111

#define IGNORE 121

/****************************************************************/

typedef struct node tree_t;

struct node {
	char *str;
	tree_t *left, *rght;
};

/****************************************************************/

/* function prototypes */

int     checkargs(int argc, char **argv);
void    print_prompt();
int     read_line(int fileinput, char *line, int maxlen);
tree_t *process_line(tree_t *root, char *line);
tree_t *do_insert(tree_t *root, char *str);
tree_t *do_rotate(tree_t *root, char *str);
void    do_print_p(tree_t *root);
void    do_print_s(tree_t *root);
void    do_tabulate(tree_t *root);
void    do_freeit(tree_t *root);

/****************************************************************/

/* Extra function prototypes */

void    printp_recursion(tree_t *root, int *count);
void    tablulate_recursion(tree_t *root, int *numwords,
                            int *count, int *maxdepth, int *total);
void    free_recursion(tree_t *root);
tree_t *createNode(char *inpstr);
void    prints_recursion(tree_t *root, int *count);
tree_t *rotate_recursion(tree_t *root, char *str);

/****************************************************************/

/* main program controls all the action
 */
int
main(int argc, char *argv[]) {
	char line[LINELEN+1];
	int fileinput=0;
	tree_t *root=NULL;

	/* check commandline, process argv */
	fileinput = checkargs(argc, argv);

	/* start the main execution loop */
	print_prompt();
	while (read_line(fileinput, line, LINELEN)) {
		if (strlen(line)>0 && (strchr(COMMENT, line[0]) == NULL)) {
			/* non empty line, so process it */
			root = process_line(root, line);
		}
		/* then round we go */
		print_prompt();
	}

	/* all done, so pack up and go home */
	printf("Ta daaa!\n");
	return 0;
}

/****************************************************************/

/*
 * if there is a valid filename on the commandline, redirect stdin
 * so that the file is read, and return FILINP to show that input
 * input lines should be echoed to the output when they are read
 */

int
checkargs(int argc, char **argv) {
	if (argc==1) {
		if (freopen(FILENAME, "r", stdin)==NULL) {
			printf("Unable to open \"%s\"\n", argv[1]);
			exit(EXIT_FAILURE);
		}
		/* Successfuly read file */
		return FILINP;
	} else {
		printf("This program takes no command line arguments.\n");
		exit(EXIT_FAILURE);
	}
	/* no command line parameters, so stdin is used unchanged */
	return 0;
}

/****************************************************************/

/* print the "ready for input" prompt
 */
void
print_prompt() {
	printf(PROMPT);
}

/****************************************************************/

/* read a line of input into the array passed as argument
 * returns false if there is no input available
 * all whitespace characters are removed
 */
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

/****************************************************************/

/* process a command by parsing the input line into parts, returns
   a tree build from the old one by returning a new root pointer
 */
tree_t
*process_line(tree_t *root, char *line) {
	int optype;

	/* determine the operation to be performed, it
	 * must be first character in line
	 */
	optype = line[0];
	if (strchr(ALLOPS, optype) == NULL) {
		printf("Unknown operator\n");
		return root;
	}

	/* determine the string argument (if one is required),
	 * it must start in second character of line
	 */
	if (optype==PRINT1 || optype==PRINT2 ||
			optype==TABULA || optype==FREEIT) {
		if (strlen(line)>1) {
			printf("No argument required\n");
			return root;
		}
	}
	if (optype==INSERT || optype==ROTATE) {
		if (strlen(line)<2) {
			printf("An argument is required\n");
			return root;
		}
	}

	/* finally, do the actual operation
	 */
	if (optype == PRINT1) {
		do_print_p(root);
		return root;
	} else if (optype == PRINT2) {
		do_print_s(root);
		return root;
	} else if (optype == TABULA) {
		do_tabulate(root);
		return root;
	} else if (optype == FREEIT) {
		do_freeit(root);
		return NULL;
	} else if (optype == INSERT) {
		return do_insert(root, line+1);
	} else if (optype == ROTATE) {
		return do_rotate(root, line+1);
	}
	/* should never get here, but keeps compiler silent... */
	return root;
}

/****************************************************************/


/* print out a tree, simple formatting
 */

void
do_print_p(tree_t *root) {
    int count = 0;
    if(root){
        printp_recursion(root, &count);
    }
}

/* By recursing down the right branch when possible, then
   the left branch, it prints the tree in alphabetical order.
   The count variable tracks recursion depth so that the
   correct whitespace can be printed.
 */

void
printp_recursion(tree_t *root, int *count){
    int i;
    
    if(root->rght){
        *count += 1;
        printp_recursion(root->rght, count);
        *count -= 1;
    }
    
    for(i=0; i < (*count); i++){
        printf("     ");
    }
    
    printf("%s\n", root->str);
    if(root->left){
        *count += 1;
        printp_recursion(root->left, count);
        *count -= 1;
    }
}


/****************************************************************/


/* print out a tree, snazzy formatting
 */
void
do_print_s(tree_t *root) {
    int count;
    /* Just could not get this snazzy print to work.
       Uncomment line 308 if you really want to take a look. */
    if(root){
        count = 0;
        /*prints_recursion(root, &count);*/
    }
}

void
prints_recursion(tree_t *root, int *count){
    int i;
    
    if(root->rght){
        *count = *count + 1;
        prints_recursion(root->rght, count);
        *count = *count - 1;
    }
    
    for(i=0; i <= *count; i++){
        if(i==*count && (!root->rght || !root->left)){
            printf("  +--");
        } else if(*count != 1 && (i==0 || i == *count-1)){
            printf("  |  ");
        } else {
            printf("     ");
        }
    }
    printf("\n");
    
    for(i=0; i < *count; i++){
        if(i==*count-1){
            printf("  +--");
        }
        else if(i == 0 && i != *count-1){
            printf("  |  ");
        } else {
            printf("     ");
        }
    }
    printf("%s\n", root->str);
    
    if(!root->left){
        for(i=0; i <= *count; i++){
            if(i==*count){
                printf("  +--");
            }
            else if(i == 0 && i != *count-1){
                printf("  |  ");
            } else {
                printf("     ");
            }
        }
        printf("\n");
    }

    if(root->left){
        *count += 1;
        prints_recursion(root->left, count);
        *count -= 1;
    }
}
    

/****************************************************************/

/* update the tree by adding in the new string; if already there
   return the same tree
 */

/* Only iterative function, all others are done recursively.
   This is because the insert is always at the end of a branch
   Moves straight down the tree, checking each node for
   alphabetical difference. Follows the pointer that strcmp
   designates if a node already exists, otherwise creating a new
   node there with createNode, thus inserting itself into the tree.
 */

tree_t
*do_insert(tree_t *root, char *str) {
    tree_t *next;
    
    /* Will not run initially, but is necessary since there
       will be no root after freeing. Also, since the root 
       is initally a null pointer, and we can't change the 
       main/function interface, this creates the 
       head of the tree upon first insert call. */
    if(!root){
        root = createNode(str);
    }
    
    next = root;
    while(next) {
        /* Alphabetically less */
        if(strcmp(str, next->str)<0) {
            if(next->left) {
                next = next->left;
            } else {
                next->left = createNode(str);
            }
        }
        /* Alphabetically more */
        else if(strcmp(str, next->str)>0) {
            if(next->rght) {
                next = next->rght;
            } else {
                next->rght = createNode(str);
            }
        }
        /* Same. Thus the string already exists in the tree */
        else {
            return root;
        }
    }
	return root;
}

/****************************************************************/

/* update the tree by rotating it at item specified, return the
   new root; if item is not there, return the original tree
 */

/* With the recusrive function, you call it again almost 
   immediately. The recusrion will go down the tree until it
   reaches what it is looking for, in this case the str.
   Then it will start going through the stack, doing the code
   written after the recursion call, namely the pointer
   manipulation required for the edge rotation.
 */

tree_t
*do_rotate(tree_t *root, char *str) {
    tree_t *check;
    char *oldhead;
    
    if(root){
        oldhead = root->str;
        
        /* If str is at the head of the tree, just return root */
        if(strcmp(str, root->str) == 0){
            return root;
        } else {
            /* If the old string at the head in oldhead is the
               same as one of the strings from the right/left
               nodes of the potential new head is the same, it
               means the edge rotate has been called a level down
               from the old head, and therefore is the new head.
               Therefore return check instead of root. */
            check = rotate_recursion(root, str);
            if(check->rght){
                if(strcmp(oldhead, check->rght->str) == 0){
                    return check;
                }
            } 
            if(check->left){
                if(strcmp(oldhead, check->left->str) == 0){
                    return check;
                }
            } else {
                return root;
            }
        }
    }
    return root;
}


/* This code essentially keeps track of 4 levels in the tree.
   If the str to be rotated around is on the first level down,
   then this code never recurses and it manipulates the head,
   the first and second level. Otherwise, by the recursive call
   it does the manipulation required for the rotate with 3 levels
   as well as making the old parent point to the new head of
   the relevant section in the tree.
 */

tree_t
*rotate_recursion(tree_t *root, char *str) {
    tree_t *temp;

    if(root->rght){
        if(strcmp(str, root->rght->str)==0){
            /* One deep */
            temp = root->rght;
            root->rght = root->rght->left;
            temp->left = root;
            return temp;
        } else {
            /* Two or more deep */
            root->rght = rotate_recursion(root->rght, str);
        }
    }
    
    if(root->left){
        if(strcmp(str, root->left->str)==0){
            temp = root->left;
            root->left = root->left->rght;
            temp->rght = root;
            return temp;
        } else {
            root->left = rotate_recursion(root->left, str);
        }
    }
    
    return root;
}

/****************************************************************/


/* print the final size of the tree, and average node depth
 */

void
do_tabulate(tree_t *root) {
    int numwords = 0, maxdepth = 0, total = 0, count = 0;
    
    if(root){
        tablulate_recursion(root, &numwords, &count,
                            &maxdepth, &total);
        numwords++;
    }
    
    printf("size     : %5d\n", numwords);
    
    /* Because when tabulate is called on an empty tree it 
       should only print size as per the spec under stage 4 */
    if(root){
        printf("avg depth: %5.2f\n", total/(double)numwords);
        printf("max depth: %5d\n", maxdepth);
    }
}


/* Firstly recurses down the right hand side of the tree before
   doing any arithmetic on the total or maxdepth. This is similar
   to the print function; it moves through the tree reverse
   alphabetically. It then recurses down the left side. 
 */

void
tablulate_recursion(tree_t *root, int *numwords, int *count,
                    int *maxdepth, int *total) {
    if(root->rght){
        *numwords += 1;
        *count += 1;
        tablulate_recursion(root->rght, numwords, count,
                            maxdepth, total);
        *count -= 1;
    }

    *total = *total + *count + 1;
    if(*count + 1 > *maxdepth){
        *maxdepth = *count + 1;
    }

    if(root->left){
        *numwords += 1;
        *count += 1;
        tablulate_recursion(root->left, numwords, count,
                            maxdepth, total);
        *count -= 1;
    }
}


/****************************************************************/

/* free all of the space, and make empty tree again 
 */
 
void
do_freeit(tree_t *root) {
    if(root){
        free_recursion(root);
        free(root->str);
        root = NULL;
        free(root);
    }
}


/* Starts at the top of the tree and recurses down until it
   finds a leaf with null left and right pointers. The str
   and node itself are freed from the node one level up.
   That pointer is then changed to NULL. The stack is then
   freed like this all the way back to the head, which is
   freed and set to NULL separately in do_freeit.
 */

void
free_recursion(tree_t *root) {
    if(root->rght){
        free_recursion(root->rght);
        free(root->rght->str);
        free(root->rght);
        root->rght = NULL;
    }
    if(root->left){
        free_recursion(root->left);
        free(root->left->str);
        free(root->left);
        root->left = NULL;
    }
}

/****************************************************************/

/* Creates a new node for the tree, then returns a pointer 
   to this new node so it can be linked to.
   Asserts that the desired memory space was indeed malloc'd.
 */

tree_t 
*createNode(char *inpstr) {
    tree_t *p = malloc(sizeof(tree_t));
    assert(p);
    p->str = malloc(LINELEN+1);
    assert(p->str);
    strncpy(p->str, inpstr, LINELEN+1);
    p->left = NULL;
    p->rght = NULL;
    return p;
}