import time
import serial
import csv
from ublox_gps import UbloxGps

class GPS_DRIVER:
    def __init__(self):
        self.baudrate = 38400
        self.port = '/dev/ttyACM0'
        
        
        
        # Wait for GPS to stabilize (allow it to get a fix)
        print("Waiting for GPS to stabilize...")
        time.sleep(45)  # Wait for 5 seconds to ensure the GPS is ready
        
        # Open the GPS serial port
        self.gps_port = serial.Serial(self.port, baudrate=self.baudrate, timeout=1)
        self.gps = UbloxGps(self.gps_port)
        
        # Open the CSV file for writing
        self.csv_file = open('gps_coordinates.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write the header to the CSV file
        self.csv_writer.writerow(['Latitude', 'Longitude', 'Height (m)', 'Number of Satellites'])

    def get_coordinates_and_satellites(self):
        try:
            geo = self.gps.geo_coords()  # Get GPS coordinates (latitude, longitude, and height)
            
            # Get the list of satellites in view
            satellites = self.gps.satellites()
            num_satellites = 0
            if satellites != None:
                num_satellites = len(satellites)  # Count the number of satellites in view
            
            return geo.lat, geo.lon, geo.hMSL / 1000.0, num_satellites  # Convert height to meters
        except Exception as e:
            print(f"Error retrieving GPS data: {e}")
            return 0.0, 0.0, -1.0, 0  # Return default values if there's an error

    def run(self):
        try:
            while True:
                # Fetch the coordinates and satellite count
                lat, lon, h, num_satellites = self.get_coordinates_and_satellites()
                
                # Print the data to the console
                print(f'lat: {lat} lon: {lon} height: {h} satellites: {num_satellites}')
                
                # Write the data to the CSV file
                self.csv_writer.writerow([lat, lon, h, num_satellites])
                
                # Wait for the next iteration
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("GPS logging stopped.")
        
        finally:
            # Close the CSV file when done
            self.csv_file.close()
            print("CSV file closed.")

def main(args=None):
    gps = GPS_DRIVER()
    gps.run()

if __name__ == '__main__':
    main()
