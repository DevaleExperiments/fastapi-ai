from datetime import datetime


class ResumeExperienceService:

    def calculate_years(
        self,
        experience: list,
    ) -> float:

        periods = []

        for entry in experience:
            if not entry.start_date:
                continue

            start = self._parse_month(entry.start_date)

            if start is None:
                continue

            if entry.end_date and entry.end_date.strip().lower() == "present":
                end = datetime.now()
            else:
                end = self._parse_month(entry.end_date)

            if end is None:
                continue

            if end <= start:
                continue

            periods.append((start, end))

        if not periods:
            return 0.0

        periods.sort(key=lambda period: period[0])

        merged_periods = []

        for start, end in periods:

            if not merged_periods:
                merged_periods.append([start, end])
                continue

            previous_start, previous_end = merged_periods[-1]

            if start <= previous_end:
                if end > previous_end:
                    merged_periods[-1][1] = end
            else:
                merged_periods.append([start, end])

        total_months = 0

        for start, end in merged_periods:
            months = (
                (end.year - start.year) * 12
                + (end.month - start.month)
            )

            total_months += months

        return round(total_months / 12, 1)

    def _parse_month(
        self,
        value: str | None,
    ) -> datetime | None:

        if not value:
            return None

        value = value.strip()

        for fmt in ("%b %Y", "%B %Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        return None