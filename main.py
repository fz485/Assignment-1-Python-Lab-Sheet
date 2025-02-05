# Import sqlite3 package
import sqlite3


# Define DBOperation class to manage all data into the database.
# Give a name of your choice to the database


# Creates the Destination table to store airport details.
class DBOperations:
  sql_create_destination =  '''
    CREATE TABLE IF NOT EXISTS Destination (
        AirportCode VARCHAR(20) NOT NULL,
        DestinationName VARCHAR(30) NOT NULL,
        Country VARCHAR(30),
        PRIMARY KEY (AirportCode)
    );
    '''
  # Creates the Flights table to store flight details.
  sql_create_flights = '''
    CREATE TABLE IF NOT EXISTS Flights (
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
        FlightNumber VARCHAR(30) NOT NULL,
        Status VARCHAR(15),
        OriginAirport VARCHAR(20) REFERENCES Destination(AirportCode),
        DestinationAirport VARCHAR(20) REFERENCES Destination(AirportCode)
    );
    '''
  # Creates the Pilot table to store pilot information.
  sql_create_pilot = '''
    CREATE TABLE IF NOT EXISTS Pilot (
    PilotID INTEGER PRIMARY KEY AUTOINCREMENT, 
    PilotName VARCHAR (30) NOT NULL, 
    LicenseNumber VARCHAR(30) NOT NULL, 
    ExperienceYears SMALLINT UNSIGNED NOT NULL); 
    '''
  # Creates the FlightPilot table to establish a many-to-many relationship between pilots and flights.
  sql_create_pilotFlight = '''
    CREATE TABLE IF NOT EXISTS FlightPilot (
    FlightPilotID INTEGER PRIMARY KEY AUTOINCREMENT, 
    FlightID INTEGER REFERENCES Flights(FlightID) ON DELETE CASCADE, 
    PilotID INTEGER REFERENCES Pilot(PilotID) ON DELETE CASCADE);
    '''
  # --------------- Data Insertion Queries --------------- #

  # Inserts a new flight record.
  sql_insert = "INSERT INTO Flights (FlightNumber, Status, OriginAirport, DestinationAirport) values (?,?,?,?);"
  # Inserts a new destination (airport).
  sql_insert_des = "INSERT INTO Destination (AirportCode, DestinationName, Country) values (?,?,?); "
  # Inserts a new pilot record.
  sql_insert_pilot = "INSERT INTO Pilot (PilotName, LicenseNumber, ExperienceYears) values (?,?,?); "
  # Inserts a new flight-pilot assignment.
  sql_insert_pilotflight = "INSERT INTO FlightPilot (FlightID, PilotID) values (?,?); "
  # Assigns a pilot to a flight using FlightNumber and LicenseNumber instead of IDs.
  sql_add_pilot_flights = "INSERT INTO FlightPilot (FlightID,PilotID) SELECT FlightID,PilotID FROM Flights CROSS JOIN Pilot WHERE LicenseNumber=? AND FlightNumber=?"
  # --------------- Search Queries --------------- #

  # Retrieves flight details by flight number.
  sql_search_flight_number = "SELECT * FROM Flights WHERE FlightNumber = ?"
  # Retrieves all flights with a specific status.
  sql_search_flight_status = "SELECT * FROM Flights WHERE Status = ?"
  # Retrieves flights departing from a specific airport.
  sql_search_origin_airport = "SELECT * FROM Flights WHERE OriginAirport = ?"
  # Retrieves flights arriving at a specific airport.
  sql_search_destination_airport = "SELECT * FROM Flights WHERE DestinationAirport = ?"
  # Retrieves all flights.
  sql_search_flight_all = "SELECT * FROM Flights"
  # Dynamic query for searching pilots based on a specific field.
  sql_search_pilot = "select * from Pilot where @=?"
  # Searches for pilots whose names contain a given substring.
  sql_search_pilot_name = "select * from Pilot where PilotName like %?%"
  # Retrieves pilots with experience greater than or equal to a specified number.
  sql_search_pilot_years_more = "select * from Pilot where ExperienceYears>=?"
  # Retrieves pilots with experience less than a specified number.
  sql_search_pilot_years_less = "select * from Pilot where ExperienceYears<?"
  # Retrieves all pilots.
  sql_search_pilot_all="SELECT * FROM Pilot"
  # Retrieves destinations based on a dynamic field.
  sql_search_destination = "select * from Destination where @=?"
  # Retrieves all destinations.
  sql_search_destination_all="SELECT * FROM Destination"
  # Retrieves all flights assigned to a specific pilot using their LicenseNumber.
  sql_search_pilot_flights = "SELECT FlightNumber,Status,OriginAirport,DestinationAirport FROM Pilot LEFT JOIN FlightPilot ON Pilot.PilotID=FlightPilot.PilotID LEFT JOIN Flights ON Flights.FlightID=FlightPilot.FlightID Where LicenseNumber=?"
  # Retrieves all pilots assigned to flights along with flight details.
  sql_view_pilot_flight_all = """
    SELECT 
        FlightPilot.FlightPilotID, 
        Pilot.PilotID, Pilot.PilotName, Pilot.LicenseNumber, Pilot.ExperienceYears, 
        Flights.FlightID, Flights.FlightNumber, Flights.Status, Flights.OriginAirport, Flights.DestinationAirport
    FROM FlightPilot
    JOIN Pilot ON FlightPilot.PilotID = Pilot.PilotID
    JOIN Flights ON FlightPilot.FlightID = Flights.FlightID;
    """
  # --------------- Update Queries --------------- #

  # Updates a destination's name and country using its AirportCode.
  sql_update_destination = "UPDATE Destination SET DestinationName=?, Country=? WHERE AirportCode=?"
  # Updates a flight's status and airport details using its FlightNumber.
  sql_update_flight = "UPDATE Flights SET Status=?, OriginAirport=?, DestinationAirport=? WHERE FlightNumber=?"
  # Updates a pilot's name and experience using their LicenseNumber.
  sql_update_pilot="UPDATE Pilot SET PilotName=?, ExperienceYears=? WHERE LicenseNumber=?"
  # --------------- Delete Queries --------------- #

  # Deletes a destination by AirportCode.
  sql_delete_destination="DELETE FROM Destination WHERE AirportCode = ?"
  # Deletes a flight by FlightNumber.
  sql_delete_flight = "DELETE FROM Flights WHERE FlightNumber = ?"
  # Deletes a pilot by LicenseNumber.
  sql_delete_pilot = "DELETE FROM Pilot WHERE LicenseNumber = ?"
  # Removes a pilot from a flight by PilotID and FlightID.
  sql_delete_flightpilot = "DELETE FROM FlightPilot WHERE PilotID = ? AND FlightID = ?"
  # --------------- Data Integrity & Validation Queries --------------- #

  # Retrieves the PilotID using LicenseNumber (case-insensitive check).
  sql_get_pilot_id = "SELECT PilotID FROM Pilot WHERE LicenseNumber = ?"
  # Retrieves the FlightID using FlightNumber.
  sql_get_flight_id = "SELECT FlightID FROM Flights WHERE FlightNumber = ?"
  # Retrieves the FlightID using a case-insensitive search.
  sql_get_flight_id_2 = "SELECT FlightID FROM Flights WHERE UPPER(FlightNumber) = UPPER(?)"
  # Checks if an airport code exists (case-insensitive).
  sql_check_airport = "SELECT AirportCode FROM Destination WHERE UPPER(AirportCode) = UPPER(?)"
  # Checks if a flight exists.
  sql_check_flight = "SELECT FlightID FROM Flights WHERE FlightNumber = ?"
  # Checks if an origin airport exists (case-insensitive).
  sql_check_origin = "SELECT AirportCode FROM Destination WHERE UPPER(AirportCode) = UPPER(?)"

  # Checks if a destination airport exists (case-insensitive).
  sql_check_destination = "SELECT AirportCode FROM Destination WHERE UPPER(AirportCode) = UPPER(?)"

  # Checks if a pilot exists based on LicenseNumber (case-insensitive).
  sql_check_license = "SELECT PilotID FROM Pilot WHERE UPPER(LicenseNumber) = UPPER(?)"
  # Checks if a pilot is already assigned to a flight.
  sql_check_existing = "SELECT FlightPilotID FROM FlightPilot WHERE PilotID = ? AND FlightID = ?"

  def get_connection(self):
    """Establish a connection to the SQLite database and create a cursor for executing queries."""
    self.conn = sqlite3.connect("AirlineManagement.db")# Connect to the database
    self.cur = self.conn.cursor()# Create a cursor for executing SQL statements

  def create_table(self):
    """Create necessary tables in the database if they do not exist."""
    try:
      self.get_connection() # Establish database connection
      self.cur.execute(self.sql_create_destination)# Create Destination table
      self.cur.execute(self.sql_create_flights)# Create Flights table
      self.cur.execute(self.sql_create_pilot)# Create Pilot table
      self.cur.execute(self.sql_create_pilotFlight)# Create FlightPilot table
      self.conn.commit()# Save changes
      print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_test_data(self):
    """Insert sample data into the database for testing."""
    try:
      self.get_connection()# Establish database connection
      # Insert sample destinations
      self.cur.execute(self.sql_insert_des, ("HRL", "London", "UK"))
      self.cur.execute(self.sql_insert_des, ("GTW", "London", "UK"))
      self.cur.execute(self.sql_insert_des, ("NYC", "NewYork", "US"))
      self.cur.execute(self.sql_insert_des, ("CAL", "California", "US"))
      self.cur.execute(self.sql_insert_des, ("PEK", "Beijing", "China"))
      self.cur.execute(self.sql_insert_des, ("PVG", "ShangHai", "China"))
      self.cur.execute(self.sql_insert_des, ("SHA", "ShangHai", "China"))
      self.cur.execute(self.sql_insert_des, ("CAN", "GuangZhou", "China"))
      self.cur.execute(self.sql_insert_des, ("PKX", "BeiJing", "China"))
      self.cur.execute(self.sql_insert_des, ("MAD", "Madrid", "Spain"))
      self.cur.execute(self.sql_insert_des, ("MLA", "Malta", "Malta"))
      self.cur.execute(self.sql_insert_des, ("DXB", "Dubai", "UAE"))
      self.cur.execute(self.sql_insert_des, ("DSS", "Dakar", "Senegal"))
      self.cur.execute(self.sql_insert_des, ("SAW", "Istanbul", "Turkey"))
      self.cur.execute(self.sql_insert_des, ("ATH", "Markopoulo", "Greece"))

      # Insert sample pilots
      self.cur.execute(self.sql_insert_pilot, ("John Smith", "LIC223", "12"))
      self.cur.execute(self.sql_insert_pilot, ("Harlan Flores", "LIC112", "2"))
      self.cur.execute(self.sql_insert_pilot, ("Emilia Freeman", "LIC512", "7"))
      self.cur.execute(self.sql_insert_pilot, ("Brian Serrano", "LIC821", "1"))
      self.cur.execute(self.sql_insert_pilot, ("Alex Feng", "LIC6677", "10"))
      self.cur.execute(self.sql_insert_pilot, ("Amelia Brown", "LIC7898", "3"))
      self.cur.execute(self.sql_insert_pilot, ("Om Johnson", "LIC123", "11"))
      self.cur.execute(self.sql_insert_pilot, ("Emma Johnson", "LIC456", "9"))
      self.cur.execute(self.sql_insert_pilot, ("Harrison Smith", "LIC789", "18"))
      self.cur.execute(self.sql_insert_pilot, ("Christina Brown", "LIC012", "20"))
      self.cur.execute(self.sql_insert_pilot, ("Emily Wilson", "LIC555", "8"))
      self.cur.execute(self.sql_insert_pilot, ("Andy Moore", "LIC765", "2"))
      # Insert sample flights
      self.cur.execute(self.sql_insert, ("BE123", "On Time", "PEK", "CAL"))
      self.cur.execute(self.sql_insert, ("CG556", "Landed", "HRL", "NYC"))
      self.cur.execute(self.sql_insert, ("LW212", "Boarding", "GTW", "NYC"))
      self.cur.execute(self.sql_insert, ("BA001", "Cancelled", "PEK", "SHA"))
      self.cur.execute(self.sql_insert, ("BA002", "Delayed", "HRL", "DSS"))
      self.cur.execute(self.sql_insert, ("BA003", "Boarding", "GTW", "MLA"))
      self.cur.execute(self.sql_insert, ("BA004", "On Time", "MLA", "PEK"))
      self.cur.execute(self.sql_insert, ("BA005", "Delayed", "PVG", "HRL"))
      self.cur.execute(self.sql_insert, ("CG001", "Boarding", "MAD", "NYC"))
      self.cur.execute(self.sql_insert, ("BE002", "On Time", "DXB", "DSS"))
      self.cur.execute(self.sql_insert, ("CG003", "Landed", "SAW", "ATH"))
      self.cur.execute(self.sql_insert, ("LW004", "Boarding", "DXB", "GTW"))
      # Assign pilots to flights
      self.cur.execute(self.sql_insert_pilotflight, ("1", "1"))
      self.cur.execute(self.sql_insert_pilotflight, ("1", "2"))
      self.cur.execute(self.sql_insert_pilotflight, ("2", "3"))
      self.cur.execute(self.sql_insert_pilotflight, ("2", "4"))
      self.cur.execute(self.sql_insert_pilotflight, ("3", "3"))
      self.cur.execute(self.sql_insert_pilotflight, ("3", "1"))
      self.cur.execute(self.sql_insert_pilotflight, ("5", "5"))
      self.cur.execute(self.sql_insert_pilotflight, ("5", "6"))
      self.cur.execute(self.sql_insert_pilotflight, ("6", "7"))
      self.cur.execute(self.sql_insert_pilotflight, ("6", "8"))
      self.cur.execute(self.sql_insert_pilotflight, ("6", "9"))
      self.cur.execute(self.sql_insert_pilotflight, ("7", "10"))
      self.conn.commit()# Commit all changes
    except Exception as e:
      print("Error inserting test data:", e)# Print error if insertion fails
    finally:
      self.conn.close()# Close the database connection

  def insert_Destination(self):
    """Insert a new destination into the database, ensuring a unique Airport Code."""
    try:
      self.get_connection()# Establish database connection

      des = DestinationInfo()
      # Validate unique Airport Code
      while True:
        airport_code = input("Please Enter Airport Code: ").strip().upper()

        # Check if Airport Code already exists (case-insensitive)

        self.cur.execute(self.sql_check_airport, (airport_code,))
        existing_airport = self.cur.fetchone()

        if existing_airport:
          print("Airport Code already exists! Please enter a different Airport Code.")
        else:
          des.set_airport_code(airport_code)
          break  # Exit loop if Airport Code is unique
      # Get additional destination details
      des.set_destination_name(input("Please Enter Destination Name:"))
      des.set_country(input("Please Enter Country of Destination: "))
      # Insert data into database
      insertvals = tuple(str(des).split("\n"))
      self.cur.execute(self.sql_insert_des, insertvals)

      self.conn.commit()# Save changes
      print("Inserted destination data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    """Insert a new flight into the database, ensuring unique Flight Number and valid data."""
    try:
      self.get_connection()# Establish database connection

      flight = FlightInfo()
      # Validate unique Flight Number
      while True:
        flight_number = input("Please Enter Flight Number: ").strip()

        # Check if Flight Number already exists in the database

        self.cur.execute(self.sql_check_flight, (flight_number,))
        existing_flight = self.cur.fetchone()

        if existing_flight:
          print("Flight Number already exists! Please enter a different Flight Number.")
        else:
          flight.set_flight_flightnumber(flight_number)
          break  # Exit loop if Flight Number is unique

      # Validate Flight Status
      valid_statuses = {
        "On Time", "Delayed", "Cancelled", "Boarding",
        "in-Flight", "Landed", "No Show", "Closed"
      }

      #Ask user for valid status
      while True:
        status_input = input(
          "Please Enter Flight Status (On Time, Delayed, Cancelled, Boarding, in-Flight, Landed, No Show, Closed): "
        ).strip()

        if status_input in valid_statuses:
          flight.set_status(status_input)
          break  # Exit loop if valid status is entered
        else:
          print("Invalid status! Please choose from the allowed options.")

      # Validate Origin Airport
      while True:
        origin_airport = input("Please Enter Origin Airport Code: ").strip().upper()


        self.cur.execute(self.sql_check_origin, (origin_airport,))
        existing_origin = self.cur.fetchone()

        if existing_origin:
          flight.set_flight_origin(origin_airport)
          break  # Exit loop if airport exists
        else:
          print("Origin Airport Code not found! Please enter a valid Airport Code.")

      # Validate Destination Airport
      while True:
        destination_airport = input("Please Enter Destination Airport Code: ").strip().upper()


        self.cur.execute(self.sql_check_destination, (destination_airport,))
        existing_destination = self.cur.fetchone()

        if existing_destination:
          flight.set_flight_destination(destination_airport)
          break  # Exit loop if airport exists
        else:
          print("Destination Airport Code not found! Please enter a valid Airport Code.")
      # Insert flight data into the database
      insertvals = tuple(str(flight).split("\n"))
      self.cur.execute(self.sql_insert, insertvals)

      self.conn.commit() #data save
      print("Inserted flight data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_Pilot(self):
    """Insert a new pilot into the database, ensuring a unique License Number."""
    try:
      self.get_connection()# Establish database connection

      pilot = PilotInfo()
      pilot.set_pilot_name(input("Please Enter Pilot's Name: "))
      # Validate unique License Number
      while True:
        license_number = input("Please Enter License Number: ").strip().upper()  # Normalize case sensitivity

        # Check if License Number already exists (case-insensitive)

        self.cur.execute(self.sql_check_license, (license_number,))
        existing_license = self.cur.fetchone()

        if existing_license:
          print("License Number already exists! Please enter a different License Number.")
        else:
          pilot.set_license_number(license_number)
          break  # Exit loop if License Number is unique
      # Validate Years of Experience (numeric input only)
      while True:
        experience_years = input("Please Enter Years of Experience: ").strip()
        if experience_years.isdigit():
          pilot.set_experience_year(str(experience_years))
          break
        else:
          print("Invalid input! Please enter a valid number for experience years.")
      # Insert pilot data into the database
      insertvals = tuple(str(pilot).split("\n"))
      self.cur.execute(self.sql_insert_pilot, insertvals)

      self.conn.commit()# Save changes
      print("Inserted pilot data successfully")
    except Exception as e:
      print(e)# Print error if insertion fails
    finally:
      self.conn.close()# Close database connection

  def insert_Pilot_flight(self):
    """Assign a pilot to a flight, ensuring valid and unique assignment."""
    try:
      self.get_connection()
      # Validate Pilot License Number
      while True:
        license_number = input("Please Enter Pilot License Number: ").strip().upper()


        self.cur.execute(self.sql_get_pilot_id, (license_number,))
        pilot_result = self.cur.fetchone()

        if pilot_result:
          pilot_id = pilot_result[0]
          break  # Exit loop if a valid PilotID is found
        else:
          print("No pilot found with this License Number. Please enter a valid one.")
      # Validate Flight Number
      while True:
        flight_number = input("Please Enter Flight Number: ").strip().upper()


        self.cur.execute(self.sql_get_flight_id_2, (flight_number,))
        flight_result = self.cur.fetchone()

        if flight_result:
          flight_id = flight_result[0]
          break  # Exit loop if a valid FlightID is found
        else:
          print("No flight found with this Flight Number. Please enter a valid one.")

        #Check if this PilotID and FlightID combination already exists

      self.cur.execute(self.sql_check_existing, (pilot_id, flight_id))
      existing_entry = self.cur.fetchone()

      if existing_entry:
        print("This pilot is already assigned to this flight. Please choose another flight or pilot.")
        return  # Exit function without inserting duplicate data
      # Assign pilot to flight
      self.cur.execute(self.sql_add_pilot_flights, (pilot_id, flight_id))
      self.conn.commit()# Save changes
      print("Pilot successfully assigned to flight!")

    except Exception as e:
      print(e)# Print error if assignment fails
    finally:
      self.conn.close()# Close database connection

  def view_flight_all(self):
    """Retrieve and display all flights from the database."""
    try:
      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_search_flight_all)# Execute query to get all flights

      result = self.cur.fetchall()# Fetch all records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Flight ID: " + str(detail))
              elif index == 1:
                print("Flight Number: " + detail)
              elif index == 2:
                print("Flight Status: " + detail)
              elif index == 3:
                print("Flight Origin: " + detail)
              elif index == 4:
                print("Flight Destination: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_flight_origin(self):
    """Retrieve and display flights based on the origin airport code."""
    try:
      self.get_connection()# Establish database connection
      flightOrigin = input("Please Enter Flight Origin Airport Code: ")

      interval=tuple(flightOrigin.split("\n"))# Convert input into a tuple
      self.cur.execute(self.sql_search_origin_airport, interval)# Execute query

      result = self.cur.fetchall() # Fetch all matching records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Flight ID: " + str(detail))
              elif index == 1:
                print("Flight Number: " + detail)
              elif index == 2:
                print("Flight Status: " + detail)
              elif index == 3:
                print("Flight Origin: " + detail)
              elif index == 4:
                print("Flight Destination: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_flight_destination(self):
    """Retrieve and display flights based on the destination airport code."""
    try:
      self.get_connection()# Establish database connection
      flightDestination = input("Please Enter Flight Destination Airport Code: ")

      interval=tuple(flightDestination.split("\n"))# Convert input into a tuple
      self.cur.execute(self.sql_search_destination_airport, interval)

      result = self.cur.fetchall()# Fetch all matching records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Flight ID: " + str(detail))
              elif index == 1:
                print("Flight Number: " + detail)
              elif index == 2:
                print("Flight Status: " + detail)
              elif index == 3:
                print("Flight Origin: " + detail)
              elif index == 4:
                print("Flight Destination: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_flight_status(self):
    """Retrieve and display flights based on their status."""
    try:
      self.get_connection()# Establish database connection
      flightStatus = input("Please Enter Flight Status: ")

      interval=tuple(flightStatus.split("\n"))# Convert input into a tuple
      self.cur.execute(self.sql_search_flight_status, interval)# Execute query

      result = self.cur.fetchall()# Fetch all matching records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Flight ID: " + str(detail))
              elif index == 1:
                print("Flight Number: " + detail)
              elif index == 2:
                print("Flight Status: " + detail)
              elif index == 3:
                print("Flight Origin: " + detail)
              elif index == 4:
                print("Flight Destination: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_flight_number(self):
    """Retrieve and display flight details based on flight number."""
    try:
      self.get_connection()# Establish database connection
      flightNumber = input("Please Enter Flight Number: ")

      interval=tuple(flightNumber.split("\n"))# Convert input into a tuple
      self.cur.execute(self.sql_search_flight_number, interval)# Execute query

      result = self.cur.fetchall()# Fetch matching records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Flight ID: " + str(detail))
              elif index == 1:
                print("Flight Number: " + detail)
              elif index == 2:
                print("Flight Status: " + detail)
              elif index == 3:
                print("Flight Origin: " + detail)
              elif index == 4:
                print("Flight Destination: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_pilot_all(self):
    """Retrieve and display all pilots from the database."""
    try:
      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_search_pilot_all)# Execute query to fetch all pilots

      result = self.cur.fetchall()# Fetch all records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Pilot Name: " + str(detail))
              elif index == 1:
                print("License Number: " + str(detail))
              elif index == 2:
                print("Experience Years: " + str(detail)+"\n")
          else:
            print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def search_pilot_years(self, op):
    """Retrieve and display pilots based on experience years using comparison operators."""
    try:
      self.get_connection()# Establish database connection
      searchId = int(input("Please Enter years: "))# Get experience years input
      searchParams = (searchId,)
      # Determine which query to use based on operator
      if op == ">":
        sqlExecute = self.sql_search_pilot_years_more
      else:
        sqlExecute = self.sql_search_pilot_years_less
      self.cur.execute(sqlExecute, searchParams)
      self.conn.commit()
      results = self.cur.fetchall()# Fetch matching records
      for result in results:
        if type(result) == type(tuple()):
          for index, detail in enumerate(result):
            if index == 0:
              print("");
            elif index == 1:
              print("Name: " + str(detail))
            elif index == 2:
              print("License: " + detail)
            else:
              print("Years Experience: " + str(detail)+"\n")
      if len(results) == 0: print("No Record")

    except Exception as e:
      print(e) # Print error if query fails
    finally:
      self.conn.close()

  def search_pilot(self, field):
    """Search and display pilot details based on a specified field."""
    try:
      self.get_connection()# Establish database connection
      searchId = input("Please Enter " + field + ": ")# Get user input
      searchParams = (searchId,)
      # Replace placeholder in SQL query with the actual field name
      sqlExecute = self.sql_search_pilot.replace("@", field)
      self.cur.execute(sqlExecute, searchParams)# Execute query
      self.conn.commit()
      results = self.cur.fetchall()# Fetch matching records
      for result in results:
        if type(result) == type(tuple()):
          for index, detail in enumerate(result):
            if index == 0:
              print("")
            elif index == 1:
              print("Name: " + str(detail))
            elif index == 2:
              print("License: " + detail)
            else:
              print("Years Experience: " + str(detail))
      if len(results) == 0: print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_pilot_flight_all(self):
    """Retrieve and display all pilot-flight assignments."""
    try:
      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_view_pilot_flight_all)# Execute query to fetch all records

      result = self.cur.fetchall()# Fetch matching records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("FlightPilot ID: " + str(detail))
              elif index == 1:
                print("Pilot ID: " + str(detail))
              elif index == 2:
                print("Pilot Name: " + detail)
              elif index == 3:
                print("License Number: " + detail)
              elif index == 4:
                print("Experience Years: " + str(detail))
              elif index == 5:
                print("Flight ID: " + str(detail))
              elif index == 6:
                print("Flight Number: " + detail)
              elif index == 7:
                print("Status: " + detail)
              elif index == 8:
                print("Origin Airport Code: " + str(detail))
              elif index == 9:
                print("Destination Airport Code: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def search_pilot_flight(self):
    """Retrieve and display flights assigned to a specific pilot based on license number."""
    try:
      self.get_connection() # Establish database connection
      flightID = input("Enter Pilot License: ")# Get and format user input
      searchParams = (flightID,)
      self.cur.execute(self.sql_search_pilot_flights, searchParams)# Execute query
      self.conn.commit()
      results = self.cur.fetchall()# Fetch matching records
      for result in results:
        if type(result) == type(tuple()):
          for index, detail in enumerate(result):
            if index == 0:
              print("Flight Number: " + str(detail))
            elif index == 1:
              print("Status: " + detail)
            elif index == 2:
              print("Flight Origin: " + detail)
            elif index == 3:
              print("Flight Destination: " + detail+"\n")
      if len(results) == 0: print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def search_destination(self, field):
    """Search and display destination details based on a specified field."""
    try:
      self.get_connection()# Establish database connection
      # Get user input with specific formatting for AirportCode
      if field=="AirportCode":
        searchId = input("Please Enter " + field + " in Capital Letter: ")
      else:
        searchId = input("Please Enter " + field + ": ")

      searchParams = (searchId,)
      sqlExecute = self.sql_search_destination.replace("@", field)# Replace placeholder with field name
      self.cur.execute(sqlExecute, searchParams)# Execute query
      self.conn.commit()
      results = self.cur.fetchall()# Fetch matching records
      for result in results:
        if type(result) == type(tuple()):
          for index, detail in enumerate(result):
            if index == 0:
              print("Airport Code: " +detail)
            elif index == 1:
              print("City of Destination: " + str(detail))
            elif index == 2:
              print("Country: " + detail+"\n")
      if len(results) == 0: print("No Record Found!")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def view_destination_all(self):
    """Retrieve and display all destinations from the database."""
    try:
      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_search_destination_all)# Execute query to fetch all destinations

      result = self.cur.fetchall()# Fetch all records
      if not result:
        print("No records found!")
      else:
        print("Records found:\n")
        for row in result:
          if type(row) == type(tuple()):
            for index, detail in enumerate(row):
              if index == 0:
                print("Airport Code: " + detail)
              elif index == 1:
                print("City of Destination: " + detail)
              elif index == 2:
                print("Country: " + detail+"\n")
              else:
                print("No Record")

    except Exception as e:
      print(e)# Print error if query fails
    finally:
      self.conn.close()# Close database connection

  def update_flight(self):
    """Update flight details, ensuring valid input and existing flight records."""
    try:
      flight = FlightInfo()
      self.get_connection() # Establish database connection
      # Validate Flight Number
      while True:
        flight_number = input("Please Enter Flight Number: ").strip()

        # Check if Flight Number already exists in the database

        self.cur.execute(self.sql_check_flight, (flight_number,))
        existing_flight = self.cur.fetchone()

        if existing_flight:
          flight.set_flight_flightnumber(flight_number)
          break  # Exit loop if Flight Number is unique
        else:
          print("Flight Number is not exists! Please enter a correct Flight Number.")
      # Validate Flight Status
      valid_statuses = {
        "On Time", "Delayed", "Cancelled", "Boarding",
        "in-Flight", "Landed", "No Show", "Closed"
      }

      #Ask user for valid status
      while True:
        status_input = input(
          "Please Enter Flight Status (On Time, Delayed, Cancelled, Boarding, in-Flight, Landed, No Show, Closed): "
        ).strip()

        if status_input in valid_statuses:
          flight.set_status(status_input)
          break  # Exit loop if valid status is entered
        else:
          print("Invalid status! Please choose from the allowed options.")
      # Validate Origin Airport
      while True:
        origin_airport = input("Please Enter Origin Airport Code: ").strip().upper()

        self.cur.execute(self.sql_check_origin, (origin_airport,))
        existing_origin = self.cur.fetchone()

        if existing_origin:
          flight.set_flight_origin(origin_airport)
          break  # Exit loop if airport exists
        else:
          print("Origin Airport Code not found! Please enter a valid Airport Code.")

      # Validate Destination Airport
      while True:
        destination_airport = input("Please Enter Destination Airport Code: ").strip().upper()

        self.cur.execute(self.sql_check_destination, (destination_airport,))
        existing_destination = self.cur.fetchone()

        if existing_destination:
          flight.set_flight_destination(destination_airport)
          break  # Exit loop if airport exists
        else:
          print("Destination Airport Code not found! Please enter a valid Airport Code.")
      # Update flight details in the database
      self.cur.execute(self.sql_update_flight,
                       (flight.status, flight.flightOrigin, flight.flightDestination, flight.flightNumber))
      self.conn.commit()# Save changes
      print("Updated successful!")

    except Exception as e:
      print(e)# Print error if update fails
    finally:
      self.conn.close()# Close database connection

  def update_pilot(self):
    """Update pilot details, ensuring valid input and existing license records."""
    try:
      pilot = PilotInfo()
      self.get_connection()# Establish database connection
      # Validate License Number
      while True:
        license_number = input("Please Enter License Number: ").strip().upper()  # Normalize case sensitivity
        # Check if License Number already exists (case-insensitive)
        self.cur.execute(self.sql_check_license, (license_number,))
        existing_license = self.cur.fetchone()

        if existing_license:
          pilot.set_license_number(license_number)
          break
        else:
          print("Can not find this License Number, Please input again!")
      # Get Pilot Name
      pilot.set_pilot_name(input("Please Enter Pilot's Name: "))
      # Validate Experience Years
      while True:
        experience_years = input("Please Enter Years of Experience: ").strip()
        if experience_years.isdigit():
          pilot.set_experience_year(str(experience_years))
          break
        else:
          print("Invalid input! Please enter a valid number for experience years.")

      # Update pilot details in the database
      self.cur.execute(self.sql_update_pilot,
                       (pilot.pilotName, pilot.experienceYears, pilot.licenseNumber))

      self.conn.commit()# Save changes
      print("Updated successful!")

    except Exception as e:
      print(e)# Print error if update fails
    finally:
      self.conn.close()# Close database connection

  def update_destination(self):
    """Update destination details, ensuring valid input and existing airport records."""
    try:
      des = DestinationInfo()
      self.get_connection() # Establish database connection
      # Validate Airport Code
      while True:
        airport_code = input("Please Enter Airport Code: ").strip().upper()

        # Check if Airport Code already exists (case-insensitive)

        self.cur.execute(self.sql_check_airport, (airport_code,))
        existing_airport = self.cur.fetchone()

        if existing_airport:
          des.set_airport_code(airport_code)
          break  # Exit loop if Airport Code is unique
        else:
          print("Airport Code is not exists! Please enter a different Airport Code.")
      # Get updated destination details
      des.set_destination_name(input("Please Enter Destination Name:"))
      des.set_country(input("Please Enter Country of Destination: "))

      # Update destination details in the database
      self.cur.execute(self.sql_update_destination,
                       (des.destinationName, des.country, des.airportCode))

      self.conn.commit()# Save changes
      print("Updated successful!")

    except Exception as e:
      print(e)# Print error if update fails
    finally:
      self.conn.close()# Close database connection

  # Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.
  def delete_destination(self):
    """Delete a destination from the database based on Airport Code."""
    try:
      des = DestinationInfo()
      des.set_airport_code(input("Please Enter the Airport Code Which You Want to Delete: "))

      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_delete_destination,(des.airportCode,))# Execute delete query

      self.conn.commit()# Save changes
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + " Row(s) deleted successful!")
      else:
        print("Cannot find this record in the database")


    except Exception as e:
      print(e)# Print error if deletion fails
    finally:
      self.conn.close()# Close database connection

  def delete_flight(self):
    """Delete a flight from the database based on Flight Number."""
    try:
      flight = FlightInfo()
      flight.set_flight_flightnumber(input("Please Enter the FlightNumber Which You Want to Delete: "))

      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_delete_flight,(flight.flightNumber,))# Execute delete query

      self.conn.commit()# Save changes
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + " Row(s) deleted successful!")
      else:
        print("Cannot find this record in the database")


    except Exception as e:
      print(e)# Print error if deletion fails
    finally:
      self.conn.close()# Close database connection

  def delete_pilot(self):
    """Delete a pilot from the database based on License Number."""
    try:
      pilot = PilotInfo()
      pilot.set_license_number(input("Please Enter the License Number of Pilot Which You Want to Delete: "))

      self.get_connection()# Establish database connection
      self.cur.execute(self.sql_delete_pilot,(pilot.licenseNumber,))

      self.conn.commit() # Save changes
      if self.cur.rowcount != 0:
        print(str(self.cur.rowcount) + " Row(s) deleted successful!")
      else:
        print("Cannot find this record in the database")
    except Exception as e:
      print(e)# Print error if deletion fails
    finally:
      self.conn.close() # Close database connection

  def delete_pilot_flight(self):
    """Remove a pilot from a specific flight in the FlightPilot table."""
    try:
      pilot = PilotInfo()
      pilot.set_license_number(input("Please Enter the License Number of Pilot Which You Want to Delete: "))
      flight = FlightInfo()
      flight.set_flight_flightnumber(input("Please Enter the FlightNumber Which You Want to Delete: "))


      self.get_connection()# Establish database connection
      # Retrieve Pilot ID using License Number
      self.cur.execute(self.sql_get_pilot_id,(pilot.licenseNumber,))
      pilot_result = self.cur.fetchone()

      if not pilot_result:
        print("No pilot found with this License Number.")
        return

      pilot_id=pilot_result[0]
      # Retrieve Flight ID using Flight Number
      self.cur.execute(self.sql_get_flight_id, (flight.flightNumber,))
      flight_result = self.cur.fetchone()

      if not flight_result:
          print("No flight found with this Flight Number.")
          return

      flight_id = flight_result[0]
      # Delete the pilot-flight assignment
      self.cur.execute(self.sql_delete_flightpilot,(pilot_id,flight_id))

      self.conn.commit()# Save changes
      if self.cur.rowcount >0:
        print(f"Deleted FlightPilot record for LicenseNumber: {pilot.licenseNumber} and FlightNumber: {flight.flightNumber}")
      else:
        print("Cannot find this record in the database")
    except Exception as e:
      print(e)# Print error if deletion fails
    finally:
      self.conn.close()# Close database connection


class DestinationInfo:
  """Class to store and manage destination details."""
  def __init__(self):
    """Initialize destination attributes."""
    self.airportCode = ''
    self.destinationName = ''
    self.country = ''

  # Setters
  def set_airport_code(self, airportCode):
    """Set the airport code."""
    self.airportCode = airportCode

  def set_destination_name(self, destinationName):
    """Set the destination name."""
    self.destinationName = destinationName

  def set_country(self, country):
    """Set the country name."""
    self.country = country

  # Getters
  def get_airport_code(self):
    """Get the airport code."""
    return self.airportCode

  def get_destination_name(self):
    """Get the destination name."""
    return self.destinationName

  def get_country(self):
    """Get the country name."""
    return self.country

  def __str__(self):
    """Return a string representation of the destination."""
    return self.airportCode + "\n" + self.destinationName + "\n" + self.country


class FlightInfo:
  """Represents flight details including number, status, origin, and destination."""
  def __init__(self):
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''
    self.flightNumber = ''

  # Setters
  def set_flight_flightnumber(self, flightNumber):
    """Set flight number."""
    self.flightNumber = flightNumber

  def set_flight_origin(self, flightOrigin):
    """Set flight origin."""
    self.flightOrigin = flightOrigin

  def set_flight_destination(self, flightDestination):
    """Set flight destination."""
    self.flightDestination = flightDestination

  def set_status(self, status):
    """Set flight status."""
    self.status = status

  # Getters
  def get_flight_id(self):
    """Get flight ID (not in use)."""
    return self.flightID

  def get_flight_origin(self):
    """Get flight origin."""
    return self.flightOrigin

  def get_flight_destination(self):
    """Get flight destination."""
    return self.flightDestination

  def get_status(self):
    """Get flight status."""
    return self.status

  def get_flightnumber(self):
    """Get flight number."""
    return self.flightNumber

  def __str__(self):
    """Return string representation of the flight."""
    return self.flightNumber + "\n" + self.status + "\n" + self.flightOrigin + "\n" + self.flightDestination


class PilotInfo:
  """Represents pilot details including name, license number, and experience."""
  def __init__(self):
    self.pilotName = ''
    self.licenseNumber = ''
    self.experienceYears = ''

  # Setters
  def set_pilot_name(self, pilotName):
    """Set pilot name."""
    self.pilotName = pilotName

  def set_license_number(self, licenseNumber):
    """Set pilot license number."""
    self.licenseNumber = licenseNumber

  def set_experience_year(self, experienceYears):
    """Set pilot experience years."""
    self.experienceYears = experienceYears

  # Getters
  def get_pilot_name(self):
    """Get pilot name."""
    return self.pilotName

  def get_license_number(self):
    """Get pilot license number."""
    return self.licenseNumber

  def get_experience_year(self):
    """Get pilot experience years."""
    return self.experienceYears

  def __str__(self):
    """Return string representation of the pilot."""
    return self.pilotName + "\n" + self.licenseNumber + "\n" + self.experienceYears


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
def menu():
  """Display the main menu options for managing flights, pilots, and destinations."""
  print("\n Menu:")
  print("**********")
  print(" 1. Add a New Flight")
  print(" 2. View Flights by Criteria")
  print(" 3. Update Flight Information")
  print(" 4. Delete a Flight")
  print(" 5. Add a New Pilots")
  print(" 6. View Pilots by Criteria")
  print(" 7. Update Pilot Information")
  print(" 8. Delete a Pilot")
  print(" 9. Assign Pilot to Flight")
  print(" 10. View Pilot Schedule")
  print(" 11. Delete a Pilot to Flight")
  print(" 12. Add a New Destination")
  print(" 13. View Destination by Criteria")
  print(" 14. Update Destination Information")
  print(" 15. Delete a Destination")
  print(" 16.Exit\n")

def viewdestinations():
  """Display options to view destinations based on different criteria."""
  print("\n View Destination by Criteria:")
  print("**********")
  print(" 1. Airport Code")
  print(" 2. City of Destination")
  print(" 3. Country")
  print(" 4. All Destination Info")
  print(" 5. Back\n")
  __choose_flights = int(input("Enter your choice: "))
  if __choose_flights == 1:
    db_ops.search_destination("AirportCode")# Search by Airport Code
  elif __choose_flights == 2:
    db_ops.search_destination("DestinationName")# Search by Destination Name
  elif __choose_flights == 3:
    db_ops.search_destination("Country")# Search by Country
  elif __choose_flights == 4:
    db_ops.view_destination_all()# View all destinations
  elif __choose_flights == 5:
    menu()# Return to main menu
  else:
    print("Invalid Choice")

def viewflights():
  """Display options to view flights based on different criteria."""
  print("\n View Flights by Criteria:")
  print("**********")
  print(" 1. Flight Number")
  print(" 2. Flight Status")
  print(" 3. Origin Airport")
  print(" 4. Destination Airport")
  print(" 5. All Flights Info")
  print(" 6. Back\n")
  __choose_flights = int(input("Enter your choice: "))
  if __choose_flights == 1:
    db_ops.view_flight_number()
  elif __choose_flights == 2:
    db_ops.view_flight_status()
  elif __choose_flights == 3:
    db_ops.view_flight_origin()
  elif __choose_flights == 4:
    db_ops.view_flight_destination()
  elif __choose_flights == 5:
    db_ops.view_flight_all()
  elif __choose_flights == 6:
    menu()# Return to the main menu
  else:
    print("Invalid Choice")

def viewpilots():
  """Display options to view pilots based on different criteria."""
  print("\n View Pilots by Criteria:")
  print("**********")
  print(" 1. Name")
  print(" 2. License Number")
  print(" 3. Years Experience More Than")
  print(" 4. Years Experience Less Than")
  print(" 5. All Pilots Info")
  print(" 6. Back\n")

  __choose = int(input("Enter your choice: "))
  if __choose == 1:
    db_ops.search_pilot("PilotName")
  elif __choose == 2:
    db_ops.search_pilot("LicenseNumber")
  elif __choose == 3:
    db_ops.search_pilot_years(">")
  elif __choose == 4:
   db_ops.search_pilot_years("<>")
  elif __choose == 5:
    db_ops.view_pilot_all()
  elif __choose == 6:
    menu()# Return to the main menu
  else:
    print("Invalid Choice")

def viewpilotflight():
  """Display options to view pilot schedules."""
  print("\n View Pilots Schedule:")
  print("**********")
  print(" 1. View One Pilot Schedule")
  print(" 2. All Pilot to Flight")
  print(" 3. Back\n")

  __choose = int(input("Enter your choice: "))
  if __choose == 1:
    db_ops.search_pilot_flight()
  elif __choose == 2:
    db_ops.view_pilot_flight_all()
  elif __choose == 3:
    menu()# Return to the main menu
  else:
    print("Invalid Choice")
# Initialize database operations
db_ops = DBOperations()
db_ops.create_table()# Create necessary tables
db_ops.insert_test_data()# Insert sample data
# Main menu loop
while True:
  menu()# Display menu options

  __choose_menu = int(input("Enter your choice: "))
  if __choose_menu == 1:
    db_ops.insert_data()
  elif __choose_menu == 2:
    viewflights()
  elif __choose_menu == 3:
    db_ops.update_flight()
  elif __choose_menu == 4:
    db_ops.delete_flight()
  elif __choose_menu == 5:
    db_ops.insert_Pilot()
  elif __choose_menu == 6:
    viewpilots()
  elif __choose_menu == 7:
    db_ops.update_pilot()
  elif __choose_menu == 8:
    db_ops.delete_pilot()
  elif __choose_menu == 9:
    db_ops.insert_Pilot_flight()
  elif __choose_menu == 10:
    viewpilotflight()
  elif __choose_menu == 11:
    db_ops.delete_pilot_flight()
  elif __choose_menu == 12:
    db_ops.insert_Destination()
  elif __choose_menu == 13:
    viewdestinations()
  elif __choose_menu == 14:
    db_ops.update_destination()
  elif __choose_menu == 15:
    db_ops.delete_destination()
  elif __choose_menu == 16:
    exit(0)# Exit the program
  else:
    print("Invalid Choice")