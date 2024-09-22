echo "Shell command that queries the Square API using cUrl."
echo "Several cUrl commands can be listed here."
echo "To save the output to a file, use pipes."
curl https://connect.squareup.com/v2/orders/search \
  -X POST \
  -H 'Square-Version: 2024-06-04' \
  -H 'Authorization: Bearer EAAAlrrFSII6zTjFkfmzjxSWwg00awBKhalHvWFJNpRcMsTajoIjyKLu6x3eeeGo' \
  -H 'Content-Type: application/json' \
  -d '{
    "location_ids": [
      "L4Z5WSQDM9WSE"
    ],
    "query": {
      "filter": {
        "date_time_filter":{
          "created_at": {
            "start_at": "2024-06-12T00:00:00+00:00",
            "end_at": "2024-06-13T00:00:00+00:00"
          }
        }
      }
    }
  }'