function mistel-reconnect -d "Remove and re-pair Mistel keyboard"
    set -l device "20:73:40:01:2C:BC"  # Mistel 1 keyboard

    echo "Removing existing pairing for Mistel keyboard..."
    bluetoothctl remove $device 2>/dev/null

    echo ""
    echo "Put your Mistel keyboard in pairing mode now!"
    echo "Hold Fn + Q for 3-5 seconds until LED blinks"
    echo ""
    read -P "Press Enter when ready to scan... "

    echo "Scanning for keyboard (15 seconds)..."
    timeout 15 bluetoothctl --timeout 15 scan on 2>&1 | grep -E "Mistel|$device"

    echo ""
    echo "Pairing with Mistel keyboard..."
    bluetoothctl pair $device
    and bluetoothctl trust $device
    and bluetoothctl connect $device

    if test $status -eq 0
        echo ""
        echo "✓ Successfully connected to Mistel keyboard"
    else
        echo ""
        echo "✗ Failed to connect. Make sure the keyboard is in pairing mode."
        return 1
    end
end
