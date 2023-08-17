import psycopg2


def save_to_db(data):
    """
    Saves radio station data to a PostgreSQL database.

    Args:
        data (list): List of dictionaries containing radio station information.
    """
    conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password",
        ssl="required"
    )

    cur = conn.cursor()

    for station in data:
        cur.execute(
            "INSERT INTO radio_stations (name, stream_url, frequency) VALUES (%s, %s, %s)",
            (station['name'], station['stream_url'], station['frequency'])
        )

    conn.commit()

    cur.close()
    conn.close()