import pika

class mqCustomer(mqConsumerInterface):
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        # Save parameters to class variables
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        # Call setupRMQConnection
        setupRMQConnection(self)

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        self.connection = pika.BlockingConnection(parameters=conParams)

        # Establish Channel
        self.channel = connection.channel()

        # Create Queue if not already present
        self.channel.queue_declare(queue=self.queue_name)

        # Create the exchange if not already present
        self.channel.exchange_declare(self.exchange_name)

        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(queue=queue_name, routing_key=self.binding_key, exchange=self.exchange_name)

        # Set-up Callback function for receiving messages
        self.channel.basic_consume(self.queue_name, self.on_message_callback)

    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        channel.basic_ack(method_frame.delivery_tag)

        #Print message (The message is contained in the body parameter variable)
        print(f"Incoming Data. Method_Frame: {method_frame}\nHeader_Frame:{header_frame}\nBody:{body}")

    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print(f"[*] Waiting for messages. To exit press CTRL+C")
        # Start consuming messages
        self.channel.start_consuming()
    
    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print(f"Closing RMQ connection on destruction")

        # Close Channel
        self.channel.stop_consuming()
        self.channel.close()

        # Close Connection
        self.connection.close()