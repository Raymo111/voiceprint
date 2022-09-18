#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include "py_identify_bridge.h"

const int ERROR = 2;

int identify()
{
	bool result;
	Py_Initialize();
	PyObject *sysPath = PySys_GetObject("path");
	assert(sysPath != NULL);
    PyObject *path = PyUnicode_DecodeFSDefault("/home/raymo/Git/voiceprint-htn/src/voice_auth");
	assert(path != NULL);
	PyList_Insert(sysPath, 0, path);

	PyObject *p_name, *p_module, *p_result;

	p_name = PyUnicode_FromString("voice_auth");
	if (p_name == NULL)
	{
		printf("Error: cannot find file 'voice_auth.py'");
		return ERROR;
	}

	p_module = PyImport_Import(p_name);
	Py_DECREF(p_name);

	if (p_module == NULL)
	{
		printf("Error importing module 'voice_auth'!");
		return ERROR;
	}
	p_result = PyObject_CallMethod(p_module, "authenticate", NULL);
	Py_DECREF(p_module);
	if (p_result == NULL)
	{
		printf("Error calling method 'authenticate'!");
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
