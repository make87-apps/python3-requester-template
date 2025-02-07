import time
from datetime import timezone

from make87_messages.core.header_pb2 import Header
from make87_messages.text.text_plain_pb2 import PlainText
import make87 as m87


def main():
    m87.initialize()
    endpoint = m87.get_requester(name="EXAMPLE_ENDPOINT", requester_message_type=PlainText,
                                 provider_message_type=PlainText)

    root_entity = m87.get_config_value("ROOT_ENTITY", "/", str)
    while True:
        message = PlainText(header=m87.create_header(Header, entity_path=root_entity), body="Hello, World! 🐍")
        try:
            response = endpoint.request(message, timeout=10.0)
            print(
                f"Received response: {response.body}. Round trip took"
                f" {response.header.timestamp.ToDatetime().replace(tzinfo=timezone.utc) - message.header.timestamp.ToDatetime().replace(tzinfo=timezone.utc)} seconds."
            )
        except m87.ProviderNotAvailable:
            print("Endpoint not available. Retrying in 1 second.")
        finally:
            time.sleep(1)


if __name__ == "__main__":
    main()
