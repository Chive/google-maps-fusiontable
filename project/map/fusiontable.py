from project.google_api.services import get_fusiontable_service

INSERT_QUERY = """
    INSERT INTO 
      {table_id} 
      (Address, Location, DateCreated) 
    VALUES 
      ('{address}', '{latlng}', '{created}')
    """

DELETE_QUERY = """
    DELETE FROM
      {table_id}
    """


def insert_location(location, table_id):
    service = get_fusiontable_service()

    def escape(s):
        """
        As far as I can see it's currently not possible to pass
        values separately from the query. According to the Google Docs
        everything that might contain quotes should be escaped with a
        backslash
        """
        for ch in ('"', "'"):
            s = s.replace(ch, '\{}'.format(ch))
        return s

    query = INSERT_QUERY.format(
        table_id=table_id,
        address=escape(location.address),
        latlng='{},{}'.format(location.latitude, location.longitude),
        created=location.created_at,
    )

    return service.query().sql(sql=query).execute()


def clear_table(table_id):
    service = get_fusiontable_service()

    query = DELETE_QUERY.format(
        table_id=table_id,
    )

    return service.query().sql(sql=query).execute()
