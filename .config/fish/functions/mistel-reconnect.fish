function mistel-reconnect -d "Remove and re-pair Mistel keyboard"
    set -l device "20:73:40:01:2C:BC"  # Mistel 1 keyboard

    echo "Removing existing pairing for Mistel keyboard..."
    bluetoothctl remove $device

    echo ""
    echo "Put your Mistel keyboard in pairing mode now!"
    echo "Hold Fn + Q for 3-5 seconds until LED blinks"
    echo ""
    echo "Scanning for 10 seconds..."

    # Start scan in background and wait
    timeout 10 bluetoothctl scan on &
    set scan_pid $last_pid
    sleep 8
    kill $scan_pid 2>/dev/null

    echo ""
    echo "Pairing with Mistel keyboard..."
    bluetoothctl pair $device
    and bluetoothctl trust $device
    and bluetoothctl connect $device

    if test $status -eq 0
        echo ""
        echo "✓ Successfully connected to Mistel keyboard"
        bluetoothctl info $device | grep -E "Name|Connected|Paired"
    else
        echo ""
        echo "✗ Failed to connect. Make sure the keyboard is in pairing mode."
        return 1
    end
end
