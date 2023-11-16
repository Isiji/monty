#include "monty.h"
#include <stdio.h>

int main(int argc, char *argv[])
{
	char *content;
	FILE *file;
	size_t size = 0;
	ssize_t input_line = 1;
	stack_t *stack = NULL;
	unsigned int len = 0;

	if (argc != 2)
	{
		fprintf(stderr, "USAGE: monty file");
		exit(EXIT_FAILURE);
	}
	file = fopen(argv[1], "r");
	bus.file = file;

	if (!file)
	{
		fprintf(stderr, "Error: Can't open file %s\n", argv[1]);
		exit(EXIT_FAILURE);
	}
	while (input_line > 0)
	{
		content = NULL;
		input_line = getline(&content, &size, file);
		bus.content = content;
		len++;

		if (input_line > 0)
		{
			execute(content, &stack, len, file);
		}
		free(content);
	
	}
	free_stack(stack);
	fclose(file);
	return (0);
}
