# plane-spotting

Spot planes using FlightRadar24's API through azimuth and horizon angles

## Usage:

`$ ./main.py [current lat] [current lon]`

e.g. if I were standing in front of the Washington Monument, I would run `./main.py 38.88945968498166 -77.03695797757808` (Though I probably won't see any planes around).

## Example Output:

```
Spotted 2 nearby flights
Flight JBU123 BCS3 @ (12.345º, -12.345º, 38000 ft)
	Traveling at 479 mph, 231.00º (SW)
	Azimuth angle: 256.85º (W)
	Horizon angle: 79.09º
	Eyeball distance: 7.33 mi
Flight UAL123 A320 @ (45.678º, -45.678º, 2825 ft)
	Traveling at 230 mph, 157.00º (SE)
	Azimuth angle: 108.32º (E)
	Horizon angle: 3.08º
	Eyeball distance: 9.73 mi
	
[ENTER] to refresh
```
