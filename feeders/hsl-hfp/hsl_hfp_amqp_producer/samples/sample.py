
"""
Sample usage of hsl_hfp_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from hsl_hfp_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FiHslHfpAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Vp message
        print("Sending Vp message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_vp(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Vp message sent successfully!")
        
        
        
        # Send Due message
        print("Sending Due message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_due(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Due message sent successfully!")
        
        
        
        # Send Arr message
        print("Sending Arr message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_arr(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Arr message sent successfully!")
        
        
        
        # Send Dep message
        print("Sending Dep message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_dep(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Dep message sent successfully!")
        
        
        
        # Send Ars message
        print("Sending Ars message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_ars(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Ars message sent successfully!")
        
        
        
        # Send Pde message
        print("Sending Pde message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_pde(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Pde message sent successfully!")
        
        
        
        # Send Pas message
        print("Sending Pas message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_pas(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Pas message sent successfully!")
        
        
        
        # Send Wait message
        print("Sending Wait message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_wait(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Wait message sent successfully!")
        
        
        
        # Send Doo message
        print("Sending Doo message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_doo(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Doo message sent successfully!")
        
        
        
        # Send Doc message
        print("Sending Doc message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_doc(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Doc message sent successfully!")
        
        
        
        # Send Vja message
        print("Sending Vja message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_vja(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Vja message sent successfully!")
        
        
        
        # Send Vjout message
        print("Sending Vjout message...")
        # TODO: Create a VehicleEvent instance with actual data
        # data = VehicleEvent(...)
        # producer.send_vjout(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Vjout message sent successfully!")
        
        
        
        # Send Tlr message
        print("Sending Tlr message...")
        # TODO: Create a TrafficLightEvent instance with actual data
        # data = TrafficLightEvent(...)
        # producer.send_tlr(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Tlr message sent successfully!")
        
        
        
        # Send Tla message
        print("Sending Tla message...")
        # TODO: Create a TrafficLightEvent instance with actual data
        # data = TrafficLightEvent(...)
        # producer.send_tla(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Tla message sent successfully!")
        
        
        
        # Send Da message
        print("Sending Da message...")
        # TODO: Create a DriverBlockEvent instance with actual data
        # data = DriverBlockEvent(...)
        # producer.send_da(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Da message sent successfully!")
        
        
        
        # Send Dout message
        print("Sending Dout message...")
        # TODO: Create a DriverBlockEvent instance with actual data
        # data = DriverBlockEvent(...)
        # producer.send_dout(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Dout message sent successfully!")
        
        
        
        # Send Ba message
        print("Sending Ba message...")
        # TODO: Create a DriverBlockEvent instance with actual data
        # data = DriverBlockEvent(...)
        # producer.send_ba(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Ba message sent successfully!")
        
        
        
        # Send Bout message
        print("Sending Bout message...")
        # TODO: Create a DriverBlockEvent instance with actual data
        # data = DriverBlockEvent(...)
        # producer.send_bout(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Bout message sent successfully!")
        
        
        print("\nAll messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending messages: {e}", file=sys.stderr)
        return 1
    finally:
        producer.close()
        print("Producer closed")
    
    return 0
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FiHslGtfsOperatorAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Operator message
        print("Sending Operator message...")
        # TODO: Create a Operator instance with actual data
        # data = Operator(...)
        # producer.send_operator(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Operator message sent successfully!")
        
        
        print("\nAll messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending messages: {e}", file=sys.stderr)
        return 1
    finally:
        producer.close()
        print("Producer closed")
    
    return 0
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FiHslGtfsRouteAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Route message
        print("Sending Route message...")
        # TODO: Create a Route instance with actual data
        # data = Route(...)
        # producer.send_route(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Route message sent successfully!")
        
        
        print("\nAll messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending messages: {e}", file=sys.stderr)
        return 1
    finally:
        producer.close()
        print("Producer closed")
    
    return 0
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = FiHslGtfsStopAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send Stop message
        print("Sending Stop message...")
        # TODO: Create a Stop instance with actual data
        # data = Stop(...)
        # producer.send_stop(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Stop message sent successfully!")
        
        
        print("\nAll messages sent successfully!")
        
    except Exception as e:
        print(f"Error sending messages: {e}", file=sys.stderr)
        return 1
    finally:
        producer.close()
        print("Producer closed")
    
    return 0
    

if __name__ == "__main__":
    sys.exit(main())