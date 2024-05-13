#include <Wire.h>
#include <Adafruit_VL53L0X.h>

Adafruit_VL53L0X sensor;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  sensor.begin();

  pinMode(8, OUTPUT);
}

void loop() {
  VL53L0X_RangingMeasurementData_t measure;
  sensor.rangingTest(&measure, false);

  Serial.print("Odległość: ");
  Serial.print(measure.RangeMilliMeter);

  Serial.println(" mm");
  delay(100);

  if (measure.RangeMilliMeter < 100) {
    tone(8, 3000);
  }
  else if (measure.RangeMilliMeter < 200) {
    tone(8, 2000);
  }

    else if (measure.RangeMilliMeter < 300) {
    tone(8, 1000);
  }

  else {
    noTone(8);
  }
}
