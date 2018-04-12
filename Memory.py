LOCAL_CONSTANT_START = 1000
LOCAL_CONSTANT_INT_START = 1000
LOCAL_CONSTANT_FLOAT_START = 4000
LOCAL_CONSTANT_BOOLEAN_START = 9000
LOCAL_TEMP_START = 10000
LOCAL_TEMP_INT_START = 10000
LOCAL_TEMP_FLOAT_START = 20000
LOCAL_TEMP_BOOLEAN_START = 30000

LOCAL_MEMORY = {
    "CONSTANTS" : {
        "INT_MEM" : {

        },
        "FLOAT_MEM" : {

        },
        "BOOLEAN_MEM" : {

        }
    },
    "TEMP" : {
        "INT_MEM" : {

        },
        "FLOAT_MEM" : {

        },
        "BOOLEAN_MEM" : {

        }
    }
}

def ADD_NEW_VAR(mem_type,data_type):
    return