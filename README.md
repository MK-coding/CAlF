# Calendar Availability Finder

This is a Python project that helps you find common free times between multiple ICS calendars. With this project, you can easily schedule meetings or events with a group of people without having to manually compare everyone's availability.

## How to Use

To use this project, you'll need to have Python installed on your computer. Once you've cloned the repository to your local machine, you can run the main.py file from the command line:

```
#python main.py example\schedule_0.ics example\schedule_1.ics 60 --startTime "2023-04-03 08:00:00" --endTime "2023-04-03 16:00:00"
```

### Help

```
usage: main.py [-h] [--startTime STARTTIME] [--endTime ENDTIME] path [path ...] length

Find common free times in ICS calendars.

positional arguments:
  path                  the paths for the ICS files
  length                the length in minutes

options:
  -h, --help            show this help message and exit
  --startTime STARTTIME
                        the start time in YYYY-MM-DD HH:MM:SS format (default: None)
  --endTime ENDTIME     the end time in YYYY-MM-DD HH:MM:SS format (default: None)
```

## Requirements

This project requires Python 3.x and the `ics` and `pytz` module. You can install the ics module pip:

```
$ pip install -r requirements.txt
```

## Contributing

If you find a bug or have a suggestion for a new feature, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits

This project was created by MK-Coding. Thanks to the [ics module](https://pypi.org/project/ics/) for making it easy to work with ICS files.