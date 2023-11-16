#include "monty.h"

/**
 * f_add - Adds the top two elements of the stack
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_add(stack_t **head, unsigned int line_number)
{
    if (!head || !*head || !(*head)->next)
    {
        fprintf(stderr, "L%u: can't add, stack too short\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

    (*head)->next->n += (*head)->n;
    f_pop(head, line_number);
}

#include "monty.h"

/**
 * f_nop - No-operation, does nothing
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_nop(stack_t **head, unsigned int line_number)
{
    (void)head;
    (void)line_number;
}

#include "monty.h"

/**
 * f_sub - Subtracts the top element of the stack from the second top element
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_sub(stack_t **head, unsigned int line_number)
{
    if (!head || !*head || !(*head)->next)
    {
        fprintf(stderr, "L%u: can't sub, stack too short\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

    (*head)->next->n -= (*head)->n;
    f_pop(head, line_number);
}

