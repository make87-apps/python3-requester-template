import time
from datetime import timezone

from make87_messages.core.header_pb2 import Header
from make87_messages.text.text_plain_pb2 import PlainText
from make87 import initialize, get_requester, resolve_endpoint_name

from make87 import ProviderNotAvailable


def main():
    initialize()
    endpoint_name = resolve_endpoint_name(name="REQUESTER_ENDPOINT")
    endpoint = get_requester(name=endpoint_name, requester_message_type=PlainText, provider_message_type=PlainText)

    while True:
        header = Header(reference_id=0, entity_path="/")
        header.timestamp.GetCurrentTime()
        message = PlainText(header=header, body="Hello, World! 🐍")
        try:
            response = endpoint.request(message, timeout=10.0)
            print(
                f"Received response: {response.body}. Round trip took"
                f" {response.header.timestamp.ToDatetime().replace(tzinfo=timezone.utc) - message.header.timestamp.ToDatetime().replace(tzinfo=timezone.utc)} seconds."
            )
        except ProviderNotAvailable:
            print("Endpoint not available. Retrying in 1 second.")
        finally:
            time.sleep(1)


if __name__ == "__main__":
    main()
