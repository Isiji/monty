#include "monty.h"
/**
 * f_pint - prints the top
 * @head: stack head
 * @counter: line_number
 * Return: no return
*/
void f_pint(stack_t **head, unsigned int counter)
{
	if (*head == NULL)
	{
		fprintf(stderr, "L%u: can't pint, stack empty\n", counter);
		fclose(bus.file);
		free(bus.content);
		free_stack(*head);
		exit(EXIT_FAILURE);
	}
	printf("%d\n", (*head)->n);
}

#include "monty.h"

/**
 * f_pop - Removes the top element of the stack
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_pop(stack_t **head, unsigned int line_number)
{
	stack_t *temp;

    if (!head || !*head)
    {
        fprintf(stderr, "L%u: can't pop an empty stack\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

    temp = *head;
    *head = temp->next;

    if (*head)
        (*head)->prev = NULL;

    free(temp);
}

#include "monty.h"

/**
 * f_swap - Swaps the top two elements of the stack
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_swap(stack_t **head, unsigned int line_number)
{
	stack_t *first, *second;

    if (!head || !*head || !(*head)->next)
    {
        fprintf(stderr, "L%u: can't swap, stack too short\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

	first = *head;
	second = first->next;

    first->prev = second;
    first->next = second->next;

    second->prev = NULL;
    second->next = first;

    if (first->next)
        first->next->prev = first;

    *head = second;
}

