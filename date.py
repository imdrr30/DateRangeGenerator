import datetime


class DateRangeGenerator:
    """This class DateRangeGenerator used to get the range of date time objects. Used for various purposes."""

    WEEK_DAYS = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    CONFIGS = ["day", "month", "year", "weekday"]
    TYPES = ["include", "exclude"]
    EMPTY = [None, []]
    VALID_DATE_CLASS = [datetime.date, datetime.datetime]

    def __init__(self, date_format: str, start_from, end_at, frequency: int = 1, *args, **kwargs):
        """
        Initializes the required data for the filter.
        :param date_format: str = '%Y-%m-%d'
        :param start_from: str = '2022-01-01'
        :param end_at: str = '2022-12-31'
        """

        # Date Format

        self.frequency = frequency
        self.date_format = date_format

        # Start and End Date
        self.start_from = datetime.datetime.strptime(start_from, date_format)
        self.end_at = datetime.datetime.strptime(end_at, date_format)

        # Range of Dates
        self.date_range = list(
            self.get_all_dates_between_ranges(self.start_from, self.end_at, self.frequency)
        )

        # Initialize Filter Configs
        self.initialize_config_data(*args, **kwargs)

        # Filtered date ranges
        # As Date Object
        self.filtered_date_range = []
        # As str Object
        self.filtered_date_range_string = []

        # Start Filter
        self.filter_dates_from_range()

    def initialize_config_data(self, *args, **kwargs):
        """This function is used to initialize the custom variables for the filters."""

        # Iterate Configs
        for config in self.CONFIGS:
            # Iterate Types
            for types in self.TYPES:
                # Name of the input field
                name = f"{types}_{config}s"
                setattr(self, name, kwargs.get(name, None))

                # Custom Configurations for specific data type
                if getattr(self, name) is not None:
                    #  If it is a week day filter index the given data
                    if config == "weekday":
                        new_list = []
                        for day_name in getattr(self, name):
                            new_list.append(
                                self.WEEK_DAYS.index(day_name.lower())
                            )  # Save the index of the given week day
                        setattr(self, name, new_list)  # Update the old List

    @staticmethod
    def get_all_dates_between_ranges(start_from, end_at, frequency):
        """This function is used to get all the date from the give ranges using start_from and end_at."""
        for ordinal in range(start_from.toordinal(), end_at.toordinal(), frequency):
            yield datetime.date.fromordinal(ordinal)

    def filter_dates_from_range(self):
        """
        This function is the brain of whole operation. Dates are filtered from the
        """
        for date in self.date_range:
            flag = True

            for config in self.CONFIGS:
                for types in self.TYPES:

                    config_list = getattr(self, f"{types}_{config}s")
                    date_config = None
                    if config in ["day", "month", "year"]:
                        date_config = getattr(date, config)
                    if config in ["weekday"]:
                        date_config = date.weekday()

                    if types == "include":
                        if (
                            config_list not in self.EMPTY
                            and date_config not in config_list
                        ):
                            flag = False
                    elif types == "exclude":
                        if config_list not in self.EMPTY and date_config in config_list:
                            flag = False

            if flag:
                self.filtered_date_range_string.append(date.strftime(self.date_format))
                self.filtered_date_range.append(date)

    def filter(self):
        """This function is used to return the filtered date range as string."""
        return self.filtered_date_range_string

    def filtered_datetime(self):
        """This function is used to return the filtered date range as list"""
        return self.filtered_date_range

    def __iter__(self):
        """This function is used to yield data for the iteration of this object."""
        for date in self.filtered_date_range_string:
            yield date
