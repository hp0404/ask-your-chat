import json
import typing

JSON = typing.Dict[str, typing.Any]


def read_json(path: str) -> JSON:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def process(data: JSON) -> typing.List[JSON]:
    messages = []
    speech = 0
    last_author: typing.Optional[str] = None
    for record in data["messages"]:
        if (
            # service messages
            record["type"] != "message"
            or
            # forwarded
            record.get("forwarded_from")
            or
            # empty texts (media)
            record["text"] == ""
        ):
            continue
        # mark consecutive messages in case they were written and sent
        # in batches
        author = record["from"]
        if author != last_author:
            speech += 1
            last_author = author
        messages.append(
            {
                "speech_id": speech,
                "message_id": record["id"],
                "author_id": author,
                "date": record["date"],
                "text": "".join(ent["text"] for ent in record["text_entities"]).strip(),
            }
        )
    return messages


def main() -> int:
    data = read_json("./chat.json")
    transformed = process(data)
    with open("./processed.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(transformed, indent=4))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
