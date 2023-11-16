#include "monty.h"
/**
 * f_push - add node to the stack
 * @head: stack head
 * @len: line_number
 * Return: no return
*/
void f_push(stack_t **head, unsigned int len)
{
	int n, j = 0, flag = 0;

	if (bus.arg)
	{
		if (bus.arg[0] == '-')
			j++;
		for (; bus.arg[j] != '\0'; j++)
		{
			if (bus.arg[j] > 57 || bus.arg[j] < 48)
				flag = 1; }
		if (flag == 1)
		{ fprintf(stderr, "L%d: usage: push integer\n", len);
			fclose(bus.file);
			free(bus.input);
			free_stack(*head);
			exit(EXIT_FAILURE); }}
	else
	{ fprintf(stderr, "L%d: usage: push integer\n", len);
		fclose(bus.file);
		free(bus.input);
		free_stack(*head);
		exit(EXIT_FAILURE); }
	n = atoi(bus.arg);
	if (bus.lifi == 0)
		addnode(head, n);
	else
		addqueue(head, n);
}

/**
 * f_pall - Prints all the values on the stack
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_pall(stack_t **head, unsigned int line_number)
{
    stack_t *current = *head;

    while (current)
    {
        printf("%d\n", current->n);
        current = current->next;
    }
    (void)line_number;
}
