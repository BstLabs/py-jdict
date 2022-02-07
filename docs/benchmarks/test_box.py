import json

from box import Box

json_data = {
    "status": True,
    "data": {
        "file": {
            "url": {
                "short": "https://anonfiles.com/n2weifEcx5",
                "full": "https://anonfiles.com/n2weifEcx5/test_py",
            },
            "metadata": {
                "size": {"bytes": 63, "readable": "63 B"},
                "name": "test_py",
                "id": "n2weifEcx5",
            },
        }
    },
}
new_data = Box(json_data)

for key, value in new_data.data.file.metadata.items():
    print(key, value)
