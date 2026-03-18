import logging 
import logging.config




LOGGING_CONFIG ={
    "version":1,
    "disable_existing_loggers": False,

    "formatters":{
        "json":{
            "()":"pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt":"%(asctime)s %(levelname)s %(name)s %(message)s"

        }
    },

    "handlers": {
        "default":{
            "class":"logging.StreamHandler",
            "formatter":"json",
            "stream":"ext://sys.stdout",
        }
    },

    "loggers":{
        "app":{
            "handlers":["default"],
            "level":"INFO",
            "propagate":False,
        },

        "uvicorn.error":{
            "handlers":["default"],
            "level":"INFO",
            "propagate":False
        },
        "uvicorn.access":{
            "handlers":["default"],
            "level":"INFO",
            "propagate":False
        }
    },

    "root":{
        "handlers":["default"],
        "level":"INFO"
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name:str):
    return logging.getLogger(name)
