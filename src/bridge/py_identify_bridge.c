#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>

const int ERROR = 2;

int do_identify()
{
	bool result;
	Py_Initialize();

	PyObject *p_name, *p_module, *p_result;

	p_name = PyUnicode_DecodeFSDefault("../auth/voice_auth.py");
	if (p_name == NULL)
	{
		printf("Error: cannot find file 'voice_auth.py'");
		return ERROR;
	}
	printf("File found: %s", p_name);

	p_module = PyImport_Import(p_name);
	Py_DECREF(p_name);

	if (p_module == NULL)
	{
		printf("Error: cannot import module 'authenticate'!");
		return ERROR;
	}
	p_result = PyObject_CallMethod(p_module, "authenticate", NULL);
	Py_DECREF(p_module);
	if (p_result == NULL)
	{
		printf("Error: cannot call method 'authenticate'!");
		return ERROR;
	}
	if (PyBool_Check(p_result))
	{
		if (p_result == Py_True)
		{
			printf("True");
			result = true;
		}
		else
		{
			printf("False");
			result = false;
		}
	}
	else
	{
		printf("Error: return value is not a boolean!");
		Py_DECREF(p_result);
		return ERROR;
	}
	Py_DECREF(p_result);
	return result;
}

int main(int argc, char const *argv[])
{
	do_identify();
	return 0;
}
