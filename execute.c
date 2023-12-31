#include "monty.h"
/**
* execute - executes the opcode
* @stack: head linked list - stack
* @len: line_counter
* @file: poiner to monty file
* @input: line content
* Return: no return
*/
int execute(char *input, stack_t **stack, unsigned int len, FILE *file)
{
	instruction_t opst[] = {
				{"push", f_push}, {"pall", f_pall}, {"pint", f_pint},
				{"pop", f_pop},
				{"swap", f_swap},
				{"add", f_add},
				{"nop", f_nop},
				{"sub", f_sub},
				{"queue", f_queue},
				{"div", f_div},
				{"mul", f_mul},
				{"mod", f_mod},
				{NULL, NULL}
				};
	unsigned int i = 0;
	char *op;

	op = strtok(input, " \n\t");
	if (op && op[0] == '#')
		return (0);
	bus.arg = strtok(NULL, " \n\t");
	while (opst[i].opcode && op)
	{
		if (strcmp(op, opst[i].opcode) == 0)
		{	opst[i].f(stack, len);
			return (0);
		}
		i++;
	}
	if (op && opst[i].opcode == NULL)
	{
		fprintf(stderr, "L%d: unknown instruction %s\n", len, op);

		fclose(file);
		free(input);
		free_stack(*stack);
		exit(EXIT_FAILURE);
	}

	return (1);
}
