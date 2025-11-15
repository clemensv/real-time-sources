# Copy generated producer files to the project root
Copy-Item -Path "pegelonline_producer\pegelonline_producer_data" -Destination "." -Recurse -Force
Copy-Item -Path "pegelonline_producer\pegelonline_producer_kafka_producer" -Destination "." -Recurse -Force

Write-Host "Producer files copied successfully"
