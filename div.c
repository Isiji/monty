#include "monty.h"

/**
 * f_div - Divides the top two elements of the stack
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_div(stack_t **head, unsigned int line_number)
{
    if (!head || !*head || !(*head)->next)
    {
        fprintf(stderr, "L%u: can't div, stack too short\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

    (*head)->next->n /= (*head)->n;
    f_pop(head, line_number);
}

#include "monty.h"

/**
 * f_mul - Multiplies the top two elements of the stack
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_mul(stack_t **head, unsigned int line_number)
{
    if (!head || !*head || !(*head)->next)
    {
        fprintf(stderr, "L%u: can't mul, stack too short\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

    (*head)->next->n *= (*head)->n;
    f_pop(head, line_number);
}

#include "monty.h"

/**
 * f_mod - Divides the top two elements of the stack and finds the remainder
 * @head: Pointer to the stack
 * @line_number: Line number for error messages
 */
void f_mod(stack_t **head, unsigned int line_number)
{
    if (!head || !*head || !(*head)->next)
    {
        fprintf(stderr, "L%u: can't mod, stack too short\n", line_number);
        free_stack(*head);
        exit(EXIT_FAILURE);
    }

    (*head)->next->n %= (*head)->n;
    f_pop(head, line_number);
}

