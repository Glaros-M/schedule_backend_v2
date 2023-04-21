# DEBUG = 10
# INFO = 20

# 5003 PROD
# 9000 PREPROD

Prod = 1
PreProd = 2
Test = 3

VERSION = 1.04

SYSTEM_TYPE = PreProd

if SYSTEM_TYPE == Test:
    LOG_LVL = 10
    PORT = 9000
    CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@0.0.0.0:0000/Schedule_test"

elif SYSTEM_TYPE == PreProd:
    LOG_LVL = 10
    PORT = 9000
    CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@0.0.0.0:0000/Schedule_preproduction"

elif SYSTEM_TYPE == Prod:
    LOG_LVL = 20
    PORT = 5003
    CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@0.0.0.0:0000/Schedule_production"


if __name__ == "__main__":
    pass