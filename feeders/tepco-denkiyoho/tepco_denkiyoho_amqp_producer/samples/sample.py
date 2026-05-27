
"""
Sample usage of tepco_denkiyoho_amqp_producer_amqp_producer

This example demonstrates how to send messages using the AMQP 1.0 producer.
"""
import sys
from tepco_denkiyoho_amqp_producer_amqp_producer import *

def main():
    """Main function"""
    
    
    # Create producer
    print("Creating AMQP producer...")
    producer = JPTEPCODenkiyohoAmqpProducer(
        host="localhost",  # Change to your AMQP broker hostname
        address="my-queue",  # Change to your queue/topic name
        port=5672,  # Use 5671 for TLS
        username="guest",  # Change to your username
        password="guest",  # Change to your password
        content_mode='structured',  # or 'binary' for CloudEvents
        format_type='application/json'
    )
    
    try:
        
        
        # Send SupplyCapacity message
        print("Sending SupplyCapacity message...")
        # TODO: Create a SupplyCapacity instance with actual data
        # data = SupplyCapacity(...)
        # producer.send_supply_capacity(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("SupplyCapacity message sent successfully!")
        
        
        
        # Send PeakDemandForecast message
        print("Sending PeakDemandForecast message...")
        # TODO: Create a PeakDemandForecast instance with actual data
        # data = PeakDemandForecast(...)
        # producer.send_peak_demand_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("PeakDemandForecast message sent successfully!")
        
        
        
        # Send DemandActual message
        print("Sending DemandActual message...")
        # TODO: Create a DemandActual instance with actual data
        # data = DemandActual(...)
        # producer.send_demand_actual(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DemandActual message sent successfully!")
        
        
        
        # Send DemandForecast message
        print("Sending DemandForecast message...")
        # TODO: Create a DemandForecast instance with actual data
        # data = DemandForecast(...)
        # producer.send_demand_forecast(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("DemandForecast message sent successfully!")
        
        
        
        # Send Info message
        print("Sending Info message...")
        # TODO: Create a Info instance with actual data
        # data = Info(...)
        # producer.send_info(
        #     data=data,
        #     content_type="application/json"
        # )
        # print("Info message sent successfully!")
        
        
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