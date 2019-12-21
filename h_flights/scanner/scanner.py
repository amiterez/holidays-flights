from h_flights import common
from h_flights.database import connection

CONFIGURATIONS_NAMESPACE = "configurations"

class FlightsScanner():
    config = None
    db_connection = None
    is_initialized = False

    def __init__(self):

        self.init()


    def init(self):
        if self.is_initialized:
            return

        db_connection = connection.DBConnection()

        # make a connection with mongodb remote database
        if not db_connection.connect_to_db(common.DB_STRING_CONNECTION):
            print("can't connect to database")
            return

        config = db_connection.get_single_document(common.HOLIDAYS_FLIGHTS_DB_NAME, CONFIGURATIONS_NAMESPACE)

        self.is_initialized = True

    def run(self):
        if not self.is_initialized:
            return




if __name__ == "__main__":
    flight_scanner = FlightsScanner()
    flight_scanner.run()
