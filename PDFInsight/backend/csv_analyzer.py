
import pandas as pd


def analyze_transaction_csv(
    file_path,
    chunksize=100_000,
    start_date=None,
    end_date=None,
    transaction_type=None,
):
    total_rows = 0
    total_amount = 0.0
    amount_count = 0
    min_amount = None
    max_amount = None

    missing_counts = {}
    transaction_types = {}
    all_transaction_types = set()
    merchant_counts = {}
    daily_amounts = {}
    duplicate_rows = 0

    date_min = None
    date_max = None
    amount_column = None
    date_column = None
    type_column = None
    merchant_column = None
    columns_detected = False

    start = (
        pd.to_datetime(start_date, errors="coerce")
        if start_date else None
    )
    end = (
        pd.to_datetime(end_date, errors="coerce")
        if end_date else None
    )

    if start_date and pd.isna(start):
        raise ValueError("Invalid start date.")

    if end_date and pd.isna(end):
        raise ValueError("Invalid end date.")

    if start is not None and end is not None and start > end:
        raise ValueError("Start date cannot be after end date.")

    for chunk in pd.read_csv(
        file_path,
        chunksize=chunksize,
        low_memory=False,
    ):
        chunk.columns = [
            str(col).strip() for col in chunk.columns
        ]

        if not columns_detected:
            columns_lower = {
                col.lower(): col for col in chunk.columns
            }

            amount_column = next(
                (
                    columns_lower[c]
                    for c in [
                        "amount",
                        "transaction_amount",
                        "amt",
                    ]
                    if c in columns_lower
                ),
                None,
            )

            date_column = next(
                (
                    columns_lower[c]
                    for c in [
                        "date",
                        "transaction_date",
                        "timestamp",
                    ]
                    if c in columns_lower
                ),
                None,
            )

            type_column = next(
                (
                    columns_lower[c]
                    for c in [
                        "use_chip",
                        "transaction_type",
                        "type",
                    ]
                    if c in columns_lower
                ),
                None,
            )

            merchant_column = next(
                (
                    columns_lower[c]
                    for c in [
                        "merchant",
                        "merchant_name",
                    ]
                    if c in columns_lower
                ),
                None,
            )

            columns_detected = True

        # Dataset-wide missing-value and duplicate statistics.
        for col, count in chunk.isna().sum().items():
            missing_counts[col] = (
                missing_counts.get(col, 0) + int(count)
            )

        duplicate_rows += int(chunk.duplicated().sum())

        # Preserve all transaction types for the dropdown.
        if type_column:
            all_transaction_types.update(
                chunk[type_column]
                .fillna("Missing")
                .astype(str)
                .unique()
            )

        dates = (
            pd.to_datetime(
                chunk[date_column],
                errors="coerce",
            )
            if date_column else None
        )

        amounts = None

        if amount_column:
            amounts = pd.to_numeric(
                chunk[amount_column]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False),
                errors="coerce",
            )

        # Begin with all rows selected.
        mask = pd.Series(True, index=chunk.index)

        # Apply start and end date filters.
        if start is not None or end is not None:
            if dates is None:
                raise ValueError(
                    "Date filtering requires a recognized date column."
                )

            if start is not None:
                mask &= dates >= start

            if end is not None:
                # Include every timestamp on the selected end date.
                end_exclusive = (
                    end.normalize() + pd.Timedelta(days=1)
                )
                mask &= dates < end_exclusive

        # Apply transaction type filter.
        if transaction_type and transaction_type != "All":
            if type_column is None:
                raise ValueError(
                    "Transaction type filtering requires a "
                    "recognized transaction type column."
                )

            mask &= (
                chunk[type_column]
                .fillna("Missing")
                .astype(str)
                == transaction_type
            )

        filtered_chunk = chunk.loc[mask]

        filtered_dates = (
            dates.loc[mask] if dates is not None else None
        )

        filtered_amounts = (
            amounts.loc[mask] if amounts is not None else None
        )

        total_rows += len(filtered_chunk)

        # Calculate amount statistics on filtered rows.
        if filtered_amounts is not None:
            valid_amounts = filtered_amounts.dropna()

            if not valid_amounts.empty:
                total_amount += float(valid_amounts.sum())
                amount_count += len(valid_amounts)

                current_min = float(valid_amounts.min())
                current_max = float(valid_amounts.max())

                min_amount = (
                    current_min
                    if min_amount is None
                    else min(min_amount, current_min)
                )

                max_amount = (
                    current_max
                    if max_amount is None
                    else max(max_amount, current_max)
                )

        # Calculate date range and daily chart totals.
        if filtered_dates is not None:
            valid_dates = filtered_dates.dropna()

            if not valid_dates.empty:
                chunk_min = valid_dates.min()
                chunk_max = valid_dates.max()

                date_min = (
                    chunk_min
                    if date_min is None
                    else min(date_min, chunk_min)
                )

                date_max = (
                    chunk_max
                    if date_max is None
                    else max(date_max, chunk_max)
                )

            if filtered_amounts is not None:
                valid_rows = (
                    filtered_dates.notna()
                    & filtered_amounts.notna()
                )

                if valid_rows.any():
                    daily = pd.DataFrame({
                        "date": filtered_dates[valid_rows]
                        .dt.strftime("%Y-%m-%d"),
                        "amount": filtered_amounts[valid_rows],
                    })

                    daily_totals = (
                        daily.groupby("date")["amount"].sum()
                    )

                    for day, value in daily_totals.items():
                        daily_amounts[day] = (
                            daily_amounts.get(day, 0.0)
                            + float(value)
                        )

        # Transaction type counts for the selected rows.
        if type_column:
            counts = (
                filtered_chunk[type_column]
                .fillna("Missing")
                .astype(str)
                .value_counts()
            )

            for name, count in counts.items():
                transaction_types[name] = (
                    transaction_types.get(name, 0)
                    + int(count)
                )

        # Merchant counts for the selected rows.
        if merchant_column:
            counts = (
                filtered_chunk[merchant_column]
                .fillna("Missing")
                .astype(str)
                .value_counts()
            )

            for name, count in counts.items():
                merchant_counts[name] = (
                    merchant_counts.get(name, 0)
                    + int(count)
                )

    if total_rows == 0:
        raise ValueError(
            "No transactions matched the selected filters, "
            "or the CSV contains no data rows."
        )

    top_types = dict(
        sorted(
            transaction_types.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:10]
    )

    top_merchants = dict(
        sorted(
            merchant_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:10]
    )

    sorted_days = sorted(daily_amounts.items())

    return {
        "total_rows": total_rows,
        "total_amount": round(total_amount, 2),
        "average_amount": (
            round(total_amount / amount_count, 2)
            if amount_count else None
        ),
        "min_amount": min_amount,
        "max_amount": max_amount,
        "amount_count": amount_count,
        "date_min": (
            str(date_min) if date_min is not None else None
        ),
        "date_max": (
            str(date_max) if date_max is not None else None
        ),
        "missing_counts": missing_counts,
        "duplicate_rows": duplicate_rows,
        "transaction_types": top_types,
        "top_merchants": top_merchants,
        "amount_column": amount_column,
        "date_column": date_column,
        "type_column": type_column,
        "merchant_column": merchant_column,
        "selected_start_date": start_date or "",
        "selected_end_date": end_date or "",
        "selected_transaction_type": transaction_type or "All",
        "available_transaction_types": sorted(
            all_transaction_types
        ),
        "daily_chart_labels": [
            day for day, _ in sorted_days
        ],
        "daily_chart_values": [
            round(value, 2) for _, value in sorted_days
        ],
        "type_chart_labels": list(top_types.keys()),
        "type_chart_values": list(top_types.values()),
        "merchant_chart_labels": list(top_merchants.keys()),
        "merchant_chart_values": list(top_merchants.values()),
    }
