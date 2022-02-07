from cleverdict import CleverDict

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

new_data = CleverDict(json_data)

print(type(new_data))

for key, value in new_data.data.file.metadata.items():
    print(key, value)
