from azure.data.tables import TableServiceClient
from datetime import datetime

CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=robotostorage;AccountKey=VkVUIVygtanG+I9XDzJsm" \
                    "+rKssZ6CtFMq3HvsA8RGzt8/W9t4dWb5qb0dJfjdDRv30VQ3Gke71AT+AStmNUrOQ==;EndpointSuffix=core.windows" \
                    ".net "
TABLE_NAME = "Locations"

table_service_client = TableServiceClient.from_connection_string(conn_str=CONNECTION_STRING)
table_client = table_service_client.get_table_client(table_name=TABLE_NAME)


def set_location(user_id, lat, long):
    location_entity = {
        u'PartitionKey': u"Locations",
        u'RowKey': str(user_id),
        u'Lat': lat,
        u'Long': long,
    }
    table_client.upsert_entity(entity=location_entity)


def get_location(user_id):
    return table_client.get_entity(partition_key="Locations", row_key=str(user_id))
