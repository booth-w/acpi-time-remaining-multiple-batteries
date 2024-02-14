import os


def getBatteryTime():
	# assumes the capacity of the batteries are the same
	batt = os.popen("acpi").read()
	isCharging = "Charging" in batt
	isZeroRate = "zero rate" in batt

	if isZeroRate:
		return "00:00:00"

	totalPercent = 0
	batteries = batt.strip().split("\n")
	batteryCount = len(batteries)
	for battery in batteries:
		percent = int(battery.split(", ")[1].split("%")[0])
		if "Charging" in battery or "Discharging" in battery:
			currentPercent = percent
		totalPercent += percent

	if isCharging:
		time = batt.split("until")[0][-9:-1]
	else:
		time = batt.split("remaining")[0][-9:-1]

	time = time.split(":")
	hours = int(time[0])
	minutes = int(time[1])
	seconds = int(time[2])

	# multiply time by percent
	if isCharging:
		totalMinutes = (hours * 60 + minutes) * ((100 * batteryCount - totalPercent) / (100 - currentPercent))
	else:
		totalMinutes = (hours * 60 + minutes) * (totalPercent / currentPercent)

	# HH:MM:SS with leading 0
	time = f"{str(int(totalMinutes / 60)).zfill(2)}:{str(int(totalMinutes % 60)).zfill(2)}:{str(seconds).zfill(2)}"
	return time


if __name__ == "__main__":
	print(getBatteryTime())